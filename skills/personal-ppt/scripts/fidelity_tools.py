"""Independent reference measurements and hash-bound sample/delivery gates.

This checks files, actual OOXML and review records; it cannot certify human
approval, independently recognize pixels, or prove render provenance.
"""
import argparse
import hashlib
import json
import math
import zipfile
import struct
from pathlib import Path
import xml.etree.ElementTree as ET
import adaptive_layout

KEYS = ("left", "top", "width", "height")
BLOCKERS = ("missing_elements", "text_overflow", "subject_cropped", "lost_emphasis",
            "wrong_layers", "changed_layout", "wrong_group_colors", "wrong_text_styles")


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8-sig"))


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def load_file(base, record, errors, label):
    if not isinstance(record, dict) or not isinstance(record.get("path"), str):
        errors.append(f"{label}: 缺少 path/sha256"); return None
    path = base / record["path"]
    if not path.is_file() or record.get("sha256") != sha(path):
        errors.append(f"{label}: 文件缺失或哈希改变"); return None
    return path


def check_measurements(spec, base):
    """Read reference observations, never derive them from construction values."""
    base = Path(base); errors = []
    registry_path = base / "design/reference-registry.json"
    measure_path = base / "design/reference-measurements.json"
    if not registry_path.is_file() or not measure_path.is_file():
        return ["缺少独立 reference-registry.json 或 reference-measurements.json"]
    registry = read(registry_path); measurements = read(measure_path)
    if measurements.get("origin") != "visual-reference-measurement":
        errors.append("测量必须来自冻结参考图，不从 build/spec 回填")
    measured_pages = {p["id"]: p for p in measurements.get("slides", [])}
    for page in spec.get("slides", []):
        sid = page["id"]; record = registry.get("slides", {}).get(sid)
        frozen = load_file(base, record, errors, sid + " 冻结参考图")
        current = base / page.get("design_reference", "")
        if frozen and (not current.is_file() or sha(current) != record["sha256"]):
            errors.append(f"{sid}: 当前设计图已被替换，必须使用已展示的冻结版本")
        observed = measured_pages.get(sid, {})
        for field in ('reference_size','image_frame'):
            if not isinstance(observed.get(field),dict) or observed.get(field)!=page.get(field):
                errors.append(f"{sid}: {field} 缺少或偏离独立映射记录")
        if frozen:
            data=frozen.read_bytes()
            if data.startswith(b'\x89PNG\r\n\x1a\n') and len(data)>=24:
                width,height=struct.unpack('>II',data[16:24])
                if observed.get('reference_size')!={'width':width,'height':height}:
                    errors.append(f"{sid}: 独立测量尺寸与实际冻结 PNG 不符")
        if not record or observed.get("reference_sha256") != record.get("sha256"):
            errors.append(f"{sid}: 独立测量不对应冻结参考图")
        if not observed.get("observations"):
            errors.append(f"{sid}: 缺少实际看图测量观察")
        if observed.get('group_color_map') != page.get('group_color_map'):
            errors.append(f"{sid}: 实验组身份色映射已改变")
        items = {e["id"]: e for e in observed.get("elements", [])}
        adjusted, adjustment_errors=adaptive_layout.effective(observed,page,spec['canvas'])
        errors.extend(f"{sid}: {error}" for error in adjustment_errors)
        items = {e["id"]: e for e in adjusted.get("elements", [])}
        planned = {e["id"]: e for e in page.get("elements", [])}
        if set(items) != set(planned):
            errors.append(f"{sid}: 独立元素清单与构建元素不一致")
        for eid, target in planned.items():
            source = items.get(eid, {})
            if source.get('box')!=target.get('box'):
                errors.append(f"{sid}/{eid}: 构建位置没有采用有效的参考/调整目标")
            for key in ("reference_box", "kind"):
                if source.get(key) != target.get(key):
                    errors.append(f"{sid}/{eid}: {key} 与独立参考测量不一致")
            if target.get("kind") == "text":
                runs = target.get("runs"); observed_runs = source.get("runs")
                if not isinstance(runs, list) or not runs or runs != observed_runs:
                    errors.append(f"{sid}/{eid}: 缺少或改变独立分段文字样式")
                else:
                    if ''.join(r.get("text", "") for r in runs) != target.get("text"):
                        errors.append(f"{sid}/{eid}: runs 与准确文字不一致")
                    for run in runs:
                        if any(k not in run for k in ("font_family", "font_size_pt", "color", "bold", "italic")):
                            errors.append(f"{sid}/{eid}: run 样式记录不完整")
                    if target.get('emphasis_scope')=='all' and any(r.get('bold') is not True for r in runs):
                        errors.append(f"{sid}/{eid}: 整段加粗未覆盖全部文字分段")
                for key in ("paragraph", "line_breaks"):
                    if not isinstance(target.get(key), dict if key == "paragraph" else list) or target.get(key) != source.get(key):
                        errors.append(f"{sid}/{eid}: {key} 未记录或偏离参考")
                paragraph = source.get('paragraph', {})
                if not all(k in paragraph for k in ('alignment','margins_px','line_spacing_pt','space_before_pt','space_after_pt')):
                    errors.append(f"{sid}/{eid}: 段落测量缺少行距/段间距/内边距")
                if not all(k in paragraph.get('margins_px',{}) for k in ('left','right','top','bottom')):
                    errors.append(f"{sid}/{eid}: 四边内边距未记录")
            for key in ("visual_style", "layer", "crop", "group_id"):
                if key in source and source[key] != target.get(key):
                    errors.append(f"{sid}/{eid}: {key} 与参考不一致")
            if not isinstance(source.get('layer'),int) or isinstance(source.get('layer'),bool):
                errors.append(f"{sid}/{eid}: 缺少参考层级")
            if target.get("kind") in {"shape", "connector"} and not source.get("visual_style"):
                errors.append(f"{sid}/{eid}: 缺少填充/描边/虚实/箭头参考样式")
            if target.get("kind") == "image":
                crop = source.get("crop", {})
                if crop.get("fit") not in {"contain", "crop-background-only"}:
                    errors.append(f"{sid}/{eid}: 缺少安全放置策略")
                if not isinstance(crop.get('subject_box'),dict):
                    errors.append(f"{sid}/{eid}: 缺少完整主体区域测量")
                asset = base / target.get("asset_path", "")
                receipt = source.get("asset_review", {})
                if not asset.is_file() or receipt.get("asset_sha256") != sha(asset):
                    errors.append(f"{sid}/{eid}: 素材未按当前文件验收")
                if receipt.get("subject_complete") is not True or receipt.get("displayed") is not True or not receipt.get("observations"):
                    errors.append(f"{sid}/{eid}: 未展示素材并确认主体完整")
                load_file(base, receipt.get("preview"), errors, f"{sid}/{eid} 素材预览")
        errors.extend(adaptive_layout.check_alignment(page,{eid:e.get('box') for eid,e in planned.items()}))
        errors.extend(adaptive_layout.check_components(page,{eid:e.get('box') for eid,e in planned.items()}))
    return errors


def check_review(base, review, errors, label, page=None):
    for key in ("reference", "render", "comparison"):
        load_file(base, review.get(key), errors, label + " " + key)
    if review.get("displayed") is not True or not review.get("observations"):
        errors.append(label + ": 未展示真实对照或缺少区域观察")
    blockers = review.get("blockers", {})
    for key in BLOCKERS:
        if blockers.get(key) is not False:
            errors.append(label + ": 未解决/未检查 " + key)
    differences=review.get('differences')
    adaptations={a['id'] for a in (page or {}).get('adaptations',[])}
    if differences != []:
        if not isinstance(differences,list) or any(not isinstance(d,dict) or d.get('status')!='resolved-design-adjustment' or d.get('adaptation_id') not in adaptations for d in differences):
            errors.append(label + ': 存在未解决差异')
    if adaptations and (set(review.get('adaptation_ids',[]))!=adaptations or review.get('adaptations_sha256')!=adaptive_layout.digest(page['adaptations'])):
        errors.append(label + ': 调整没有进入当前视觉复查')


def check_sample(spec, base):
    base = Path(base); errors = []
    filename = spec.get("fidelity", {}).get("sample_approval_path", "build/sample-approval.json")
    path = base / filename
    if not path.is_file(): return ["复杂样页未验收；禁止批量重建"]
    receipt = read(path)
    import workflow_policy
    if workflow_policy.needs_user_review(spec):
        if receipt.get("approved") is not True or not receipt.get("user_reply"):
            errors.append("当前模式需要样页的真实用户验收")
    elif receipt.get("reviewed") is not True or receipt.get("reviewer") != "agent" or receipt.get("user_reply") or receipt.get("approved") is True:
        errors.append("自动模式需真实内部样页检查，不能伪造用户验收")
    sample_pptx = load_file(base, receipt.get("pptx"), errors, "样页 PPT")
    pages = {p["id"]: p for p in spec.get("slides", [])}
    sid = receipt.get("slide_id")
    if sid not in pages: errors.append("验收样页不在当前项目")
    else:
        reference = base / pages[sid].get("design_reference", "")
        if not reference.is_file() or receipt.get("reference", {}).get("sha256") != sha(reference):
            errors.append("样页验收引用了另一设计图")
        complexity = receipt.get("complexity", [])
        minimum = 1 if workflow_policy.is_v2(spec) else 3
        allowed = {"mixed-text", "layered-panel", "source-image", "connectors", "chart", "mechanism"}
        if workflow_policy.is_v2(spec):
            allowed |= {"text-layout", "table"}
        if not isinstance(complexity, list) or len(set(complexity)) < minimum or not set(complexity) <= allowed:
            errors.append("样页特征应对应本项目实际内容；旧项目仍要求至少三项")
        if 'mixed-text' in complexity and not any(len(e.get('runs', [])) > 1 for e in pages[sid].get('elements', [])):
            errors.append("样页声称混合文字但没有分段")
        elements = pages[sid].get('elements', [])
        kinds = [e.get('kind') for e in elements]
        for feature, valid in {
            'text-layout': 'text' in kinds,
            'table': 'table' in kinds,
            'layered-panel': kinds.count('shape') >= 2,
            'source-image': any(e.get('kind') == 'image' and e.get('role') == 'evidence' for e in elements),
            'connectors': 'connector' in kinds,
            'chart': 'chart' in kinds,
            'mechanism': 'connector' in kinds and 'shape' in kinds,
        }.items():
            if feature in complexity and not valid: errors.append('样页复杂特征不真实: ' + feature)
        if sample_pptx:
            import ppt_tools as ppt
            sample_spec = dict(spec, slides=[pages[sid]], slide_count=1)
            sample_structure=ppt.inspect(sample_spec, sample_pptx)
            errors.extend(sample_structure['errors'])
            errors.extend(check_actual_runs(sample_spec, sample_pptx))
            errors.extend(check_actual_geometry(sample_spec, base, sample_structure))
    load_file(base, receipt.get("measurements"), errors, "样页独立测量")
    measurement_path = base / "design/reference-measurements.json"
    if measurement_path.is_file() and receipt.get("measurements", {}).get("sha256") != sha(measurement_path):
        errors.append("样页验收后测量已变，需重新对照验收")
    check_review(base, receipt, errors, "复杂样页",pages.get(sid))
    return errors


def check_actual_runs(spec, pptx):
    """Audit explicit OOXML run styles. Inherited/unsupported styles stay blockers."""
    import ppt_tools as ppt
    errors = []
    with zipfile.ZipFile(pptx) as z:
        presentation = ET.fromstring(z.read('ppt/presentation.xml'))
        rels = {r.attrib['Id']: r.attrib['Target'] for r in ET.fromstring(z.read('ppt/_rels/presentation.xml.rels'))}
        import posixpath
        for page, sid in zip(spec['slides'], presentation.findall('p:sldIdLst/p:sldId', ppt.NS)):
            target = rels[sid.attrib['{' + ppt.NS['r'] + '}id']]
            path = target.lstrip('/') if target.startswith('/') else posixpath.normpath('ppt/' + target)
            root = ET.fromstring(z.read(path))
            named = {}
            for obj in root.findall('.//p:sp', ppt.NS):
                cn = obj.find('.//p:cNvPr', ppt.NS)
                if cn is not None: named[cn.get('name')] = obj
            for element in page['elements']:
                if element.get('kind') != 'text': continue
                label = f"pppt:{page['id']}:{element['id']}"; obj = named.get(label)
                if obj is None: errors.append(label + ': 缺少实际文字'); continue
                expected = [(char, r) for r in element.get('runs', []) for char in r.get('text', '')]
                actual = []
                breaks=[];paragraphs=obj.findall('p:txBody/a:p',ppt.NS)
                for pi, para in enumerate(paragraphs):
                    if pi:breaks.append(len(actual))
                    for node in para:
                        tag=node.tag.rsplit('}',1)[-1]
                        if tag=='br':breaks.append(len(actual))
                        elif tag=='r':
                            prop=node.find('a:rPr',ppt.NS);text=node.find('a:t',ppt.NS)
                            actual.extend((char,prop) for char in ((text.text or '') if text is not None else ''))
                expected=[(c,r) for c,r in expected if c!='\n']
                if breaks!=element.get('line_breaks',[]):errors.append(label+': 实际硬换行偏离参考')
                if ''.join(c for c, _ in expected) != ''.join(c for c, _ in actual):
                    errors.append(label + ': 实际分段文字不一致'); continue
                for (char, exp), (_, prop) in zip(expected, actual):
                    if prop is None: errors.append(label + ': 样式继承未解析'); break
                    family_tag = 'ea' if '\u3400' <= char <= '\u9fff' else 'latin'
                    family = prop.find('a:' + family_tag, ppt.NS)
                    color = prop.find('a:solidFill/a:srgbClr', ppt.NS)
                    valid = (family is not None and family.get('typeface') == exp.get('font_family')
                             and prop.get('sz') is not None and abs(int(prop.get('sz')) / 100 - exp.get('font_size_pt', 0)) <= .2
                             and color is not None and color.get('val', '').upper() == exp.get('color', '').lstrip('#').upper()
                             and (prop.get('b', '0') in {'1', 'true'}) == exp.get('bold')
                             and (prop.get('i', '0') in {'1', 'true'}) == exp.get('italic'))
                    if not valid: errors.append(label + ': 实际字体/字号/颜色/粗斜体偏离独立测量'); break
                body = obj.find('p:txBody/a:bodyPr', ppt.NS)
                paragraph = element.get('paragraph', {})
                if 'continuation_indent_px' in paragraph:
                    for para in paragraphs:
                        prop=para.find('a:pPr',ppt.NS)
                        value=prop.get('marL') if prop is not None else None
                        if value is None or abs(int(value)/9525-paragraph['continuation_indent_px'])>.2:
                            errors.append(label+': 后续正文行未共享指定起始位置');break
                vertical={'top':'t','center':'ctr','bottom':'b'}.get(paragraph.get('vertical_alignment'))
                if vertical and (body is None or body.get('anchor','t')!=vertical):
                    errors.append(label+': 实际文字没有按要求垂直对齐')
                if element.get('emphasis_scope')=='all' and any(r.get('bold') is not True for r in element.get('runs',[])):
                    errors.append(label+': 整段加粗要求未覆盖所有中英文分段')
                for key, attribute in [('left','lIns'),('right','rIns'),('top','tIns'),('bottom','bIns')]:
                    value = paragraph.get('margins_px', {}).get(key)
                    if value is not None and (body is None or body.get(attribute) is None or abs(int(body.get(attribute))/9525-value)>.2):
                        errors.append(label + ': 实际文本内边距未匹配 ' + key)
                props = obj.findall('p:txBody/a:p/a:pPr', ppt.NS)
                alignment = {'left':'l','center':'ctr','right':'r','justify':'just'}.get(paragraph.get('alignment'))
                if alignment and (not props or any(p.get('algn') != alignment for p in props)):
                    errors.append(label + ': 实际段落对齐未匹配')
                for key, tag in [('line_spacing_pt','lnSpc'),('space_before_pt','spcBef'),('space_after_pt','spcAft')]:
                    if key not in paragraph: continue
                    for prop in props or [None]:
                        spacing = prop.find(f'a:{tag}/a:spcPts',ppt.NS) if prop is not None else None
                        if spacing is None or abs(int(spacing.get('val',0))/100-paragraph[key])>.2:
                            errors.append(label + ': 实际段落间距未匹配 ' + key);break
            # Explicit panel/line attributes are measured separately; never a default 2px.
            objects = []
            for obj in root.iter():
                if obj.tag.rsplit('}',1)[-1] not in {'sp','grpSp','pic','cxnSp','graphicFrame'}:continue
                cn = obj.find('.//p:cNvPr',ppt.NS)
                if cn is not None:objects.append((cn.get('name'),obj))
            actual_order = {name:index for index,(name,_) in enumerate(objects)}
            object_map = dict(objects)
            planned_order = sorted(page['elements'],key=lambda e:e.get('layer',0))
            ranks = [actual_order[f"pppt:{page['id']}:{e['id']}"] for e in planned_order if f"pppt:{page['id']}:{e['id']}" in actual_order]
            if ranks != sorted(ranks): errors.append(page['id'] + ': 实际对象层叠顺序偏离参考')
            for element in page['elements']:
                label=f"pppt:{page['id']}:{element['id']}";obj=object_map.get(label)
                if obj is None:continue
                style=element.get('visual_style',{})
                sp=obj.find('p:spPr',ppt.NS)
                if element.get('kind')=='image' and element.get('crop',{}).get('fit')=='contain':
                    crop=obj.find('p:blipFill/a:srcRect',ppt.NS)
                    if crop is not None and any(int(crop.get(k,'0'))!=0 for k in ('l','r','t','b')):
                        errors.append(label+': 等比完整素材被实际裁剪')
                if style.get('fill_none') is True and (sp is None or sp.find('a:noFill',ppt.NS) is None):
                    errors.append(label+': 无填充被替换为实色')
                for field,xml_path in [('fill','a:solidFill/a:srgbClr'),('stroke','a:ln/a:solidFill/a:srgbClr')]:
                    if field not in style:continue
                    if style[field]=='none':
                        parent=sp if field=='fill' else (sp.find('a:ln',ppt.NS) if sp is not None else None)
                        if parent is None or parent.find('a:noFill',ppt.NS) is None:
                            errors.append(label + ': 实际 ' + field + ' 应为无填充')
                        continue
                    node=sp.find(xml_path,ppt.NS) if sp is not None else None
                    if node is None or node.get('val','').upper()!=style[field].lstrip('#').upper():
                        errors.append(label + ': 实际 ' + field + ' 未匹配参考')
                line=sp.find('a:ln',ppt.NS) if sp is not None else None
                if 'stroke_width_pt' in style and (line is None or line.get('w') is None or abs(int(line.get('w'))/12700-style['stroke_width_pt'])>.1):
                    errors.append(label + ': 实际线宽未匹配参考')
                if 'dash' in style:
                    node=line.find('a:prstDash',ppt.NS) if line is not None else None
                    actual_dash=node.get('val') if node is not None else 'solid'
                    if actual_dash!=style['dash']:errors.append(label + ': 虚实线未匹配参考')
                for field,tag in [('start_arrow','headEnd'),('end_arrow','tailEnd')]:
                    if field not in style:continue
                    node=line.find('a:'+tag,ppt.NS) if line is not None else None
                    if (node.get('type') if node is not None else 'none')!=style[field]:
                        errors.append(label + ': 实际箭头端点未匹配参考；方向还需渲染核查')
    return errors


def delivery(spec, base, pptx, review_path):
    import ppt_tools as ppt
    errors = check_measurements(spec, base) + check_sample(spec, base)
    if spec.get('workflow_version') in {'1.7','2.0','2.1'}:
        import editorial_tools,color_sampler
        errors.extend(editorial_tools.check(spec,base));errors.extend(color_sampler.verify(spec,base))
        errors.extend(editorial_tools.check_visible_copy(spec,pptx))
    structure = ppt.inspect(spec, pptx)
    errors.extend(structure['errors']); errors.extend(check_actual_runs(spec, pptx))
    errors.extend(check_actual_geometry(spec, base, structure))
    review = read(review_path)
    if review.get('pptx_sha256') != sha(pptx): errors.append('视觉记录不是当前成品')
    if review.get('measurements_sha256') != sha(base/'design/reference-measurements.json'):
        errors.append('视觉记录不是当前独立测量')
    pages = {p['id']: p for p in review.get('slides', [])}
    for page in spec['slides']:
        sid = page['id']; item = pages.get(sid, {})
        if item.get('reference', {}).get('sha256') != sha(base/page['design_reference']):
            errors.append(sid + ': 对照参考已换稿')
        check_review(base, item, errors, sid, page)
        if spec.get('workflow_version') in {'1.7','2.0','2.1'}:
            for gate in ('content','layout','color'):
                record=item.get('review_sections',{}).get(gate,{})
                if record.get('passed') is not True or not record.get('observations'):
                    errors.append(sid+': '+gate+' 独立验收缺失')
    return {'status': 'fail' if errors else 'pass', 'errors': errors,
            'structural_status': structure['status'], 'visual_status': 'blocked' if errors else 'record-complete',
            'limits': '核验实际 OOXML 与哈希绑定的观察记录；不自动证明用户授权、图片渲染真实性或像素视觉通过'}


def check_actual_geometry(spec, base, structure):
    import reconstruction_tools as reconstruction
    errors=[]
    observed={p['id']:p for p in read(base/'design/reference-measurements.json').get('slides',[])}
    pages={p['id']:p for p in structure.get('slides',[])}
    for page in spec['slides']:
        sid=page['id'];source=observed.get(sid,{})
        source,adjustment_errors=adaptive_layout.effective(source,page,spec['canvas'])
        errors.extend(adjustment_errors)
        trace={e['element_id']:e for e in pages.get(sid,{}).get('conversion_trace',[])}
        for element in source.get('elements',[]):
            actual=trace.get(element['id'],{}).get('actual_box')
            if not actual:errors.append(f"{sid}/{element['id']}: 成品位置未解析，禁止默认通过");continue
            expected=element.get('box') or reconstruction.map_box(source.get('reference_size',{}),source.get('image_frame',{}),element.get('reference_box',{}))
            if any(abs(actual[k]-expected[k])>3 for k in KEYS):
                errors.append(f"{sid}/{element['id']}: 成品位置偏离独立参考测量")
        errors.extend(adaptive_layout.check_alignment(page,{eid:item.get('actual_box') for eid,item in trace.items()}))
        errors.extend(adaptive_layout.check_components(page,{eid:item.get('actual_box') for eid,item in trace.items()}))
    return errors


def pin(spec, base):
    """One-time snapshots of images already shown; cannot silently refresh."""
    registry = base/'design/reference-registry.json'
    if registry.exists(): raise ValueError('参考图已冻结；禁止覆盖或重钉以消除偏差')
    records = {}
    for page in spec['slides']:
        source = base/page['design_reference']; digest = sha(source)
        if page.get('design_generation', {}).get('image_sha256') != digest or page.get('design_generation', {}).get('displayed') is not True:
            raise ValueError(page['id'] + ': 必须先真实展示设计图并记录哈希')
        destination = base/'design/frozen'/page['id']/(digest + source.suffix.lower())
        if destination.resolve() == source.resolve(): raise ValueError('冻结目标不得为源图')
        records[page['id']] = {'path': str(destination.relative_to(base)), 'sha256': digest,
                              'original_path': page['design_reference']}
    for sid, record in records.items():
        destination = base/record['path']; destination.parent.mkdir(parents=True, exist_ok=True)
        with destination.open('xb') as output: output.write((base/record['original_path']).read_bytes())
    registry.write_text(json.dumps({'schema_version':1, 'slides':records}, ensure_ascii=False, indent=2), encoding='utf-8')
    return {'status':'pass', 'slides':len(records), 'registry':str(registry)}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command',choices=['pin','check','sample','delivery'])
    parser.add_argument('--spec',required=True);parser.add_argument('--pptx');parser.add_argument('--review')
    args=parser.parse_args()
    try:
        path=Path(args.spec).resolve();base=path.parent;spec=read(path)
        if args.command=='pin':result=pin(spec,base)
        elif args.command=='delivery':
            if not args.pptx or not args.review:raise ValueError('delivery 需要 --pptx 和 --review')
            result=delivery(spec,base,Path(args.pptx).resolve(),Path(args.review).resolve())
        else:
            errors=check_measurements(spec,base) if args.command=='check' else check_sample(spec,base)
            result={'status':'fail' if errors else 'pass','errors':errors}
        print(json.dumps(result,ensure_ascii=False,indent=2));return 2 if result['status']=='fail' else 0
    except (OSError,ValueError,TypeError,KeyError,ET.ParseError,zipfile.BadZipFile) as error:
        print(json.dumps({'status':'fail','error':str(error)},ensure_ascii=False));return 2


if __name__=='__main__':raise SystemExit(main())
