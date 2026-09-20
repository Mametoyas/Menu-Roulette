# Menu Recipe Roulette — Design System & UI Specification

## 1. Executive Summary & Design Vision
The **Recipe Roulette** design system is designed to provide an inviting, warm, modern, and highly responsive user experience for a recipe discovery web application. The core feature focuses on resolving decision fatigue ("What should I eat today?") by matching available fridge ingredients to recipes or randomly spinning a **Menu Recipe Roulette**.

---

## 2. Overall Visual Style
- **Aesthetic:** Warm Culinary Modernism with Clean Flat Interfaces and Soft Skeuomorphism (Gradients + Soft Drop Shadows).
- **Vibe:** Friendly, encouraging, energetic, and clean (food-focused).
- **Backdrops & Surfaces:** Subtle warm undertones (`bg-amber-50/40`) with clean white cards (`bg-white`) and translucent frosted glass overlays (`backdrop-blur-md`).
- **Borders & Radii:** Rounded, approachable shapes utilizing smooth corners (`rounded-2xl` to `rounded-3xl` for cards, modals, and heroes).

---

## 3. Color Palette

### Primary / Brand Colors (Warm Culinary Theme)
- **Amber 50 (`#fffbeedb`):** App Background & Soft Highlight Containers.
- **Amber 100 (`#fef3c7`):** Secondary Chips & Soft Hover States.
- **Amber 500 (`#f59e0b`):** Brand Accent, Primary Buttons & Hero Gradients.
- **Amber 600 (`#d97706`):** Active Tab Highlights & Focused Borders.
- **Orange 500 / 600 (`#f97316` / `#ea580c`):** Accent Highlights, Hot Recommendations, Gradient Endpoints.

### Functional & Status Colors
- **Emerald / Accent Green 500 (`#10b981`):** Match Success Badge (80%+ ingredients present), High-Match Filters, Primary Action Buttons.
- **Rose 500 (`#f43f5e`):** Favorites Icon, Remove Badges, Hot Badges.
- **Slate Neutral Spectrum:**
  - `slate-800` (`#1e293b`): Primary Headings & Bold Text.
  - `slate-600` (`#475569`): Body Text.
  - `slate-400` (`#94a3b8`): Subtitles, Muted Labels, Placeholder Text.
  - `slate-100` (`#f1f5f9`): Soft Borders & Inactive Input Surfaces.

---

## 4. Typography

### Font Family
- **Primary:** `'Kanit', sans-serif` (Google Fonts) — Selected for modern, legibility-first Thai and Latin character alignment.

### Scale & Hierarchy
- **Hero Display:** `text-2xl` (Mobile) / `text-4xl` (Desktop) — `font-extrabold`, leading tight.
- **Section Heading:** `text-xl` (Mobile) / `text-2xl` (Desktop) — `font-bold`, `slate-800`.
- **Card Title:** `text-base` (Mobile) / `text-lg` (Desktop) — `font-bold`, `slate-800`.
- **Body Regular:** `text-sm` — `font-normal`, `slate-600`.
- **Caption / Badges:** `text-xs` (12px) to `text-[10px]` — `font-medium` or `font-semibold`.

---

## 5. Spacing System
Built on a standard 4px/8px incremental grid system:
- **Component Padding (Compact):** `px-2.5 py-1.5` (6px / 10px) for tags and small badges.
- **Component Padding (Standard):** `p-4` (16px) or `p-5` (20px) for cards and filter bars.
- **Section Margins:** `space-y-4` (16px) to `space-y-8` (32px) for page section stacking.
- **Container Insets:** `px-4 sm:px-6 lg:px-8` for responsive layout boundaries.

---

## 6. Grid & Layout Structure

### Max Container Width
- `max-w-7xl` (1280px max width) with centered alignment (`mx-auto`).

### Responsive Grid System
- **Mobile (< 640px):** Single column (`grid-cols-1`).
- **Tablet (640px - 1024px):** Dual column (`grid-cols-2`, gap 24px).
- **Desktop (> 1024px):** Three column (`grid-cols-3`, gap 24px).

---

## 7. Navigation Specification
- **Sticky Top Bar:** Fixed header with `backdrop-blur-md` glassmorphism and bottom accent border (`border-amber-100`).
- **Brand Logo:** Icon box with amber gradient + bold title with gradient text mask (`bg-clip-text text-transparent`).
- **Navigation Tabs:** Pill-shaped navigation items (`rounded-xl`):
  - **Explore Tab (`#nav-explore`):** Active default state with solid tint (`bg-amber-50 text-amber-700`).
  - **My Fridge Tab (`#nav-fridge`):** Displays a dynamic item counter badge (`bg-amber-500`).
  - **Favorites Tab (`#nav-favorites`):** Displays saved recipe badge (`bg-rose-500`).

---

## 8. Buttons & Interactive Controls

### Primary Action Buttons (e.g., Search Recipes, Roulette Spin)
- **Style:** Gradient fill (`from-emerald-500 to-teal-600` or `from-amber-500 to-orange-500`), rounded corners (`rounded-xl`), soft shadow (`shadow-md shadow-emerald-500/20`).
- **Hover/Active:** Gradient shift, slight dark shade overlay, subtle drop shadow scale.

### Quick Tag Buttons (Ingredient Chips)
- **Inactive State:** `bg-slate-100 hover:bg-amber-100 text-slate-600`.
- **Active / Selected State:** `bg-amber-500 text-white shadow-sm`.
- **Dismissible Badges:** Includes an `xmark` icon (`fa-xmark`) for instant deletion.

### Categorization Chips
- Horizontal scrolling flex container (`overflow-x-auto` with custom scrollbar).
- White background with soft slate border (`border-slate-200`), active button switches to full amber fill (`bg-amber-500 text-white`).

---

## 9. Recipe Cards & Content Container Specification

### Recipe Card Layout
1. **Aspect Ratio / Image Header:** Height `h-48`, hidden overflow with continuous `transform scale(1.05)` image zoom on hover.
2. **Badges Overlay:**
   - Cuisine tag on top-left (`bg-slate-900/60 backdrop-blur-md`).
   - Favorite heart button on top-right (`w-8 h-8 rounded-full bg-white/80`).
   - Ingredient Match % Badge on bottom-left (`bg-emerald-500` or `bg-amber-500`).
3. **Card Body:**
   - Category line & Star Rating display.
   - Truncated 1-line bold Title (`line-clamp-1`).
   - Truncated 2-line Description (`line-clamp-2`).
   - Key Specs Grid: 3-column divider for Time, Calories, and Difficulty level.
   - Ingredient Tag Preview: Displays up to 4 tags with checkmarks (`✓`) for matched items.

---

## 10. Forms & Input Controls
- **Input Container:** Elevated clean white panel (`bg-white shadow-2xl rounded-2xl`).
- **Text Inputs:** Borderless within container, clear placeholder styling (`placeholder-slate-400`), explicit focus state transitions (`focus:outline-none`).
- **Select Dropdowns:** Rounded compact controls (`bg-slate-50 border-slate-200 focus:border-amber-500 text-xs sm:text-sm`).

---

## 11. Iconography
- **Library:** FontAwesome 6 (Free Solid & Regular).
- **Icon Usage Patterns:**
  - Utensils (`fa-utensils`) for branding and main food themes.
  - Wand Magic / Roulette (`fa-wand-magic-sparkles` / `fa-arrows-spin`) for auto-matching and roulette randomizer.
  - Clock (`fa-clock`) for prep time.
  - Flame (`fa-fire`) for calories/heat.
  - Heart (`fa-heart`) for favorite states (Outline = Regular, Solid = Favorited).

---

## 12. Responsive Behavior Matrix

| Element | Mobile (< 640px) | Tablet (640px - 1024px) | Desktop (> 1024px) |
| :--- | :--- | :--- | :--- |
| **Header Nav Labels** | Hidden (Icons only) | Full Text + Icons | Full Text + Icons |
| **Hero Heading** | `text-2xl` | `text-3xl` | `text-4xl` |
| **Recipe Grid** | 1 Column | 2 Columns | 3 Columns |
| **Modal Width** | 95% screen width | Max 768px width | Max 768px width |
| **Filters Bar** | Vertical Stack / Scroll | Inline Wrappable | Inline Single Line Bar |

---

## 13. Hover / Active / Focus States
- **Card Hover:** Card elevates via box shadow expansion (`shadow-md` -> `shadow-xl`), image zooms by 5%.
- **Button Active State:** Active press scales button down slightly (`scale-95`).
- **Focus Rings:** Accessibility focus rings on interactive elements (`focus:ring-2 focus:ring-amber-400`).

---

## 14. Animations & Transitions
- **Scale Transitions:** Smooth 300ms cubic bezier transitions for modals and overlays (`transition-transform duration-300`).
- **Fade Transitions:** Smooth opacity transitions (`opacity-0` to `opacity-100`).
- **Spin / Roulette Animation:** Continuous CSS keyframe rotation for the Menu Roulette spin wheel action.

---

## 15. Component Hierarchy Tree

```
└── App Root (<body class="bg-amber-50/40">)
    ├── Header Navigation (<header>)
    │   ├── Logo Component
    │   └── Navigation Tabs (Explore, My Fridge, Favorites)
    ├── Main Layout (<main>)
    │   ├── Hero & Ingredient Input Section (<section>)
    │   │   ├── Ingredient Input Box & Add Button
    │   │   ├── Quick Selection Chips
    │   │   ├── Selected Ingredients Container (Badges)
    │   │   └── Search / Roulette Spin Action Bar
    │   ├── Filter & Toolbar Section
    │   │   ├── Category Chips Scroll View
    │   │   └── Filter Dropdowns Bar (Cuisine, Time, Calorie, Sort)
    │   ├── Results Counter & Section Header
    │   ├── Recipe Cards Grid Container
    │   │   └── Recipe Cards (Repeated)
    │   └── Empty State Placeholder
    ├── Modal Overlay Window (#recipe-modal)
    │   ├── Header Image Banner & Title Overlay
    │   ├── Quick Stats Row (Time, Calories, Difficulty)
    │   ├── Matching Status Banner (% calculation)
    │   ├── Ingredients Check List (Interactive Checkboxes)
    │   ├── Step-by-Step Instructions
    │   ├── Nutrition Breakdown Grid
    │   └── Modal Footer (Favorite Toggle & Close)
    └── Footer Component (<footer>)
```