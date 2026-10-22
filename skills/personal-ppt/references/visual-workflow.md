# 生图与视觉流程 2.0

保持逐页生图：真实调用内置 imagegen，为每页生成并在聊天中展示完整设计参考图，再制作 PPT。提示词文件不能代替生图，PPT 渲染也不能倒填为事先生成的设计图。使用前读当前 imagegen 技能，参数以真实工具为准。

## 母版与交互

先完成定稿文案。自动模式生成并展示母版设计图，自主选型并记录任务相关理由，然后继续。review 模式通常提供 2–3 个有构图差异的候选，等待用户选择。用户已选风格时复用，不重复询问。

每页调用都把所选母版作为实际风格图像输入，不只在 prompt 中提母版名称。真实照片、证据、数据图和 logo 标明严格输入，与风格图分开。原图按真实比例预留；复杂非证据素材可单独生图。严格原图在成品中直接插入原文件。

## 生图输入

`ppt_tools.py prompts` 为新项目生成 visible_content、visual_brief、master_reference、input_sources 和独立 assets 任务。它只准备输入，不调用 imagegen。

- visible_content：唯一允许上屏的准确文字、标签、表格与图表数据。页面标题要有对应 text 元素。
- visual_brief：布局、重点、母版样式、颜色、字体与留白，不能作为正文印出来。
- input_sources：真实素材的文件路径与角色。
- speaker_notes、production_records、检查报告、任务目的的解释文字留在项目，不进入生图提示词。

不让模型补副标题、口号、免责声明和结论框。出现额外文字时，在重建前修正；不能因为它在生成图中出现就加入正文。生图文字或数字有误时以定稿 spec 为准，必要时修订设计图；不从图中猜业务数据。

## 文件与显示

每页 design_reference 指向真实图片；reference_size 为真实像素尺寸，image_frame 为等比放置区域。design_generation 记录 backend="built-in-imagegen"、实际 tool、prompt_path、image_sha256、master_sha256、displayed=true、display_method（tool-inline/markdown-inline）。图片实际显示后才能写 displayed=true，页数多可分组展示，不增加逐页批准。

完成后 `fidelity_tools.py pin` 冻结已经展示的设计图，独立观察后建立 reference-measurements.json 和完整元素清单。重建时先查看图像再按图定位，调整按 adaptive-layout.md 记录。

纯背景和独立插画不含正文、数字和图表标签，透明素材请求真实透明背景；不裁一张带正文整页图再覆盖几个文本框冒充重建。缺少内置生图能力时报告实际阻碍，保留项目，不静默切换成无需生图的制作路线。

## 2.1 独立图片层

复杂画面按需要拆分 background/subject/foreground，实际字段用 layer_role=base/subject/foreground/cutout。每一层都传入同一原始设计图，不用前一层的生图作为下一层参考。文本用原生对象，干净背景不得残留重复文字；透明层保持画布和注册位置。真实证据不再生成。layer-jobs 只提供调用清单，仍须实际调用内置 imagegen 并查看素材。见 [native-bridge.md](native-bridge.md)。
