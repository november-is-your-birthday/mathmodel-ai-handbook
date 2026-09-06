# 数学建模 AI 手册（提示词 × 资源库 · 合并版）

> 生成日期：2026-09-06 · 由《数学建模AI提示词精选》与《数学建模AI资源库索引》合并而成
>
> **三种用法**：
> 1. **HTML 版（推荐）**：双击同目录的《数学建模AI手册.html》——左侧目录树点击跳转、顶部搜索框全文过滤；
> 2. **本 Markdown**：在 VSCode / Typora / Obsidian 中点击下方目录锚点跳转（不同编辑器对中文锚点的处理略有差异，跳转异常时用 HTML 版或 Ctrl+F）；
> 3. **检索**：任何环境 `Ctrl+F` 全文搜索。

---

## 📑 总目录

**第一部分 · 提示词精选**

- [〇、使用心法（比提示词本身更重要）](#〇使用心法比提示词本身更重要) —— 开题信息卡模板
- [一、开题定型主工作流 ★](#一开题定型主工作流-核心推荐) —— 7 步定型一条可辩护路线
- [二、拆题与思路构建](#二拆题与思路构建) —— FRAME 拆题 / 三视角头脑风暴 / LangGPT 模板 / 难点分析
- [三、假设与模型规格](#三假设与模型规格开题定型的最后一公里) —— 假设生成与红蓝对抗 / 选型 / 目标函数 / 灵敏度
- [四、思维扩展工具箱](#四思维扩展工具箱卡壳--想突破时用) —— 类比迁移 / 反向推演 / 机制覆盖 / 脆弱性测试
- [五、数据、求解与代码](#五数据求解与代码高频复用精选) —— 数据清洗 / AHP / TOPSIS / NSGA-II / RK4 …
- [六、论文写作与摘要](#六论文写作与摘要) —— 摘要 / 英文润色 / 优缺点 / 结论
- [七、答辩与评委视角自检](#七答辩与评委视角自检) —— 评委提问预测 / 局限性写作
- [八、英文互联网精选：Deep Research 提示词](#八英文互联网精选针对难题-deep-research-提示词) —— Research Plan / Meta Prompt / 研究简报（中英对照）
- [九、英文开源 Skill 与三个方法论模式](#九英文开源-skill--agent深度研究--数学建模) —— STORM 圆桌 / OptiMUS 三件套 / LLM-as-Judge（中文详解）
- [十、进阶：直接安装的获奖级工作流](#十进阶直接安装的获奖级工作流skill--agent) —— mathodology 一键安装命令 + 三大工具对比
- [附录 · 完整来源索引](#附录--完整来源索引) —— 全部资源的出处与可信度依据（位于文末）

**第二部分 · 资源库索引**（约 75 条，R1-R11）

- [R1、全流程 Agent 工作流与 Skills](#r1全流程-agent-工作流与-skills)
- [R2、提示词库合集](#r2提示词库合集)
- [R3、学术论文与基准（LLM × 数学建模）](#r3学术论文与基准llm--数学建模)
- [R4、深度研究困难问题专题](#r4深度研究困难问题专题) —— 提问方法论 / 商业产品 / 开源框架 / 论文与基准 / 方法论速览
- [R5、AI 文献检索与核验工具](#r5ai-文献检索与核验工具)
- [R6、数据来源](#r6数据来源)
- [R7、LaTeX 模板与优秀论文范例](#r7latex-模板与优秀论文范例)
- [R8、算法代码库与真题档案](#r8算法代码库与真题档案)
- [R9、学习路径与教程](#r9学习路径与教程)
- [R10、比赛规则与 AI 合规](#r10比赛规则与-ai-合规)
- [R11、按场景速查表](#r11按场景速查表) —— "现在要做什么 → 首选/备选"最快入口

---


# 第一部分 · 提示词精选

## 〇、使用心法（比提示词本身更重要）

1. **先喂上下文，再提问**：开一个新对话，先用"信息卡"把题目原文、附件数据、团队技能、时间预算一次性投喂给 AI，之后所有提问都基于这个上下文（"基于之前的题目背景……"）。
2. **迭代提问**：AI 第一轮输出通常不完美。代码报错直接贴报错信息；模型太简单就追加"考虑更复杂的约束条件/非线性因素"。
3. **验证一切**：AI 会产生幻觉（编造文献、错误公式）。关键数据、引用、公式必须交叉核验；每一行代码和公式要能自己讲明白。
4. **拆步骤问**：不要指望一次问出完整方案。按"拆题 → 多路线 → 定型 → 假设 → 求解 → 写作"逐段推进，每步确认后再进下一步。

**开题信息卡模板**（每次开新对话先发这个，来源：知乎"北海"美赛模板，实战改良版）：

```text
【赛题信息】
1. 竞赛类型：[全国大学生数学建模竞赛(CUMCM) / 美国大学生数学建模竞赛(MCM/ICM) __题(A-F) / 研究生数学建模竞赛]
2. 赛题原文：【粘贴完整题目文本及附件说明】
3. 数据说明：【附件列名、数据规模、缺失/异常情况】
4. 目标与要求：【题目要求交付什么：预测/优化/评价/方案+论文】
5. 团队情况：擅长语言[Python/MATLAB/无编程基础]、建模经验[首次/有基础]、可用时间[X天]
```

---

## 一、开题定型主工作流（★ 核心推荐）

综合获奖级开源方法论（mathodology 9-phase 工作流、NeurIPS 2025 MM-Agent 四阶段、模型视角 FRAME 拆题法）整理。**用途：拿到赛题后 1-2 小时内定型一条可辩护的建模路线。**

```text
# 角色
你是数学建模竞赛的国奖级指导教练，熟悉 CUMCM/MCM/ICM 评审标准。你的任务不是直接给答案，
而是带我完成一次"可辩护"的开题定型。逐步执行，每步先输出结果再等我确认。

（此处粘贴"〇"中的信息卡）

# 工作流
Step1 拆题：用 FRAME 框架拆解——F(题给事实/数据)、R(为谁解决什么问题)、
      A(要做哪些决策/预测)、M(可量化的变量、目标、约束)、E(怎样算"好")。
      然后列出题目全部要求并编号，每条标注对应交付物；指出歧义，并给出保守的默认解释。
Step2 可行性：对照给定数据逐条评估每条要求的可行性（能直接算 / 需代理变量 / 只能靠假设），标红风险项。
Step3 三路线提案：给出 3 条差异明显的建模路线（机理/微分方程类、统计/机器学习类、优化/运筹类），
      每条写清：核心方程或算法族、输入输出、所需数据、实现成本(人时)、与题目评分点的匹配度、
      最可能的失败模式。禁止只报模型名词，禁止堆砌通用方法。
Step4 定型：用表格按"数据匹配度、创新空间、可实现性、可解释性、评委亮点"五个维度
      给三条路线打分(1-5)并加权求和；明确推荐 1 条主路线 + 1 条保底路线，
      说明推荐理由和放弃其他路线的具体原因。
Step5 规格化：为选定路线输出——符号表；6-8 条假设(每条注明依据+验证方式)；
      目标函数与约束；求解算法与伪代码；验证指标(含 baseline 对比与敏感性检验计划)；
      至少 1 条"非教科书式"的创新点设计。
Step6 红队攻击：切换成挑剔的国奖评委，对上述方案提出 5 个最可能被质疑的问题
      (假设站不住/方法太通用/结果不可信/创新点牵强…)，每条给出最低成本的修补方案。
Step7 交付：输出 800 字《开题方案书》：问题重述 → 分问题的模型链条 → 创新点 →
      风险与备选 → 时间表。

现在从 Step1 开始。
```

---

## 二、拆题与思路构建

### 2.1 FRAME 五要素拆题（来源：模型视角提示词库 modelinsight.chat，配套《巧用DeepSeek进行数学建模》）

```text
请使用 FRAME 方法帮我拆解这个数学建模问题：
- F(事实)：题中给出的关键数据和信息
- R(角色)：我需要为谁解决什么问题
- A(行动)：需要做出哪些决策或预测
- M(数学)：哪些量可以量化为变量、目标和约束
- E(评估)：什么样的解决方案算是好的
请系统列出各要素，并指出题目中的隐含要求和潜在歧义。
```

### 2.2 三视角头脑风暴（来源：模型视角提示词库 + 100 问仓库 Prompt #3，两处高度一致——社区公认有效）

```text
针对问题【粘贴具体问题】，请分别从【物理机理建模】、【统计学习建模】、【优化决策建模】
三个视角给出建模思路。对每个视角说明：核心变量与假设、适用的数学模型、预期效果、实现难度。
最后用表格对比三个方案的优劣，并推荐最适合的方案。
```

### 2.3 数学建模题目思路 · 结构化长模板（来源：知乎《你所需要的数学建模国赛提示词都在这里》，LangGPT 格式，高收藏）

```text
# Role: 数学建模专家

## Background
用户正在参加数学建模竞赛，需要对题目进行思路分析并建立数学模型。

## Profile
- 精通各类数学建模方法：评价类(AHP/TOPSIS/熵权法)、预测类(灰色预测/ARIMA/机器学习)、
  优化类(线性规划/遗传算法/模拟退火)、微分方程建模等
- 熟悉竞赛论文的评审标准，能给出针对性强、可落地的建模思路

## Goals
对用户给出的赛题，完成：问题分析 → 建模方法选择 → 模型建立 → 求解思路 → 结果检验 → 论文写作框架

## Constrains
- 每一步都要说明理由，不能只给方法名
- 假设必须合理且可辩护
- 方法要与题目数据规模和类型匹配

## Workflow
1. 分析题目背景和所给数据，确定问题的核心和难点
2. 根据问题类型(评价/预测/优化/分类等)，选择 2-3 种合适的建模方法并对比
3. 建立数学模型，明确模型假设和适用范围
4. 给出模型的求解思路和算法步骤
5. 对模型结果的分析与检验方法(误差分析/灵敏度分析)
6. 给出论文写作的思路框架

## Initialization
作为数学建模专家，我会逐步引导你完成建模。请先发送题目原文和附件数据说明。
```

### 2.4 难点与关键变量（来源：100 问仓库 Prompt #4、#9）

```text
# 变量定义
根据题目背景，请列出可能涉及的所有关键变量、参数及其符号表示（推荐希腊字母），并说明其物理意义。

# 难点分析
你认为解决这个问题最大的数学难点在哪里？是数据缺失、非线性求解还是多目标冲突？
请给出应对策略和备选方案。
```

---

## 三、假设与模型规格（开题定型的"最后一公里"）

### 3.1 假设生成（来源：100 问仓库 Prompt #5）

```text
为了简化模型【模型名称】，我们需要提出哪些合理的假设？
请列出至少 5 条，并逐条解释该假设的合理性依据，以及如果该假设不成立模型会怎样。
```

### 3.2 假设合理性红蓝对抗（来源：模型视角提示词库，"假设合理性评估"）

```text
我打算做这些假设：【假设列表】。
请逐条评估：
1. 这条假设是否合理？有什么证据或常识支撑？
2. 对最终结果的影响大不大？
3. 如果评委质疑，如何辩护？
4. 哪些假设需要做敏感性分析？请给出检验方案。
```

### 3.3 三步确定模型选型（来源：模型视角提示词库）

```text
请帮我确定解决【问题】的模型：
Step1 根据问题类型和数据特点，列出 3 个候选模型及其适用条件；
Step2 从准确性、可解释性、实现难度、数据要求四个维度对比打分；
Step3 给出最终推荐及理由，并说明该模型的求解步骤和所需工具库。
```

### 3.4 目标函数与约束的数学化（来源：模型视角提示词库）

```text
请帮我将以下文字描述转化为规范的数学表达：
- 决策变量：【描述】
- 优化目标：【描述】
- 约束条件：【描述】
要求：给出符号定义、目标函数表达式、约束条件表达式，并检查量纲一致性；
如描述中有含糊之处，请先列出你做的解释假设。
```

### 3.5 灵敏度分析与鲁棒性检验（来源：模型视角提示词库 #20，*mathodology 工作流把此项列为获奖硬门槛*）

```text
请为模型中的关键参数【参数列表】设计敏感性分析方案：
1. 每个参数合理的变动范围；
2. 用龙卷风图(Tornado Chart)展示各参数对头条结果的影响排序；
3. 给出 Python 代码，参数在范围内扫描并绘图；
4. 结论：模型对哪些参数鲁棒、对哪些参数敏感，敏感项如何应对。
```

---

## 四、思维扩展工具箱（卡壳 / 想突破时用）

以下 5 条为综合 mathodology 评审要点与获奖论文共性整理的扩展提问，专治"思路定型后想再上一个档次"或"完全没有思路"。

```text
# 1. 类比迁移
列出 5 个其他领域解决过、与本题结构上相似的问题及其经典建模方法，
说明各自的迁移方式和对本题的具体启发。

# 2. 反向推演
假设这篇论文最终拿了国一/O奖，反推摘要里最亮眼的 3 个"头条数字"会是什么？
当前路线能否稳定产出它们？不能的话差在哪里？

# 3. 机制覆盖
题目中点名的每个现象/机制逐一过一遍：被建模了，还是被简化掉了？
被简化的哪些必须在论文局限性中显式说明，否则会被评委抓住？

# 4. 脆弱性测试
指出 3 个"若被质疑会使整个结论崩塌"的关键参数或假设，
并为每个设计一个最低成本的压力测试。

# 5. 领域科普
我不熟悉【领域，如：光伏发电/传染病学】，请在 500 字内为我科普该领域的
核心公式和基础理论，并指出对建模最关键的 2-3 个领域常数从哪里查。
```

---

## 五、数据、求解与代码（高频复用精选）

精选自 GitHub 开源《数学建模 AI 100 问》仓库（MIT 协议，按比赛流程组织，社区反馈最实用的部分）。

```text
# 数据清洗（#11）
我有一份 CSV 数据，包含【列名】，其中存在缺失值和异常值。请写一段 Python (Pandas) 代码，
用插值法填补缺失值并清洗异常值，同时输出清洗前后的对比统计。

# AHP 层次分析法（#21）
我正在构建评价体系，准则层有【因素A, B, C】。请帮我构建判断矩阵的示例，
并写出计算权重和一致性检验的 Python 代码。

# 熵权 TOPSIS（#22）
请给出基于熵权法的 TOPSIS 模型的完整 Python 实现代码，用于对【对象列表】进行排序。

# ARIMA 自动定阶（#32）
针对这个时间序列数据，请写一段 Python 代码，自动寻找 ARIMA 模型的最佳 (p,d,q) 参数。

# 多目标优化 NSGA-II（#48）
目标 A 最大化，目标 B 最小化。请解释帕累托最优概念，并使用 NSGA-II 算法求解，
给出帕累托前沿图代码。

# 遗传算法（#49）
这是一个复杂的非线性优化问题，请实现遗传算法求解函数极值，并说明参数设置依据。

# 微分方程数值解（#62）
这个微分方程无法求出解析解，请使用四阶 Runge-Kutta (RK4) 方法编写 Python 代码求数值解。

# 元胞自动机仿真（#64）
请模拟【如森林火灾蔓延】过程，定义状态转移规则，并写出 Python 仿真代码。

# 代码调试（#91）
我的代码报错了【粘贴错误信息】，请分析原因并给出修正后的代码，并解释错误根源。
```

---

## 六、论文写作与摘要

```text
# 竞赛摘要（100 问 #71 —— 摘要是评委第一眼，权重极高）
这是我的建模思路和结果【粘贴草稿】，请帮我写一段标准的数学建模竞赛摘要(Abstract)，
包含：问题重述、模型建立、求解算法、主要结果数字、结论与建议，约 300 词。
要求：出现具体数字，突出创新点，避免空话套话。

# 英文润色·美赛风格（模型视角 #37 + 100 问 #72）
请将以下段落翻译成学术英语，要求：用词专业、句式多变、符合美赛论文风格；
保留数学符号格式，专业术语使用该领域标准表达。【中文段落】

# 模型优缺点（100 问 #75）
请帮我总结我所用的【模型名称】的 3 个优点和 2 个缺点，语言要客观中肯，
缺点要写"可改进的方向"而不是自我否定。

# 结论与建议（100 问 #78）
请根据我的计算结果【结果】，写一段强有力的结论(Conclusion)，
并提出给决策者的具体建议，建议必须与模型结果数字一一对应。

# 敏感性结果写作（100 问 #82）
请帮我描述敏感性分析的结果图表，说明模型对参数【参数】是否鲁棒，
用"改变 ±X% 时结果仅变化 Y%"的量化句式。
```

---

## 七、答辩与评委视角自检

```text
# 评委提问预测（来源：模型视角提示词库 #39）
现在你是数学建模竞赛评委，刚读完我的论文摘要和方法描述【粘贴】。
请从以下角度预测评委可能提出的 10 个尖锐问题：模型假设合理性、方法选择依据、
结果可信度、创新性、数据局限性。并为每个问题给出建议的回答要点。

# 局限性写作（模型视角 #31）
请帮我撰写模型的局限性部分：哪些结论在什么条件下才成立？
模型没有考虑哪些现实因素？这些局限是否影响主要结论的有效性？
要求：诚实但不自我否定，每条局限对应一个"未来改进方向"。
```

---

## 八、英文互联网精选：针对难题的 Deep Research 提示词

> 以下来自英文社区高声量资源：Reddit r/ChatGPTPro 高赞研究指南、X(Twitter) 病毒式传播模板、[langgptai/awesome-deep-research-prompts](https://github.com/langgptai/awesome-deep-research-prompts) 仓库汇编、[promptingguide.ai 官方 Deep Research 指南](https://www.promptingguide.ai/guides/deep-research)。适用于 ChatGPT/Gemini/Claude 的 Deep Research 模式，也适用于普通对话模式。所有英文提示词均附**中文对照版**：英文版适合让模型直接检索英文语料（Deep Research 场景），中文版适合日常中文对话。

### 8.1 Research Plan：把候选方案变成结构化研究计划（★ 开题定型直接可用）

> 来源：Reddit r/ChatGPTPro《Mastering AI-powered research》高赞帖，awesome-deep-research-prompts 仓库收录。**用法：把 "options" 换成你的 2-3 条候选建模路线，产出的就是一份开题研究计划。**

```text
You are given various potential options or approaches for a project. Convert these into a
well-structured research plan that:

1. Identifies Key Objectives
   - Clarify what questions each option aims to answer
   - Detail the data/info needed for evaluation

2. Describes Research Methods
   - Outline how you'll gather and analyze data
   - Mention tools or methodologies for each approach

3. Provides Evaluation Criteria
   - Metrics, benchmarks, or qualitative factors to compare options
   - Criteria for success or viability

4. Specifies Expected Outcomes
   - Possible findings or results
   - Next steps or actions following the research

Produce a methodical plan focusing on clear, practical steps.
```

**中文对照版（可直接粘贴到中文对话）：**

```text
你面前有某个项目的若干候选方案或技术路线。请把它们转化为一份结构清晰的研究计划，包含：

1. 明确关键目标
   - 说清每条路线分别要回答什么问题
   - 列出评估每条路线所需的数据/信息

2. 描述研究方法
   - 说明将如何收集和分析数据
   - 指明每条路线适用的工具或方法学

3. 给出评估标准
   - 用于对比各路线的指标、基准或定性因素
   - 成功/可行的判定标准

4. 说明预期产出
   - 可能得到的结果或发现
   - 研究完成后的下一步行动

只输出聚焦、清晰、可执行的研究计划。
```

### 8.2 Meta Prompt：让 AI 替你写"深度研究提示词"

> 来源：X @buccocapital。操作：把你的想法全部倒出来发给推理模型（o1/o3/DeepSeek-R1），让它按以下最佳实践替你生成一条定制研究提示词。

```text
Please build a prompt using the following guidelines:

- Define the Objective: clearly state the main research question or task; specify the
  desired outcome (detailed analysis / comparison / recommendations)
- Gather Context and Background: include all relevant background, definitions and data;
  specify boundaries (scope, timeframes, geographic limits)
- Use Specific and Clear Language: precise wording, define key terms, no ambiguity
- Provide Step-by-Step Guidance: break the task into sequential sub-tasks, numbered lists
- Specify the Desired Output Format: report structure, headings, citations, tables
- Balance Detail with Flexibility: guide without over-constraining exploration
- Incorporate Iterative Refinement: test the prompt and refine based on initial outputs
- Apply Proven Techniques: chain-of-thought ("think step by step") for complex tasks
- Set a Role or Perspective: e.g. "act as an operations research analyst"
- Avoid Overloading: one primary objective per prompt
- Request Justification and References: evidence-backed claims only
- Review and Edit Thoroughly before finalizing
```

**中文对照版：**

```text
请按以下准则帮我构建一条"深度研究"提示词：

- 明确目标：说清核心研究问题/任务，以及期望产出（深入分析 / 方案对比 / 行动建议）
- 收集背景：附上所有相关背景、定义和数据；划清边界（范围、时间、地域限制）
- 用词具体清晰：措辞精确，定义关键术语，不留歧义
- 分步指引：把任务拆成顺序化的子任务，用编号列表组织
- 指定输出格式：报告结构、标题层级、引用要求、表格样式
- 细节与弹性平衡：给足指引，但不堵死探索空间
- 内置迭代优化：先试跑这条提示词，根据初次输出修订
- 使用成熟技巧：复杂任务加"请一步步思考"
- 设定角色视角：如"以运筹学分析师的身份"
- 避免过载：一条提示词只放一个核心目标
- 要求论证与引用：结论必须有证据或来源支撑
- 定稿前通读修订：删掉含糊、冗余的指令
```

### 8.3 Elite Research Analyst：结构化拆解式研究简报

> 来源：X @godofprompt。适合对陌生领域快速建立全景认知（数模拿到不熟悉的领域题时先用这条）。

```text
I want you to act as an elite research analyst with deep experience in synthesizing
complex information into clear, concise insights.

Your task is to conduct a comprehensive research breakdown on the following topic:
[Insert your topic here]

Here's how I want you to proceed:
1. Start with a brief, plain-English overview of the topic.
2. Break the topic into 3–5 major sub-topics or components.
3. For each sub-topic, provide: a short definition, key facts/trends/recent developments,
   and any major debates or differing perspectives.
4. Include notable data, statistics, or real-world examples where relevant.
5. Recommend 3–5 high-quality resources for further reading (articles, papers, videos, tools).
6. End with a "Smart Summary" — 5 bullet points as an executive-style briefing.

Act like you're preparing a research memo for someone who needs to grasp this fast —
no fluff, just value.
```

**中文对照版：**

```text
我想让你扮演一位资深研究分析师，擅长把复杂信息综合成清晰扼要的洞见。

你的任务是对以下主题做一次全面的研究拆解：【填入主题】

请按以下步骤进行：
1. 先用平实的语言对主题做一段简短综述；
2. 把主题拆成 3-5 个主要子话题或组成部分；
3. 对每个子话题给出：简短定义；关键事实、趋势或最新进展；主要争论或不同观点；
4. 在相关处给出值得注意的数据、统计或真实案例；
5. 推荐 3-5 个高质量延伸阅读资源（文章、论文、视频或工具）；
6. 以"智慧摘要"收尾——5 条要点式的执行层简报。

要求：结构清晰、便于速读（标题+要点）；假装你在为一位需要在会前快速掌握全局的高管
写研究备忘录——不要废话，只要价值。
```

### 8.4 "英文搜索、中文报告"通用深度研究提示词

> 来源：X @python_xxt。对你最有用的一点：**明确要求 AI 用英文检索英文资料**——英文资料的数量与质量显著优于中文圈，这能直接解决信息源狭窄的问题。

```text
请帮我开展一次深度研究，帮我快速、全面、深刻地理解【XXX】。

通用要求：
- 语言：使用英文搜索，只采纳英文资料，用中文撰写报告
- 长度：尽可能长、细致深入，以全面深刻为基本目标
- 参考：Wikipedia、相关书籍、学术与科普期刊网站、权威媒体
- 可视化：按需在报告中采用图表辅助理解
```

**English 对照版（用于英文优先的 Deep Research 工具）：**

```text
Please conduct an in-depth research to help me quickly, comprehensively and profoundly
understand [XXX].

General requirements:
- Language: search in English only; adopt English sources only; write the report in Chinese
- Length: as long and in-depth as possible; comprehensiveness and depth are the primary goals
- Sources: Wikipedia, relevant books, academic and popular-science journals, authoritative media
- Visualization: use charts and figures where they aid understanding
```

### 8.5 Deep Research 六条使用技巧（promptingguide.ai 官方指南总结）

1. 指令清晰具体、一次到位——深度研究任务又贵又慢，别浪费在含糊提问上；
2. 模型反问澄清时**认真回答**（clarify, don't ignore），回答质量直接决定研究质量；
3. 多给**关键词和精确术语**（技术名词、专有名词），搜索是靠关键词驱动的；
4. 用明确动词：compare / suggest / recommend / report——模型被训练为服从这些指令；
5. 指定输出格式（章节结构、表格、列数），否则它会默认给通用报告体；
6. 上传 PDF 作上下文（尤其冷门技术领域），并且**永远自查来源**。

学术场景高价值用法（官方建议）：文献综述、识别研究缺口 → 转化成新的研究问题、来源核验。

---

## 九、英文开源 Skill / Agent：深度研究 × 数学建模

| 项目 | 是什么 | 呼声 / 背书 |
|---|---|---|
| [gpt-researcher](https://github.com/assafelovic/gpt-researcher) | 最早最流行的开源自主研究 Agent，生成带引用的长报告 | ~29k stars |
| [STORM / Co-STORM](https://github.com/stanford-oval/storm) | Stanford 知识策展系统：**先多视角模拟专家对话，再写**维基级长文 | Stanford OVAL，论文 + 高星开源 |
| [deer-flow](https://github.com/bytedance/deer-flow) | 字节开源 Deep Research 框架（LangGraph 多 Agent），可出报告/PPT/播客 | 大厂开源 |
| [dzhng/deep-research](https://github.com/dzhng/deep-research) | 轻量迭代式深度研究脚本（搜索→评估→追问→报告），可自托管 | GitHub 高星 |
| [last30days-skill](https://github.com/mvanhorn/last30days-skill) | Agent Skill：跨 Reddit/X/YouTube/HN 做近 30 天主题综述 | Claude/Codex skill 形态 |
| [OptiMUS](https://github.com/teshnizi/OptiMUS) | 从自然语言描述建 MILP 模型→验证→写求解代码→生成测试→检查解有效性 | ICML 2024，在线 demo：optimus-solver.com |
| [ORLM](https://github.com/Cardinal-Operations/ORLM) | 运筹优化建模专用开源 LLM（OR-Instruct 数据合成法） | NeurIPS 2024 + INFORMS《Operations Research》期刊 |
| [Anthropic 多智能体研究系统](https://www.anthropic.com/engineering/built-multi-agent-research-system) | Claude Research 背后的系统，官方工程复盘 + Cookbook 开源提示词 | Anthropic 官方 |

### 9.1 从这些项目提炼的三个高价值提示词模式

**模式一：STORM 式多视角圆桌会（写模型之前先"会诊"）**

方法论（中文详解）：STORM 是 Stanford OVAL 实验室的知识策展系统（NAACL 2024 论文），专门从零生成维基百科级长文。它的核心发现是**"好问题先于好写作"**：研究者观察真人维基编辑的工作方式后发现，文章质量取决于写作之前的调研深度，而不是写作本身。因此 STORM 在"动笔"前加了一个前置阶段——让 LLM 扮演持不同视角的提问者（历史学家和经济学家的问法完全不同），与"话题专家"模拟多轮对话，再用对话中产生的问题与答案构建大纲和素材，形成"多视角提问 → 检索回答 → 生成大纲 → 成文"的四段式流程。

对数模的启示：开题最大的风险不是"算不出来"，而是"问错了问题"——只从一个视角拆题，会漏掉题目真正想考核的机制。圆桌会提示词强制模型在给方案之前，先把"该问的问题"问完。使用要点：① 视角之间要存在真实的立场差异（领域专家关心现实约束，评委关心可辩护性）；② 限定轮次（每人 2 问）防止无限寒暄；③ 必须要求输出"分歧清单"——分歧点往往就是题目难点所在。

```text
我要解决的难题是：【题目/子问题】。
在给出任何建模方案之前，请先模拟一场多视角专家圆桌会：
① 领域背景专家（该行业实际约束与常识）
② 统计学家 ③ 运筹优化专家 ④ 数据工程师 ⑤ 挑剔的竞赛评委
每位专家轮流就"这个问题的正确打开方式"提出 2 个尖锐问题并回应他人，
焦点：数据能否支撑建模、目标函数怎么定、哪些现实机制不能丢。
会诊结束后输出三份清单：共识清单、分歧清单、由讨论激发出的 3 条新建模路线。
```

**模式二：OptiMUS 式"验证-测试-检查"三件套（优化类题目专用）**

方法论（中文详解）：OptiMUS 是 Stanford Udell 实验室的 LLM 优化建模 agent（ICML 2024，在线 demo：optimus-solver.com），任务是把自然语言描述自动变成 MILP 模型并求解。它在 NLP4LP 基准上总结出的核心教训是：LLM 建模的错误分三类——**建模错误**（误解文字意图，目标函数/约束写错）、**代码错误**（模型对但实现错）、**解的错误**（求解结果没检查就当结论用）。三类错误常常叠加出现，单靠"再检查一遍"防不住，必须分道设防：

- 验证（Verification）：把文字意图与数学表达**逐条对照**——防建模错误；
- 测试（Testing）：构造能**手工算出最优解**的小算例去跑代码——这是软件工程"单元测试"思想在建模上的移植——防代码错误；
- 有效性检查（Validity）：拿到解后检查约束满足性与常识合理性（产量不能为负、流量不能超容量）——防"垃圾进、垃圾出"被当成结论。

对数模的启示：选址、调度、资源分配这类优化题最容易死在"模型自洽但与题意脱节"上；三件套每步只需 10-30 分钟，是性价比最高的防翻车手段。

```text
针对我刚建立的优化模型：【模型描述 + 代码】。请按以下三步走完：
① 验证(Verification)：逐行检查数学表达是否符合我的文字意图，列出所有误解点；
② 测试(Testing)：为模型写 3 个小规模算例，其中一个的最优解能被手工算出，用于验证代码正确性；
③ 有效性检查(Validity)：求解后检查解是否满足全部约束、是否违反常识（如负产量、超容量）；
若结果异常，回溯判断是建模错误还是求解错误。
```

**模式三：Anthropic 式 LLM-as-Judge 五维自检**

方法论（中文详解）：Anthropic 在构建 Claude Research 时遇到一个评估难题——开放式研究产出没有唯一正确答案，程序化检查无从下手。他们的解法是 **LLM-as-judge**：另派一个独立的 LLM 按评分细则（rubric）给产出打分。三条实验结论值得照抄：

1. **单次调用 + 单一提示词 + 0-1 连续分 + pass/fail** 的组合，比多个 judge 投票更稳定、更贴近人类判断——不是 judge 越多越好；
2. **judge 必须与产出者无关**（独立上下文、不共享历史），否则会给自己人放水；且每个分数都要"列出证据"，防止凭感觉打分；
3. **评最终状态，不评中间步骤**（end-state evaluation）：agent 可能走不同路径到达同一结果，只看结果状态是否达标，比检查"过程是否标准"更可靠。

迁移到数模的做法：五维 rubric 从"事实/引用/完整性/来源质量/工具效率"换成"数学正确性/引用准确性/覆盖完整性/来源质量/可复现性"；用法是**开一个全新对话**（无历史上下文）让它当 judge，用自己的方案去评。

```text
请作为与本次建模完全无关的独立评审，按五个维度给我的方案/论文打分(0-1)并为每个分数列出证据：
① 数学正确性（推导、公式、量纲一致性）
② 引用与事实准确性（每个数字和结论是否可溯源）
③ 覆盖完整性（题目的每一条要求是否都有对应交付）
④ 来源质量（一手数据/权威文献，还是二手博客）
⑤ 计算可复现性（固定随机种子了吗？别人能重跑出这些数字吗？）
任一维度低于 0.7，给出具体、可执行的修复建议。
```

### 9.2 Anthropic 官方工程复盘的五条提示词原则（给 Agent/长任务用）

Anthropic 用这些原则造出了 Claude Research，全部可平移到数模 Agent 工作流：

1. **分解难题**：把难问题拆成小任务，而不是一次性甩给模型。为什么：agent 在长任务里错误会复合，单步超载是最主要的失败源；拆小之后每一步都可验证、可重跑。
2. **来源质量启发式**：警惕 SEO 内容农场，优先一手来源和学术 PDF。为什么：他们发现 agent 会系统性偏向高排名的内容农场、错过低排名但权威的学术资料，把"优先一手来源"明确写进提示词才修掉这个偏差。
3. **明确 depth vs breadth**：告诉模型何时深挖一个主题、何时并行铺开多个方向。为什么：研究方向是动态展开的，不给"收/放"的判断标准，模型要么浅尝辄止、要么无限漫游。
4. **给"努力程度"定预算**：简单问题不许滥开子任务，复杂问题才允许更多分派。为什么：他们见过一个简单查询被拆成 50 个子代理的失控案例——token 烧完结果还没对，把预算写进提示词就能拉回。
5. **产物落盘**：让子任务把结果写进文件、只回传轻量引用。为什么：层层转述会失真（"传话游戏"效应），文件系统是天然的事实源；引用比复制更省上下文且保真。

---

## 十、进阶：直接安装的获奖级工作流（Skill / Agent）

如果希望整套方法论自动化执行，这三个开源项目呼声和可信度最高：

| 项目 | 一句话介绍 | 适用 |
|---|---|---|
| [mathodology](https://github.com/sweetcornna/mathodology) | 专为数模竞赛设计的 Agent Skills：9 阶段获奖工作流 + 三席盲评判审团，覆盖国赛/美赛/研赛/华数杯等十余种赛制 | Claude Code / Codex 用户 |
| [MathModelAgent](https://github.com/jihe520/MathModelAgent) | 全自动多智能体：题目分析→建模→代码执行→出图→完整论文 | 想一键跑通全流程 |
| [LLM-MM-Agent](https://github.com/usail-hkust/LLM-MM-Agent) | NeurIPS 2025 学术成果，内置 98 个建模方法的层级方法库(HMML)；2025 年真实辅助两支队伍获美赛 Finalist(前 2%) | 学术级方法检索与对照 |

mathodology 一键安装（在比赛项目根目录执行）：

```bash
npx -y skills@latest add sweetcornna/mathodology --global --copy --yes --skill '*' --agent codex claude-code
```

---


---

# 第二部分 · 资源库索引

## R1、全流程 Agent 工作流与 Skills

数模专用（可直接装进 Claude Code / Codex）：

| 资源 | 一句话定位 | 背书 / 热度 |
|---|---|---|
| ★ [sweetcornna/mathodology](https://github.com/sweetcornna/mathodology) | 9 阶段获奖级工作流 + 三席盲评判审团，覆盖国赛/美赛/研赛/华数杯/HiMCM 等 12 类赛制，内置文献检索 skill | MIT 开源，方法论最完整 |
| ★ [jihe520/MathModelAgent](https://github.com/jihe520/MathModelAgent) | 全自动多智能体：题目分析→建模→代码执行→出图→完整论文 | 高星，有在线版 mathmodel.top |
| ★ [usail-hkust/LLM-MM-Agent](https://github.com/usail-hkust/LLM-MM-Agent) | 学术级建模 agent，HMML 三层方法库（98 个建模 schema） | NeurIPS 2025；2025 美赛两支队伍 Finalist（前 2%） |
| [caojian1134/mathmodel-agent-resources](https://github.com/caojian1134/mathmodel-agent-resources) | **32 个数模 AI 项目**的分类导航库，含选型对比指南，全部下载验证过 | 2026-09-06 全量校验 |
| [HandsomeZR/mathmodel-skill](https://github.com/HandsomeZR/mathmodel-skill) | 完整竞赛工作流 skill（checkpoint 齐全） | 收录于上述导航库 |
| [Hjdd14/math-modeling](https://github.com/Hjdd14/math-modeling) | 数模全流程工作流 starter kit | 收录于导航库 |
| [xuec699/math-modeling-skills](https://github.com/xuec699/math-modeling-skills) | 多 skill 拆分的数模工作流 | 收录于导航库 |
| [chengziyue1222/math-model-agent](https://github.com/chengziyue1222/math-model-agent) | 多角色协作型数模 agent | 收录于导航库 |
| [zhnnky329/MathModeling-skills](https://github.com/zhnnky329/MathModeling-skills) | 多 skill 工具包（建模/写作/图表分工） | 收录于导航库 |
| [MCM-AI-Starter-Kit](https://github.com/caojian1134/mathmodel-agent-resources) | 美赛起步套件（模板+工作流） | 收录于导航库 |

通用 Skill 生态（想自己搭工具箱时用）：

| 资源 | 一句话定位 | 背书 / 热度 |
|---|---|---|
| ★ [anthropics/skills](https://github.com/anthropics/skills) | Anthropic 官方 Agent Skills 仓库 | 官方 |
| [VoltAgent/awesome-agent-skills](https://github.com/VoltAgent/awesome-agent-skills) | 1000+ 社区 skills 精选清单，兼容 Claude Code/Codex/Gemini CLI | 社区最大合集 |
| [mcpservers.org/agent-skills](https://mcpservers.org/agent-skills) | skills 市场页，ZIP 一键安装 | 第三方市场 |

---

## R2、提示词库合集

> 提示词**正文精选**在配套文档第一部分（提示词精选）里，这里放原始出处。

| 资源 | 一句话定位 | 背书 / 热度 |
|---|---|---|
| ★ [模型视角提示词库](https://www.modelinsight.chat/prompts) | 52 条场景化数模提示词（FRAME 拆题/选型/灵敏度/答辩） | 配套出版书《巧用DeepSeek进行数学建模》 |
| ★ [数学建模 AI 100 问](https://github.com/yugwl/-MCM-ICM-CUMCM-100-AI-Prompts-) | 100 条按比赛流程组织的提示词（[正文](https://github.com/yugwl/-MCM-ICM-CUMCM-100-AI-Prompts-/blob/main/prompts.md)） | MIT 开源 |
| ★ [awesome-deep-research-prompts](https://github.com/langgptai/awesome-deep-research-prompts) | Deep Research 提示词汇编（Research Plan/Meta Prompt/领域调研） | 汇集 Reddit/X 高声量模板 |
| [知乎：国赛提示词合集](https://zhuanlan.zhihu.com/p/717717112) | LangGPT 结构化模板 5 条（建模思路/论文优化等） | 知乎高收藏 |
| [知乎：美赛 AI 提示词通用模板](https://zhuanlan.zhihu.com/p/1997036450554856550) | 赛题信息卡 + A-F 六题适配方案 | 数模机构"数学建模BOOM" |
| [DavidZWZ/Awesome-Deep-Research](https://github.com/DavidZWZ/Awesome-Deep-Research) | Agentic Deep Research 论文/方法全景导航 | 学术向 |
| [ai-boost/awesome-prompts](https://github.com/ai-boost/awesome-prompts) | ChatGPT 提示词聚合 + 各产品泄露系统提示词索引 | 社区合集 |
| [ChatGPT Deep Research 系统提示词](https://xuanwo.io/links/2025/02/chatgpt-deep-research-system-prompt/) | OpenAI Deep Research 的真实系统提示词（学其结构） | 提取自官方产品 |

---

## R3、学术论文与基准（LLM × 数学建模）

| 资源 | 一句话定位 | 背书 |
|---|---|---|
| ★ [MM-Agent](https://arxiv.org/abs/2505.14148) | 模拟人类专家解题流程的建模 agent（[代码](https://github.com/usail-hkust/LLM-MM-Agent)） | NeurIPS 2025 |
| ★ [OptiMUS](https://arxiv.org/abs/2310.06116) | 自然语言→MILP 建模+验证+求解 agent，三版迭代（[代码](https://github.com/teshnizi/OptiMUS)、[在线 demo](https://optimus-solver.com/)） | ICML 2024（Stanford Udell Lab） |
| ★ [ORLM](https://arxiv.org/abs/2405.17743) | 运筹优化建模专用开源 LLM 训练框架（OR-Instruct 数据合成）（[代码](https://github.com/Cardinal-Operations/ORLM)） | NeurIPS 2024 + INFORMS《Operations Research》 |
| [OptiBench / ReSocratic](https://arxiv.org/abs/2407.09887) | 优化建模基准（含非线性难题）+ 数据合成法（[代码](https://github.com/yangzhch6/ReSocratic)） | arXiv, 被多个后续工作引用 |
| [AgenticDataBench](https://arxiv.org/abs/2607.01647) | LLM 数据科学 agent 的综合基准（[代码](https://github.com/AgenticDataBench/AgenticDataBench)） | arXiv |
| [LLM4OR 综述](https://llm4or.github.io/LLM4OR) | LLM×运筹建模领域系统综述 | 领域 survey |

---

## R4、深度研究困难问题专题

> 专门回答"怎么让 AI 对一个难题做深度研究"：**怎么问（方法论）→ 用什么跑（产品/框架）→ 前沿在做什么（论文）**。可直接复制的提示词在第一部分（提示词精选）§八，三个方法论模式的中文详解在 §九。

### 4.1 提问方法论与实战技巧

| 资源 | 一句话定位 |
|---|---|
| ★ [Prompting Guide：Deep Research 指南](https://www.promptingguide.ai/guides/deep-research) | 实测提问法：给计划、答澄清、给关键词、明确动词（compare/recommend）、定输出格式、传 PDF 上下文、永远自查来源 |
| ★ [awesome-deep-research-prompts](https://github.com/langgptai/awesome-deep-research-prompts) | Reddit/X 高声量研究提示词汇编（Research Plan / Meta Prompt / 领域调研），有中文注释 |
| [ChatGPT Deep Research 系统提示词](https://xuanwo.io/links/2025/02/chatgpt-deep-research-system-prompt/) | OpenAI 生产系统的真实提示词——学它怎么做任务分解与引用管理 |
| [Anthropic：Building Effective Agents](https://www.anthropic.com/engineering/building-effective-agents) | 五种 agent 工作流模式（提示链/路由/并行/编排者-工人/评估者-优化者），核心建议：先找最简方案 |
| [Claude Cookbook](https://platform.claude.com/cookbook/) | 官方可复用提示词与配方（[GitHub 仓库](https://github.com/anthropics/claude-cookbooks)） |

### 4.2 商业产品

| 产品 | 定位 |
|---|---|
| [ChatGPT Deep Research](https://openai.com/index/introducing-deep-research/) | o3 驱动多步网络研究，生态最成熟 |
| [Claude Research](https://www.anthropic.com/engineering/built-multi-agent-research-system) | 多智能体编排（lead + 并行 subagents），官方工程复盘公开 |
| Gemini Deep Research | Google 生态整合，擅长长报告 |
| [Perplexity Deep Research](https://www.perplexity.ai/) | 快速多层检索，免费额度多 |

### 4.3 开源框架（可自托管）

| 资源 | 一句话定位 | 背书 / 热度 |
|---|---|---|
| ★ [gpt-researcher](https://github.com/assafelovic/gpt-researcher) | 最早最流行的自主研究 agent，生成带引用长报告 | ~29k stars |
| ★ [STORM / Co-STORM](https://github.com/stanford-oval/storm) | Stanford 知识策展系统：先多视角专家对话再写长文（"好问题先于好写作"） | Stanford OVAL |
| [deer-flow](https://github.com/bytedance/deer-flow) | 字节开源 Deep Research 框架（LangGraph），可出报告/PPT/播客 | 大厂开源 |
| [dzhng/deep-research](https://github.com/dzhng/deep-research) | 轻量迭代式研究脚本（搜索→评估→追问→报告），可自托管 | GitHub 高星 |
| [OpenScience](https://github.com/synthetic-sciences/openscience) | 开源 AI 科研工作台：读文献、跑实验、写报告 | 开源 |
| [last30days-skill](https://github.com/mvanhorn/last30days-skill) | Agent Skill：跨 Reddit/X/YouTube/HN 的近 30 天主题综述 | Claude skill 形态 |
| [deepseek-harness](https://github.com/deepseek-ai/deepseek-harness) | DeepSeek 官方 agent 框架，配合联网插件跑研究计划 | 官方 |
| [topic: deep-research-agent](https://github.com/topics/deep-research-agent) | GitHub 该主题下 ~83 个仓库的聚合页 | 索引页 |

### 4.4 学术论文与基准

| 资源 | 一句话定位 | 背书 |
|---|---|---|
| ★ [The AI Scientist](https://arxiv.org/abs/2408.06292) | 全自动科研闭环：提出想法→做实验→写论文→自动评审（[代码](https://github.com/SakanaAI/AI-Scientist)） | Sakana AI；引用 1300+；**Nature 专题报道** |
| ★ [PaperQA2](https://arxiv.org/abs/2409.13740) | 科学文献 RAG agent，在文献综合与矛盾检测上达到**超人类**水平（[代码](https://github.com/Future-House/paper-qa)） | FutureHouse |
| [Agent Laboratory](https://arxiv.org/abs/2501.04227) | 人机协作"科研副驾驶"：文献综述→实验→报告三阶段（[项目页](https://agentlaboratory.github.io/)），成本比全自动方案低一个量级 | AMD + Johns Hopkins |
| [DeepResearcher](https://arxiv.org/abs/2504.03160) | 首个在**真实网络环境**中端到端强化学习训练的深度研究 agent（[代码](https://github.com/GAIR-NLP/DeepResearcher)） | EMNLP 2025 主会 |
| [RL 深度研究系统综述](https://github.com/wenjunli-0/deepresearch-survey) | 用强化学习训练深度研究系统的领域综述 + 论文清单 | GitHub survey |
| [BrowseComp](https://openai.com/index/browsecomp/) | "难找信息检索"基准——衡量研究 agent 能否找到冷门信息 | OpenAI 官方基准 |
| ★ [DeepResearch Bench](https://arxiv.org/abs/2506.11763) | **100 道博士级研究任务**（覆盖 22 个领域），从两个维度评测深度研究 agent：报告质量（参考基准+自适应评分）与检索能力（有效引用数+引用准确率）（[代码](https://github.com/Ayanami0730/deep_research_bench)） | 开源基准；与人类判断高度对齐 |
| [DavidZWZ/Awesome-Deep-Research](https://github.com/DavidZWZ/Awesome-Deep-Research) | Agentic Deep Research 论文/方法全景导航 | 社区 |

### 4.5 方法论一页速览

- **分解再研究**（Anthropic）：难题先拆成可并行、可验证的子问题，一条提示词只放一个目标；
- **先问题后答案**（STORM）：给方案之前，先让多个视角互相提问，输出共识清单和分歧清单；
- **三道防线**（OptiMUS）：验证文字意图 → 小算例测试 → 检查解的常识性，三类错误分道设防；
- **独立评审**（LLM-as-Judge）：0-1 打分、每分给证据、judge 与产出者无共享上下文；
- **来源质量与努力预算**：一手来源优先；简单问题不滥开子任务；产物写文件防层层转述失真。
- （以上每个模式的可直接复制提示词：第一部分（提示词精选）§8.1-8.5 与 §9.1）

---

## R5、AI 文献检索与核验工具

> 分工建议（来自多篇 2026 对比评测）：快问快答用 Consensus，系统综述+数据抽取用 Elicit，查"支持还是反驳"用 Scite，免费发现层用 Semantic Scholar + Research Rabbit。

| 工具 | 一句话定位 | 费用 |
|---|---|---|
| ★ [Semantic Scholar](https://www.semanticscholar.org/) | 2 亿+论文的免费语义检索，API 开放 | 免费 |
| ★ [Consensus](https://consensus.app/) | 基于 ~2 亿同行评审文献回答"是/否"型问题，带共识计量 | 免费额度 |
| [Elicit](https://elicit.com/) | 结构化文献综述 + 论文数据抽取表 | 免费额度 |
| [Scite](https://scite.ai/) | 显示某论文被"支持/反驳"的引用分布，查结论是否翻车 | 付费 |
| [Research Rabbit](https://www.researchrabbit.ai/) | 论文关系图谱，顺藤摸瓜找相关工作 | 免费 |
| [Connected Papers](https://www.connectedpapers.com/) | 输入一篇论文，可视化它的学术谱系 | 免费额度 |
| [free-search-mcp](https://github.com/sweetcornna/free-search-mcp) | 免 key 多引擎检索 + PDF 阅读 + paper_graph 引用/撤稿核查（**本机已装**） | 开源免费 |

---

## R6、数据来源

| 来源 | 覆盖 | 链接 |
|---|---|---|
| ★ 国家统计局 | 中国宏观/行业/人口全量统计数据 | https://data.stats.gov.cn/ |
| ★ 世界银行公开数据 | 各国宏观指标，可按国家/指标下载 | https://data.worldbank.org/ |
| [data.gov](https://data.gov/) | 美国政府开放数据（环境/交通/健康） | 美国官方 |
| [Kaggle Datasets](https://www.kaggle.com/datasets) | 社区数据集 + 竞赛数据 | 免费 |
| [UCI Machine Learning Repository](https://archive.ics.uci.edu/) | 经典 ML 数据集（分类/回归练手） | 免费 |
| [和鲸社区 Heywhale](https://www.heywhale.com/) | 中文数据科学社区，带中文数据集 | 免费 |
| [Awesome Public Datasets](https://github.com/awesomedata/awesome-public-datasets) | GitHub 上最全的公开数据集索引 | 社区维护 |
| [知乎：30 个数模数据库网站](https://zhuanlan.zhihu.com/p/1946956091494737052) | 政府数据/行业数据/统计网站的中文导航合集 | 知乎整理 |
| [知乎：数模数据网站](https://zhuanlan.zhihu.com/p/348581297) | 推荐从世界银行+国家统计局入手的路径 | 知乎整理 |

---

## R7、LaTeX 模板与优秀论文范例

模板（国赛）：

| 模板 | 一句话定位 |
|---|---|
| ★ [latexstudio/CUMCMThesis](https://github.com/latexstudio/CUMCMThesis) | 国赛 LaTeX 模板事实标准，已适配 2026 格式 |
| [jayxin/cumcm](https://github.com/jayxin/cumcm) | 基于 CUMCMThesis 重构，结构更清晰 |
| [Sustainable-Enjoyment/CUMCM-LaTeX-Template](https://github.com/Sustainable-Enjoyment/CUMCM-LaTeX-Template) | 现代化、高度自定义的 CUMCM/MCM 模板 |
| [yifengchen07/cumcm-latex-template](https://github.com/yifengchen07/cumcm-latex-template) | 按 **2026 官方格式规范 + AI 使用规定**设计 |

模板（美赛）：[MCM-Template](https://github.com/caojian1134/mathmodel-agent-resources)、[icmmcm](https://github.com/caojian1134/mathmodel-agent-resources)（收录于 32 项目导航库）。

优秀论文范例（公开 O 奖/国一，mathodology 工作流引用的校准样本）：

| 范例 | 说明 |
|---|---|
| [2024 MCM F 题 O 奖论文](https://reformship.github.io/pages/3competition/4mcm/MCM%20Outstanding/2024/F/2413565.pdf) | 完整 O 奖 PDF，学结构与图表密度 |
| [O 奖论文范例 2](https://explcre.github.io/files/mcm.pdf) | 公开优秀论文 |
| [ydchen0806/24ICM_E_O_Award_Paper_code](https://github.com/ydchen0806/24ICM_E_O_Award_Paper_code) | 2024 ICM E 题 Outstanding/INFORMS 奖论文+全部源码+图表 |
| [GuangLun2000/COMAP-MCM-2026](https://github.com/GuangLun2000/COMAP-MCM-2026) | 美赛论文 PDF、MATLAB/Python 代码、绘图模板、写作笔记合集 |

---

## R8、算法代码库与真题档案

| 资源 | 一句话定位 |
|---|---|
| ★ [personqianduixue/Math_Model](https://github.com/personqianduixue/Math_Model) | "最全数模资料库"：书籍/MATLAB 算法/国赛评阅要点/LaTeX 模板 |
| ★ [HuangCongQing/Algorithms_MathModels](https://github.com/HuangCongQing/Algorithms_MathModels) | 国赛美赛常用算法 MATLAB 实现合集 |
| [MathematicalModelingAlgorithm](https://github.com/caojian1134/mathmodel-agent-resources) | 数模常用算法代码集（收录于导航库） |
| [fanjufei/CUMCM](https://github.com/caojian1134/mathmodel-agent-resources) | CUMCM 算法示例（收录于导航库） |
| ★ [CosmicLinks/cumcm-problems](https://github.com/CosmicLinks/cumcm-problems) | 历年国赛真题 + 附件归档 |
| [CQULeaf/MCM-ICM_Study_Resources](https://github.com/CQULeaf/MCM-ICM_Study_Resources) | 美赛备赛：模型建立/代码实现/论文写作资料 |

---

## R9、学习路径与教程

| 资源 | 一句话定位 | 备注 |
|---|---|---|
| ★ [知乎：数模保姆级入门教程](https://zhuanlan.zhihu.com/p/356780549) | 八千字零基础入门 + B 站/公众号资源整合 | 快速入门首选 |
| ★ [知乎：我是如何学习数学建模的](https://zhuanlan.zhihu.com/p/403832962) | 真实学习经验，含清风课程优缺点评价 | 避坑向 |
| [知乎：学习路线规划问答](https://www.zhihu.com/question/609495832) | B 站清华 83 讲、姜启源教材等书目清单 | 书单参考 |
| [B站：从小白到国一/O奖系统课](https://www.bilibili.com/video/BV1shvzBMEjW) | 181 讲系统课程，20+ 国一/O 奖作者授课 | 免费系统课 |
| 姜启源《数学模型》（第 4/5 版） | 数模教材事实标准，赛题方法的原典 | 配合清华 83 讲食用 |
| [数模加油站（B站/公众号）](https://www.bilibili.com/video/BV1QE4m1R7L3/) | 国赛/美赛一站式备赛资源 | 实时更新 |

---

## R10、比赛规则与 AI 合规

| 资源 | 关键点 |
|---|---|
| ★ [COMAP MCM/ICM 官方规则](https://www.contest.comap.com/undergraduate/contests/mcm/instructions.php) | AI 使用允许但须披露：**AI Use Report 附在 PDF 末尾，不计入 25 页限制**；须注明用了什么模型、做什么用，并对 AI 内容的准确性负全责；未披露视为违规 |
| [COMAP 2026 赛前说明会资料](https://comap.org/images/blog/MCM-ICM_InfoSession_1-2026.pdf) | 官方逐条讲解 AI Use Report 等提交要求 |
| [国赛官网（中国大学生数模竞赛）](https://www.mcm.edu.cn/) | 论文与支撑材料分开提交；全国奖评审有相似度查验；注意当年 AI 使用规定 |
| [HiMCM 官方规则](https://himcm.org.cn/instructions/) | 高中美赛：英文 PDF、匿名、AI 使用需正文+报告双重披露 |
| [M3 Challenge 规则](https://m3challenge.siam.org/the-challenge/rules-and-guidelines/) | 14 小时冲刺、单 PDF、summary 首页 |
| [IMMC 规则](https://www.immchallenge.org/Pages/Rules.html) | 5 天窗口、不收软件包、需模型测试/敏感性/误差分析 |

---

## R11、按场景速查表

| 你现在要做什么 | 首选 | 备选 |
|---|---|---|
| 拿到题目，开题定型 | 提示词文档 §一 主工作流 | mathodology（Phase 0-2）/ MM-Agent |
| 三条路线对比取舍 | Research Plan 提示词（§8.1） | FRAME 拆题（§2.1） |
| 优化/规划类题目 | OptiMUS 在线 demo + "三件套"提示词 | ORLM / ReSocratic 基准 |
| 缺数据找数据 | 国家统计局 / 世界银行 / Kaggle | Awesome Public Datasets / 和鲸 |
| 对陌生领域/难题做深度调研 | Deep Research 产品 + R4 专题 + 第一部分 §八 | gpt-researcher / STORM / AI Scientist |
| 查文献、核引用 | Semantic Scholar + Consensus | Elicit / Scite / Connected Papers / free-search-mcp |
| 论文排版 | CUMCMThesis（2026 适配） | jayxin/cumcm / MCM-Template |
| 论文写完自查 | LLM-as-Judge 五维提示词（§9.1） | mathodology 盲评判审 / 本机 math-modeling-review skill |
| 图表不够专业 | 本机 modelviz-skill | mathodology 图表规范 |
| 系统学习补课 | 知乎保姆级教程 + 清风课 | B站系统课 / 姜启源《数学模型》 |
| 赛前查规则 | COMAP 官方规则页 | 国赛官网 / 对应赛事规则页 |

---

> **维护说明**：本索引中"收录于导航库"的条目，其具体仓库地址、版本快照与许可证信息请到 [mathmodel-agent-resources](https://github.com/caojian1134/mathmodel-agent-resources) 的 CATALOG.md 查询。资源失效时优先从该目录与各 awesome 列表找替代。


---

# 附录 · 完整来源索引


| 来源 | 链接 | 可信度依据 |
|---|---|---|
| 模型视角提示词库（52 条场景化） | https://www.modelinsight.chat/prompts | 配套出版书籍《巧用DeepSeek进行数学建模》 |
| 数学建模 AI 100 问（GitHub） | https://github.com/yugwl/-MCM-ICM-CUMCM-100-AI-Prompts- | MIT 开源，按比赛流程组织 |
| 知乎：数学建模国赛提示词合集 | https://zhuanlan.zhihu.com/p/717717112 | 知乎高收藏实战文 |
| 知乎：美赛 AI 提示词通用模板（北海） | https://zhuanlan.zhihu.com/p/1997036450554856550 | 数模机构"数学建模BOOM"实战模板 |
| mathodology 获奖级工作流 | https://github.com/sweetcornna/mathodology | 9-phase + 盲评判审，免费检索文献/数据 |
| MathModelAgent | https://github.com/jihe520/MathModelAgent | 高星开源全自动建模 Agent |
| MM-Agent (NeurIPS 2025) | https://github.com/usail-hkust/LLM-MM-Agent | 论文 arXiv:2505.14148，美赛 Finalist 实证 |
| 32 个数模 AI 项目导航 | https://github.com/caojian1134/mathmodel-agent-resources | 2026-09 全量下载验证的项目目录 |
| langgptai/awesome-deep-research-prompts | https://github.com/langgptai/awesome-deep-research-prompts | Reddit/X 高声量深度研究提示词汇编 |
| OpenAI Deep Research 指南 | https://www.promptingguide.ai/guides/deep-research | Prompt Engineering Guide 官方深度研究指南 |
| Anthropic 多智能体研究系统 | https://www.anthropic.com/engineering/built-multi-agent-research-system | Claude Research 官方工程复盘 |
| OptiMUS | https://github.com/teshnizi/OptiMUS | ICML 2024（Stanford Udell Lab） |
| ORLM | https://github.com/Cardinal-Operations/ORLM | NeurIPS 2024 / INFORMS《Operations Research》 |
| STORM | https://github.com/stanford-oval/storm | Stanford OVAL 开源知识策展系统 |
| gpt-researcher | https://github.com/assafelovic/gpt-researcher | ~29k stars，最流行开源深度研究 Agent |
| Reddit：Mastering AI-powered research | https://www.reddit.com/r/ChatGPTPro/comments/1in87ic/ | r/ChatGPTPro 高赞研究方法帖 |

> **最后提醒**：AI 是副驾驶不是司机。所有关键公式、文献、数字必须交叉验证；比赛中按规则披露 AI 使用情况；理解你提交的每一个模型，答辩时才立得住。