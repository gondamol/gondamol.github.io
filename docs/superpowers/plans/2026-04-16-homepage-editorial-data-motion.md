# Homepage Editorial Data Motion Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Rebuild the homepage into a quieter editorial composition with restrained data-native motion, chapter bands, an evidence-led work section, and a hybrid collaboration CTA.

**Architecture:** Keep the work native to the current Quarto homepage by replacing the oversized `index.qmd` composition with a smaller, more narrative markup structure and a single supporting interaction script. Add new homepage-specific styles in `custom.scss` so the redesign stays isolated from the rest of the site, and use a render-based smoke test to validate the final HTML structure.

**Tech Stack:** Quarto, HTML-in-QMD, SCSS, small vanilla JavaScript, Bash smoke test

---

### Task 1: Add Homepage Regression Smoke Test

**Files:**
- Create: `tests/homepage-editorial-smoke.sh`
- Modify: `.gitignore`
- Test: `tests/homepage-editorial-smoke.sh`

- [ ] **Step 1: Write the failing smoke test**

```bash
#!/usr/bin/env bash
set -euo pipefail

html_file="${1:-_site/index.html}"

require() {
  local pattern="$1"
  if ! grep -q "$pattern" "$html_file"; then
    echo "Missing pattern: $pattern" >&2
    exit 1
  fi
}

require "editorial-hero"
require "proof-ribbon-track"
require "chapter-band"
require "featured-ledger"
require "collab-channel"
```

- [ ] **Step 2: Run the test against the current homepage to verify it fails**

Run: `quarto render index.qmd && bash tests/homepage-editorial-smoke.sh`

Expected: FAIL with at least one missing pattern because the current homepage does not yet include the new editorial structure.

- [ ] **Step 3: Save the test file and ensure it is executable**

```bash
chmod +x tests/homepage-editorial-smoke.sh
```

- [ ] **Step 4: Re-run the failing test and confirm the failure is real**

Run: `quarto render index.qmd && bash tests/homepage-editorial-smoke.sh`

Expected: FAIL again for the same missing homepage markers.


### Task 2: Rebuild Homepage Markup And Interaction

**Files:**
- Modify: `index.qmd`
- Test: `tests/homepage-editorial-smoke.sh`

- [ ] **Step 1: Replace the current homepage sections with the new narrative structure**

```html
<section class="editorial-hero reveal-on-scroll">
  <!-- thesis copy -->
  <!-- image and provenance -->
</section>

<section class="proof-ribbon-shell reveal-on-scroll">
  <div class="proof-ribbon-track">...</div>
</section>

<section class="chapter-band chapter-band--research reveal-on-scroll">...</section>
<section class="chapter-band chapter-band--systems reveal-on-scroll">...</section>
<section class="chapter-band chapter-band--impact reveal-on-scroll">...</section>

<section class="featured-ledger reveal-on-scroll">...</section>
<section class="positioning-bridge reveal-on-scroll">...</section>
<section class="collab-channel reveal-on-scroll">...</section>
```

- [ ] **Step 2: Keep exactly two hero actions and exactly three featured evidence items**

```html
<div class="editorial-hero__actions">
  <a href="projects/index.html" class="btn-solid">Selected Work</a>
  <a href="about/index.html" class="btn-ghost">My Story</a>
</div>
```

- [ ] **Step 3: Add restrained interaction hooks for scroll reveal and proof ribbon duplication**

```js
var proofRibbon = document.querySelector('.proof-ribbon-track');
if (proofRibbon && !proofRibbon.dataset.enhanced) {
  proofRibbon.innerHTML += proofRibbon.innerHTML;
  proofRibbon.dataset.enhanced = 'true';
}
```

- [ ] **Step 4: Keep accessibility basics in the new markup**

```html
<p class="editorial-hero__caption">Field systems, evidence, and operational reality.</p>
<article class="ledger-card" tabindex="0">...</article>
<a href="mailto:nichodemuswerre@gmail.com" class="collab-channel__cta">Initiate Contact</a>
```

- [ ] **Step 5: Run the smoke test to confirm the new structure exists**

Run: `quarto render index.qmd && bash tests/homepage-editorial-smoke.sh`

Expected: PASS once the new homepage markers are present in `_site/index.html`.


### Task 3: Add Homepage Styles And Motion

**Files:**
- Modify: `custom.scss`
- Optionally modify: `styles.scss`
- Test: `tests/homepage-editorial-smoke.sh`

- [ ] **Step 1: Add a homepage-specific style block for the new structure**

```scss
.editorial-hero { ... }
.proof-ribbon-shell { ... }
.chapter-band { ... }
.featured-ledger { ... }
.ledger-card { ... }
.collab-channel { ... }
```

- [ ] **Step 2: Implement restrained motion with reduced-motion fallback**

```scss
@keyframes proofRibbonDrift {
  from { transform: translateX(0); }
  to { transform: translateX(-50%); }
}

.proof-ribbon-track {
  animation: proofRibbonDrift 32s linear infinite;
}

@media (prefers-reduced-motion: reduce) {
  .proof-ribbon-track {
    animation: none;
    transform: none;
  }
}
```

- [ ] **Step 3: Style the collaboration CTA as hybrid editorial/transmission**

```scss
.collab-channel__status { ... }
.collab-channel__title { ... }
.collab-channel__cta { ... }
.collab-channel__links a { ... }
```

- [ ] **Step 4: Add responsive rules for mobile layouts**

```scss
@media (max-width: 900px) {
  .editorial-hero,
  .featured-ledger__grid,
  .collab-channel__layout {
    grid-template-columns: 1fr;
  }
}
```

- [ ] **Step 5: Re-render and re-run the smoke test**

Run: `quarto render index.qmd && bash tests/homepage-editorial-smoke.sh`

Expected: PASS with no missing-pattern output.


### Task 4: Verify Final Build

**Files:**
- Verify: `index.qmd`
- Verify: `custom.scss`
- Verify: `_site/index.html`
- Test: `tests/homepage-editorial-smoke.sh`

- [ ] **Step 1: Run the homepage render**

Run: `quarto render index.qmd`

Expected: exit code 0 and updated `_site/index.html`.

- [ ] **Step 2: Run the homepage smoke test**

Run: `bash tests/homepage-editorial-smoke.sh`

Expected: PASS with no output.

- [ ] **Step 3: Inspect the diff for the intended scope**

Run: `git diff -- index.qmd custom.scss styles.scss tests/homepage-editorial-smoke.sh`

Expected: diff shows homepage structure, style changes, and the smoke test only.

- [ ] **Step 4: Record any residual risks**

```text
- Visual polish still depends on browser review
- Homepage-only smoke test validates structure, not pixel-perfect layout
- Reduced-motion behavior must be inferred from CSS rules if no browser QA is run
```
