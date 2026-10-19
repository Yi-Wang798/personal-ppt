# 2.0 validation / 2.0 验证说明

Verified on 2026-10-19. 27 regression tests passed.

- Task planning covers report, business, teaching, product, research, personal, and general scenarios without requiring research-only fields.
- Image-generation prompts retain visible text and numeric data while excluding speaker notes, production records, and internal purpose text.
- Automatic master selection and sample checks are distinct from user approval. Review mode and old projects retain user approval requirements.
- Real PPTX/OOXML fixtures check sample-file binding; missing and changed files remain errors.
- Microsoft YaHei, Times New Roman, per-slide image generation, and the existing visual reconstruction checks remain in place.
- Skill frontmatter and local Markdown links were checked. Source, installed cache, and the published files are compared during release.

Run the regression suite with a Python environment containing python-pptx and Pillow:

```shell
python tests/test_workflow_v2.py
```

These are synthetic regression fixtures, not completed presentations. This release has not been validated by generating, rendering, and reviewing six finished decks across all scenarios. It does not claim an AI-detector score or guaranteed first-pass perfection.

本次通过 27 项脚本回归，覆盖场景、文案分流、数值保留、确认逻辑、旧版兼容和实际 PPTX 文件检查。测试素材为合成夹具，没有冒充真实生图或用户验收。尚未完成六种场景成套生图、渲染和审阅，不将脚本通过等同于成品质量证明。
