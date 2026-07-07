#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import os
import re
import shutil
import subprocess
import sys
from collections import Counter
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path, PurePosixPath

try:
    from zoneinfo import ZoneInfo
except ImportError:  # pragma: no cover - Python < 3.9 fallback
    ZoneInfo = None

try:
    import fcntl
except ImportError:  # pragma: no cover - script is intended to run in WSL/Linux
    fcntl = None


DEFAULT_SOURCE = Path(
    "/mnt/c/Users/15805/AppData/Local/Doubao/User Data/Default/"
    ".doubao/agent_mode/workspace/.skills"
)
DEFAULT_TIMEZONE = "Asia/Shanghai"
TASK_NAME = "DoubaoSkillsDailySync"
README_NAME = "README.md"


@dataclass(frozen=True)
class ChangeSet:
    added: tuple[str, ...]
    modified: tuple[str, ...]
    deleted: tuple[str, ...]
    new_skills: tuple[str, ...]
    removed_skills: tuple[str, ...]

    @property
    def has_skill_changes(self) -> bool:
        return bool(self.added or self.modified or self.deleted)

    @property
    def total_count(self) -> int:
        return len(self.added) + len(self.modified) + len(self.deleted)


@dataclass(frozen=True)
class SkillInfo:
    dir_name: str
    display_name: str
    description: str
    file_count: int


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Sync Doubao workspace skills into this Git repository."
    )
    parser.add_argument(
        "--source",
        type=Path,
        default=DEFAULT_SOURCE,
        help=f"Source .skills directory. Default: {DEFAULT_SOURCE}",
    )
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="Repository root. Defaults to this script's parent repository.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Report changes without copying, archiving, writing docs, or running Git.",
    )
    parser.add_argument(
        "--commit",
        action="store_true",
        help="Commit sync changes when any files changed.",
    )
    parser.add_argument(
        "--push",
        action="store_true",
        help="Push committed changes to origin/main. Implies --commit.",
    )
    parser.add_argument(
        "--refresh-docs",
        action="store_true",
        help="Regenerate README from the current skills and change logs even when skills did not change.",
    )
    parser.add_argument(
        "--timezone",
        default=DEFAULT_TIMEZONE,
        help=f"Timezone for log names and timestamps. Default: {DEFAULT_TIMEZONE}",
    )
    return parser.parse_args()


def now_in_timezone(name: str) -> datetime:
    if ZoneInfo is None:
        return datetime.now().astimezone()
    return datetime.now(ZoneInfo(name))


def acquire_lock(repo_root: Path):
    lock_path = repo_root / ".sync.lock"
    lock_file = lock_path.open("w", encoding="utf-8")
    if fcntl is not None:
        try:
            fcntl.flock(lock_file.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            raise RuntimeError(f"another sync process is already running: {lock_path}")
    lock_file.write(f"pid={os.getpid()}\n")
    lock_file.flush()
    return lock_file


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def list_files(root: Path) -> dict[str, Path]:
    if not root.exists():
        raise FileNotFoundError(f"source directory does not exist: {root}")
    if not root.is_dir():
        raise NotADirectoryError(f"source path is not a directory: {root}")
    files: dict[str, Path] = {}
    for path in root.rglob("*"):
        if path.is_file():
            files[path.relative_to(root).as_posix()] = path
    return files


def repo_path_from_rel(root: Path, rel: str) -> Path:
    return root.joinpath(*PurePosixPath(rel).parts)


def skill_from_rel(rel: str) -> str:
    return PurePosixPath(rel).parts[0] if PurePosixPath(rel).parts else "(root)"


def skill_names_from_files(files: dict[str, Path]) -> set[str]:
    return {skill_from_rel(rel) for rel in files}


def detect_changes(source_files: dict[str, Path], target_files: dict[str, Path]) -> ChangeSet:
    source_rels = set(source_files)
    target_rels = set(target_files)
    added = sorted(source_rels - target_rels)
    deleted = sorted(target_rels - source_rels)
    modified: list[str] = []
    for rel in sorted(source_rels & target_rels):
        if sha256_file(source_files[rel]) != sha256_file(target_files[rel]):
            modified.append(rel)

    old_skills = skill_names_from_files(target_files)
    new_source_skills = skill_names_from_files(source_files)
    return ChangeSet(
        added=tuple(added),
        modified=tuple(modified),
        deleted=tuple(deleted),
        new_skills=tuple(sorted(new_source_skills - old_skills)),
        removed_skills=tuple(sorted(old_skills - new_source_skills)),
    )


def copy_changed_files(
    source_root: Path, target_root: Path, added: tuple[str, ...], modified: tuple[str, ...]
) -> None:
    for rel in (*added, *modified):
        source = repo_path_from_rel(source_root, rel)
        target = repo_path_from_rel(target_root, rel)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)


def archive_deleted_files(
    target_root: Path, archive_root: Path, deleted: tuple[str, ...]
) -> None:
    for rel in deleted:
        target = repo_path_from_rel(target_root, rel)
        archived = repo_path_from_rel(archive_root, rel)
        if not target.exists():
            continue
        archived.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(target), str(archived))
    remove_empty_dirs(target_root)


def remove_empty_dirs(root: Path) -> None:
    if not root.exists():
        return
    directories = [path for path in root.rglob("*") if path.is_dir()]
    for path in sorted(directories, key=lambda p: len(p.parts), reverse=True):
        try:
            path.rmdir()
        except OSError:
            pass


def parse_simple_front_matter(text: str) -> dict[str, str]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}

    block: list[str] = []
    for line in lines[1:]:
        if line.strip() == "---":
            break
        block.append(line)

    data: dict[str, str] = {}
    i = 0
    while i < len(block):
        line = block[i]
        match = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", line)
        if not match:
            i += 1
            continue
        key, raw_value = match.groups()
        value = raw_value.strip()
        if value in {"|", ">"}:
            i += 1
            collected: list[str] = []
            while i < len(block):
                next_line = block[i]
                if re.match(r"^[A-Za-z0-9_-]+:\s*", next_line):
                    break
                stripped = next_line.strip()
                if stripped:
                    collected.append(stripped)
                i += 1
            data[key] = " ".join(collected).strip()
            continue
        if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
            value = value[1:-1]
        data[key] = value
        i += 1
    return data


def one_line(text: str, limit: int = 220) -> str:
    cleaned = re.sub(r"\s+", " ", text).strip()
    if len(cleaned) <= limit:
        return cleaned
    return cleaned[: limit - 3].rstrip() + "..."


def escape_table_cell(text: str) -> str:
    return text.replace("\\", "\\\\").replace("|", "\\|").replace("\n", " ")


def collect_skill_infos(target_root: Path) -> list[SkillInfo]:
    infos: list[SkillInfo] = []
    if not target_root.exists():
        return infos
    for skill_dir in sorted((p for p in target_root.iterdir() if p.is_dir()), key=lambda p: p.name):
        skill_md = skill_dir / "SKILL.md"
        front_matter: dict[str, str] = {}
        description = ""
        if skill_md.exists():
            text = skill_md.read_text(encoding="utf-8", errors="replace")
            front_matter = parse_simple_front_matter(text)
            description = front_matter.get("description", "")
        file_count = sum(1 for p in skill_dir.rglob("*") if p.is_file())
        infos.append(
            SkillInfo(
                dir_name=skill_dir.name,
                display_name=front_matter.get("name") or skill_dir.name,
                description=one_line(description or "No description found."),
                file_count=file_count,
            )
        )
    return infos


def summarize_changes(changes: ChangeSet) -> list[str]:
    summaries = [
        f"本次同步新增 {len(changes.added)} 个文件、修改 {len(changes.modified)} 个文件、删除 {len(changes.deleted)} 个文件。"
    ]
    if changes.new_skills:
        summaries.append("新增 skill：" + ", ".join(changes.new_skills) + "。")
    if changes.removed_skills:
        summaries.append("移除的 skill 已归档：" + ", ".join(changes.removed_skills) + "。")
    affected = sorted(
        {skill_from_rel(rel) for rel in (*changes.added, *changes.modified, *changes.deleted)}
    )
    if affected:
        visible = ", ".join(affected[:12])
        if len(affected) > 12:
            visible += f" 等 {len(affected)} 个 skill"
        summaries.append("受影响范围：" + visible + "。")
    if changes.deleted:
        summaries.append("源目录中删除的文件已移动到本次归档目录，`skills/` 保持为当前源目录镜像。")
    return summaries


def render_file_list(paths: tuple[str, ...], prefix: str = "skills/") -> str:
    if not paths:
        return "- 无\n"
    return "\n".join(f"- `{prefix}{path}`" for path in paths) + "\n"


def render_deleted_file_list(paths: tuple[str, ...], archive_rel: str) -> str:
    if not paths:
        return "- 无\n"
    return "\n".join(
        f"- `skills/{path}` -> `{archive_rel}/{path}`" for path in paths
    ) + "\n"


def render_skill_count_table(changes: ChangeSet) -> str:
    counts: Counter[str] = Counter()
    for rel in changes.added:
        counts[skill_from_rel(rel)] += 1
    for rel in changes.modified:
        counts[skill_from_rel(rel)] += 1
    for rel in changes.deleted:
        counts[skill_from_rel(rel)] += 1
    if not counts:
        return "- 无\n"
    lines = ["| Skill | Changed Files |", "| --- | ---: |"]
    for skill, count in sorted(counts.items()):
        lines.append(f"| `{escape_table_cell(skill)}` | {count} |")
    return "\n".join(lines) + "\n"


def write_change_log(
    change_logs_dir: Path,
    timestamp: datetime,
    timestamp_slug: str,
    changes: ChangeSet,
    archive_rel: str,
) -> Path:
    change_logs_dir.mkdir(parents=True, exist_ok=True)
    log_path = change_logs_dir / f"{timestamp_slug}.md"
    summary_lines = "\n".join(f"- {line}" for line in summarize_changes(changes))
    content = f"""# Doubao Skills Sync - {timestamp.strftime('%Y-%m-%d %H:%M:%S %z')}

## Summary
{summary_lines}

## Changed Skills
{render_skill_count_table(changes)}
## Added Files ({len(changes.added)})
{render_file_list(changes.added)}
## Modified Files ({len(changes.modified)})
{render_file_list(changes.modified)}
## Deleted And Archived Files ({len(changes.deleted)})
{render_deleted_file_list(changes.deleted, archive_rel)}
"""
    log_path.write_text(content, encoding="utf-8")
    return log_path


def read_log_summary(log_path: Path) -> str:
    text = log_path.read_text(encoding="utf-8", errors="replace")
    lines = text.splitlines()
    in_summary = False
    parts: list[str] = []
    for line in lines:
        if line.strip() == "## Summary":
            in_summary = True
            continue
        if in_summary and line.startswith("## "):
            break
        if in_summary and line.startswith("- "):
            parts.append(line[2:].strip())
    return one_line(" ".join(parts), limit=180) if parts else "No summary found."


def collect_recent_logs(
    repo_root: Path, change_logs_dir: Path, limit: int = 20
) -> list[tuple[str, str, str]]:
    if not change_logs_dir.exists():
        return []
    entries: list[tuple[str, str, str]] = []
    for path in sorted(change_logs_dir.glob("*.md"), reverse=True)[:limit]:
        entries.append((path.stem, path.relative_to(repo_root).as_posix(), read_log_summary(path)))
    return entries


def render_readme(
    repo_root: Path,
    target_root: Path,
    change_logs_dir: Path,
    latest_log: Path | None,
) -> str:
    skills = collect_skill_infos(target_root)
    total_files = sum(info.file_count for info in skills)
    recent_logs = collect_recent_logs(repo_root, change_logs_dir)

    if latest_log is not None:
        latest_summary = read_log_summary(latest_log)
        latest_rel = latest_log.relative_to(repo_root).as_posix()
        latest_line = f"[{latest_log.stem}]({latest_rel}) - {latest_summary}"
    elif recent_logs:
        latest_slug, latest_path, latest_summary = recent_logs[0]
        latest_line = f"[{latest_slug}]({latest_path}) - {latest_summary}"
    else:
        latest_line = "暂无同步变更记录。"

    skill_rows = ["| Skill | Files | Description |", "| --- | ---: | --- |"]
    for info in skills:
        skill_rows.append(
            "| "
            f"`{escape_table_cell(info.display_name)}` "
            f"(`skills/{escape_table_cell(info.dir_name)}`) | "
            f"{info.file_count} | "
            f"{escape_table_cell(info.description)} |"
        )

    if recent_logs:
        log_rows = ["| Date | Change Log | Summary |", "| --- | --- | --- |"]
        for slug, path, summary in recent_logs:
            log_rows.append(
                f"| {slug} | [{slug}]({path}) | {escape_table_cell(summary)} |"
            )
        recent_changes = "\n".join(log_rows)
    else:
        recent_changes = "暂无。"

    return f"""# Doubao Skills

本仓库每天同步 Doubao 本地工作区的 `.skills` 目录，保留当前 skill 文件、自动生成索引，并为每次变化生成独立说明。

## 同步概览

- 源目录：`C:\\Users\\15805\\AppData\\Local\\Doubao\\User Data\\Default\\.doubao\\agent_mode\\workspace\\.skills`
- 同步目录：`skills/`
- 任务计划：`{TASK_NAME}`，每天 18:00 运行
- 当前 skill 数：{len(skills)}
- 当前文件数：{total_files}
- 最近变更：{latest_line}

## Skill 索引

{chr(10).join(skill_rows)}

## 最近变更

{recent_changes}
"""


def write_readme(
    repo_root: Path,
    target_root: Path,
    change_logs_dir: Path,
    latest_log: Path | None,
) -> Path:
    readme_path = repo_root / README_NAME
    readme_path.write_text(
        render_readme(repo_root, target_root, change_logs_dir, latest_log),
        encoding="utf-8",
    )
    return readme_path


def run_git(repo_root: Path, args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=repo_root,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=True,
    )


def git_has_changes(repo_root: Path) -> bool:
    result = run_git(repo_root, ["status", "--porcelain"])
    return bool(result.stdout.strip())


def git_add_sync_paths(repo_root: Path) -> None:
    paths = [
        README_NAME,
        "skills",
        "change-logs",
        "archive",
    ]
    existing = [path for path in paths if (repo_root / path).exists()]
    if existing:
        run_git(repo_root, ["add", *existing])


def commit_and_maybe_push(repo_root: Path, timestamp: datetime, push: bool) -> None:
    if not git_has_changes(repo_root):
        print("No Git changes to commit.")
        return
    git_add_sync_paths(repo_root)
    staged = run_git(repo_root, ["diff", "--cached", "--name-only"]).stdout.strip()
    if not staged:
        print("No staged sync changes to commit.")
        return
    message = f"sync doubao skills: {timestamp.strftime('%Y-%m-%d %H:%M')}"
    print(run_git(repo_root, ["commit", "-m", message]).stdout.strip())
    if push:
        gh = shutil.which("gh")
        if gh is None:
            raise RuntimeError("gh CLI is required for --push but was not found in PATH")
        subprocess.run(
            ["gh", "auth", "setup-git", "-h", "github.com"],
            cwd=repo_root,
            check=True,
        )
        print(run_git(repo_root, ["push", "-u", "origin", "main"]).stdout.strip())


def print_change_summary(changes: ChangeSet) -> None:
    print(
        "Detected changes: "
        f"{len(changes.added)} added, "
        f"{len(changes.modified)} modified, "
        f"{len(changes.deleted)} deleted."
    )
    if changes.new_skills:
        print("New skills: " + ", ".join(changes.new_skills))
    if changes.removed_skills:
        print("Removed skills: " + ", ".join(changes.removed_skills))


def sync(args: argparse.Namespace) -> int:
    repo_root = args.repo_root.resolve()
    source_root = args.source
    target_root = repo_root / "skills"
    change_logs_dir = repo_root / "change-logs"
    deleted_archive_root = repo_root / "archive" / "deleted"
    timestamp = now_in_timezone(args.timezone)
    timestamp_slug = timestamp.strftime("%Y-%m-%d-%H%M%S")
    archive_root = deleted_archive_root / timestamp_slug
    archive_rel = archive_root.relative_to(repo_root).as_posix()

    lock_file = acquire_lock(repo_root)
    try:
        source_files = list_files(source_root)
        target_root.mkdir(parents=True, exist_ok=True)
        target_files = list_files(target_root)
        changes = detect_changes(source_files, target_files)
        print_change_summary(changes)

        if args.dry_run:
            print("Dry run only; no files were changed.")
            return 0

        if not changes.has_skill_changes:
            if args.refresh_docs:
                write_readme(
                    repo_root=repo_root,
                    target_root=target_root,
                    change_logs_dir=change_logs_dir,
                    latest_log=None,
                )
                print("No skill file changes found; README was refreshed by request.")
                if args.commit or args.push:
                    commit_and_maybe_push(repo_root, timestamp, push=args.push)
            else:
                print("No skill file changes found; README, changelog, and Git were left untouched.")
            return 0

        copy_changed_files(source_root, target_root, changes.added, changes.modified)
        if changes.deleted:
            archive_deleted_files(target_root, archive_root, changes.deleted)

        latest_log = write_change_log(
            change_logs_dir=change_logs_dir,
            timestamp=timestamp,
            timestamp_slug=timestamp_slug,
            changes=changes,
            archive_rel=archive_rel,
        )
        write_readme(
            repo_root=repo_root,
            target_root=target_root,
            change_logs_dir=change_logs_dir,
            latest_log=latest_log,
        )

        if args.commit or args.push:
            commit_and_maybe_push(repo_root, timestamp, push=args.push)

        return 0
    finally:
        lock_file.close()


def main() -> int:
    args = parse_args()
    if args.push:
        args.commit = True
    try:
        return sync(args)
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
