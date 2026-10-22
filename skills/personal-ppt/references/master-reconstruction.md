# 母版与逐页重建 2.0

## 母版选择

母版包括整体风格、固定元素、字体层级、颜色角色及内容布局体系。先实际生成并展示母版图，再进入分页。自动模式自主选择；review 模式等待用户选择。项目外观已明确时直接延续。

master 保存 id、reference_image、reference_size、image_sha256、approval、tokens、ppt_template_path。tokens.fonts 固定 zh="Microsoft YaHei"、en="Times New Roman"；text_styles 的每个角色记录 font_size_pt，可附 bold/alignment。字号按内容和排版判断，同角色全套固定。

自动选择的 approval 为 selected_by="agent"、confirmed=false、selection_reason、reference_sha256，user_selection 留空。用户选择则 selected_by="user"、confirmed=true、user_selection 为真实回复、reference_sha256。不能把“自动完成”写成用户已批准某张未看过的图。旧项目仍需要原来的明确确认。

## 分页输入与原生母版

每页实际引用所选母版，design_generation.master_sha256 对应它；不只参考上一页导致风格漂移。内容区根据任务选择 layout，固定结构、文字层级和颜色含义统一。

构建前先保存具有真实 slideMaster/layout 的 PPT 母版。插入母版图校准；分页用自己的设计图作测量底图。参考图像素通过 image_frame 等比映射到画布，不能横纵独立拉伸。用 reconstruction_tools.py map 可计算坐标。

## 元素与素材

查看整页图建立 reference_inventory，每项含 id、description、reference_box、route、element_ids。route 为 native/generated-image/source-image/master-element，指元素实现方式，非另一套制作路线。文字、连线、背景层、标签、角标与独立图像都应有成品对应物。

文本关联 master_slot，并记录混合 runs、颜色、字重与必要段落设置；标题角色统一不能抹掉局部强调。复杂元素独立生图插入，严格数据图和证据用原文件。所有图片保持主体、图例、刻度完整，先查看独立素材再插入。

选择本项目最有代表性的复杂页先重建。自动模式内部查看真实渲染及对照，修复后继续；review 模式展示对照等待用户验收。同一版已有验收复用。简单任务不需要凭空凑齐三种复杂元素。记录字段见 fidelity-gates.md。

叠图定位后，按真实素材、语义换行、可读性与整体平衡作局部调整；规则见 adaptive-layout.md。完整重建后从交付副本删除 pppt:underlay 底图，私人草稿可保留。检查实际 PPT 的对齐、字号、完整加粗和图像比例。

## 2.1 母版落实

固定对象写 master.elements，由 native_bridge master 生成可复用 PPTX，再将真实路径写回 ppt_template_path。页面沿用同一个 slideMaster/layout；master_slot 的文字默认值在 scene 编译时继承。同一套对象描述用于母版与正式导出，禁止各页重新手写一套固定装饰。具体见 [native-bridge.md](native-bridge.md)。
