---
title: "皮层下脑区终于能像皮层一样稳定画图了"
summary: "一个把 subcortex_visualization 包装成可复现 Codex workflow 的小工具：从 ROI 表、MNI 图像到 SVG/PDF 图，一路检查 atlas、标签和输出 provenance。"
description: "适合做丘脑、脑干、小脑、皮层下 ROI 可视化的 Python/R 双路线 skill。"
author: "A Man's Brainhole"
sourceUrl: "https://github.com/mqqq333/subcortex-visualization-skill"
coverImage: "assets/gallery/all_atlas_showcase.png"
---

# 皮层下脑区终于能像皮层一样稳定画图了

做脑科学图的时候，皮层往往比较“幸福”：有熟悉的 2D atlas schematic，有 ggseg，有各种现成模板。

但一到皮层下、丘脑、脑干、小脑，事情就容易变成另一种画风：有人截 Workbench，有人截 slice，有人手动拼图，有人用不同 palette，最后同一篇文章里的 cortex 和 subcortex 看起来像来自两个项目。

我最近把这个问题整理成了一个 Codex Skill：**subcortex-visualization skill**。

它不是重新发明一个绘图库，而是把 Annie Bryant 的 `subcortex_visualization` toolbox 包成一个更适合日常研究使用的 workflow：从 ROI 表、MNI-space NIfTI 图，到可编辑 SVG/PDF 输出，中间每一步都尽量可检查、可复现、可写进 Methods。

## 它解决的不是“画一张脑图”，而是“稳定地画一类脑图”

很多时候，我们真正缺的不是一个单次脚本，而是一条稳定路线：

1. 我现在要画哪个 atlas？
2. 我的 ROI 名字和 atlas region 能不能对上？
3. 这次是 Python pipeline 还是 R pipeline？
4. 输出要 PNG 预览，还是 SVG/PDF 进论文？
5. 如果别人要复现，我能不能说清楚用的是哪个 atlas、哪个 value column、哪个 backend？

这个 skill 的默认流程就是：

```text
backend -> environment check -> figure contract -> atlas/region validation -> preview/export -> QC -> revision
```

也就是说，它会先问你用 Python 还是 R，再检查依赖，然后确认 atlas、输入表、value column、色标和输出格式。不是直接上来就画，而是先把容易出错的地方卡住。

## 现在支持哪些皮层下/小脑 atlas？

目前 README 里已经放了一个本地生成的 atlas showcase。这个 skill 支持的 atlas 包括：

- `aseg_subcortex`
- Melbourne S1–S4
- `AICHA_subcortex`
- `Brainnetome_subcortex`
- `CIT168_subcortex`
- `Thalamus_HCP`
- `Thalamus_THOMAS`
- `Brainstem_Navigator`
- `SUIT_cerebellar_lobule`

这意味着它不只是“丘脑画图工具”，也能覆盖更完整的 subcortex / brainstem / cerebellum 场景。

## 我最在意的是：图要能进入论文 workflow

我不希望这个 skill 只是生成一张好看的 PNG。

所以它默认强调几件事：

- 先验证 ROI label，不让错别字悄悄进入图里；
- 优先输出 SVG/PDF，方便后期排版；
- 保留 PNG preview，方便快速检查；
- 每次输出都说明 atlas、value column、backend 和 unmatched labels；
- 帮你写 Methods / caption / provenance note。

这也是为什么它更像一个“可视化 workflow skill”，而不是单纯的 plot wrapper。

## 它和 cortex skill 是一套设计语言

我后来又做了一个 companion project：`cortex-visualization-skill`。

两个项目的目标是一致的：让 cortex 和 subcortex 的图都保持白底、哑光填色、清晰边界、可编辑矢量输出，不要一边像 ggseg，一边像 Workbench，一边又像手工截图。

如果你有一套分析同时包含皮层和皮层下 ROI，这两个 skill 可以让图的风格更统一，也更方便维护 Python/R 两条分析分支。

## 适合谁用？

如果你经常遇到这些情况，它应该会有用：

- 有一张 ROI value table，想快速画 thalamus / brainstem / cerebellum；
- 有 MNI-space NIfTI 图，想抽 parcel summary；
- 希望 figure 输出可以直接进论文或 supplement；
- 不想每次都重新写 atlas label 检查；
- 希望 Python 和 R workflow 都能保留。

项目地址：

https://github.com/mqqq333/subcortex-visualization-skill

## 关于这个频道

这里是 **A Man's Brainhole｜脑科学  计算神经科学  NeuroAI**。

我会在这里持续记录我读到的论文、做过的工具和踩过的坑：从脑区、神经数据、表征空间，到 AI 模型和可复现 workflow。希望每一篇都不只是“看个热闹”，而是能帮我们多理解一点大脑，也多理解一点连接大脑与 AI 的方法。

如果这篇文章对你有启发，欢迎点赞、评论、转发，也欢迎关注这个频道。我们一起读论文、拆方法、做工具，一起学习进步。

