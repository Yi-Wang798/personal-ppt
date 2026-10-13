"""Bounded local design corrections; keep original measurements unchanged."""
import copy
import hashlib
import json


def digest(value):
    return hashlib.sha256(json.dumps(value,ensure_ascii=False,sort_keys=True,
                                    separators=(',',':'),allow_nan=False).encode()).hexdigest()


def effective(source, page, canvas):
    import reconstruction_tools as reconstruction
    adjusted=copy.deepcopy(source);errors=[];ids=set();modified=set()
    elements={e['id']:e for e in adjusted.get('elements',[])}
    for element in elements.values():
        element['box']=reconstruction.map_box(source['reference_size'],source['image_frame'],element['reference_box'])
    for item in page.get('adaptations',[]):
        aid=item.get('id');eid=item.get('element_id')
        if not aid or aid in ids:errors.append('调整 id 缺失或重复')
        ids.add(aid)
        if eid not in elements:errors.append('调整不能删除/虚构元素');continue
        if item.get('reference_sha256')!=source.get('reference_sha256'):
            errors.append('调整依据不是冻结参考图')
        if item.get('category') not in {'source-fit','text-readability','alignment','balance','reference-error'} or not item.get('reason') or not item.get('observations'):
            errors.append('局部调整缺少具体原因与观察')
        changes=item.get('changes',{})
        if not isinstance(changes,dict) or not changes:errors.append('调整无明确前后值');continue
        element=elements[eid]
        for field, change in changes.items():
            if field not in {'box','paragraph','runs','line_breaks'}:
                errors.append('局部排版不能改数据、内容、身份色、拓扑或原图');continue
            if (eid,field) in modified:errors.append('同一属性不能被多次含糊覆盖')
            modified.add((eid,field))
            before=(reconstruction.map_box(source['reference_size'],source['image_frame'],element['reference_box']) if field=='box' else element.get(field))
            if not isinstance(change,dict) or change.get('before')!=before or 'after' not in change:
                errors.append('调整前值与独立测量不符');continue
            after=change['after']
            if field=='box':
                values=reconstruction.box_values(after)
                if values is None or values[0]<0 or values[1]<0 or values[2]<0 or values[3]<0 or values[0]+values[2]>canvas['width'] or values[1]+values[3]>canvas['height']:
                    errors.append('调整后对象越出画布');continue
            if field=='runs':
                old=element.get('runs',[])
                if not isinstance(after,list) or len(after)!=len(old) or any(a.get('text')!=b.get('text') or a.get('font_family')!=b.get('font_family') or a.get('color')!=b.get('color') for a,b in zip(old,after)):
                    errors.append('排版调整不能改准确文字、字体偏好或语义颜色');continue
                if any(not isinstance(r.get('bold'),bool) or not isinstance(r.get('italic'),bool) or not reconstruction.number(r.get('font_size_pt')) or r['font_size_pt']<=0 for r in after):
                    errors.append('调整后分段字重/字号无效');continue
            if field=='paragraph':
                if not isinstance(after,dict) or after.get('alignment') not in {'left','center','right','justify'} or after.get('vertical_alignment','top') not in {'top','center','bottom'}:
                    errors.append('段落调整无效');continue
                numeric=list(after.get('margins_px',{}).values())+[after.get(k) for k in ('line_spacing_pt','space_before_pt','space_after_pt')]
                if any(not reconstruction.number(v) or v<0 for v in numeric) or after.get('line_spacing_pt',0)<=0:
                    errors.append('段落间距必须为有效数值');continue
            if field=='line_breaks' and (not isinstance(after,list) or any(not isinstance(v,int) or isinstance(v,bool) or v<0 for v in after) or after!=sorted(after)):
                errors.append('换行调整无效');continue
            element[field]=copy.deepcopy(after)
    return adjusted,errors


def check_alignment(page, actual_boxes):
    """Center relative to the declared container, not necessarily the whole slide."""
    errors=[]
    for item in page.get('alignment_constraints',[]):
        axis=item.get('axis');container=item.get('container_box');targets=item.get('element_ids',[])
        if axis not in {'horizontal','vertical','both'} or not isinstance(container,dict) or not targets:
            errors.append('居中约束缺少轴、容器或对象');continue
        tolerance=item.get('tolerance_px',3)
        if not isinstance(tolerance,(int,float)) or not 0<=tolerance<=3:errors.append('居中容差必须在 0–3px');continue
        for eid in targets:
            box=actual_boxes.get(eid)
            if box is None:errors.append(eid+': 居中对象未解析');continue
            for position,size in ([('left','width')] if axis=='horizontal' else [('top','height')] if axis=='vertical' else [('left','width'),('top','height')]):
                if abs(box[position]+box[size]/2-container[position]-container[size]/2)>tolerance:
                    errors.append(eid+': 实际对象没有相对指定容器居中')
    return errors


def check_components(page, actual_boxes):
    """Check native group bounds and peer geometry; optical baselines need rendering."""
    errors=[]
    for group in page.get('component_groups',[]):
        values=[actual_boxes.get(eid) for eid in group.get('element_ids',[])]
        if not values or any(box is None for box in values):
            errors.append('组合 '+str(group.get('id'))+': 成员缺失');continue
        left=min(b['left'] for b in values);top=min(b['top'] for b in values)
        union={'left':left,'top':top,'width':max(b['left']+b['width'] for b in values)-left,'height':max(b['top']+b['height'] for b in values)-top}
        container=group.get('container_box');axis=group.get('center_axis')
        if axis:
            errors.extend(check_alignment({'alignment_constraints':[{'axis':axis,'container_box':container,'element_ids':[group['id']]}]},{group['id']:union}))
    for rule in page.get('component_constraints',[]):
        boxes=[actual_boxes.get(eid) for eid in rule.get('element_ids',[])]
        if len(boxes)<2 or any(b is None for b in boxes):errors.append('跨组件约束成员不足/缺失');continue
        kind=rule.get('kind')
        if kind in {'equal-width','equal-height','common-top','common-bottom','common-center-y'}:
            values=[b['width'] if kind=='equal-width' else b['height'] if kind=='equal-height' else b['top'] if kind=='common-top' else b['top']+b['height'] if kind=='common-bottom' else b['top']+b['height']/2 for b in boxes]
        elif kind=='equal-horizontal-gap':
            boxes=sorted(boxes,key=lambda b:b['left']);values=[b['left']-a['left']-a['width'] for a,b in zip(boxes,boxes[1:])]
            if any(v<0 for v in values):errors.append('跨组件水平间距出现重叠')
        else:errors.append('未知跨组件约束');continue
        if max(values)-min(values)>3:errors.append(kind+': 实际跨组件几何不一致')
    return errors
