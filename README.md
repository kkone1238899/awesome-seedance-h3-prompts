# Awesome Seedance H3 Prompts

Seedance 2.0 / 2.5 + MiniMax H3 视频提示词实战库：从 X 上每天的实战帖子里提炼出的写法、双模型对照模板，外加 GitHub 同类仓库的每日自动归集。

> Seedance（即梦，字节）和 MiniMax H3 是现在出片最猛的两个视频模型，但写法各成一套。这个库把两边的实战经验放在一起：同一创意，两边分别怎么写；以及每天自动从 GitHub 捞新的相关仓库进来。

## 快速选型：三个模型什么时候用哪个

| 场景 | 首选 | 为什么 |
|---|---|---|
| 电影感短片、广告、MV | Seedance 2.5 | 运镜语言最精密，多参考绑定（@image/@video/@audio）最成熟 |
| 短剧、连贯叙事、换脸 | Seedance 2.0 / 2.5 | 角色一致性打法成熟，社区沉淀最多 |
| 写实人物、口型/音频同步、本地跑 | MiniMax H3 | 音画一体是强项；有 Mac 本地推理和 ComfyUI 工作流 |
| 预算敏感、想先低成本试错 | 先 Seedance 480p 抽卡 | 480p 先抽 4 条挑 keeper，再上高清——高清费用约翻倍，别盲跑 |

## Seedance 2.5：七段式 prompt 框架

按这个顺序写，缺一段就少一分控制力：

1. **参考绑定** — `@image1` 锁人物、`@video1` 锁运镜参考、`@audio1` 锁声音，一张表只放一张脸（多张脸会漂移）
2. **动作** — 写具体肌肉动作，不写情绪词。"两下点头、一个耸肩"而不是"他很开心"
3. **空间** — 机位、景别、场景布局；人物乱瞬移就给一张俯视布局图
4. **运镜** — 一条 clip 只给一个运镜；精确术语（推/拉/摇/移/跟），"电影感"这种模糊词无效
5. **风格** — 顶部贴固定风格块：全局问题只修风格块前缀，单镜头问题只改单条
6. **音频** — 台词加引号并附语气注（"轻蔑的不信"而不是"大喊"）；环境声单独写
7. **约束** — 负面约束用正说：写"他站稳、双脚扎地"，不写"不要摔倒"（模型会把 not 读成肯定）

**10 条实战铁律**（提炼自 175 节官方课程沉淀）：
- 角色表一次建好反复用：16:9 三面板（无头全身背面 / 无头全身正面 / 表情特写），存成固定元素
- 15 秒一个镜头包，镜头按 1a/1b/2a 命名
- 做连续性直接喂上一镜的**实际视频**，文字梗概会丢信息
- 对白戏从全景开场再切入
- 每轮跑 4 条：1 条失败重抽，4 条同方式失败就重写 prompt；一次只改一个变量，先说出失败类型（资产/动作/机位/坏种子）
- 换脸分两遍：第一遍定场景姿态表情颗粒，第二遍再换脸，每遍只干一件事
- 夜景 + 换脸是高危组合，多留预算；1080p 脸/口型易漂移，4k 更稳
- 常驻场景当角色一样锁定：固定机位、色卡、时间段，清理画面文字杂物（会变异）

详见 [prompts/seedance-2.5-framework.md](prompts/seedance-2.5-framework.md)。

## Seedance 2.0：核心要点

- **@ 引用语法**：`@image1` `@video1` `@audio1`，输入文件合计不超过 12 个
- **输入约束**：单条上限 15 秒、720p，长片分段做
- **运镜语言**：精确术语 > 形容词；时间线写法（每秒时间戳 + 镜头 + 灯光 + 声音）
- **2 秒钩子**：前 2 秒决定 50% 去留，钩子单独写一行
- **省钱**：480p 低清试条 → 确认方向 → 再生成正式版

详见 [prompts/seedance-2.0-essentials.md](prompts/seedance-2.0-essentials.md)。

## MiniMax H3：保姆级指南

H3 是音画一体模型，提示词要**同时写画面和声音**：

1. **定锚**：一句话说清"谁、在哪、干什么"（人物锚 + 场景锚 + 动作锚）
2. **锁脸**：传参考图锁定人物，防漂移
3. **写声音**：对白/环境声/音乐分开写，H3 的音频是加分项不是附赠
4. **控镜头**：一次一个运镜；多镜头用"镜头包"写法（1a/1b/2a）
5. **防翻车**：六个高频翻车点——人物漂移、镜头混乱、声音失控、口型错位、场景跳变、风格漂移；出问题先定位类型再改

**万能模板**（填空即用）：
```
[景别+角度]，[人物外貌+服装]，[具体动作]，[场景+时间+天气]，
[布光]，[运镜]，[声音：对白"…" + 环境声 + 音乐]，[风格+色彩]，
[技术：时长/比例]
```

详见 [prompts/minimax-h3-guide.md](prompts/minimax-h3-guide.md)。

## 双模型对照：同一创意，两边怎么写

| 要素 | Seedance 2.5 写法 | MiniMax H3 写法 |
|---|---|---|
| 人物锁定 | `@image1` 引用 + 角色表三面板 | 参考图直传 + 人物锚描述 |
| 运镜 | 精确术语，一条一个 | 同样一条一个，支持首尾帧 |
| 音频 | `@audio1` 绑定 + 台词引号注语气 | prompt 内分层写（对白/环境/音乐） |
| 否定 | 正说，不用"不要" | 同样正说 |
| 连续性 | 喂上一镜实际视频 | 喂上一镜实际视频 |
| 省钱 | 480p 抽卡再升档 | 低分辨率先跑，确认再高清 |

完整对照 + 3 个实战案例见 [prompts/dual-model-cheatsheet.md](prompts/dual-model-cheatsheet.md)。

## Skills 与工具（装完就能用）

<!-- AUTO-SKILLS:START -->
| [dexhunter/seedance2-skill](https://github.com/dexhunter/seedance2-skill) | Seedance 2.0 官方手册外挂：输入约束、@ 引用、运镜语言 | 4338 |
| [rediumvex/ai-video-generator-claude](https://github.com/rediumvex/ai-video-generator-claude) | 一句话想法 → 15–25 行生产级提示词（时间戳/运镜/布光/声音分层） | 422 |
| [zhouwei713/seedance-prompt](https://github.com/zhouwei713/seedance-prompt) | 真实感视频 prompt：反向设计"谁拍的、用什么拍的" | 328 |
| [AtlasCloudAI/awesome-seedance-2.5-prompts-skills](https://github.com/AtlasCloudAI/awesome-seedance-2.5-prompts-skills) | Seedance 2.5 七段式生成 + 分镜 + 复查一条龙 | 241 |
| [benjiyaya/Minimax-H3-Prompt-AgentSkill](https://github.com/benjiyaya/Minimax-H3-Prompt-AgentSkill) | 从素材 + 想法生成格式化 H3 提示词 | 150 |
| [penposs/minimax-h3-video-prompt](https://github.com/penposs/minimax-h3-video-prompt) | H3 提示词生成与评审 | 65 |
| [EVZheng-Lab/h3-seedance-prompt](https://github.com/EVZheng-Lab/h3-seedance-prompt) | 一个创意同时产出 H3 和 Seedance 2.5 两版官方格式提示词 | 21 |
<!-- AUTO-SKILLS:END -->

## 仓库导航（同类项目）

<!-- AUTO-REPOS:START -->
| [songguoxs/seedance-prompt-skill](https://github.com/songguoxs/seedance-prompt-skill) | Seedance 2.0 提示词生成 skill | 2939 |
| [antirez/h3.c](https://github.com/antirez/h3.c) | MiniMax H3 Mac 本地推理引擎 | 2919 |
| [ZeroLu/awesome-seedance](https://github.com/ZeroLu/awesome-seedance) | 高质量 Seedance 2.0 prompt 合集（电影/动漫/UGC/广告/meme） | 2734 |
| [AIMixer/ComfyUI_MiniMaxH3_Director](https://github.com/AIMixer/ComfyUI_MiniMaxH3_Director) | 多段落 H3 导演级 ComfyUI 工作流 | 2421 |
| [YouMind-OpenLab/awesome-seedance-2-prompts](https://github.com/YouMind-OpenLab/awesome-seedance-2-prompts) | 2000+ Seedance 2.0 prompt，API 指南、角色一致性技巧 | 2149 |
| [LearnPrompt/awesome-seedance](https://github.com/LearnPrompt/awesome-seedance) | 600+ 案例可溯源原帖，260+ 跨模型复测 | 2130 |
| [FlashML-org/FreeVideo](https://github.com/FlashML-org/FreeVideo) | 8GB 显存本地跑 MiniMax H3 | 2089 |
| [EvoLinkAI/awesome-seedance-2.5-guide](https://github.com/EvoLinkAI/awesome-seedance-2.5-guide) | Seedance 2.5 官方指南，36 个官方素材 | 412 |
| [Anil-matcha/awesome-seedance-2.5-api-prompts](https://github.com/Anil-matcha/awesome-seedance-2.5-api-prompts) | Seedance 2.5 API 指南、参数、示例 | 324 |
| [xianyu110/awesome-minimax-h3-prompts](https://github.com/xianyu110/awesome-minimax-h3-prompts) | MiniMax H3 提示词精选 | 60 |
| [AtlasCloudAI/awesome-minimax-h3-prompts](https://github.com/AtlasCloudAI/awesome-minimax-h3-prompts) | H3 官方展示案例（品牌片/动效/叙事/电商/游戏/工业） | 60 |
<!-- AUTO-REPOS:END -->

> 新发现的仓库会先进入 [data/candidates.json](data/candidates.json)，人工整理提炼后并入正文。自动归集脚本见 [scripts/collect.py](scripts/collect.py)。

## 怎么用它搞钱

- **商单**：用七段式框架 + 双模型对照接 AI 视频商单（广告/短剧/电商），交付物就是 prompt 包 + 成片
- **提示词代写**：按模板给客户写 Seedance/H3 提示词，一条龙收费
- **教学**：10 条铁律 + 万能模板做成教程/课程卖
- **矩阵号**：用 POV/舞蹈/换装模板批量起号，接广告或带货

## 更新日志

- 2026-10-18：建库。Seedance 2.5 七段式框架、2.0 要点、H3 保姆级指南、双模型对照、skills/仓库索引首版；接入每日自动归集（GitHub Actions + scripts/collect.py）。
