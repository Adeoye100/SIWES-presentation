from pathlib import Path

path = Path('index.html')
html = path.read_text(encoding='utf-8')

replacements = {
    "  .workflow-desc { font-size: 16px; color: rgba(255,255,255,0.85); line-height: 1.8; max-width: 380px; margin-bottom: 36px; font-weight: 400; }":
    "  .workflow-desc { font-size: 16px; color: var(--text-muted); line-height: 1.8; max-width: 380px; margin-bottom: 36px; font-weight: 400; }",
    "  .workflow-method { padding: 18px 0; border-bottom: 1px solid rgba(255,255,255,0.12); display: flex; flex-direction: row; gap: 16px; align-items: center; justify-content: space-between; }":
    "  .workflow-method { padding: 18px 0; border-bottom: 1px solid var(--border-color); display: flex; flex-direction: row; gap: 16px; align-items: center; justify-content: space-between; }",
    "  .kanban-label { font-size: 11px; letter-spacing: 0.15em; text-transform: uppercase; color: rgba(255,255,255,0.6); margin-bottom: 12px; font-family: 'Poppins', sans-serif; font-weight: 600; }":
    "  .kanban-label { font-size: 11px; letter-spacing: 0.15em; text-transform: uppercase; color: var(--text-muted); margin-bottom: 12px; font-family: 'Poppins', sans-serif; font-weight: 600; }",
    "  .kanban-card { background: rgba(255,255,255,0.08); border: 1px solid rgba(255,255,255,0.12); padding: 12px 14px; font-size: 13px; color: rgba(255,255,255,0.85); line-height: 1.5; border-radius: 4px; }":
    "  .kanban-card { background: var(--active-bg); border: 1px solid var(--border-color); padding: 12px 14px; font-size: 13px; color: var(--text-primary); line-height: 1.5; border-radius: 4px; }",
    "  .detail-label { font-size: 12px; letter-spacing: 0.15em; color: rgba(255,255,255,0.6); text-transform: uppercase; font-weight: 600; }":
    "  .detail-label { font-size: 12px; letter-spacing: 0.15em; color: var(--text-muted); text-transform: uppercase; font-weight: 600; }",
    "  .acc-item { border-bottom: 1px solid rgba(255,255,255,0.06); padding-bottom: 12px; }":
    "  .acc-item { border-bottom: 1px solid var(--border-color); padding-bottom: 12px; }",
    "  --card-bg: #050505;\n  --card-hover: rgba(255, 255, 255, 0.03);\n  --line: rgba(255, 255, 255, 0.14);\n  --surface: #000000;\n  --head-solid: #ffffff;\n  --sub: rgba(255, 255, 255, 0.55);\n\n  --accent: #ffffff;\n  --accent-hover: #e0e0e0;\n  --accent-subtle: rgba(255, 255, 255, 0.08);":
    "  --card-bg: var(--surface-elevated);\n  --card-hover: var(--hover-bg);\n  --line: var(--border-color);\n  --surface: var(--bg-color);\n  --head-solid: var(--text-primary);\n  --sub: var(--text-muted);\n\n  --accent: var(--text-primary);\n  --accent-hover: var(--text-muted);\n  --accent-subtle: var(--active-bg);",
}

for old, new in replacements.items():
    if old not in html:
        raise SystemExit('Expected theme consistency anchor not found:\n' + old[:120])
    html = html.replace(old, new, 1)

# Make focus indicators visible in either theme without touching QR/media whites.
html = html.replace('outline: 2px solid #ffffff;', 'outline: 2px solid var(--text-primary);')

# The project-image hover overlay must stay dark in light mode so its white label remains legible.
light_media_anchor = ''':root[data-theme="light"] .gal-caption,
:root[data-theme="light"] .project-media-overlay,
:root[data-theme="light"] .project-gallery-stage .gal-caption {
  color: #ffffff !important;
}
'''
light_media_replacement = ''':root[data-theme="light"] .gal-caption,
:root[data-theme="light"] .project-media-overlay,
:root[data-theme="light"] .project-gallery-stage .gal-caption {
  color: #ffffff !important;
}
:root[data-theme="light"] .project-media-overlay {
  background: rgba(0, 0, 0, 0.72) !important;
}
'''
if light_media_anchor not in html:
    raise SystemExit('Light media overlay anchor not found')
html = html.replace(light_media_anchor, light_media_replacement, 1)

# Theme the small workflow diagram strokes/bars through currentColor in light mode.
workflow_light = '''
:root[data-theme="light"] #panel-workflow svg circle:first-child {
  stroke: rgba(17, 17, 17, 0.18) !important;
}
:root[data-theme="light"] #panel-workflow svg .pie-progress {
  stroke: rgba(17, 17, 17, 0.82) !important;
}
:root[data-theme="light"] #panel-workflow .kb-bar {
  background: var(--text-primary) !important;
}
'''
anchor = '/* Media caption zones intentionally stay dark so photographs/screenshots remain readable. */'
if workflow_light.strip() not in html:
    html = html.replace(anchor, workflow_light + '\n' + anchor, 1)

# Normalize whitespace so the production diff passes git diff --check.
html = '\n'.join(line.rstrip() for line in html.splitlines()) + '\n'
path.write_text(html, encoding='utf-8')

required = [
    '--card-bg: var(--surface-elevated);',
    '.workflow-desc { font-size: 16px; color: var(--text-muted);',
    '.kanban-card { background: var(--active-bg);',
    ':root[data-theme="light"] .project-media-overlay {',
    "localStorage.setItem(THEME_STORAGE_KEY",
]
for needle in required:
    if needle not in html:
        raise SystemExit('Post-patch verification failed: ' + needle)

print('Theme consistency refinements applied')
