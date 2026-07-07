# Doubao Skills

本仓库每天同步 Doubao 任务模式的 `.skills` 目录，保留当前 skill 文件、自动生成索引，并为每次变化生成独立说明。

## 同步概览

- 同步目录：`skills/`
- 任务计划：`DoubaoSkillsDailySync`，每天 18:00 运行
- 当前 skill 数：37
- 当前文件数：461
- 最近变更：[2026-07-07-161744](change-logs/2026-07-07-161744.md) - 本次同步新增 461 个文件、修改 0 个文件、删除 0 个文件。 新增 skill：browser-task, doubao-app-builder, doubao-creative-design, doubao-creative-drama, doubao-creative-video, doubao-cron-scheduler, doubao-...

## Skill 索引

| Skill | Files | Description |
| --- | ---: | --- |
| `browser-task` (`skills/browser-task`) | 15 | 浏览器自动化任务处理技能。仅在以下情况使用：1) 其他 skill/工具（搜索、API、数据接口等）都无法满足需求，需要通过真实浏览器 GUI 兜底执行；2) 任务必须在具体网站完成登录 / 授权 / 账号内动作（点赞 / 收藏 / 评论 / 发布 / 加购）；3) 命中白名单网站（淘宝/天猫、微博、小红书）的站内检索 / 互动 / 发布需求。当用户仅需要信息检索、文本生成、代码或数据处理时，不要使用本 skill。 |
| `doubao-app-builder` (`skills/doubao-app-builder`) | 1 | 统一处理网页应用的生成、编辑，以及围绕已生成产物的问答。既负责把自然语言需求端到端转成可运行、可预览、可交付的网页应用产物，也负责在用户追问产物时基于真实产物作答。当用户要生成网站、H5、网页应用、管理后台、数据看板时使用。当用户要编辑已有网页应用、做功能新增、页面调整或 Bug 修复时使用。当用户提供 PRD、文档、截图或素材包并要求产出可预览网页应用时使用。当用户针对已生成的网页应用，要求总结或解读网页内容、查看或分析源码、解... |
| `doubao-creative-design` (`skills/doubao-creative-design`) | 8 | 用于创意设计与视觉生成场景，面向从单张图片生产到多资产视觉交付的各类设计任务。可覆盖品牌视觉、营销物料、社媒内容、电商素材、信息表达、产品展示、包装设计、IP形象及多资产视觉系统等图片设计场景。 |
| `doubao-creative-drama` (`skills/doubao-creative-drama`) | 6 | 当用户提出短剧、动画、微电影、剧情视频、AI视频、电影、影视化、动态漫、宣传片、预告片等制作需求，或包含“做个短剧”、“弄个动画片”、“写个剧本”、“画个分镜”、“搞个人设/场景资产”、“出个关键帧”、“写图生视频提示词/Seedance提示词”等表达时调用。适用于需要按“规划-剧本-分镜-资产-关键帧-视频生成”推进完整视频生产流程的任何场景。 |
| `doubao-creative-video` (`skills/doubao-creative-video`) | 4 | 当用户需要通用视频生成、视频创作、视频提示词规划或文生/图生视频时使用，包括创意视频、产品广告、商品广告、UGC口播/带货/信息流视频、marketing/TVC风格广告、企业宣传片、商务视频、品牌形象片、产品功能介绍、带旁白视频，以及带 ref/参考素材的视频生成。禁止用于短剧创作、剧情脚本、分集剧情、角色扮演故事或影视叙事创作；此类需求应调用 doubao-creative-drama。仅当用户明确要求把短剧/剧情素材改造成普... |
| `doubao-cron-scheduler` (`skills/doubao-cron-scheduler`) | 1 | 创建、查看、更新或删除定时任务：一次性提醒、周期任务、后台监控、多轮编辑已有任务、登录态/权限敏感任务。用于用户要求提醒我、稍后检查、持续关注、每天/每周/每小时运行、创建定时任务/提醒/监控、修改/暂停/删除刚才或已有定时任务。 |
| `doubao-daily-stock` (`skills/doubao-daily-stock`) | 9 | 用于单一上市股票或二级市场公司的当日/近期个股日报，解释涨跌和异动原因，梳理行情、资金流、新闻公告、板块联动、技术面、预期与风险。适用于“某股今天为什么涨跌”“做个日报”“近期表现”“资金面和消息面”等问题；默认先输出结构完整、观点深入的对话版分析，并询问是否写入飞书文档；不用于长期商业模式/护城河、财报业绩、行业/板块、多股主题、一级市场或大盘事件解读。 |
| `doubao-earnings-analysis` (`skills/doubao-earnings-analysis`) | 23 | 上市公司财报/季报/年报/业绩的深度因果分析，覆盖A股、港股、美股和中概股。用于解读财报表现、亮点/风险、收入利润等指标变动、超预期或低于预期原因，以及针对毛利率、现金流、费用率等具体变量的归因问题。不用于纯股价、估值、评级、目标价、非财报新闻或未锚定具体公司报告期的宏观行业讨论。 |
| `doubao-finance-sector` (`skills/doubao-finance-sector`) | 36 | 对【板块/概念/主题/题材】的短期市场热度做专业、可证伪的深度分析，并在用户要求『生成飞书文档』时通过 lark-doc 写入结构化飞书文档。触发场景：当用户问某板块/概念/题材现在热不热、能不能追、为什么走强或降温、持续性如何、成交主要活跃在哪些方向、内部谁强谁弱，或要求生成对应飞书文档时触发。不适用场景：行业长期趋势、单股行情、公司基本面/财报、大盘/宏观等话题，不触发本skill。 |
| `doubao-market-hotspot` (`skills/doubao-market-hotspot`) | 13 | 面向普通股民的市场整体与宏观事件解读。用户关注全市场涨跌、交易主线、市场热点、宏观/政策/新闻/风险事件、央行利率、通胀就业、跨资产联动、资金风险偏好或市场情绪时使用。命中后先输出结构完整、观点深入的对话框分析，用户确认后通过 lark-doc 写入飞书 XML 文档。不要用于单股、具体板块/行业/公司/财报分析，或荐股、目标价、买卖点、仓位建议；不确定时先澄清。飞书交付需已安装 lark-doc 伴生 Skill。 |
| `doubao-qa` (`skills/doubao-qa`) | 7 | 当用户询问豆包产品身份、能力、会员、第三方服务、平台规则、隐私安全、记忆功能、数据处理或其他豆包产品本身相关问题时使用。 |
| `doubao-sentiment-tracker` (`skills/doubao-sentiment-tracker`) | 6 | 当用户在网页端或电脑客户端需要进行舆情监控、调研、社交媒体反馈收集、用户评价、品牌声量追踪时使用。支持微博、知乎、即刻、脉脉、B站、抖音.等多平台的舆情搜索、内容筛选和原始帖子溯源。注意：判断用户所处平台是手机端时，禁止触发这个skill。 |
| `doubao-visualization` (`skills/doubao-visualization`) | 5 | 当用户的需求依赖可视化展示、画图、图解、趋势图、关系图、交互/动态演示、动画讲解，或数据趋势占比排名、多指标对比、算法状态机、参数变化教学、结构化知识、几何构造证明需要图示时使用；地图、附件生成、纯文字足够场景不使用。 |
| `lark-approval` (`skills/lark-approval`) | 4 | 飞书审批：查询和处理审批待办/已办/实例，搜索可发起审批定义、查看定义详情并发起原生审批实例。当用户要处理审批任务、查看审批实例、搜索或发起审批时使用。审批待办不是飞书任务；非审批类待办走 lark-task。不负责创建审批定义；三方审批定义不走原生提单。 |
| `lark-attendance` (`skills/lark-attendance`) | 1 | 飞书考勤打卡：查询自己的考勤打卡记录 |
| `lark-base` (`skills/lark-base`) | 26 | 飞书多维表格（Base）操作：建表、字段、记录、视图、统计、公式/lookup、表单、仪表盘、workflow、角色权限；遇到 Base/多维表格/bitable 或 /base/ 链接时使用。文件导入转 lark-drive。 |
| `lark-calendar` (`skills/lark-calendar`) | 11 | 飞书日历：管理日历日程和会议室。查看/搜索日程、创建/更新日程、管理参会人、查询忙闲和推荐时段、预定会议室。当用户需要查看日程安排、创建/修改会议、查询/预定会议室时使用。不负责：查询过去的视频会议记录（走 lark-vc）、待办任务（走 lark-task）。 |
| `lark-contact` (`skills/lark-contact`) | 3 | 飞书 / Lark 通讯录:按姓名 / 邮箱解析成 open_id,或按 open_id 反查姓名 / 部门 / 邮箱 / 联系方式 / 个人状态 / 签名。当用户提到某人姓名要下一步发消息 / 排日程,或拿到 open_id 想查具体信息时使用。不负责部门树遍历、按部门列员工、组织架构图,这类需求走原生 OpenAPI。 |
| `lark-doc` (`skills/lark-doc`) | 42 | Lark Doc 文档统一入口：处理在线 Docx/Wiki 与本地 Word/PDF 文档任务。在线文档 URL/token、读取、创建、编辑、总结等任务路由到 online-doc；本地 .docx/.doc/.pdf 文件、明确要求 Word/PDF 交付或格式保留处理的任务路由到 office-word。不处理 Sheet、Slide、Excel、PowerPoint、Base 表内操作。 |
| `lark-drive` (`skills/lark-drive`) | 41 | 飞书云空间（云盘/云存储）：管理 Drive 文件和文件夹，包含上传/下载、创建文件夹、复制/移动/删除、查看元数据、评论/权限/订阅、标题、版本和本地文件导入。用户需要整理云盘目录、处理云空间资源 URL/token，或导入 Word/Markdown/Excel/CSV/PPTX/.base 为 docx/sheet/bitable/slides 时使用；doubao.com 云空间 URL/token 也按资源路径和 tok... |
| `lark-im` (`skills/lark-im`) | 25 | 飞书即时通讯：收发消息和管理群聊。发送和回复消息、搜索聊天记录、管理群聊成员、上传下载图片和文件（支持大文件分片下载）、管理表情回复、发送应用内/短信/电话加急、发送交互卡片（Interactive Card）。当用户需要发消息、查看或搜索聊天记录、下载聊天中的文件、查看群成员、搜索群、创建群聊或话题群、管理标记数据、管理 Feed 置顶（添加/移除/查询置顶会话）、管理标签数据时使用。 |
| `lark-mail` (`skills/lark-mail`) | 31 | 飞书邮箱：Use when user mentions 起草邮件、写邮件、草稿、发送/回复/转发邮件、查阅邮件、看邮件、搜索邮件、邮件文件夹、邮件标签、邮件联系人、监听新邮件、邮件收信规则等；use for mail/email intent only. Do not use for docs/sheets/calendar/auth setup/pure contact lookup/IM chat tasks. |
| `lark-markdown` (`skills/lark-markdown`) | 6 | 飞书 Markdown：查看、创建、上传、编辑和比较 Markdown 文件。当用户需要创建或编辑 Markdown 文件、读取、修改、局部 patch 或比较差异时使用。不负责将 Markdown 导入为飞书在线文档，也不负责文件搜索、权限、评论、移动、删除等云空间管理操作。 |
| `lark-minutes` (`skills/lark-minutes`) | 9 | 飞书妙记：搜索妙记、查看妙记基础信息、下载/上传音视频、读取或编辑妙记的产物内容、改标题、替换说话人/关键词。当给出minute_token、本地音视频文件，要查/改/转妙记产物时使用；本地音视频转纪要/逐字稿优先走本 skill，不要用 ffmpeg/whisper 本地转写。不负责：获取会议关联妙记，或仅按自然语言标题定位纪要 |
| `lark-note` (`skills/lark-note`) | 3 | 飞书会议纪要（Note）直查：已知 note_id 时查询纪要详情、展示类型、关联文档 token，并读取 unified 原始逐字记录。当用户已持有 note_id，或从文档显式 vc-node-id 获得 note_id 时使用。不负责会议/日程/妙记定位、文档标题搜索或 Docx 正文读取。 |
| `lark-okr` (`skills/lark-okr`) | 15 | 飞书 OKR：管理目标与关键结果。查看和编辑 OKR 周期、目标、关键结果、对齐关系、量化指标和进展记录。当用户需要查看或创建 OKR、管理目标和关键结果、查看对齐关系时使用。不负责：待办任务管理（lark-task）、日程/会议安排（lark-calendar）、绩效评估 |
| `lark-openapi-explorer` (`skills/lark-openapi-explorer`) | 1 | 飞书/Lark 原生 OpenAPI 探索：从官方文档库中挖掘未经 CLI 封装的原生 OpenAPI 接口。当用户的需求无法被现有 lark-* skill 或 lark-cli 已注册命令满足，需要查找并调用原生飞书 OpenAPI 时使用。 |
| `lark-ppt` (`skills/lark-ppt`) | 1 | 创建令人惊艳的 PPT 演示文稿。当用户要求制作、生成、创建 PPT/演示文稿/幻灯片，或者要求生成 PPT 大纲、修改已有 PPT 页面内容时，使用此技能。覆盖完整的 PPT 工作流：素材收集（互联网搜索与网页抓取）、图片获取（搜索真实图片或生成创意图片）、PPT 页面生成与编辑。也适用于用户上传附件并要求据此制作 PPT、提供模板要求套用、或就 PPT 设计（配色/排版/字体）进行咨询的场景。即使用户只是简单说'帮我做个 PP... |
| `lark-project` (`skills/lark-project`) | 4 | 飞书项目（Meego/Meegle）操作工具。支持查询和管理工作项、节点流转、视图查询、个人待办、排期统计等功能。 Use when user needs to work with Feishu/Lark Meego project management — including querying work items, creating/updating work items, completing workflow nodes,... |
| `lark-sheets` (`skills/lark-sheets`) | 30 | 表格全场景处理：本地 Excel/CSV 与在线表格（飞书、doubao.com 的 /sheets/ 链接）的创建、读写、分析、计算、建模、语义处理、可视化与美化。**只要用户输入包含表格类附件——上传 .xlsx/.xls/.csv 文件，或给出 feishu/doubao.com 的 /sheets/ 链接或 token——必须加载本技能。** 此外，用户口述数据要整理成表，或要求计算/统计/建模/预测/透视/可视化/美化/... |
| `lark-task` (`skills/lark-task`) | 18 | 飞书任务：管理任务、清单和任务智能体。创建待办任务、查看和更新任务状态、拆分子任务、组织任务清单、分配协作成员、上传任务附件、注册或注销任务智能体、更新任务智能体的主页数据、写入智能体任务记录。当用户需要创建待办事项、查看任务列表、跟踪任务进度、管理项目清单或给他人分配任务、为任务上传附件文件、注册注销任务智能体、更新智能体主页数据、写入任务记录时使用。 |
| `lark-vc` (`skills/lark-vc`) | 5 | 飞书视频会议：搜索历史会议记录、查询会议纪要（总结/待办/章节/逐字稿）、查询参会人快照。当用户查询已结束的会议、获取会议产物（纪要/妙记）、查看参会人时使用；查询未来日程走 lark-calendar。不负责：Agent 真实入会/离会、会中实时事件。 |
| `lark-whiteboard` (`skills/lark-whiteboard`) | 30 | 飞书画板：查询和编辑飞书云文档中的画板。支持导出画板为预览图片、导出原始节点结构、使用多种格式更新画板内容。 当用户需要查看画板内容、导出画板图片、编辑画板时使用此 skill。不负责：飞书云文档内容编辑（lark-doc）、文档内嵌电子表格/Base（lark-sheets / lark-base）。 |
| `lark-wiki` (`skills/lark-wiki`) | 13 | 飞书知识库：管理知识空间、空间成员和文档节点。创建和查询知识空间、查看和管理空间成员、管理节点层级结构、在知识库中组织文档和快捷方式。当用户需要在知识库中查找或创建文档、浏览知识空间结构、查看或管理空间成员、移动或复制节点时使用。当用户给出 doubao.com 的 /wiki/ URL/token 时，也应直接使用本 skill，不要因为域名不是飞书而回退到 WebFetch；路由依据是 URL 路径模式和 token，而不是域... |
| `lark-workflow-meeting-summary` (`skills/lark-workflow-meeting-summary`) | 1 | 会议纪要整理工作流：汇总指定时间范围内的会议纪要并生成结构化报告。当用户需要整理会议纪要、生成会议周报、回顾一段时间内的会议内容时使用。 |
| `lark-workflow-standup-report` (`skills/lark-workflow-standup-report`) | 1 | 日程待办摘要：编排 calendar +agenda 和 task +get-my-tasks，生成指定日期的日程与未完成任务摘要。适用于了解今天/明天/本周的安排。 |
| `skill-creator-for-task` (`skills/skill-creator-for-task`) | 6 | 创建有效 Skill 的指南。当用户想要创建新的 Skill，或更新现有 Skill，以便通过专门知识、工作流程或工具集成来扩展 AI Agent 能力时，应使用此 Skill。 |

## 最近变更

| Date | Change Log | Summary |
| --- | --- | --- |
| 2026-07-07-161744 | [2026-07-07-161744](change-logs/2026-07-07-161744.md) | 本次同步新增 461 个文件、修改 0 个文件、删除 0 个文件。 新增 skill：browser-task, doubao-app-builder, doubao-creative-design, doubao-creative-drama, doubao-creative-video, doubao-cron-scheduler, doubao-... |
