# MuseForge

**把优秀的图像生成知识，提炼成更好的视觉提示词。**

> 你的 AI 图像生成创意副驾。
>
> English version: [README.md](README.md)

描述你想要什么。MuseForge 会:

1. **理解你的意图** —— 从自然语言需求中推断 use case、平台、画幅比例、风格、可能的视觉 Pattern。
2. **找到经过验证的图像生成 Pattern** —— 从知识库中检索 Recipe、Visual Pattern、Style、Technique。
3. **推荐视觉方向** —— Creative Director 设计图像，不是套模板。
4. **设计构图** —— 视觉层级、前景/中景/背景、光影、色彩、字体、负空间。
5. **应用相关 Prompt Technique** —— 文字渲染、产品保护、品牌保护、相机/镜头控制、留白等。
6. **产出可投产的 Prompt** —— 结构化、任务驱动、清晰、具体、视觉一致、不冗余、没有低信息形容词的 Super Prompt。

```
想法
  ↓
意图分析
  ↓
知识检索（cases / recipes / patterns / styles / techniques / DNA）
  ↓
Creative Director（设计图像）
  ↓
Prompt Composer（把设计转成 prompt）
  ↓
Model Optimizer（模型特化变体）
  ↓
结构化回答 + Super Prompt
```

---

## MuseForge 是什么

MuseForge 是一个 **AI 图像生成助手**，把图像生成知识提炼成更好的视觉 prompt。它扮演 **Creative Director + Prompt Engineer** 的角色。

它来源于对 17+ 个高质量图像生成仓库的系统性研究，并把它们的智慧提炼成一套带类型的知识模型 —— Recipe、Visual Pattern、Style、Technique、Prompt DNA —— 从而能推荐"如何设计一张图像"，而不仅仅是"该复制哪条 prompt"。

## MuseForge 不是什么

- ❌ Prompt 收藏库 / Awesome List。
- ❌ Prompt 清洗 / 格式化工具。
- ❌ Prompt 数据库前端。
- ❌ 图像生成 API 客户端（V0 不调用任何图像模型）。
- ❌ 评测 / 排行榜。

> *知识 > 收藏。Pattern > Prompt 仓库。Recipe > 随机例子。质量 > 数量。可复用系统 > 病毒式 Prompt。Creative Direction > Prompt 扩展。归属 > 复制。*

---

## 30 秒演示

```bash
$ museforge ask "帮我做一张 AI 公司招聘小红书封面，3:4，极简，专业，有一点编辑感。"
```

MuseForge 不只是返回一条 prompt —— 它返回**一整套设计方向**:

```
Intent: recruitment marketing / social media poster
Platform: Xiaohongshu  Aspect ratio: 3:4

## Creative Direction
Concept: Communicate a message clearly and elegantly.
Goal: A text-first editorial poster with clear hierarchy.
Rationale: the Editorial Poster recipe matches the recruitment marketing use case;
           the Editorial Text-first Poster pattern fits the visual goal;
           the editorial minimalism style matches the requested aesthetic;
           5 technique(s) apply to this task.

## Recommended Recipe: Editorial Poster
  1. Set canvas/format and aspect ratio.
  2. Define the visual goal and message.
  3. Choose the layout (text-first, grid, centered).
  4. Place the headline as the dominant element.
  5. Add supporting text with clear hierarchy.
  6. Add a supporting illustration or icon.
  7. Select the style (editorial minimalism, retro, Swiss).
  8. Choose a restrained color palette.
  9. Specify typography (headline + supporting).
  10. Add details and constraints (text readability, low density).

## Recommended Pattern: Editorial Text-first Poster
Headline-first layout with supporting text and illustration.

## Style: editorial minimalism

## Composition
text-first with a single focal point

## Key Techniques
text rendering, visual hierarchy, whitespace / negative space,
negative constraints, reference image

## Super Prompt
Format: 3:4 Xiaohongshu
Visual goal: Communicate a message clearly and elegantly.
Layout: text-first with a single focal point
Visual hierarchy: headline -> supporting text -> illustration
Style: editorial minimalism
Color: muted, 1-2 accent colors
Typography: strong sans-serif or serif headline, small supporting text
Negative space: generous margins
Details: small illustration or icon
Constraints: text readability first; low density
Avoid: clutter; high density; many competing elements
```

六个完整 demo 见 [`examples/`](examples/):

1. [`demo-1-xiaohongshu-recruitment.md`](examples/demo-1-xiaohongshu-recruitment.md) — 小红书招聘封面。
2. [`demo-2-fintech-card-ad.md`](examples/demo-2-fintech-card-ad.md) — 金融科技银行卡广告。
3. [`demo-3-saas-hero.md`](examples/demo-3-saas-hero.md) — SaaS / AI 产品 Hero Visual。
4. [`demo-4-cinematic-portrait.md`](examples/demo-4-cinematic-portrait.md) — 电影感人物肖像。
5. [`demo-5-chinese-infographic.md`](examples/demo-5-chinese-infographic.md) — 中文信息图。
6. [`demo-6-multi-panel-comic.md`](examples/demo-6-multi-panel-comic.md) — 多格漫画。

---

## 快速开始

### 安装

```bash
git clone https://github.com/Lunar-feedmob/museforge.git
cd museforge
pip install -e ".[dev]"
```

不需要 API key。核心路径走离线确定性启发式。如需启用 LLM 驱动的意图理解、分析与编排，在 `.env` 中配置一个 provider：

```bash
cp .env.example .env
# 编辑 .env，设置你的 provider（例如 ANTHROPIC_API_KEY=... 或其他厂商 key）
```

### Ask

```bash
museforge ask "Create a premium fintech card advertisement"
museforge ask "Create a clean SaaS AI product hero" --model gpt-image-2
museforge ask "Create a Chinese infographic about AI trends" --prompt-only
```

### 检索知识库

```bash
museforge recipes search "poster"
museforge patterns search "product hero"
museforge styles search "editorial"
museforge techniques search "text rendering"
museforge cases search "fintech"
museforge prompts search "luxury product"
```

### 分析 / 改进 / 模型特化

```bash
museforge analyze "帮我做一张 AI 公司招聘小红书封面"        # 意图分析
museforge improve "amazing stunning product shot"          # 去除低信息形容词
museforge optimize "A product hero shot" --model nano-banana-pro  # 模型特化变体
```

### 检查

```bash
museforge stats     # 知识库各实体数量
museforge sources   # 已注册的来源仓库
```

---

## CLI 参考

```
museforge ask "..." [--model MODEL] [--prompt-only]
    把图像想法转成结构化的 Creative Direction + Super Prompt。

museforge analyze "..."
    把需求解析为结构化 Intent（use case、平台、画幅比例、…）。

museforge improve "..." [--feedback "..."]
    改进现有 prompt（去除低信息形容词 + 追加反馈）。

museforge optimize "..." --model MODEL
    生成模型特化的 prompt 变体。输出带有 `optimization_basis` 标签
    （repository-derived / community-derived / heuristic）。

museforge {cases,prompts,recipes,patterns,styles,techniques} search "..." [--top K]
    检索知识库。

museforge sources   列出已注册的来源（license、归属要求）。
museforge stats      显示知识库各实体类型的数量。

# 后台命令（维护者使用，不是 README 的第一卖点）
museforge ingest  SOURCE_ID SOURCE_URL [--license LICENSE]
museforge normalize TEXT
museforge dedup {exact|normalized|near|semantic|visual-intent} TEXT1|TEXT2|...
```

### `--model` 取值

`universal`（默认）、`gpt-image`、`gpt-image-2`、`nano-banana`、`nano-banana-pro`、
`seedream`（及别名）。`universal` 不返回模型特化变体；其他选项会附加该模型的已知指导并标注 `optimization_basis`。

---

## MuseForge 知道什么

MuseForge 存储的是**带类型的知识**，不是原始 prompt。

| 实体 | 是什么 | 为什么重要 |
|---|---|---|
| **Case** | 完整分析后的例子（主体、构图、光影、风格、…） | "MuseForge 之前见过类似的优秀案例吗？" |
| **Recipe** | 完成某类图像任务的方法（步骤、决策点、失败模式） | 最有价值的实体。一个 Recipe 覆盖一千条 prompt。 |
| **Visual Pattern** | 可复用的视觉结构（如 Breakout Product Hero） | 可跨产品、品牌、主体复用。 |
| **Style** | 可复用的视觉系统（如 editorial minimalism） | 严格与 Category（图像的用途）分开。 |
| **Technique** | 影响输出质量的 prompt engineering 杠杆（如文字渲染、产品保护） | 可迁移的"如何提问"最小单位。 |
| **Prompt DNA** | 可组合的 prompt 结构单元 | 替换变量，保留视觉系统。 |
| **Model** | 模型能力，带 `source_type` 标签 | 永远不是未经验证的 benchmark。 |
| **Source** | 来源仓库或出处 | 归属是 schema 字段，不是事后补充。 |

每一条推荐都是**可解释的**：Assistant 永远能说出*为什么*推荐某个方向（"这个 case 实例化了 Breakout Product Hero pattern，而 Product Hero Ad recipe 正好推荐它"）。

---

## 流水线

```
User request
  → IntentAnalyzer.understand_request()       → Intent
  → Retrieval（cases / recipes / patterns / styles / techniques / DNA）
  → CreativeDirector.design()                 → CreativeDirection
  → PromptComposer.compose()                  → Super Prompt
  → ModelOptimizer.optimize()                 → 模型特化变体
  → MuseForgeAssistant.generate_response()    → 结构化回答
```

V0 的每一个环节都带有**确定性启发式**实现，因此 `museforge ask` 在没有 API key 时也能工作。当配置了 LLM provider 时，同样的环节会自动改用 LLM。

---

## MuseForge 与普通 prompt 仓库的不同

| 普通 prompt 仓库 | MuseForge |
|---|---|
| 存储**文本** | 存储**带类型、带链接的知识** |
| "有哪些 prompt？" | "这张图应该怎么设计，为什么？" |
| 通过增加更多 prompt 扩展 | 通过增加**抽象**扩展（一个新 Recipe 覆盖一千条 prompt） |
| 一次性灵感 | 可复用系统 |
| 归属是事后补充 | 归属是 schema 字段（`source_repo`、`source_url`、`author`、`license`） |
| "10,000+ prompts" 作为卖点 | "懂得如何设计一张图" 作为卖点 |
| 没有 Creative Director | 真正的 Creative Director 先设计、再编排 |

在已有项目中，与 MuseForge 哲学最接近的是
[`freestylefly/awesome-gpt-image-2`](https://github.com/freestylefly/awesome-gpt-image-2)（"Prompt as Code"——原子化 schema、模板）。MuseForge 更上一层：**Recipe**（带步骤和失败模式的方法）、**Visual Pattern**（可复用的视觉结构），以及一个**Creative Director** 来选择和适配它们。

---

## 研究基础

MuseForge 的知识模型建立在对 17+ 个高质量图像生成仓库的系统研究之上。详见：

- [`docs/repository-comparison.md`](docs/repository-comparison.md) —— 每项设计决策的证据基础（继承什么、改进什么、避免什么）。
- [`docs/best-of-existing-repos.md`](docs/best-of-existing-repos.md) —— 提炼出的资产（最佳 Recipe、Pattern、Technique、Style、元数据思路）。
- [`docs/feature-comparison.md`](docs/feature-comparison.md) —— 功能采纳决策（V0 / V1 / V2 / Later / Do Not Build）。

## 架构

- [`docs/architecture.md`](docs/architecture.md) —— 分层架构（Knowledge → Retrieval → Service → CLI；MCP 作为未来 adapter）。
- [`docs/methodology.md`](docs/methodology.md) —— 知识获取与 prompt 生成流水线。
- [`docs/knowledge-model.md`](docs/knowledge-model.md) —— 完整的知识 schema 与实体关系。
- [`docs/mcp-roadmap.md`](docs/mcp-roadmap.md) —— 如何接入 MCP（小改动，不是重构）。

---

## 许可证与归属

> *"License 不明 → 不要复制 prompt 文本。"*

每一条被再分发的 prompt，MuseForge 都记录 `source_repo`、`source_url`、`author`、`license`。每一条关于模型的声明都带有 `source_type` 标签（`official` / `repository-derived` / `community-derived` / `inferred` / `experimental` / `unverified`）。

完整策略与 license 决策表见 [`docs/licensing.md`](docs/licensing.md)。

`data/` 中的种子知识是**合成的**（为 MuseForge 编写），其 `source_repositories` 字段指向**启发了**这些抽象的仓库（作为公开事实）。三条种子 prompt 是来自 MIT / CC BY 4.0 来源的带完整归属的注释样例。

---

## 状态

**V0** —— 知识获取、去重、分析、抽取、检索、Creative Direction、Prompt 编排。尚未接入图像生成 API。

- ✅ 研究 17+ 个真实仓库。
- ✅ 9 个带类型的知识实体 + JSON Schema + Pydantic 模型。
- ✅ 五级去重（exact → normalized → near → semantic → visual-intent）。
- ✅ 检索（元数据 + BM25/fuzzy + provider-agnostic embedding 接口）。
- ✅ Creative Director + Prompt Composer + Model Optimizer。
- ✅ CLI（`ask`、search groups、`analyze`、`improve`、`optimize`、`sources`、`stats`、后台 `ingest`/`normalize`/`dedup`）。
- ✅ 6 个 demo + 合成种子知识。
- ✅ 58 个测试，ruff 通过，mypy 通过。

V1+ 规划见 [`docs/roadmap.md`](docs/roadmap.md)（Web Gallery、语义搜索、Prompt Remix、MCP Server、图像生成）以及反目标（MuseForge 永远**不会**做的事）。

## 自检

项目简报里的 V0 自检 8 问在 [`docs/self-check.md`](docs/self-check.md) 中如实回答。

---

## 贡献

贡献应增加**可复用知识**（recipe、pattern、style、technique、DNA），而不是原始 prompt。归属不可妥协：每一条被再分发的 prompt 都必须带 `source_repo`、`source_url`、`author`、`license`。License 不明 → 只存元数据 + 分析。

完整贡献指南和知识 schema 见 [`CONTRIBUTING.md`](CONTRIBUTING.md) 和 `schemas/`。

## 许可证

MIT。被再分发的第三方 prompt 携带各自的 license 和归属 —— 见 [`docs/licensing.md`](docs/licensing.md)。

## 致谢

MuseForge 的灵感与基础来自 [`docs/repository-comparison.md`](docs/repository-comparison.md) 中所研究仓库的维护者与贡献者。尤其感谢：

- [`freestylefly/awesome-gpt-image-2`](https://github.com/freestylefly/awesome-gpt-image-2) —— "Prompt as Code" 原子化 schema 思路。
- [`VigoZhao/AI-Visual-Prompt-Cookbook`](https://github.com/VigoZhao/AI-Visual-Prompt-Cookbook) —— "复制一个 JSON，得到一个风格"的封装思路。
- [`wuyoscar/GPT-Image2-Skill`](https://github.com/wuyoscar/GPT-Image2-Skill) —— CLI + skill 的交付模型。
- [`mythkiven/rednote-director-skill`](https://github.com/mythkiven/rednote-director-skill) —— 视觉导演工作流。
- [`ZeroLu/awesome-nanobanana-pro`](https://github.com/ZeroLu/awesome-nanobanana-pro) —— `[VARIABLE]` 模板化 prompt。
- [`jamez-bondos/awesome-gpt4o-images`](https://github.com/jamez-bondos/awesome-gpt4o-images) —— case template + 归属纪律。
- [`YouMind-OpenLab`](https://github.com/YouMind-OpenLab) 系列 —— 多语言规模与推荐 skill。
- [`alexewerlof`](https://gist.github.com/alexewerlof/1d13401a7647339469141dc2960e66a9) —— 图像 prompt 的类型化 JSON schema 思路。
