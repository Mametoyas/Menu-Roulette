Design Specification — Travel-Booking Marketing/Search Homepage UI
Reusable system, extended for a "Menu Recipe Roulette" ingredient-to-recipe web app

Source: single screenshot of a Booking.com-style homepage — hero banner, primary search widget, a "why us" feature-card grid, and the top of an offers section. Sections marked [Inferred] are not directly visible in the source screenshot and have been extrapolated from the visible tokens to keep the system internally consistent and reusable. Sections marked [Observed] are read directly off the screenshot. Note: the crop does not include a top global nav bar (logo, sign-in, currency/language switcher) — it starts at the hero. Section 7 notes a reasonable [Inferred] nav, clearly flagged as not directly visible.

1. Overview
A conversion-focused, consumer marketing homepage. Everything above the fold points at one large, high-contrast search widget — the page's single "hero decision." Two strong brand colors (deep blue + bright gold) carry almost all of the visual weight; supporting content below the fold (the "why us" cards) drops to a quiet neutral gray-on-white palette so it doesn't compete with the hero.

Design principles to carry forward:

One hero moment per page: large bold headline + one clear primary action (the search widget), given maximum color contrast against everything else.
The primary action container is allowed to visually "break the grid" — it overlaps the boundary between the colored hero and the white body, signaling "this is the important part, interact with it first."
Below the fold, content flattens to quiet gray cards with flat icon illustrations — no competing saturated color once the primary action has been made.
Multi-field forms are presented as one continuous segmented control, not separate boxed inputs — visually one decision, not several.
2. Visual Style
Attribute	Value
Overall tone	Bold, friendly, consumer-facing; trustworthy-but-energetic brand feel
Shape language	Rounded rectangles throughout (~8–12px), pill-ish input/button corners, rounded-corner illustrated icons
Surface style	Flat blocks of strong color (hero) + flat neutral cards (below the fold); no shadows, minimal borders [Observed]
Contrast strategy	Hero = maximum contrast (dark blue bg, white text, gold accent bar); body = low contrast (white bg, light-gray cards, dark text)
Imagery	Small flat, multi-color illustrated icons in the feature cards (not line icons) — the one place the system allows more than two colors at once
3. Color Palette
Token	Approx. Hex	Usage
--color-brand-navy	#003580	Hero/header background, deepest brand color
--color-brand-gold	#FEBB02	Search-widget background band, the system's single "look here" accent
--color-action-blue	#0071C2	Primary button fill ("Search") — deliberately a different, brighter blue than the hero navy
--color-bg	#FFFFFF	Body background, input field fill
--color-card-bg	#F5F5F5	Feature-card background (the only non-white, non-brand surface)
--color-text-primary	#262626	Body headings, card titles
--color-text-secondary	#6B6B6B	Card body copy, section subtext
--color-text-on-brand	#FFFFFF	Hero headline/subhead, text sitting on --color-brand-navy
--color-divider	#E7E7E7 [Inferred]	Thin vertical separators inside the segmented search field
Usage rule: gold appears exactly once per page — behind the primary action — never as a body accent. Navy is the "brand" color (headers, hero); action-blue is a distinct "click me" color reserved for buttons/links. Keeping these two blues separate is a deliberate system rule, not a mistake to normalize away.

4. Typography
Role	Weight	Approx. Size	Notes
Hero H1 ("Find your next stay")	Extra-bold	~44–48px	White, on navy, tight line-height
Hero subhead	Regular	~18–20px	White, lower-contrast weight than the H1 for clear hierarchy
Search-field caption labels ("Check-in", "Travelers")	Semibold	~12–13px	Dark text sitting directly on the gold band
Search-field value text ("Where are you going?", "2 adults · 0 children · 1 room")	Regular	~16px	Dark gray placeholder / near-black filled value
Section heading ("Why Booking.com?", "Offers")	Bold	~24–28px	Text-primary
Card title	Bold	~16–18px	Text-primary, can wrap to two lines
Card body	Regular	~14px	Text-secondary
Checkbox label ("I'm traveling for work")	Regular	~14px	Text-primary
Typeface [Inferred]: Rounded, friendly geometric/humanist sans with strong weight contrast between headline and body — consistent with a system stack such as:

font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
5. Spacing System
Base unit: 8px, but the hero uses noticeably larger multiples than the body to reinforce "this section matters most."

Token	Value	Usage
--space-1	8px	Icon-to-label gaps inside search fields
--space-2	16px	Gap between card icon, title, and body within a feature card
--space-3	24px	Grid gutter between feature cards; padding inside cards
--space-4	32px	Gap between the search widget and the "traveling for work" checkbox
--space-6	56–64px	Hero top padding before the H1
--space-7	40–48px	Gap between major page sections (hero → "Why Booking.com?" → "Offers")
6. Grid / Layout
Top nav [Inferred, not visible in crop]: typically a slim white or transparent bar above the hero (logo left, sign-in/register + currency/language right) — not present in this screenshot but assumed present above the visible crop for a real implementation.
Hero band: full-bleed navy background, content constrained to a centered max-width container (~1200–1300px) with side margins; headline and subhead left-aligned within that container.
Search widget: a full-width gold band that continues the hero's max-width container; the white segmented field row is a card that overlaps the hero/body seam — its top half sits inside the gold band, its bottom half extends past it into the white body, using negative margin to visually anchor it as the page's single most important control.
Feature-card section: 4-column equal-width grid on desktop, consistent gutter, cards are equal height regardless of content length.
Offers section: heading + subtext at full container width, followed by a vertical (or horizontally-scrolling) list/grid of offer cards — partially cropped in source.
7. Navigation
Global nav [Inferred, not visible]: logo, primary account actions (sign in / register), and locale/currency switcher — standard for this category of site, but not evidenced in this crop; flagged here rather than fabricated in detail.
In-page "navigation" is really the search widget itself — there is no tab bar or sidebar; the page is single-purpose (drive a search), so all wayfinding below the fold is just section headings ("Why Booking.com?", "Offers") in normal document flow, not an interactive nav pattern.
8. Buttons
Variant	Fill	Text	Border	Use for
Primary (filled)	Solid --color-action-blue, rounded rect (~6–8px)	White, bold	none	The one commit action per widget — "Search"
Checkbox control	White fill, thin gray border, small square, rounded corners	n/a	1–2px gray, fills solid on check	Low-commitment opt-in toggles ("I'm traveling for work")
Text/link button [Inferred]	Transparent	--color-action-blue	none	Secondary actions elsewhere on the page (e.g. "See all offers"), not directly visible in this crop but consistent with the palette
Rule: exactly one filled primary button is visible on the entire page, and it lives inside the segmented search field, not floating separately — reinforcing that the search widget is one unified decision ending in one action.

9. Cards
Two card contexts are present:

A. Search widget "card" [Observed] — functions as a form container, not a content card; see Section 10 for its internal field structure. White fill, rounded corners, overlaps the hero/body seam as described in Section 6.

B. Feature card ("Why Booking.com?") [Observed]

Property	Value
Background	--color-card-bg (light gray)
Border	none
Corner radius	~10–12px
Padding	24px
Content	Flat multi-color icon illustration (top) → bold title (2 lines max) → gray body copy
Grid behavior	Equal-width, equal-height, 4-across on desktop
Card B's "icon → bold title → gray description" stack is the system's general-purpose explainer-card pattern — reusable anywhere the page needs to communicate several short, parallel value props.

10. Forms
The search widget is the system's signature form pattern: a single segmented control, not separate boxed inputs.

Element	Style
Caption labels	Small semibold text sitting directly on the gold band, above the white field row (not inside the fields themselves)
Destination field	Largest segment, leading bed/pin icon, free-text input, placeholder text
Check-in / Check-out field	Calendar icon + two date values separated by a short dash, opens a date-range picker
Travelers field	Person icon + a compact summary string ("2 adults · 0 children · 1 room") + a small up/down stepper chevron indicating an inline dropdown/stepper
Field dividers	Thin vertical --color-divider lines between segments — no gaps, no individual borders, so the whole row reads as one control
Submit	The primary button (Section 8) sits flush at the end of the same row, same height as the fields
Checkbox	Simple square checkbox + label, sits just below the widget, unrelated to the segmented-field styling — a plain, low-emphasis form control
11. Icons
Two distinct icon styles coexist, used for two different purposes:
Functional line icons (bed, calendar, person) inside the search fields — small, single-color dark gray, purely utilitarian.
Flat, multi-color illustrated icons in the feature cards — larger, decorative-but-informative, each combining 2–3 brand-adjacent colors (blue, gold, orange) per icon.
New icons for extensions [Inferred]: keep functional icons as simple single-color line glyphs (a fork/whisk icon for an ingredient field, a clock icon for cook time, a person/servings icon for portion count); keep any "why this matters" explainer cards using the flatter, multi-color illustration style — don't mix the two styles within the same component.
12. Responsive Behavior [Inferred — single desktop breakpoint visible]
Breakpoint	Behavior
≥1024px (desktop)	As observed: hero + overlapping 4-segment search widget, 4-column card grid
768–1023px (tablet)	Search widget segments may wrap to two rows (destination full-width on its own row, dates + travelers + button sharing a second row); card grid drops to 2 columns
<768px (mobile)	Search widget fully stacks — each field becomes its own full-width row, submit button becomes full-width beneath the fields; card grid becomes a single column or a horizontally-scrolling row; hero headline shrinks and hero vertical padding tightens significantly
13. Hover / Active States [Inferred — static image, limited direct evidence]
Element	Rest	Hover	Active/Focus
Search field segment	White bg	Very light gray tint on the hovered segment	Focused segment gets a visible inner border/outline in --color-action-blue; picker/dropdown opens
Primary button	Solid --color-action-blue	Darkens ~8%	Darkens ~15%, slight inset feel
Checkbox	Empty box, gray border	Border darkens	Fills solid --color-action-blue with a white check mark
Feature card	Flat gray	Very subtle lift/darken (optional) — cards are informational, not links, so hover feedback should stay minimal or absent	
14. Animation & Motion [Inferred — none visible in a static screenshot]
Date-range and travelers pickers: dropdown panels fade/slide open beneath their trigger segment, ~150–200ms.
Primary button: simple background-color transition on hover, ~120ms, no ripple.
Checkbox: quick fill + checkmark draw-in, ~120–150ms.
Section entrance (optional, common on marketing pages): feature cards may fade/slide up slightly on scroll into view — a nice-to-have, not evidenced in the static source.
15. Component Hierarchy
Page
├── [Inferred] Global Nav (logo, sign in/register, locale switcher)
│
├── Hero Section (navy background)
│   ├── Heading (H1 — "Find your next stay")
│   ├── Subheading
│   └── Search Widget (gold band, overlaps hero/body seam)
│       ├── Caption Labels row
│       └── Segmented Field Row (white card)
│           ├── Field — Destination (icon + text input)
│           ├── Field — Check-in/Check-out (icon + date-range trigger)
│           ├── Field — Travelers (icon + summary + stepper chevron)
│           └── Button — Primary ("Search")
│
├── Checkbox Row ("I'm traveling for work")
│
├── Section — "Why Booking.com?"
│   └── Feature Card Grid (4-across)
│       └── Feature Card × 4 (illustrated icon + bold title + gray body)
│
└── Section — "Offers"
    ├── Section Header + gray subtext
    └── Offer Card List (partially visible in source)

    ── [Extension] Menu Recipe Roulette ──
    ├── Hero Section (navy background)
    │   ├── Heading (H1 — "Find your next meal")
    │   ├── Subheading ("Tell us what's in your kitchen — we'll do the rest")
    │   └── Ingredient Widget (gold band, overlaps hero/body seam)
    │       ├── Field — Ingredients (icon + chip/tag multi-input: "Add an ingredient…", entered items shown as removable pills)
    │       ├── Field — Meal type (icon + dropdown: "Any meal · Breakfast · Lunch · Dinner · Dessert")
    │       ├── Field — Servings (icon + summary + stepper chevron, mirrors "Travelers")
    │       └── Button — Primary ("Spin the Roulette 🎲")
    │
    ├── Checkbox Row ("Only show recipes I can make right now")
    │
    ├── Section — "Why Recipe Roulette?"
    │   └── Feature Card Grid (4-across, reuses exact card style)
    │       └── e.g. "Zero food waste", "10,000+ tested recipes", "Step-by-step photos", "Save your favorites"
    │
    ├── Result Section — "Your Recipe" (revealed after spin/search)
    │   ├── Recipe Hero Card: full-width photo of the finished dish + title overlay (mirrors the hero-band treatment, image instead of flat color)
    │   ├── Ingredients Checklist (reuses the search-widget's chip styling for "have it" vs. gray for "need to buy")
    │   └── Step-by-step Instructions List
    │       └── Step Card × N (small step photo + step number badge + instruction text — reuses Feature Card B's icon/title/body stack, photo replacing the flat illustration)
    │
    └── Section — "Saved Recipes" (reuses the "Offers" list pattern)
16. Extending the System — Menu Recipe Roulette Notes
The defining trait of this system is a single, high-contrast "hero decision" per page, backed by quiet, low-contrast supporting content — that maps unusually well onto a "roulette" mechanic, since both are fundamentally "make one bold choice, then get a payoff":

Ingredient input widget: Replace the destination text field with a chip/tag multi-input ("Add an ingredient…") — each typed ingredient becomes a small removable pill inside the field, visually similar in weight to the destination field's placeholder-to-value transition. Keep "Meal type" and "Servings" as the second and third segments, exactly mirroring "Check-in/Check-out" and "Travelers" in structure (icon + label + compact summary), so the whole row still reads as one continuous decision. The primary button becomes "Spin the Roulette" — keep it the single filled --color-action-blue button flush at the row's end, and consider a brief spin/shuffle micro-animation on click (Section 14) before the result reveals, to earn the "roulette" name without breaking the system's otherwise restrained motion language.
Why-us explainer grid: Reuse Feature Card B exactly — icon, bold title, gray body — for value props like "reduces food waste," "step-by-step photos," or "save your favorites." No new card pattern needed.
Recipe result: Give the finished recipe its own hero band, but swap the flat navy fill for the recipe's photo (with a dark gradient overlay so the white title text stays legible) — this keeps the "one hero moment per page" rule intact while adapting it from a brand-color block to a photographic one, appropriate for a food app where the payoff is the image. Instruction steps reuse Feature Card B's icon/title/body stack, with a numbered badge in place of the flat icon and a small photo where useful.
In both the original and this extension, preserve the one-hero-decision rule: exactly one primary button per page/section, sitting at the end of the one row that matters most; everything else (checkboxes, secondary links, explainer cards) stays deliberately quiet so it never competes with that single action.
End of specification. This document defines reusable tokens and patterns; no implementation code included per request.