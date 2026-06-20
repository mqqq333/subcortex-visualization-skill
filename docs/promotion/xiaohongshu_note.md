# 小红书笔记：subcortex-visualization skill

## 标题

皮层下脑区图，终于不用手搓了

## 正文

如果你做过丘脑、脑干、小脑或者其他皮层下 ROI 可视化，应该懂这种痛：

皮层图很好找模板，皮层下结果却经常变成 slice 截图、手工拼图、不同 palette 混在一起。

所以我把 Annie Bryant 的 subcortex_visualization 包整理成了一个 Codex Skill：subcortex-visualization。

01｜它不是单纯画图脚本

它更像一条可复现 workflow：

先选 Python/R backend，再检查环境，再确认 atlas、ROI 表、value column、色标和输出格式。

02｜最有用的点

它会先验证 ROI label，避免 region 名字错了还悄悄画出图。

输出也不是只有 PNG，而是偏论文友好的 SVG/PDF + PNG preview。

03｜支持什么 atlas？

aseg_subcortex、Melbourne、AICHA、Brainnetome、CIT168、Thalamus_HCP、Thalamus_THOMAS、Brainstem_Navigator、SUIT cerebellum 都有覆盖。

04｜为什么我想做成 skill？

因为我不想每次从零写同一套检查代码。

真正重要的是：图能复现，label 能检查，Methods 能说清楚。

项目：
https://github.com/mqqq333/subcortex-visualization-skill

A Man's Brainhole｜脑科学  计算神经科学  NeuroAI
一起读论文、拆方法、做工具，一起学习进步。

## Hashtags

#脑科学 #计算神经科学 #NeuroAI #科研工具 #数据可视化 #Python科研 #R语言 #神经影像 #可复现研究

## 轮播卡片文案

1. 皮层下脑区图，终于不用手搓了
2. 痛点：ROI 表有了，但图总是不统一
3. workflow：backend → 检查环境 → 验证 label → 输出图
4. 支持：丘脑、脑干、小脑、皮层下多个 atlas
5. 输出：SVG/PDF 进论文，PNG 做预览
6. 重点：不是漂亮截图，是可复现 figure
7. GitHub：subcortex-visualization-skill

