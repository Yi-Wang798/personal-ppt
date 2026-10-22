"""Freeze measured slide instructions and detect drift; no raster-to-vector conversion."""
import argparse
import hashlib
import json
from pathlib import Path


def snapshot(spec):
    keys = ("canvas", "style", "master", "sources", "narrative_mode", "layout_catalog", "slides")
    if spec.get("workflow_version") in {"2.0", "2.1"}:
        keys += ("task_profile", "audience", "purpose", "density", "interaction", "mode")
    return {key: spec.get(key) for key in keys}


def digest(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True,
                                    separators=(",", ":"), allow_nan=False).encode()).hexdigest()


def check_lock(spec, base):
    errors = []
    lock_path = base / "build" / "design-lock.json"
    if not lock_path.is_file():
        return ["缺少 build/design-lock.json；先测量确认设计稿，再执行 freeze"]
    lock = json.loads(lock_path.read_text(encoding="utf-8"))
    locked = lock.get("design")
    if lock.get("sha256") != digest(locked):
        errors.append("设计锁自身哈希无效")
    if locked != snapshot(spec):
        errors.append("设计稿已变化；同步预览与构建源、重新校准后显式刷新设计锁")
    for page in spec.get("slides", []):
        if page.get("page_rhythm") not in {"anchor", "dense", "breathing"}:
            errors.append(f"{page.get('id')}: 缺少有效 page_rhythm")
        if not page.get("layout_family"):
            errors.append(f"{page.get('id')}: 缺少 layout_family")
        for element in page.get("elements", []):
            if not isinstance(element.get("box"), dict):
                errors.append(f"{page.get('id')}/{element.get('id')}: 缺少已测量 box")
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("freeze", "check"))
    parser.add_argument("--spec", required=True)
    parser.add_argument("--replace", action="store_true", help="Explicitly replace an existing lock after recalibration")
    args = parser.parse_args()
    source = Path(args.spec).resolve()
    spec = json.loads(source.read_text(encoding="utf-8"))
    lock_path = source.parent / "build" / "design-lock.json"
    if args.command == "freeze":
        if lock_path.exists() and not args.replace:
            parser.error("设计锁已存在；已完成重新校准时才使用 --replace")
        design = snapshot(spec)
        lock_path.parent.mkdir(parents=True, exist_ok=True)
        lock_path.write_text(json.dumps({"schema_version": 1, "sha256": digest(design),
                                        "design": design}, ensure_ascii=False, indent=2), encoding="utf-8")
    errors = check_lock(spec, source.parent)
    print(json.dumps({"status": "fail" if errors else "pass", "errors": errors,
                      "lock": str(lock_path), "limits": "检查设计合同与漂移，不证明已生图、视觉还原或构建源确实读取合同"}, ensure_ascii=False))
    return bool(errors)


if __name__ == "__main__":
    raise SystemExit(main())
