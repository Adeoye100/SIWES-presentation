from pathlib import Path

path = Path("index.html")
html = path.read_text(encoding="utf-8")

if 'id="theme-toggle"' in html:
    raise SystemExit("Theme toggle already present; refusing to patch twice.")

# 1) Remove network-only font requests. The same fonts are already bundled locally.
google_fonts = '''<!-- Fonts: Google Fonts fallback preconnect -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap">

'''
if google_fonts not in html:
    raise SystemExit("Expected Google Fonts block not found")
html = html.replace(google_fonts, '<!-- Fonts are bundled locally for reliable offline presentation. -->\n\n', 1)

# 2) Apply the saved theme before paint to avoid a dark/light flash.
boot = '''<script>
(function () {
  try {
    var savedTheme = localStorage.getItem('siwes-theme');
    var theme = savedTheme === 'light' || savedTheme === 'dark' ? savedTheme : 'dark';
    document.documentElement.setAttribute('data-theme', theme);
    document.documentElement.style.colorScheme = theme;
  } catch (error) {
    document.documentElement.setAttribute('data-theme', 'dark');
    document.documentElement.style.colorScheme = 'dark';
  }
})();
</script>
'''
robots = '<meta name="robots" content="noindex">\n'
if robots not in html:
    raise SystemExit("robots meta anchor not found")
html = html.replace(robots, robots + boot + '\n', 1)

# 3) Extend the existing design tokens rather than creating section-specific themes.
old_root = ''':root {
  --bg-color: #000000;
  --text-primary: #FFFFFF;
  --text-muted: rgba(255, 255, 255, 0.55);
  --text-dim: rgba(255, 255, 255, 0.3);
  --border-color: rgba(255, 255, 255, 0.14);
  --border-bright: rgba(255, 255, 255, 0.4);
  --font-header: 'Clash Display', 'Poppins', system-ui, sans-serif;
  --font-body: 'Poppins', system-ui, sans-serif;
}
'''
new_root = ''':root {
  color-scheme: dark;
  --bg-color: #000000;
  --surface-elevated: #050505;
  --surface-deep: #080808;
  --surface-open: #090909;
  --surface-hover: #0a0a0a;
  --surface-overlay: rgba(0, 0, 0, 0.85);
  --nav-bg: rgba(0, 0, 0, 0.88);
  --modal-backdrop: rgba(0, 0, 0, 0.94);
  --hover-bg: rgba(255, 255, 255, 0.03);
  --hover-strong: rgba(255, 255, 255, 0.12);
  --active-bg: rgba(255, 255, 255, 0.08);
  --progress-track: rgba(255, 255, 255, 0.15);
  --grid-line: rgba(255, 255, 255, 0.03);
  --text-primary: #FFFFFF;
  --text-muted: rgba(255, 255, 255, 0.55);
  --text-dim: rgba(255, 255, 255, 0.3);
  --border-color: rgba(255, 255, 255, 0.14);
  --border-bright: rgba(255, 255, 255, 0.4);
  --font-header: 'Clash Display', 'Poppins', system-ui, sans-serif;
  --font-body: 'Poppins', system-ui, sans-serif;
}

:root[data-theme="light"] {
  color-scheme: light;
  --bg-color: #f5f3ee;
  --surface-elevated: #ffffff;
  --surface-deep: #ece8df;
  --surface-open: #e8e3d8;
  --surface-hover: #e3ded3;
  --surface-overlay: rgba(245, 243, 238, 0.94);
  --nav-bg: rgba(245, 243, 238, 0.96);
  --modal-backdrop: rgba(245, 243, 238, 0.96);
  --hover-bg: rgba(17, 17, 17, 0.045);
  --hover-strong: rgba(17, 17, 17, 0.11);
  --active-bg: rgba(17, 17, 17, 0.085);
  --progress-track: rgba(17, 17, 17, 0.18);
  --grid-line: rgba(17, 17, 17, 0.055);
  --text-primary: #111111;
  --text-muted: rgba(17, 17, 17, 0.72);
  --text-dim: rgba(17, 17, 17, 0.56);
  --border-color: rgba(17, 17, 17, 0.24);
  --border-bright: rgba(17, 17, 17, 0.52);
}
'''
if old_root not in html:
    raise SystemExit("Existing :root design token block not found")
html = html.replace(old_root, new_root, 1)

# 4) Move repeated black/white UI surfaces onto the global tokens.
replacements = {
    'background: #000000;': 'background: var(--bg-color);',
    'background: #000;': 'background: var(--bg-color);',
    'background: #050505;': 'background: var(--surface-elevated);',
    'background: #080808;': 'background: var(--surface-deep);',
    'background: #090909;': 'background: var(--surface-open);',
    'background: #0a0a0a;': 'background: var(--surface-hover);',
    'background: rgba(0, 0, 0, 0.85);': 'background: var(--surface-overlay);',
    'background: rgba(0,0,0,0.85);': 'background: var(--surface-overlay);',
    'background: rgba(0, 0, 0, 0.88);': 'background: var(--nav-bg);',
    'background: rgba(0, 0, 0, 0.94);': 'background: var(--modal-backdrop);',
    'background: rgba(255, 255, 255, 0.03);': 'background: var(--hover-bg);',
    'background: rgba(255, 255, 255, 0.12);': 'background: var(--hover-strong);',
    'background: rgba(255, 255, 255, 0.08);': 'background: var(--active-bg);',
    'background: rgba(255,255,255,0.15);': 'background: var(--progress-track);',
    'color: #ffffff;': 'color: var(--text-primary);',
    'color: #fff;': 'color: var(--text-primary);',
}
for old, new in replacements.items():
    html = html.replace(old, new)

# Active controls should remain an inverse pair in either theme.
html = html.replace(
    'background: #ffffff;\n  color: #000000;\n  border-color: #ffffff;',
    'background: var(--text-primary);\n  color: var(--bg-color);\n  border-color: var(--text-primary);'
)
html = html.replace(
    'border-color: #ffffff;\n  background: #ffffff;\n  color: #000000;',
    'border-color: var(--text-primary);\n  background: var(--text-primary);\n  color: var(--bg-color);'
)

# 5) Add a compact, offline-safe toggle and final light-theme bridge rules.
theme_css = r'''

/* ─── GLOBAL THEME TOGGLE / PROJECTION MODE ─────────────── */
.top-bar-actions {
  display: flex;
  align-items: center;
  gap: 8px;
}

.theme-toggle {
  min-height: 30px;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 6px 10px;
  border: 1px solid var(--border-color);
  background: var(--surface-overlay);
  color: var(--text-primary);
  font-family: var(--font-body);
  font-size: 9px;
  font-weight: 600;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  cursor: pointer;
  transition: background-color 160ms ease, border-color 160ms ease, color 160ms ease;
}

.theme-toggle:hover,
.theme-toggle:focus-visible {
  border-color: var(--border-bright);
  background: var(--hover-strong);
  outline: none;
}

.theme-toggle-glyph {
  width: 12px;
  height: 12px;
  border: 1px solid currentColor;
  position: relative;
  flex: 0 0 12px;
}
.theme-toggle-glyph::after {
  content: '';
  position: absolute;
  top: 2px;
  right: 2px;
  bottom: 2px;
  width: 3px;
  background: currentColor;
}
:root[data-theme="light"] .theme-toggle-glyph::after {
  left: 2px;
  right: auto;
}

html,
body,
#track-wrap,
.panel,
.eleya-card,
#bottom-nav,
.status-pill,
.qr-block,
.qr-modal-content,
.showcase-card,
.showcase-info,
.radial-card,
.accordion-item,
.project-card,
.kanban-col,
.gallery-modal-content,
.gallery-modal-backdrop,
.project-gallery-modal-overlay,
.project-gallery-shell {
  transition: background-color 160ms ease, color 160ms ease, border-color 160ms ease;
}

.grid-lines-overlay {
  background-image: linear-gradient(var(--grid-line) 1px, transparent 1px),
                    linear-gradient(90deg, var(--grid-line) 1px, transparent 1px) !important;
}

#progress-track { background: var(--progress-track) !important; }
#progress-bar { background: var(--text-primary) !important; }

:root[data-theme="light"] .panel,
:root[data-theme="light"] #track-wrap,
:root[data-theme="light"] #panel-gallery,
:root[data-theme="light"] #panel-workflow {
  background-color: var(--bg-color) !important;
  color: var(--text-primary);
}

:root[data-theme="light"] .eleya-card,
:root[data-theme="light"] .showcase-card,
:root[data-theme="light"] .showcase-info,
:root[data-theme="light"] .radial-card,
:root[data-theme="light"] .accordion-item,
:root[data-theme="light"] .project-card,
:root[data-theme="light"] .kanban-col,
:root[data-theme="light"] .qr-block,
:root[data-theme="light"] .qr-modal-content {
  background-color: var(--surface-elevated) !important;
  border-color: var(--border-color) !important;
}

:root[data-theme="light"] .accordion-item.is-open {
  background-color: var(--surface-open) !important;
}

:root[data-theme="light"] .section-title,
:root[data-theme="light"] .brand-mark,
:root[data-theme="light"] .showcase-title,
:root[data-theme="light"] .accordion-header,
:root[data-theme="light"] .acc-trigger,
:root[data-theme="light"] .detail-value,
:root[data-theme="light"] .nav-btn:hover,
:root[data-theme="light"] .nav-btn.active,
:root[data-theme="light"] .hero-logo-card:hover .hero-logo-label {
  color: var(--text-primary) !important;
}

:root[data-theme="light"] .growth-tab-btn.is-active,
:root[data-theme="light"] .btn-card-gallery:hover,
:root[data-theme="light"] .project-gallery-badge:hover {
  background: var(--text-primary) !important;
  border-color: var(--text-primary) !important;
  color: var(--bg-color) !important;
}

:root[data-theme="light"] .hero-backdrop img {
  opacity: 0.24;
  filter: grayscale(0.25) brightness(1.2) contrast(0.9);
}
:root[data-theme="light"] .hero-backdrop::after {
  background: linear-gradient(180deg, rgba(245,243,238,0.70) 0%, rgba(245,243,238,0.88) 100%);
}

/* Media caption zones intentionally stay dark so photographs/screenshots remain readable. */
:root[data-theme="light"] .gal-caption,
:root[data-theme="light"] .project-media-overlay,
:root[data-theme="light"] .project-gallery-stage .gal-caption {
  color: #ffffff !important;
}
:root[data-theme="light"] .gal-caption .gal-tag,
:root[data-theme="light"] .gal-caption .gal-desc,
:root[data-theme="light"] .project-gallery-stage .gal-tag,
:root[data-theme="light"] .project-gallery-stage .gal-desc {
  color: rgba(255,255,255,0.82) !important;
}

/* QR artwork remains pure black-on-white in both themes for scan reliability. */
.qr-box,
.qr-modal-img {
  background: #ffffff !important;
  color: #000000 !important;
}

@media (max-width: 760px) {
  .top-bar-actions { gap: 6px; }
  .theme-toggle { padding: 5px 8px; font-size: 8px; }
  .status-pill { display: none; }
}
'''
style_close = '\n</style>'
if style_close not in html:
    raise SystemExit("style closing tag not found")
html = html.replace(style_close, theme_css + style_close, 1)

# 6) Add the toggle next to the existing presentation status.
old_topbar = '''<div id="top-bar">
  <div class="brand-mark f-clash">SIWES 2026 PRESENTATION</div>
  <div class="status-pill f-poppins">INDUSTRIAL TRAINING PRESENTATION</div>
</div>'''
new_topbar = '''<div id="top-bar">
  <div class="brand-mark f-clash">SIWES 2026 PRESENTATION</div>
  <div class="top-bar-actions">
    <button id="theme-toggle" class="theme-toggle" type="button" aria-pressed="false" aria-label="Switch to light projection theme" title="Toggle light / dark theme">
      <span class="theme-toggle-glyph" aria-hidden="true"></span>
      <span id="theme-toggle-label">LIGHT</span>
    </button>
    <div class="status-pill f-poppins">INDUSTRIAL TRAINING PRESENTATION</div>
  </div>
</div>'''
if old_topbar not in html:
    raise SystemExit("top bar anchor not found")
html = html.replace(old_topbar, new_topbar, 1)

# 7) Keep the animation runtime offline too; both files already exist in the repo.
old_scripts = '''<!-- ─── SCRIPT LIBRARIES (LOCAL + CDN FALLBACK) ─── -->
<script src="gsap.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/ScrollTrigger.min.js"></script>
'''
new_scripts = '''<!-- ─── SCRIPT LIBRARIES (LOCAL / OFFLINE) ─── -->
<script src="gsap.min.js"></script>
<script src="ScrollTrigger.min.js"></script>
'''
if old_scripts not in html:
    raise SystemExit("Expected GSAP script block not found")
html = html.replace(old_scripts, new_scripts, 1)

# 8) Initialize and persist the toggle inside the existing vanilla-JS controller.
theme_js = r'''
  // ─── GLOBAL THEME TOGGLE (OFFLINE, VANILLA JS) ──────────
  const THEME_STORAGE_KEY = 'siwes-theme';
  const root = document.documentElement;
  const themeToggle = document.getElementById('theme-toggle');
  const themeToggleLabel = document.getElementById('theme-toggle-label');

  function setTheme(theme, persist) {
    const nextTheme = theme === 'light' ? 'light' : 'dark';
    const isLight = nextTheme === 'light';

    root.setAttribute('data-theme', nextTheme);
    root.style.colorScheme = nextTheme;

    if (themeToggle) {
      themeToggle.setAttribute('aria-pressed', String(isLight));
      themeToggle.setAttribute('aria-label', isLight ? 'Switch to dark theme' : 'Switch to light projection theme');
      themeToggle.title = isLight ? 'Use dark theme' : 'Use light projection theme';
    }
    if (themeToggleLabel) {
      themeToggleLabel.textContent = isLight ? 'DARK' : 'LIGHT';
    }

    if (persist !== false) {
      try { localStorage.setItem(THEME_STORAGE_KEY, nextTheme); } catch (error) { /* storage can be unavailable in strict/private contexts */ }
    }
  }

  setTheme(root.getAttribute('data-theme') || 'dark', false);
  if (themeToggle) {
    themeToggle.addEventListener('click', function (event) {
      event.stopPropagation();
      setTheme(root.getAttribute('data-theme') === 'light' ? 'dark' : 'light', true);
    });
  }

'''
iife_anchor = '''(function() {
  'use strict';
'''
if iife_anchor not in html:
    raise SystemExit("main JS IIFE anchor not found")
html = html.replace(iife_anchor, iife_anchor + theme_js, 1)

path.write_text(html, encoding="utf-8")

# Guardrails: make the patch fail loudly if offline/theme invariants are broken.
checks = {
    'theme button': 'id="theme-toggle"',
    'light token set': ':root[data-theme="light"]',
    'saved theme': "localStorage.setItem(THEME_STORAGE_KEY",
    'local ScrollTrigger': '<script src="ScrollTrigger.min.js"></script>',
}
for name, needle in checks.items():
    if needle not in html:
        raise SystemExit(f"Verification failed: {name}")

for forbidden in ('fonts.googleapis.com', 'fonts.gstatic.com', 'cdnjs.cloudflare.com'):
    if forbidden in html:
        raise SystemExit(f"Offline verification failed; external runtime remains: {forbidden}")

print("Theme toggle patch applied successfully")
