"""Read-only regional color sampling with image hashes; never edit the input image."""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path


def sample(path, region, role):
    from PIL import Image
    with Image.open(path) as source:
        x,y,w,h=region
        if x<0 or y<0 or w<2 or h<2 or x+w>source.width or y+h>source.height:
            raise ValueError('取样区域须为图内至少 2×2 像素，不能用单个抗锯齿边缘像素')
        pixels=list(source.convert('RGBA').crop((x,y,x+w,y+h)).getdata())
    # Dominant exact RGB avoids creating a color absent from the source.
    opaque=[p[:3] for p in pixels if p[3]>=250]
    if not opaque:raise ValueError('区域无足够不透明像素；半透明/渐变需另记录背景和透明度')
    color,count=Counter(opaque).most_common(1)[0]
    ratio=count/len(opaque)
    return {'image_sha256':hashlib.sha256(Path(path).read_bytes()).hexdigest(),
            'image_path':str(Path(path).resolve()),'region':dict(zip(('left','top','width','height'),region)),
            'role':role,'method':'dominant-opaque-rgb','rgb':list(color),
            'hex':'#'+''.join(f'{v:02X}' for v in color),'dominant_fraction':round(ratio,4),
            'status':'sampled' if ratio>=.6 else 'needs-region-review',
            'note':'低占比可能为渐变、文字边缘或复杂背景，不自动将采样结果当作单一填色'}


def verify(spec,base):
    errors=[]
    filename=Path(base)/'design/color-samples.json'
    if not filename.is_file():return ['缺少参考图颜色区域取样记录']
    data=json.loads(filename.read_text(encoding='utf-8-sig'))
    roles=spec.get('master',{}).get('tokens',{}).get('color_roles',{})
    samples=data.get('samples',[])
    frozen=[Path(base)/p['design_reference'] for p in spec.get('slides',[]) if p.get('design_reference')]
    mother=spec.get('master',{}).get('reference_image')
    if mother:frozen.append(Path(base)/mother)
    registry=Path(base)/'design/reference-registry.json'
    if registry.is_file():
        frozen.extend(Path(base)/r['path'] for r in json.loads(registry.read_text(encoding='utf-8-sig')).get('slides',{}).values())
    hashes={hashlib.sha256(p.read_bytes()).hexdigest() for p in frozen if p.is_file()}
    known=set()
    for record in samples:
        role=record.get('role');known.add(role)
        path=Path(base)/record.get('image_path','')
        if not path.is_file() or record.get('image_sha256') not in hashes:
            errors.append(str(role)+': 取色来源不是当前参考图');continue
        region=record.get('region',{})
        current=sample(path,[region[k] for k in ('left','top','width','height')],role)
        if current['image_sha256']!=record.get('image_sha256') or current['hex']!=record.get('hex'):
            errors.append(str(role)+': 取色文件/结果过期')
        if current['status']!='sampled':errors.append(str(role)+': 该区域不能视为单一纯色')
        if roles.get(role)!=current['hex']:errors.append(str(role)+': 母版颜色角色未采用参考区域取样值')
    if not samples:errors.append('颜色取样清单为空')
    for role in roles:
        if role not in known:errors.append(role+': 母版颜色角色无取样来源')
    for page in spec.get('slides',[]):
        for element in page.get('elements',[]):
            for run in element.get('runs',[]):
                role=run.get('color_role')
                if role not in roles or run.get('color')!=roles.get(role):
                    errors.append(f"{page['id']}/{element['id']}: 文字颜色未引用已取样母版角色")
            style=element.get('visual_style',{})
            for field in ('fill','stroke'):
                if field in style:
                    role=style.get(field+'_role')
                    if role not in roles or style[field]!=roles.get(role):
                        errors.append(f"{page['id']}/{element['id']}: {field} 未引用已取样母版角色")
    return errors


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    sub=parser.add_subparsers(dest='command',required=True)
    s=sub.add_parser('sample');s.add_argument('--image',required=True);s.add_argument('--region',nargs=4,type=int,required=True);s.add_argument('--role',required=True);s.add_argument('--out',required=True)
    v=sub.add_parser('check');v.add_argument('--spec',required=True)
    args=parser.parse_args()
    try:
        if args.command=='sample':
            output=Path(args.out).resolve()
            if output.exists():raise ValueError('取色结果使用新名字，不能覆盖既有记录')
            result=sample(Path(args.image).resolve(),args.region,args.role)
            output.parent.mkdir(parents=True,exist_ok=True);output.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
        else:
            path=Path(args.spec).resolve();errors=verify(json.loads(path.read_text(encoding='utf-8-sig')),path.parent)
            result={'status':'fail' if errors else 'pass','errors':errors}
        print(json.dumps(result,ensure_ascii=False,indent=2));return 2 if result['status'] in {'fail','needs-region-review'} else 0
    except (OSError,ValueError,KeyError,TypeError,ImportError) as error:
        print(json.dumps({'status':'fail','error':str(error)},ensure_ascii=False));return 2


if __name__=='__main__':raise SystemExit(main())
