from pathlib import Path
import re

path = Path("index.html")
text = path.read_text(encoding="utf-8")
original = text

# Remove the duplicated visible Gallery badge from each project image.
text, badge_count = re.subn(
    r'\n\s*<div class="project-mockup-badge">.*?</div>',
    "",
    text,
    flags=re.S,
)
if badge_count != 2:
    raise SystemExit(f"Expected 2 project image Gallery badges, found {badge_count}")

# Remove Source code and Live website actions from both project cards.
text, source_count = re.subn(
    r'\n\s*<a href="https://github\.com/Adeoye100"[^>]*class="btn-card-outline">.*?</a>',
    "",
    text,
    flags=re.S,
)
text, live_count = re.subn(
    r'\n\s*<a href="https://github\.com/Adeoye100"[^>]*class="btn-card-solid">.*?</a>',
    "",
    text,
    flags=re.S,
)
if source_count != 2 or live_count != 2:
    raise SystemExit(
        f"Expected 2 Source and 2 Live website actions, found {source_count} and {live_count}"
    )

# Replace the Nexos placeholder card image with an existing project screenshot.
nexos_placeholder = '''            <div style="display: flex; width: 100%; height: 100%; align-items: center; justify-content: center; font-size: 12px; color: var(--sub); text-transform: uppercase; border: 1px dashed var(--line);">
              [ PLATFORM INTERFACE PREVIEW ]
            </div>'''
nexos_preview = '''            <img src="ss01.png" alt="Nexos productivity workspace preview" class="project-mockup-img" onerror="this.style.display='none';" />'''
if nexos_placeholder not in text:
    raise SystemExit("Nexos placeholder block was not found")
text = text.replace(nexos_placeholder, nexos_preview, 1)

# Swiper is no longer needed after the project popup is simplified.
text = re.sub(
    r'\n<!-- Swiper CSS & JS -->\n<link rel="stylesheet" href="https://cdn\.jsdelivr\.net/npm/swiper@11/swiper-bundle\.min\.css" />\n<script src="https://cdn\.jsdelivr\.net/npm/swiper@11/swiper-bundle\.min\.js"></script>\n',
    "\n",
    text,
    count=1,
)

# Replace the Swiper popup with a full-screen project gallery using Section 05's visual primitives.
modal_start = "<!-- PROJECT GALLERY SWIPABLE LIGHTBOX MODAL -->"
modal_end = "<!-- ─── SCRIPT LIBRARIES (LOCAL + CDN FALLBACK) ─── -->"
start_i = text.find(modal_start)
end_i = text.find(modal_end)
if start_i == -1 or end_i == -1 or end_i <= start_i:
    raise SystemExit("Project gallery modal markers not found")

modal_html = '''<!-- PROJECT GALLERY — SECTION 05 STYLE FULL-SCREEN POPUP -->
<div id="project-gallery-modal" class="gallery-modal-overlay project-gallery-modal-overlay" role="dialog" aria-modal="true" aria-labelledby="gallery-title-text" aria-describedby="gallery-subtitle-text">
  <div class="gallery-modal-backdrop" id="gallery-modal-backdrop"></div>

  <div class="project-gallery-shell">
    <div class="gal-hdr project-gallery-header">
      <p class="section-num">06 — Project Gallery</p>
      <h3 id="gallery-title-text" class="panel-heading f-clash">Project Title</h3>
      <p id="gallery-subtitle-text" class="project-gallery-subtitle">Project image gallery</p>

      <button type="button" class="project-gallery-close" id="gallery-modal-close-btn" aria-label="Close project gallery">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
          <line x1="18" y1="6" x2="6" y2="18"></line>
          <line x1="6" y1="6" x2="18" y2="18"></line>
        </svg>
      </button>
    </div>

    <div class="gal-stage project-gallery-stage" id="project-gallery-stage">
      <div id="project-gallery-slides"></div>

      <button type="button" class="gal-zone gal-zone-prev project-gallery-zone" id="project-gallery-prev" aria-label="Previous project image"></button>
      <button type="button" class="gal-zone gal-zone-next project-gallery-zone" id="project-gallery-next" aria-label="Next project image"></button>
    </div>

    <div class="gal-dots project-gallery-dots" id="project-gallery-dots" aria-label="Project gallery image navigation"></div>
  </div>
</div>

'''
text = text[:start_i] + modal_html + text[end_i:]

style_anchor = "\n</style>\n</head>"
if style_anchor not in text:
    raise SystemExit("Main style closing tag not found")

modal_css = r'''

/* ── SECTION 06 PROJECT GALLERY — SECTION 05 VISUAL LANGUAGE ── */
.project-gallery-modal-overlay {
  opacity: 0;
  visibility: hidden;
  pointer-events: none;
  background: #000000;
  transition: opacity 220ms cubic-bezier(0.32, 0.72, 0, 1), visibility 220ms cubic-bezier(0.32, 0.72, 0, 1);
}

.project-gallery-modal-overlay.active {
  opacity: 1;
  visibility: visible;
  pointer-events: auto;
}

.project-gallery-modal-overlay .gallery-modal-backdrop {
  position: absolute;
  inset: 0;
  background: rgba(0, 0, 0, 0.96);
}

.project-gallery-shell {
  position: relative;
  z-index: 2;
  width: 100vw;
  height: 100dvh;
  display: flex;
  flex-direction: column;
  padding: 48px 72px 24px;
  background: #000000;
}

.project-gallery-header {
  position: relative;
  flex: 0 0 auto;
  padding-right: 64px;
  margin-bottom: 0;
}

.project-gallery-header .panel-heading {
  margin-bottom: 4px;
}

.project-gallery-subtitle {
  font-size: 10px;
  letter-spacing: 0.16em;
  text-transform: uppercase;
  color: var(--text-dim);
}

.project-gallery-close {
  position: absolute;
  top: 0;
  right: 0;
  width: 44px;
  height: 44px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border: 1px solid var(--border-color);
  background: #050505;
  color: #ffffff;
  cursor: pointer;
  opacity: 0.78;
  transition: opacity 180ms cubic-bezier(0.32, 0.72, 0, 1), background 180ms cubic-bezier(0.32, 0.72, 0, 1), border-color 180ms cubic-bezier(0.32, 0.72, 0, 1);
}

.project-gallery-close:hover {
  opacity: 1;
  background: #131313;
  border-color: var(--border-bright);
}

.project-gallery-close:focus-visible,
.project-gallery-zone:focus-visible,
.project-gallery-dots .gal-dot:focus-visible {
  outline: 2px solid #ffffff;
  outline-offset: 3px;
}

.project-gallery-stage.gal-stage {
  flex: 1 1 auto;
  width: 100%;
  min-height: 0;
  margin: 20px 0 18px;
  aspect-ratio: 16 / 9;
  border: 1px solid var(--border-color);
  background: #050505;
}

.project-gallery-stage .gal-slide {
  opacity: 0;
  visibility: hidden;
  z-index: 0;
  transition: opacity 220ms cubic-bezier(0.32, 0.72, 0, 1);
}

.project-gallery-stage .gal-slide.active {
  opacity: 1;
  visibility: visible;
  z-index: 1;
}

.project-gallery-stage .gal-img img {
  object-fit: contain;
  background: #050505;
  transform: none !important;
  will-change: opacity;
}

.project-gallery-stage .gal-num {
  opacity: 1;
}

.project-gallery-zone {
  border: 0;
  padding: 0;
  background: transparent;
}

.project-gallery-dots {
  flex: 0 0 auto;
  min-height: 18px;
  padding-bottom: 4px;
}

@media (max-width: 768px) {
  .project-gallery-shell {
    padding: 28px 20px 20px;
  }

  .project-gallery-stage.gal-stage {
    margin-top: 16px;
    margin-bottom: 14px;
  }

  .project-gallery-stage .gal-caption {
    width: 78%;
    padding: 24px 20px 18px;
  }

  .project-gallery-stage .gal-num {
    top: 16px;
    right: 18px;
    font-size: clamp(44px, 14vw, 72px);
  }

  .project-gallery-stage .gal-zone {
    width: 64px;
  }
}

@media (prefers-reduced-motion: reduce) {
  .project-gallery-modal-overlay,
  .project-gallery-stage .gal-slide,
  .project-gallery-close {
    transition: none !important;
  }
}
'''
text = text.replace(style_anchor, modal_css + style_anchor, 1)

# Replace the multi-effect Swiper controller with a restrained three-image controller.
js_start = "  // ─── PROJECT GALLERY LIGHTBOX & SWIPABLE SLIDER ───"
js_end = "  // QR Enlargement Lightbox Handlers"
js_start_i = text.find(js_start)
js_end_i = text.find(js_end)
if js_start_i == -1 or js_end_i == -1 or js_end_i <= js_start_i:
    raise SystemExit("Project gallery JavaScript markers not found")

gallery_js = r'''  // ─── SECTION 06 PROJECT GALLERY — RESTRAINED SECTION 05 PATTERN ───
  const projectGalleries = {
    'sanfaani': {
      title: 'SanfaaniService',
      subtitle: 'ENTERPRISE SAAS PLATFORM | 3 IMAGE GALLERY',
      slides: [
        {
          src: 'Sanfaani_service_00.png',
          title: 'Client dashboard & workflow overview',
          caption: 'Main enterprise dashboard showing service activity, client workflow, and operational status at a glance.'
        },
        {
          src: 'Sanfaani_service_01.png',
          title: 'Service management & detailed tracking',
          caption: 'Detailed service workflow showing request progress, operational states, and client-facing tracking.'
        },
        {
          src: 'sanfaani_service_02.svg',
          title: 'System analytics & engineering view',
          caption: 'A technical view of the system used to communicate platform behaviour and engineering detail.'
        }
      ]
    },
    'nexos': {
      title: 'Nexos Productivity Platform',
      subtitle: 'PRODUCTIVITY WORKSPACE | 3 IMAGE GALLERY',
      slides: [
        {
          src: 'ss01.png',
          title: 'Workspace overview',
          caption: 'Nexos workspace view focused on structured project visibility, task organisation, and practical daily use.'
        },
        {
          src: 'ss02.png',
          title: 'Task and workflow detail',
          caption: 'A closer look at the task workflow and the information hierarchy used to keep project work understandable.'
        },
        {
          src: 'ss03.png',
          title: 'Project management interface',
          caption: 'Project-level interface showing how the productivity system presents work states and supporting context.'
        }
      ]
    }
  };

  let activeProjectGallery = null;
  let projectGalleryIndex = 0;
  let projectGalleryReturnFocus = null;

  function setProjectGallerySlide(nextIndex) {
    if (!activeProjectGallery) return;

    const total = activeProjectGallery.slides.length;
    const normalizedIndex = (nextIndex + total) % total;
    const slideEls = Array.from(document.querySelectorAll('#project-gallery-slides .gal-slide'));
    const dotEls = Array.from(document.querySelectorAll('#project-gallery-dots .gal-dot'));

    slideEls.forEach(function(slideEl, index) {
      slideEl.classList.toggle('active', index === normalizedIndex);
      slideEl.setAttribute('aria-hidden', index === normalizedIndex ? 'false' : 'true');
    });

    dotEls.forEach(function(dotEl, index) {
      dotEl.classList.toggle('active', index === normalizedIndex);
      dotEl.setAttribute('aria-current', index === normalizedIndex ? 'true' : 'false');
    });

    projectGalleryIndex = normalizedIndex;
  }

  function renderProjectGallery(galleryData) {
    const slidesEl = document.getElementById('project-gallery-slides');
    const dotsEl = document.getElementById('project-gallery-dots');
    if (!slidesEl || !dotsEl) return;

    slidesEl.innerHTML = galleryData.slides.map(function(slide, index) {
      const num = String(index + 1).padStart(2, '0');
      return '<div class="gal-slide' + (index === 0 ? ' active' : '') + '" data-index="' + index + '" aria-hidden="' + (index === 0 ? 'false' : 'true') + '">' +
        '<div class="gal-img">' +
          '<img src="' + slide.src + '" alt="' + slide.title + '" draggable="false" />' +
        '</div>' +
        '<div class="gal-num">' + num + '</div>' +
        '<div class="gal-caption">' +
          '<span class="gal-tag">' + slide.title + '</span>' +
          '<p class="gal-desc">' + slide.caption + '</p>' +
        '</div>' +
      '</div>';
    }).join('');

    dotsEl.innerHTML = galleryData.slides.map(function(_, index) {
      return '<button type="button" class="gal-dot' + (index === 0 ? ' active' : '') + '" aria-label="Image ' + (index + 1) + ' of ' + galleryData.slides.length + '" aria-current="' + (index === 0 ? 'true' : 'false') + '" data-project-gallery-dot="' + index + '"></button>';
    }).join('');

    dotsEl.querySelectorAll('[data-project-gallery-dot]').forEach(function(dot) {
      dot.addEventListener('click', function() {
        setProjectGallerySlide(parseInt(dot.getAttribute('data-project-gallery-dot'), 10));
      });
    });
  }

  window.openProjectGallery = function(key) {
    const galleryData = projectGalleries[key];
    if (!galleryData) return;

    const modal = document.getElementById('project-gallery-modal');
    const titleEl = document.getElementById('gallery-title-text');
    const subtitleEl = document.getElementById('gallery-subtitle-text');
    const closeBtn = document.getElementById('gallery-modal-close-btn');
    if (!modal) return;

    projectGalleryReturnFocus = document.activeElement;
    activeProjectGallery = galleryData;
    projectGalleryIndex = 0;

    if (titleEl) titleEl.textContent = galleryData.title;
    if (subtitleEl) subtitleEl.textContent = galleryData.subtitle;

    renderProjectGallery(galleryData);
    modal.classList.add('active');
    document.body.style.overflow = 'hidden';

    if (closeBtn) closeBtn.focus({ preventScroll: true });
  };

  window.stepProjectGallery = function(direction) {
    if (!activeProjectGallery) return;
    setProjectGallerySlide(projectGalleryIndex + direction);
  };

  window.closeProjectGallery = function() {
    const modal = document.getElementById('project-gallery-modal');
    if (modal) modal.classList.remove('active');
    document.body.style.overflow = '';
    activeProjectGallery = null;
    projectGalleryIndex = 0;

    if (projectGalleryReturnFocus && typeof projectGalleryReturnFocus.focus === 'function') {
      projectGalleryReturnFocus.focus({ preventScroll: true });
    }
    projectGalleryReturnFocus = null;
  };

  const galleryModalCloseBtn = document.getElementById('gallery-modal-close-btn');
  if (galleryModalCloseBtn) {
    galleryModalCloseBtn.addEventListener('click', function(e) {
      e.stopPropagation();
      closeProjectGallery();
    });
  }

  const galleryModalBackdrop = document.getElementById('gallery-modal-backdrop');
  if (galleryModalBackdrop) {
    galleryModalBackdrop.addEventListener('click', function(e) {
      e.stopPropagation();
      closeProjectGallery();
    });
  }

  const projectGalleryPrev = document.getElementById('project-gallery-prev');
  const projectGalleryNext = document.getElementById('project-gallery-next');
  if (projectGalleryPrev) {
    projectGalleryPrev.addEventListener('click', function(e) {
      e.stopPropagation();
      stepProjectGallery(-1);
    });
  }
  if (projectGalleryNext) {
    projectGalleryNext.addEventListener('click', function(e) {
      e.stopPropagation();
      stepProjectGallery(1);
    });
  }

'''
text = text[:js_start_i] + gallery_js + text[js_end_i:]

# Keyboard navigation now uses the lightweight controller.
text = text.replace("if (swiperInstance) swiperInstance.slideNext();", "stepProjectGallery(1);")
text = text.replace("if (swiperInstance) swiperInstance.slidePrev();", "stepProjectGallery(-1);")

# Do not navigate the presentation behind an open project popup.
wheel_needle = "  window.addEventListener('wheel', function(e) {\n    e.preventDefault();"
wheel_replacement = "  window.addEventListener('wheel', function(e) {\n    e.preventDefault();\n    const projectModal = document.getElementById('project-gallery-modal');\n    if (projectModal && projectModal.classList.contains('active')) return;"
if wheel_needle not in text:
    raise SystemExit("Wheel navigation listener was not found")
text = text.replace(wheel_needle, wheel_replacement, 1)

touch_end_needle = "  window.addEventListener('touchend', function(e) {\n    if (e.changedTouches.length === 1) {"
touch_end_replacement = "  window.addEventListener('touchend', function(e) {\n    const projectModal = document.getElementById('project-gallery-modal');\n    if (projectModal && projectModal.classList.contains('active')) return;\n    if (e.changedTouches.length === 1) {"
if touch_end_needle not in text:
    raise SystemExit("Touch navigation listener was not found")
text = text.replace(touch_end_needle, touch_end_replacement, 1)

# Verification gates.
checks = {
    "single visible Gallery CTA per project": text.count('class="btn-card-gallery"') == 2,
    "no Source code actions": "Source code" not in text,
    "no Live website actions": "Live website" not in text,
    "no Swiper instance": "new Swiper(" not in text,
    "Section 05 retained": "PANEL 05: PHOTO GALLERY (SEAMLESS LOOP)" in text and 'id="gal-stage"' in text,
    "three-image Sanfaani gallery": all(
        name in text
        for name in ["Sanfaani_service_00.png", "Sanfaani_service_01.png", "sanfaani_service_02.svg"]
    ),
    "three-image Nexos gallery": all(name in text for name in ["ss01.png", "ss02.png", "ss03.png"]),
    "closable popup": 'id="gallery-modal-close-btn"' in text and "window.closeProjectGallery" in text,
}
failed = [name for name, ok in checks.items() if not ok]
for name, ok in checks.items():
    print(f"{'PASS' if ok else 'FAIL'}: {name}")
if failed:
    raise SystemExit("Verification failed: " + ", ".join(failed))
if text == original:
    raise SystemExit("Patch produced no changes")

path.write_text(text, encoding="utf-8")
print("Section 06 gallery refinement applied successfully.")
