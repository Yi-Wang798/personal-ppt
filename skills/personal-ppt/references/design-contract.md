# 内容与构建设计合同

生图与原生制作共用 deck-spec.json 的准确内容。生成图提供视觉参考，独立测量记录原图所见，构建 spec 记录实现目标；不得由构建脚本回填独立测量。原图与测量、PPT 实际对象分别核对。

测量与必要局部调整完成后，用 design_contract.py freeze 保存 build/design-lock.json。新项目的锁还包括 task_profile、audience、purpose、density、interaction 与 mode，防止制作中悄悄改变用途或确认方式。变更后同步构建源、重新渲染和检查，再显式 freeze --replace；不要只刷新哈希来掩盖不一致。

每页记录 layout_family、page_rhythm（anchor/dense/breathing）与 design_features。统一母版可有多个按内容需要命名的 layout，不强制三种布局或固定轮换。

PPT 实际对象通过 conversion_trace 追踪到 spec；文字、表格、图表和图片的编辑方式与声明一致。实际坐标、样式、对齐、层次与参考或有效调整目标一致，细节见 fidelity-gates.md 和 adaptive-layout.md。

有数据时把原数据、spec 值与导出图表/嵌入工作簿核对。数据图、公式和数字不从生成图片提取。科研附加要求见 scientific-design.md；业务数据核对时间范围、金额与计算口径；没有数值的页面不生成 data-review 待办来填充正文。

```text
<python> scripts/design_contract.py freeze --spec <deck-spec.json>
<python> scripts/design_contract.py check --spec <deck-spec.json>
```

schema_version 保持 1；新任务 workflow_version="2.1"。旧版本的 snapshot 不增加新字段，保持原检查行为；只有明确修订范围需要时才迁移项目。
