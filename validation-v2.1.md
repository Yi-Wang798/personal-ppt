# 2.1 validation

2026-10-22. 45 regression tests passed: 27 existing workflow checks and 18 native-bridge tests.

The added tests cover actual upstream native geometry conversion, editable freeform/preset/group objects, attached connectors, mixed-language fonts and bold text, native charts with embedded workbook data, original transparent PNG bytes, a shared native slide master, template-only export, inherited text roles, scene isolation, asset changes, aspect ratios, registered layers, active SVG rejection, and output overwrite protection.

A synthetic two-slide PPTX was exported and imported for rendering with the installed Presentations artifact-tool. Both pages rendered and were visually reviewed. The chart axis IDs were normalized to positive values to support this reader. The fixture contains only demonstration values and simple technical assets. It was not generated with imagegen and is not evidence of a completed end-to-end image-to-PPT task.

Run tests with a Python environment containing python-pptx, Pillow, and lxml:

```shell
python -m unittest discover -s tests -p "test*.py"
```

Public native_bridge commands retain the existing workflow preflight. Low-level synthetic tests exercise the conversion boundary directly and do not assert user approval, real generation receipts, or visual fidelity for arbitrary production decks. Animations, formula conversion, complex SVG effects, and all Office presets have not been validated.
