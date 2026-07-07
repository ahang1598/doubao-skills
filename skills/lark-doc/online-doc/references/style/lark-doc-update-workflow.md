# 改写增强工作流

用户提供已有文档链接或 token，需要改写、润色、补充或重排版时，遵循本工作流。

## 核心方法论 — Code-Act Loop
通过自适应的 **Code-Act Loop** 驱动文档改写，而非固定模板式的工作流。每次任务都循环执行：
1. **Plan（规划）** — 根据用户目标和文档当前状态，评估下一步该做什么
2. **Execute（执行）** — 由主 Agent 自己运行 `lark-cli docs` 命令推进改写；仅画板渲染按需隔离到 SubAgent（见步骤二）
3. **Observe（观察）** — 检查命令输出，验证正确性，确认内容是否满足用户目标
4. **Iterate（迭代）** — 如需调整，回到 Plan 继续循环

## 核心原则：精准手术优于全量覆盖
1. **精准手术**：只改用户指定的 block，不改其他 block。
2. **全量覆盖**：如果用户明确要改整篇，才用 `overwrite` 命令。
3. **保真约束**：改写时原文里的 `<cite type="user">`（@人）、`<cite type="doc">`（@文档）、`<img>`、`<source>`、`<whiteboard>`、`<sheet>`、`<bitable>`、`<synced_reference>` 等行内组件和资源块一律原样保留（含所有 token / user-id / doc-id 属性），不许替换成纯文本姓名、链接或占位符。

## 工作流程

### 步骤一：分析与画板识别（串行）

1. **选择读取范围**（节省上下文的关键）：
   - 用户只改某一节 / 文档较大 → 先 `docs +fetch --api-version v2 --scope outline --max-depth 2` 拿目录，再 `docs +fetch --api-version v2 --scope section --start-block-id <目标标题id> --detail with-ids` 精读该节（`section` 会自动展开到下一个同级/更高级标题前，不用手动算结束 block id）
   - 需要精确跨节区间 → `docs +fetch --api-version v2 --scope range --start-block-id xxx --end-block-id yyy`（或 `--end-block-id -1` 读到末尾）
   - 用户只给了模糊关键词 → `docs +fetch --api-version v2 --scope keyword --keyword xxx --context-before 1 --context-after 1 --detail with-ids`
   - 用户明确要改整篇 → `docs +fetch --api-version v2 --detail with-ids`
   - 详见 [`lark-doc-fetch.md`](../lark-doc-fetch.md) 的「选 `--scope`（读取范围）」
2. 系统性评估：用户想改什么、现有文档风格是什么、哪些内容需要保留、哪些问题影响理解
3. **画板识别**：逐章节扫描，判断是否有段落用图明显比文字更易懂（流程 / 架构 / 时间线 / 对比 / 占比等，见 `lark-doc-style.md` 的画板原则）。默认用文字，只有确需图示才记录需要插图的章节（block ID）、推荐画板类型、mermaid/SVG路径和源内容片段
4. 向用户简要说明改进计划（包含识别出的画板机会）

### 步骤二：定向改写（单 Agent 串行）

5. **优先处理步骤一识别出的画板候选段落**：参考 [lark-doc-whiteboard.md](../lark-doc-whiteboard.md) 中的方式插入图表画板。画板渲染仍隔离到 SubAgent（见下方「画板 SubAgent 子任务要求」），正文本身不交给子 Agent
6. 由主 Agent **顺序逐节**改写，**不拆分给并行子 Agent**——这样能始终对照全文，保证风格一致、不重复、不顾此失彼，也能执行「全文级」的组件约束：
   - 沿用或轻微调整已有文档风格，除非用户要求彻底重排版
   - 优先通过重写段落、调整标题、补充小标题提升可读性；叙述内容保持成段，**不要默认改成列表**，只有确属并列要点 / 步骤才用列表（见 `lark-doc-style.md`）
   - 富 block 是可选表达手段，不因固定比例而添加，取舍遵循 `lark-doc-style.md` 的写作原则；画板类需求只走第 5 步

### 步骤三：验证（串行）

7. 获取更新后文档局部内容，检查是否符合用户目标和已有风格
8. 检查是否满足用户目标并保留原有关键内容。再按 `lark-doc-style.md` 的写作原则**逐节核对**，发现问题则定向修正：
   - **去列举**：叙述性内容（背景 / 现状 / 认识 / 分析 / 成效等）是否被做成了列举？是则改成段落；列举只留给真正并列的具体措施 / 步骤 / 清单。
   - **查"通篇一是二是"**：是不是每个方面 / 每节都齐刷刷"一是 / 二是 / 三是"、几乎没有叙述段落？是则给背景 / 认识 / 分析 / 过渡补上段落，「一是 / 二是」只收到列具体问题 / 措施那一处（纯清单 / 台账类除外）。
   - **查编号**：全篇是否一套、不跳号、不跳级；**有没有中文序号 + 阿拉伯小数混用（一、+ 1.1）**。
   - **查呈现**：成行成列的数据是否该用表格却写成了段落 / "A+B+C"串？"小标题 + 一句话"的小项是否被升成了标题？是则按 `lark-doc-style.md` §二改成表格 / 标签行 / 加粗引导句段落。
   - **查组件**：高亮块 / 分栏 / 画板 / 颜色是否克制、符合体裁。
   
   修正后向用户呈现结果。

### 步骤四：字数校验（无明确字数要求则跳过）

**仅当**用户给了明确字数要求（写 N 字 / x-y 字 / x 字左右 / 上下浮动）时执行；否则**跳过本步**。字数必须用脚本量，不要自己估。

1. 把要求归一成参数：`>x`→`--min x`；`<y`→`--max y`；`x-y`→`--min x --max y`；`x 字左右`→`--approx x`（自动 ±10%）
2. 量实际字数（对齐飞书「总字数」）：`uv run scripts/count_chars.py --doc <document_id> <上面的目标参数>`（脚本在 online-doc skill 根的 `scripts/` 下）
3. 看输出 `verdict`：`pass` 即通过；`under` → 在最该展开处补**实质内容**（非注水）；`over` → 从最长/最冗余处删减。改完**重新跑脚本复测**
4. **最多 2 轮**。2 轮后仍不达标：停止，不得为达标而注水或删关键内容；如实汇报【目标区间 / 当前字数 / 差值与方向 / 已试 2 轮 / 未达原因】并交付文档链接，**禁止谎称达标**

## 画板 SubAgent 子任务要求

Mermaid 图由主 Agent 直接插入 `<whiteboard type="mermaid">...</whiteboard>`，无需 SubAgent。

SVG SubAgent 必须收到：文档 token、插入位置（标题/block ID）、图表目标、源内容片段、`lark-doc-xml.md` 路径，以及 [lark-doc-whiteboard.md](../lark-doc-whiteboard.md) 中的 "SVG 设计 Workflow" 指南。它只负责插入一个 `<whiteboard type="svg">...</whiteboard>`，不改其他正文，也不读取 `lark-whiteboard`。

已有画板更新 SubAgent 必须收到：board_token、图表目标、推荐画板类型、源内容片段、[`../../../../lark-whiteboard/SKILL.md`](../../../../lark-whiteboard/SKILL.md) 路径。它只负责写入画板，不改文档正文。

**上下文节省提示**：主 Agent 改某节时如需重新读取，优先用 `docs +fetch --api-version v2 --scope section --start-block-id <章节标题id>`（自动覆盖整节），或 `--scope range --start-block-id xxx --end-block-id yyy` 精确区间，只拉当前章节，不要重复拉全文。
