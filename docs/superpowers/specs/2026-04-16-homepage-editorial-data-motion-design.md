# Homepage Editorial Data Motion Design

Date: 2026-04-16
Surface: homepage
Primary files for implementation: `index.qmd`, `custom.scss`, `styles.scss`

## Context

The current homepage is strong on content coverage but does too much at once. It reads more like a comprehensive capabilities page than a distinct editorial front door. The goal of this redesign is to keep the existing Quarto stack, warm paper palette, serif/sans typography, and research-first credibility while making the homepage feel quieter, more intentional, and more memorable.

Three external references inform the direction:

- `https://ksenialitvinenko.space/` for sparse editorial composition, image-led rhythm, and calm confidence
- `https://blueyard.com/#section-3` for chapter-based scroll rhythm, strong section boundaries, and directional motion
- `https://killianherzer.com/` for the clarity and memorability of the collaboration CTA framing

The approved direction is `editorial + data motion`, with restrained chapter motion and a hybrid collaboration CTA. Motion should add energy without turning the portfolio into an experimental frontend showcase.

## Goals

- Make the homepage feel like an editorial thesis statement instead of a dense overview
- Use stronger hierarchy, whitespace, and image/caption treatment to increase perceived quality
- Introduce measured motion that feels data-native and narrative rather than decorative
- Make featured work feel more like evidence or case files than generic project cards
- End with a memorable but credible collaboration CTA

## Non-Goals

- No full clone of any reference site
- No WebGL, Three.js, or immersive 3D work
- No pinned scroll-heavy choreography or motion that interrupts reading
- No terminal-roleplay tone across the full site
- No redesign of every internal page in this phase

## User And Message

The homepage should quickly communicate that Nichodemus Amollo is a serious researcher-builder working at the intersection of field research, data engineering, analytics, and AI-ready systems. The page should speak to collaborators, hiring managers, research leads, and technically literate decision-makers who value rigor, clarity, and real-world delivery.

The message is not "I do everything." The message is:

`I build research and data systems that hold up in the real world, and I can show you the evidence.`

## Information Architecture

Approved homepage order:

1. Hero thesis plus editorial image
2. Moving proof ribbon
3. Chapter 01: Research
4. Chapter 02: Systems
5. Chapter 03: Impact
6. Featured evidence / selected work
7. Short positioning bridge
8. Collaboration CTA
9. Footer

The homepage should do less summarizing and more framing. Projects, Research, CV, and About remain the deeper destinations for full detail.

## Section Design

### 1. Hero Thesis Plus Editorial Image

The hero becomes a calmer two-column composition. The left side holds a short thesis, a tighter supporting paragraph, and exactly two clear actions: one work-facing action and one story/about-facing action. The right side holds one strong field/archive-style image with a small caption or provenance line. The composition should feel more like the opening spread of a journal or report than a startup landing page.

The hero copy should be shorter than the current version. It should establish point of view, not summarize the full resume. Visual breathing room is more important than density here.

### 2. Moving Proof Ribbon

Replace static proof blocks with a restrained horizontal ribbon carrying quantitative and qualitative proof points such as:

- `1,000+ households`
- `50+ field staff`
- `4 countries`
- `AI-ready systems`
- `decision-grade analytics`

This is the main BlueYard-inspired motion element on the page, but translated into a data portfolio idiom. It should feel like directional signal, not a marketing ticker.

### 3. Chapter Bands

Introduce three clear chapter transitions:

- `Research`
- `Systems`
- `Impact`

Each chapter band should act as both separator and narrative cue. These bands create a strong page spine and reduce the feeling of an undifferentiated wall of content. Their styling can use the existing warm/terra/gold/green palette rather than importing the references' exact colors.

### 4. Featured Evidence / Selected Work

The homepage should feature exactly three evidence items, and each item should feel more editorial and evidence-backed. Instead of a generic grid of cards, each featured work entry should include:

- title
- short framing sentence
- year
- domain
- tools or stack
- evidence of outcome or scope
- optional thumbnail / artifact image

The interaction should feel like opening a dossier or case file. Hover can reveal slightly more metadata, but the default state should already be readable and useful.

### 5. Positioning Bridge

After the featured work section, include a short bridge that connects the homepage thesis to the broader portfolio. This section can briefly reinforce the through-line: field reality, systems thinking, reproducible analytics, and AI direction. It should be concise and should mainly route users deeper into the portfolio.

### 6. Collaboration CTA

The CTA should borrow Killian Herzer's directness, not his full visual language. Approved tone: hybrid.

Structure:

- small status label such as `Channel Open`
- human headline such as `What if we worked together?`
- email address in a prominent line
- one primary action using a direct contact label such as `Initiate Contact`
- GitHub and LinkedIn as clean utility links

This block should feel memorable and slightly distinctive, but still warm and credible for a research-facing audience.

## Motion And Interaction

Approved motion level: restrained chapter motion.

Use:

- fade/slide reveals on major sections
- subtle stagger on evidence items
- a horizontal moving proof ribbon
- chapter bands that animate into place as the user enters each major section
- delayed reveal of captions and metadata where helpful

Do not use:

- pinned or scroll-jacking transitions
- large motion on every element
- constant parallax
- theatrical interaction that competes with reading

Motion must support the reading experience and must degrade gracefully when reduced-motion preferences are enabled.

## Visual Language

Keep:

- the current warm paper background and existing token family
- `Playfair Display` for editorial gravitas in headings
- `DM Sans` and `DM Mono` for body copy and metadata
- the scholarly, report-adjacent tone already established in the repo

Shift toward:

- more whitespace
- stronger image/caption pairings
- tighter copy blocks
- more visible section boundaries
- more disciplined metadata presentation

Avoid:

- glossy startup aesthetics
- overly futuristic UI language
- dark, militarized, or terminal-heavy styling as the primary mode

## Technical Implementation Notes

Primary implementation targets:

- `index.qmd` for homepage structure and markup
- `custom.scss` for tokens, chapter bands, motion primitives, evidence-card styling, and collaboration CTA styling
- `styles.scss` for supporting polish where page-level adjustments make sense

Global footer changes are optional. The collaboration CTA should live inside the homepage first. `_includes/footer.html` should only be changed if the new homepage rhythm exposes an obvious mismatch.

The implementation should stay native to the current Quarto + SCSS setup. No framework migration, no new rendering model, and no dependency-heavy frontend layer should be introduced for this work.

## Accessibility And Performance

- Respect `prefers-reduced-motion`
- Preserve clear heading order and reading flow
- Keep CTA and evidence links keyboard accessible
- Ensure metadata contrast remains readable on warm backgrounds
- Keep homepage motion lightweight enough not to harm page performance
- Maintain good mobile behavior for chapter bands, ribbons, and editorial image layouts

## Testing

Before implementation is considered complete:

1. Render the Quarto site successfully
2. Review the homepage on desktop and mobile widths
3. Verify motion behavior with reduced motion enabled
4. Confirm CTA email and social links work correctly
5. Check that the homepage feels calmer and more distinctive, not just different
6. Confirm the work remains legible and credible even with motion turned off

## Success Criteria

The redesign succeeds if:

- the homepage feels more editorial and less crowded
- the narrative spine is clearer through chaptering
- motion adds energy without undermining trust
- featured work feels more like evidence than marketing
- the collaboration CTA is more memorable and inviting
- the page still feels native to the existing portfolio rather than imported from another brand
