"""Review visible slide copy before image generation; never rewrite scientific facts."""
import argparse
import hashlib
import json
import re
from pathlib import Path


def content_snapshot(spec):
    pages = [{'id':page['id'],'title':page.get('title'),'elements':[
        {k:e[k] for k in ('id','kind','text','label','rows','categories','series','unit','text_channel','content_role','claim_type','semantic_lines','editorial_exception','source_ids') if k in e}
        for e in page.get('elements',[])]} for page in spec.get('slides',[])]
    if spec.get('workflow_version') in {'2.0','2.1'}:
        context = {key: spec.get(key) for key in ('task_profile','audience','purpose','density','language')}
        for page in pages:
            page['context'] = context
    return pages


def hash_value(value):
    return hashlib.sha256(json.dumps(value,ensure_ascii=False,sort_keys=True,
                                    separators=(',',':'),allow_nan=False).encode()).hexdigest()


def digest(spec):
    return hash_value(content_snapshot(spec))


def page_digests(spec):
    return {p['id']:hash_value(p) for p in content_snapshot(spec)}


def audit(spec):
    errors=[];warnings=[]
    from workflow_policy import is_v2
    v2 = is_v2(spec)
    production=re.compile(r'待核对|待补充|本次生成|制作备注|制作记录|重绘限制|资料未提供|定义与计算公式待')
    wrapper=re.compile(r'当前解释[：:]|希望这对|为了让.*(?:页面|版面)|保留完整来源与成像记录')
    for page in spec.get('slides',[]):
        items={e['id']:e for e in page.get('elements',[])}
        for e in items.values():
            if e.get('kind')!='text':
                if v2:
                    values = [e.get('label', ''), *e.get('categories', [])]
                    values.extend(cell for row in e.get('rows', []) for cell in row)
                    values.extend(s.get('name', '') for s in e.get('series', []))
                    if any(isinstance(value, str) and production.search(value) for value in values):
                        exception = e.get('editorial_exception', {})
                        if e.get('content_role') != 'reader-condition' or not exception.get('reason') or not e.get('source_ids'):
                            errors.append(f"{page['id']}/{e['id']}: 标签或表格混入制作记录")
                    if any(e.get(key) for key in ('label','rows','categories','series')) and e.get('text_channel', 'slide-body') != 'slide-body':
                        errors.append(f"{page['id']}/{e['id']}: 非正文文字不能进入可见结构")
                continue
            label=f"{page['id']}/{e['id']}";text=e.get('text','')
            if e.get('text_channel')!='slide-body':errors.append(label+': 可见文本未分类为页面正文，演讲备注/制作记录不能混入')
            if e.get('content_role') not in {'research','reader-condition','navigation','caption','citation'}:
                errors.append(label+': 缺少正文用途分类')
            if production.search(text):
                exception=e.get('editorial_exception',{})
                if e.get('content_role')!='reader-condition' or not exception.get('reason') or not e.get('source_ids'):
                    errors.append(label+': 制作过程/待办文字混入正文')
            if wrapper.search(text):
                exception=e.get('editorial_exception',{})
                if not exception.get('reason'):
                    (warnings if v2 else errors).append(label+': 存在编辑口吻或重复表述，结合本页用途复读')
            if not v2 and e.get('claim_type')=='inference' and not re.search('可能|提示|推测|或与|或许',text):
                errors.append(label+': 推测文字缺少相应限定，不能写成证实因果')
            lines=e.get('semantic_lines')
            if lines is not None:
                if not isinstance(lines,list) or not lines or any(not isinstance(line,str) or not line for line in lines) or ''.join(lines)!=text.replace('\n',''):
                    errors.append(label+': 语义行与定稿文字不一致')
                elif any(line[0] in '，。；：、！？)]）】' or line[-1] in '([{（【' for line in lines):
                    errors.append(label+': 换行将标点/括号孤立')
                elif e.get('line_breaks') or '\n' in text:
                    offsets=[];count=0
                    for line in lines[:-1]:count+=len(line);offsets.append(count)
                    if e.get('line_breaks')!=offsets:errors.append(label+': 人工硬换行未采用语义行计划')
            if '\n' in text and not lines:errors.append(label+': 人工硬换行未登记语义行计划')
        for group in page.get('editorial_groups',[]):
            texts=[re.sub(r'\s+','',items[eid].get('text','')) for eid in group.get('element_ids',[]) if eid in items]
            if len(texts)!=len(group.get('element_ids',[])):errors.append(page['id']+': 文案组引用了不存在对象')
            if len([t for t in texts if t])!=len(set(t for t in texts if t)):
                errors.append(page['id']+': 同组件标题/副标题/正文存在重复文字')
        if not v2:
            warnings.append(page['id']+': 近义重复、科学含义和语义断行需人工复读及实际渲染确认')
    return errors,warnings


def check(spec,base,allow_subset=False):
    errors,_=audit(spec)
    path=Path(base)/'build/content-review.json'
    if not path.is_file():return errors+['缺少生图前独立文案审核记录']
    report=json.loads(path.read_text(encoding='utf-8-sig'))
    matches=report.get('content_sha256')==digest(spec)
    if allow_subset:matches=matches or all(report.get('page_sha256',{}).get(sid)==value for sid,value in page_digests(spec).items())
    if report.get('status')!='pass' or not matches:
        errors.append('文案审核未通过或定稿文字已改变')
    keys = ('channels_reviewed','facts_preserved','claim_strength_reviewed','redundancy_reviewed','semantic_wrap_reviewed') if spec.get('workflow_version') in {'2.0','2.1'} else ('channels_reviewed','scientific_details_preserved','redundancy_reviewed','semantic_wrap_reviewed')
    for key in keys:
        if report.get(key) is not True:errors.append('文案审核未完成 '+key)
    if not report.get('observations'):errors.append('文案审核没有具体修改/核对观察')
    return errors


def check_visible_copy(spec,pptx):
    """Find slide-local text added after the approved copy; inherited text needs render QA."""
    import zipfile,posixpath
    import xml.etree.ElementTree as ET
    import ppt_tools as ppt
    errors=[]
    with zipfile.ZipFile(pptx) as package:
        pres=ET.fromstring(package.read('ppt/presentation.xml'))
        rels={r.attrib['Id']:r.attrib['Target'] for r in ET.fromstring(package.read('ppt/_rels/presentation.xml.rels'))}
        for page,sid in zip(spec['slides'],pres.findall('p:sldIdLst/p:sldId',ppt.NS)):
            target=rels[sid.attrib['{'+ppt.NS['r']+'}id']]
            path=target.lstrip('/') if target.startswith('/') else posixpath.normpath('ppt/'+target)
            expected={f"pppt:{page['id']}:{e['id']}":e for e in page['elements']}
            root=ET.fromstring(package.read(path))
            for obj in root.findall('.//p:sp',ppt.NS):
                text=ppt.object_text(obj)
                if not text.strip():continue
                cn=obj.find('.//p:cNvPr',ppt.NS);name=cn.get('name') if cn is not None else None
                if name not in expected:errors.append(page['id']+': 实际 PPT 出现未列入定稿的文字 '+text[:60])
    return errors


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command',choices=['audit','check']);parser.add_argument('--spec',required=True)
    args=parser.parse_args()
    try:
        path=Path(args.spec).resolve();spec=json.loads(path.read_text(encoding='utf-8-sig'))
        errors,warnings=audit(spec) if args.command=='audit' else (check(spec,path.parent),[])
        print(json.dumps({'status':'fail' if errors else 'pass','errors':errors,'warnings':warnings,'content_sha256':digest(spec),'page_sha256':page_digests(spec),
                          'limits':'规则检查不自动改写文案、不证明科学内容核实或 Humanizer 已真实执行'},ensure_ascii=False,indent=2))
        return 2 if errors else 0
    except (OSError,ValueError,KeyError,TypeError) as error:
        print(json.dumps({'status':'fail','error':str(error)},ensure_ascii=False));return 2


if __name__=='__main__':raise SystemExit(main())
