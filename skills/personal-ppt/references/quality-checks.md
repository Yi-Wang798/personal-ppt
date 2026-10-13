# 内容、视觉与可编辑性检查

v1.3 增加母版确认和重建契约检查：分页生成前 `reconstruction_tools.py check --stage pagination`，构建前 `check --stage production`。确认母版哈希匹配用户选择，PPT 母版已保存，分页采用所选母版，参考元素无遗漏、测量位置未偏移、文字角色大小一致。正式 inspect 增查实际对象位置/尺寸、编码字号和遗留 pppt:underlay 底图。原生字体继承、旋转外观和科学拓扑仍需实际渲染检查。

分区域叠图对照后移除底图，检查 clean 渲染，特别看隐藏在底图里的缺失元素。不得仅清点“spec 中已有元素”，还需核对原图所有可见组件是否进入 reference_inventory。复杂元素用实际独立素材补齐，不允许直接删掉。母版共用结构不触发强制换版式建议。

v1.2 默认逐页生图。production 和 inspect 都检查逐页设计图与显示记录：不能缺图直接交付，也不能把 PPT 最终渲染图倒填为事先生图。图片记录必须源于真实内置工具输出和聊天显示；结构检查本身不认证调用真实性。明确跳过生图的用户要求保留原话，其他情况下缺失就先补生图及显示。

构建前 preflight：页数、id、有限坐标、字号、图表数据长度、表格结构、来源和素材。未生成的 illustration/background 可用 asset_prompt；实际构建前落到真实路径。

内容阶段 preflight --stage planning 允许未确定坐标；样张后 layout 检查坐标；构建前 production 要求所有图片存在。另执行 design-check 检查材料用途、颜色角色、重复构图和科研结论/证据映射。设计警告需结合内容和真实渲染处理，不能为了分数强行换版式。

构建后：Presentations finalizer 必须声明实际总页数、原生图表/表格所在页与适用字体。PPTX ZIP 能打开不等于通过。

数据图表不仅要存在 c:chart，还需有唯一有效的 externalData 关系与嵌入 Excel 工作簿，便于编辑数据。完整字面数据的新图可明确物化快照；已有图表公式和来源关系需要保留时不可用快照替代。

补充 inspect：检查准确文字、对象命名及类型、数量、全页图片风险。报告带最终 PPTX SHA256；成品改变后旧报告失效。不得删掉内容要求来消除错误。

渲染全部最终页，逐页全尺寸查看，联系表只检查全套节奏。核对中文断行、字号、裁切、边距、重叠、轴/图例/单位、表格、流程方向、色彩、原图是否保持。对照真实样张与资料，不能仅用自动 pass 证明美观。

审美复查：连续页面是否都为同一标题+小图+大段正文；颜色是否只有清单却没有体现语义；证据是否足够大；重点是否一眼可见；版式变化是否服务论证。检查同实验组全套同色、标签可辨、原图不被随意重着色。构图只换色不算结构变化。

对使用样张的页面，将成品与参考并排查看，逐条核对 design_features，并在私人 build/design-review.json 记录实际观察。无溢出但单调或明显丢失样张特色，也属于需修改的问题。该记录由真实查看产生，不自动填 pass。

抽查修改文字、图表数值后的合理排版；文本为原生段落、表格为 table、图表含数据、节点线为原生对象。独立图片只承诺替换与位置编辑。没有在 PowerPoint 打开检查时，不声称通过 PowerPoint 内验证。

存在真实问题才修复，局部重建后重新 finalizer 和渲染，新成品用新名字。通常最多 3 次有针对性修正；未解决时报告页码、原因和实际可用程度，不假装完成。

交付最终 output/、previews/ 与可复用项目源。日志不进入演讲内容；用户索取完整项目时可含 build/，说明它是构建与检查目录。验收需准确内容、指定范围、主要视觉关系、要求的原生编辑性，无重大溢出、裁切和数据错误。


v1.4 新项目生产预检增加设计锁检查；inspect 增加逐项 conversion_trace。verified 仅代表已执行的结构检查，pending_visual_checks 与最终视觉检查仍需处理。科研结果还应完成来源数据→spec→导出图表/工作簿核对及公式检查，记录 build/data-review.json；详见 [设计稿与科研校验](design-contract.md)。


v1.5 的交付 gate 为 reconstruction_tools.py delivery：冻结图与独立测量、复杂样页明确验收、实际分段样式/可解析段落参数/层次/线宽/虚实、逐页文件哈希绑定视觉记录。记录完整不自动等于视觉通过。具体八类阻断项、对照与差异清单见 [还原验收](fidelity-gates.md)。不能以 inspect pass 或自填“已检查”代替此流程。


v1.6 更新优先于本文旧版的机械坐标/差异清零约束：参考保留原样，允许授权范围内按真实素材、可读性、居中和均衡纠正布局；记录 adaptations 的原始 before 与目标 after，未解决问题仍阻断，合理调整可作为已解决差异。新增 alignment_constraints、paragraph.vertical_alignment 与 emphasis_scope=all，核对实际 PPT；完整字段与调整边界见 [灵活排版](adaptive-layout.md)。新项目 workflow_version="1.6"。


v1.7：生图前完成正文/演讲备注/制作记录分流、Humanizer 有限精简与独立文案审核；新增 semantic_lines、component_groups、component_constraints、editorial_groups、continuation_indent_px；颜色逐角色区域取样并链接母版；最终独立 content/layout/color 三项验收。新项目 workflow_version="1.7"，规则与命令见 [文案、组合布局和取色](editorial-layout-color.md)。保持 1.6 的可追溯灵活调整，不能用新规则强制机械复刻。
