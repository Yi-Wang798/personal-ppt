"""Measured geometry and master/inventory contracts. No generation or image editing."""
import argparse
import hashlib
import json
import math
import sys
import zipfile
import base64
import html
import struct
from pathlib import Path


def number(value):
    return isinstance(value, (int,float)) and not isinstance(value,bool) and math.isfinite(value)


def box_values(box):
    if not isinstance(box,dict):
        return None
    values=[box.get(k) for k in ("left","top","width","height")]
    return values if all(number(v) for v in values) else None


def map_box(reference_size, frame, source_box):
    width,height=reference_size.get("width"),reference_size.get("height")
    f,b=box_values(frame),box_values(source_box)
    if not all(number(v) and v>0 for v in (width,height)) or f is None or b is None:
        raise ValueError("真实像素尺寸、frame 和 reference_box 必须是有限数值")
    x,y,w,h=f
    if w<=0 or h<=0 or b[0]<0 or b[1]<0 or b[2]<0 or b[3]<0 or b[0]+b[2]>width+.1 or b[1]+b[3]>height+.1:
        raise ValueError("参考区域越界或 frame 尺寸无效")
    sx,sy=w/width,h/height
    if abs(sx-sy)>max(sx,sy)*.001:
        raise ValueError("底图必须等比映射，不能横纵独立拉伸")
    return dict(zip(("left","top","width","height"),(x+b[0]*sx,y+b[1]*sx,b[2]*sx,b[3]*sx)))


def check_contract(spec,base,stage="production"):
    base=Path(base)
    errors=[]
    if spec.get("reconstruction_policy")=="skip-explicit":
        return [] if isinstance(spec.get("reconstruction_skip_request"),str) and spec["reconstruction_skip_request"].strip() else ["跳过母版重建需用户明确要求原话"]
    master=spec.get("master",{})
    if not isinstance(master,dict):master={}
    reference=master.get("reference_image")
    digest=None
    if not isinstance(reference,str) or not reference.strip() or not (base/reference).is_file():
        errors.append("缺少母版设计图")
    else:
        data=(base/reference).read_bytes()
        digest=hashlib.sha256(data).hexdigest()
        if master.get("image_sha256")!=digest:errors.append("母版设计图哈希不一致")
        if data.startswith(b"\x89PNG\r\n\x1a\n") and len(data)>=24:
            size=struct.unpack(">II",data[16:24])
            declared=master.get("reference_size",{})
            if not isinstance(declared,dict) or size!=(declared.get("width"),declared.get("height")):
                errors.append("母版 reference_size 与实际 PNG 尺寸不一致")
    approval=master.get("approval",{})
    if not isinstance(approval,dict):approval={}
    if approval.get("confirmed") is not True or not isinstance(approval.get("user_selection"),str) or not approval["user_selection"].strip():
        errors.append("母版未收到作者明确选择确认，不能制作分页")
    if digest and approval.get("reference_sha256")!=digest:
        errors.append("作者确认记录与当前母版图不一致，需重新确认")
    tokens=master.get("tokens",{})
    if not isinstance(tokens,dict):tokens={}
    fonts=tokens.get("fonts",{})
    if fonts!={"zh":"Microsoft YaHei","en":"Times New Roman"}:
        errors.append("母版须明确中文微软雅黑、英文 Times New Roman")
    text_styles=tokens.get("text_styles",{})
    if not isinstance(text_styles,dict) or not text_styles:
        errors.append("母版缺少统一文字层级/字号")
        text_styles={}
    for role,value in text_styles.items():
        if not isinstance(value,dict) or not number(value.get("font_size_pt")) or value["font_size_pt"]<=0:
            errors.append(f"母版文字角色 {role} 字号无效")
    if stage=="pagination":return errors
    template=master.get("ppt_template_path")
    if not isinstance(template,str) or not template.strip() or not (base/template).is_file():
        errors.append("必须先建立并保存原生 PPT 母版")
    else:
        try:
            with zipfile.ZipFile(base/template) as package:
                if not any(p.startswith("ppt/slideMasters/") and p.endswith(".xml") for p in package.namelist()):
                    errors.append("母版 PPT 缺少原生 slideMaster")
        except (zipfile.BadZipFile,OSError):errors.append("母版 PPT 不是可读取的 PPTX")
    tolerance=3
    for page in spec.get("slides",[]):
        if not isinstance(page,dict):continue
        sid=page.get("id","unknown")
        page_reference=page.get("design_reference")
        if isinstance(page_reference,str) and (base/page_reference).is_file():
            data=(base/page_reference).read_bytes()
            if data.startswith(b"\x89PNG\r\n\x1a\n") and len(data)>=24:
                declared=page.get("reference_size",{})
                if not isinstance(declared,dict) or struct.unpack(">II",data[16:24])!=(declared.get("width"),declared.get("height")):
                    errors.append(f"{sid} reference_size 与实际 PNG 尺寸不一致")
        generation=page.get("design_generation",{})
        if not isinstance(generation,dict) or generation.get("master_sha256")!=digest or not digest:
            errors.append(f"{sid} 生图未记录所选母版引用")
        elements={e.get("id"):e for e in page.get("elements",[]) if isinstance(e,dict)}
        adjusted_elements={}
        if spec.get('workflow_version') in {'1.6','1.7'} and page.get('adaptations'):
            import adaptive_layout
            measurement_path=base/'design/reference-measurements.json'
            if measurement_path.is_file():
                measurements=json.loads(measurement_path.read_text(encoding='utf-8-sig'))
                source=next((p for p in measurements.get('slides',[]) if p.get('id')==sid),{})
                adjusted,adjustment_errors=adaptive_layout.effective(source,page,spec['canvas'])
                errors.extend(adjustment_errors)
                adjusted_elements={e['id']:e for e in adjusted.get('elements',[])}
        inventory=page.get("reference_inventory",[])
        if not isinstance(inventory,list) or not inventory:
            errors.append(f"{sid} 缺少原图元素完整清单")
            inventory=[]
        covered=set()
        inventory_ids=set()
        for item in inventory:
            if not isinstance(item,dict):
                errors.append(f"{sid} 清单项无效");continue
            iid=item.get("id")
            if not isinstance(iid,str) or not iid or iid in inventory_ids:
                errors.append(f"{sid} 清单 id 缺失或重复")
            inventory_ids.add(str(iid))
            if item.get("route") not in {"native","generated-image","source-image","master-element"}:
                errors.append(f"{sid}/{iid} 没有明确重建路线")
            refs=item.get("element_ids",[])
            if not isinstance(refs,list) or not refs:
                errors.append(f"{sid}/{iid} 元素未落实到成品对象");continue
            for eid in refs:
                if eid not in elements:errors.append(f"{sid}/{iid} 对应元素 {eid} 已丢失")
                else:covered.add(eid)
            if not box_values(item.get("reference_box")):
                errors.append(f"{sid}/{iid} 清单缺少原图位置测量")
        for eid,e in elements.items():
            if eid not in covered:errors.append(f"{sid}/{eid} 没有进入原图清单")
            try:
                mapped=map_box(page.get("reference_size",{}),page.get("image_frame",{}),e.get("reference_box",{}))
                if eid in adjusted_elements:mapped=adjusted_elements[eid]['box']
                actual=box_values(e.get("box"))
                if actual is None or any(abs(mapped[k]-actual[i])>tolerance for i,k in enumerate(("left","top","width","height"))):
                    errors.append(f"{sid}/{eid} 位置/大小偏离原图测量")
            except (ValueError,AttributeError,TypeError):errors.append(f"{sid}/{eid} 缺少有效的等比原图坐标映射")
            if e.get("kind")=="text":
                role=e.get("master_slot")
                style=text_styles.get(role)
                if not isinstance(style,dict):errors.append(f"{sid}/{eid} 未关联母版文字角色")
                else:
                    if e.get("font_size_pt")!=style.get("font_size_pt"):errors.append(f"{sid}/{eid} 字号与母版不一致")
                    for key in ("bold","alignment"):
                        if key in style and not e.get("runs") and e.get(key)!=style[key]:errors.append(f"{sid}/{eid} {key} 与母版不一致")
    return errors


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    subs=parser.add_subparsers(dest="command",required=True)
    check=subs.add_parser("check");check.add_argument("--spec",required=True)
    check.add_argument("--stage",choices=["pagination","sample","production"],default="production")
    delivery=subs.add_parser("delivery")
    delivery.add_argument("--spec",required=True);delivery.add_argument("--pptx",required=True);delivery.add_argument("--review",required=True)
    mapping=subs.add_parser("map")
    mapping.add_argument("--reference-width",type=float,required=True);mapping.add_argument("--reference-height",type=float,required=True)
    mapping.add_argument("--frame",nargs=4,type=float,required=True);mapping.add_argument("--box",nargs=4,type=float,required=True)
    compare=subs.add_parser("compare")
    compare.add_argument("--reference",required=True);compare.add_argument("--render",required=True);compare.add_argument("--out",required=True)
    compare.add_argument("--canvas",nargs=2,type=float,default=[1280,720]);compare.add_argument("--frame",nargs=4,type=float)
    args=parser.parse_args()
    try:
        if args.command=="check":
            file=Path(args.spec).resolve();spec=json.loads(file.read_text(encoding="utf-8-sig"))
            errors=check_contract(spec,file.parent,args.stage)
            if spec.get("workflow_version") in {"1.5","1.6","1.7"} and args.stage!="pagination" and spec.get("reconstruction_policy")!="skip-explicit":
                import fidelity_tools
                errors.extend(fidelity_tools.check_measurements(spec,file.parent))
                if args.stage=="production":errors.extend(fidelity_tools.check_sample(spec,file.parent))
            result={"status":"fail" if errors else "pass","errors":errors,"limits":"检查声明和几何关系；不能认证用户选择、清单覆盖率或实际生图，需真实工具/聊天证据与逐区域视觉检查"}
        elif args.command=="delivery":
            import fidelity_tools
            file=Path(args.spec).resolve();spec=json.loads(file.read_text(encoding="utf-8-sig"))
            result=fidelity_tools.delivery(spec,file.parent,Path(args.pptx).resolve(),Path(args.review).resolve())
        elif args.command=="map":
            keys=("left","top","width","height")
            result={"status":"pass","box":map_box({"width":args.reference_width,"height":args.reference_height},dict(zip(keys,args.frame)),dict(zip(keys,args.box)))}
        else:
            output=Path(args.out).resolve()
            if output.exists():raise ValueError("对照文件必须使用新名字")
            paths=[Path(args.reference).resolve(),Path(args.render).resolve()]
            if output in paths:raise ValueError("对照文件不能覆盖图片")
            def image_uri(file):
                data=file.read_bytes()
                if data.startswith(b"\x89PNG\r\n\x1a\n"):mime="image/png"
                elif data.startswith(b"\xff\xd8\xff"):mime="image/jpeg"
                elif data.startswith(b"RIFF") and data[8:12]==b"WEBP":mime="image/webp"
                else:raise ValueError("只接受真实 PNG/JPEG/WebP 图片")
                return "data:"+mime+";base64,"+base64.b64encode(data).decode("ascii")
            reference,render=map(image_uri,paths)
            width,height=args.canvas
            if not all(number(v) and v>0 for v in (width,height)):raise ValueError("canvas 无效")
            x,y,w,h=args.frame or [0,0,width,height]
            if not all(number(v) for v in (x,y,w,h)) or w<=0 or h<=0:raise ValueError("frame 无效")
            placement=f"left:{x/width*100}%;top:{y/height*100}%;width:{w/width*100}%;height:{h/height*100}%;"
            page=f'''<!doctype html><meta charset="utf-8"><title>设计图与 PPT 对照</title>
<style>body{{font:16px 'Microsoft YaHei',sans-serif;background:#eef0f2;color:#20242a;margin:24px}}.row{{display:flex;gap:16px}}.pane{{flex:1;min-width:0}}.stage{{position:relative;aspect-ratio:{width}/{height};background:white;overflow:hidden}}img{{position:absolute;width:100%;height:100%;object-fit:contain;inset:0}}.ref{{inset:auto;{placement}}}label{{display:block;margin:16px 0}}input{{width:min(600px,80vw)}}</style>
<h1>设计图 / 清洁 PPT 渲染</h1><p>仅用于真实视觉核对，不自动认证还原度。滑块控制 PPT 渲染透明度。</p>
<div class="row"><div class="pane"><h2>参考设计</h2><div class="stage"><img class="ref" src="{reference}"></div></div><div class="pane"><h2>原生 PPT</h2><div class="stage"><img src="{render}"></div></div></div>
<label>PPT 叠图透明度 <input type="range" min="0" max="100" value="50" oninput="document.getElementById('overlay').style.opacity=this.value/100"></label>
<div class="stage"><img class="ref" src="{reference}"><img id="overlay" style="opacity:.5" src="{render}"></div>
<p>参考：{html.escape(str(paths[0]))}<br>渲染：{html.escape(str(paths[1]))}</p>'''
            output.parent.mkdir(parents=True,exist_ok=True)
            output.write_text(page,encoding="utf-8")
            result={"status":"pass","path":str(output),"note":"只显示两幅真实图像及交互叠图，未修改图片或给出视觉通过结论"}
        print(json.dumps(result,ensure_ascii=False,indent=2));return 2 if result["status"]=="fail" else 0
    except (OSError,ValueError,TypeError,KeyError) as error:
        print(json.dumps({"status":"fail","error":str(error)},ensure_ascii=False));return 2


if __name__=="__main__":sys.exit(main())
