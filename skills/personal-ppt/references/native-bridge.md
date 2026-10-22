# 原生转换接入（2.1）

这层接在逐页生图和测量之后，不是新增制作路线。先完成内容、母版和逐页设计图，再由同一份 spec 编译 scene。PPT Master 处理 SVG 几何到 DrawingML 的转换；python-pptx 统一封装文字、图片、表格、图表、母版和页面。不要再用另一个引擎重新导出这个文件。

使用 load_workspace_dependencies 找 Python；需要 python-pptx、Pillow、lxml。转换依赖已随 skill 的 vendor 目录完整保留，不临时下载，不要求外部生图 API。vendor 中的 SKILL.md 是上游署名及完整性依赖，不是本插件的执行入口。使用本目录的 SKILL.md。

## 同一对象描述

对象沿用 deck-spec 的 elements。scene 只含可见文字、样式、几何和素材指纹；speaker_notes、production_records 不上屏。构建时重新读取 spec，不维护第二套手写坐标。公开命令仍检查既有的内容、设计图、测量、样页和设计锁要求。

```shell
python scripts/native_bridge.py compile --spec PROJECT/deck-spec.json --out PROJECT/build/scene-v1.json
python scripts/native_bridge.py master --spec PROJECT/deck-spec.json --out PROJECT/build/master-v1.pptx
```

把生成的母版路径写入 master.ppt_template_path。固定且全套相同的对象写入 master.elements（仅 text/shape/image）；不同页的标题、内容放在 slides[].elements。固定母版对象只写一次，不逐页复制。master 命令创建可复用的无分页 PPTX；正式导出根据相同 master.elements 重建同一个原生母版。旧母版不能改写后继续声称沿用了旧版；改变后按原合同刷新。

```shell
python scripts/native_bridge.py export --spec PROJECT/deck-spec.json --stage sample --out PROJECT/output/sample-v1.pptx
python scripts/native_bridge.py export --spec PROJECT/deck-spec.json --out PROJECT/output/deck-v1.pptx
```

先检查代表性复杂页，再完成全套。`sample` 仍检查其 spec 中所有页面，因此需要生成样页子集 spec，按既有样页流程保留来源关联。不要删掉正式项目的页面来绕过验收。命令不覆盖已有文件。输出旁的 report.json 保留对象级转换记录和实际 PPTX 哈希。

## 几何和数据

- shape.geometry：rect、roundRect、ellipse、triangle、chevron、hexagon；`preset:chevron`、`preset:hexagon` 使用上游 Office 预设语义，adjustments 可记录已知调节点。其他 preset 需单独导出并看渲染，不能声称全库已验证。
- freeform 配合 svg_path，路径使用页面坐标。svg_asset_path 是简单矢量素材，须有 viewBox，包含后保持比例。首批不接受内嵌 SVG 文字、位图、脚本或外链。不支持的效果保留为独立图片，不能默默丢失。
- text 支持 runs、完整加粗、混排字体、段落对齐、内边距与明确断行。中文微软雅黑，英文 Times New Roman。文字尺寸使用 pt，box 使用 px。
- connector 使用 from/to 附着原生节点；方向和箭头必须看实际渲染。
- table.rows 保持单元格；chart 支持 column/bar/line/pie 的 categories/series，并嵌入 Excel 字面数据。仅适用于新建的已知数据图，不替换既有公式工作簿。

## 独立图层

需要分层的 image 对象可写 layer_role=base/subject/foreground/cutout、registration_group 和 asset_prompt。运行：

```shell
python scripts/native_bridge.py layer-jobs --spec PROJECT/deck-spec.json --out PROJECT/prompts/layers-v1.json
```

这是生图任务清单，不是假装已生成的图片。每个任务必须把 canonical_reference 指向的原始设计图真实传给内置 imagegen；不要用上一次分层生成图作为下一层的新参考。背景移除将被重建的文字和主体；主体与前景使用透明背景。相互注册的图层保持相同画布、相同放置 box，不裁紧再凭感觉找位置。用独立预览检查边缘与重叠，真实写入 asset_path 后再导出。证据图和 logo 不进入再生成队列。

原图与设计图比例不同时，先在 spec 中按真实素材重排，并记录必要差异。转换器不拉伸原图。不要为了图层一致而保留设计图的遮挡或溢出。

## 组件参考

assets/components/index.json 收录六个上游构图参考：对比、重点句、图文分栏、时间流程、图表解读、表格摘要。只在内容适合时查看对应 SVG，重新组织自己的准确文字和真实素材，然后照常生图；不照搬上游占位内容、字体或整页模板。它们用于减少重复设计，不要求每页都卡片化。

## 验收边界

使用 Presentations 读取并渲染最终 PPTX，检查实际文字、独立图层、原生几何、数据与母版继承。不要把导入渲染后重新导出的副本当作正式文件，以免改写原生对象。ppt_tools.inspect 与 fidelity 检查仍作用于实际 PPTX。结构通过不等于视觉通过。

本版不集成上游动画、外部生图服务或公式管线；不宣称整张图片已自动转成可编辑对象。
