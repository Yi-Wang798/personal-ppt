"""Versioned interaction policy. Selection by an agent never counts as user approval."""


def is_v2(spec):
    return spec.get("workflow_version") == "2.0"


def needs_user_review(spec):
    return not is_v2(spec) or spec.get("interaction") == "review"


def check_master_selection(spec, reference_sha256):
    approval = spec.get("master", {}).get("approval", {})
    if not isinstance(approval, dict):
        return ["母版选择记录无效"]
    errors = []
    if needs_user_review(spec):
        if approval.get("confirmed") is not True or not isinstance(approval.get("user_selection"), str) or not approval["user_selection"].strip():
            errors.append("当前模式需要用户明确选择母版")
    else:
        by = approval.get("selected_by")
        if by == "user":
            if approval.get("confirmed") is not True or not approval.get("user_selection"):
                errors.append("用户选择必须保存真实回复")
        elif by == "agent":
            if approval.get("confirmed") is not False or approval.get("user_selection"):
                errors.append("自主选型不能记录成用户确认")
            if not approval.get("selection_reason"):
                errors.append("自主选择母版需记录与任务有关的理由")
        else:
            errors.append("自动模式需明确母版 selected_by=agent 或 user")
    if reference_sha256 and approval.get("reference_sha256") != reference_sha256:
        errors.append("母版选择记录与当前设计图不一致")
    return errors


def check_task(spec):
    if not is_v2(spec):
        return []
    errors = []
    profile = spec.get("task_profile", {})
    if not isinstance(profile, dict):
        return ["task_profile 必须为对象"]
    for key in ("scenario", "objective", "delivery_context"):
        if not isinstance(profile.get(key), str) or not profile[key].strip():
            errors.append("task_profile 缺少 " + key)
    if profile.get("delivery_context") not in {"live", "standalone", "mixed"}:
        errors.append("delivery_context 使用 live/standalone/mixed")
    if spec.get("mode") != "per-slide":
        errors.append("2.0 保持 per-slide：每页先生成并显示设计图，再重建")
    return errors
