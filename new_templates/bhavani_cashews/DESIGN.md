---
name: Bhavani Cashews
colors:
  surface: '#f7f9fd'
  surface-dim: '#d8dade'
  surface-bright: '#f7f9fd'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#f2f4f8'
  surface-container: '#eceef2'
  surface-container-high: '#e6e8ec'
  surface-container-highest: '#e0e2e6'
  on-surface: '#191c1f'
  on-surface-variant: '#454742'
  inverse-surface: '#2d3134'
  inverse-on-surface: '#eff1f5'
  outline: '#767872'
  outline-variant: '#c6c7c0'
  surface-tint: '#5e5e5c'
  primary: '#5e5e5c'
  on-primary: '#ffffff'
  primary-container: '#fdfbf7'
  on-primary-container: '#747471'
  inverse-primary: '#c8c6c3'
  secondary: '#675d4e'
  on-secondary: '#ffffff'
  secondary-container: '#efe0cd'
  on-secondary-container: '#6d6354'
  tertiary: '#705a4f'
  on-tertiary: '#ffffff'
  tertiary-container: '#fffaf9'
  on-tertiary-container: '#866e63'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#e4e2de'
  primary-fixed-dim: '#c8c6c3'
  on-primary-fixed: '#1b1c1a'
  on-primary-fixed-variant: '#474744'
  secondary-fixed: '#efe0cd'
  secondary-fixed-dim: '#d2c4b2'
  on-secondary-fixed: '#221a0f'
  on-secondary-fixed-variant: '#4f4538'
  tertiary-fixed: '#fbdcce'
  tertiary-fixed-dim: '#dec1b3'
  on-tertiary-fixed: '#281810'
  on-tertiary-fixed-variant: '#574238'
  background: '#f7f9fd'
  on-background: '#191c1f'
  surface-variant: '#e0e2e6'
typography:
  display-lg:
    fontFamily: Playfair Display
    fontSize: 64px
    fontWeight: '700'
    lineHeight: '1.1'
    letterSpacing: -0.02em
  display-lg-mobile:
    fontFamily: Playfair Display
    fontSize: 40px
    fontWeight: '700'
    lineHeight: '1.2'
  headline-lg:
    fontFamily: Playfair Display
    fontSize: 40px
    fontWeight: '600'
    lineHeight: '1.2'
  headline-md:
    fontFamily: Playfair Display
    fontSize: 32px
    fontWeight: '600'
    lineHeight: '1.3'
  body-lg:
    fontFamily: Inter
    fontSize: 18px
    fontWeight: '400'
    lineHeight: '1.6'
  body-md:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: '1.6'
  label-caps:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '600'
    lineHeight: '1.0'
    letterSpacing: 0.1em
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  unit: 8px
  container-max: 1280px
  gutter: 24px
  margin-desktop: 64px
  margin-mobile: 20px
---

## Brand & Style
The design system embodies "Artisanal Luxury." It bridges the gap between raw organic nature and high-end editorial sophistication. Drawing inspiration from modern Scandinavian interiors and Apple’s industrial design, the interface prioritizes clarity, tactile smoothness, and a sense of "quiet wealth."

The aesthetic is **Minimalist with a Glassmorphic layer**, utilizing generous whitespace to allow product photography to breathe. The emotional goal is to evoke trust, purity, and the sensory indulgence of premium cashews. Interactions should feel deliberate, weighted, and smooth, moving away from frantic digital patterns toward a calm, gallery-like experience.

## Colors
The palette is rooted in the earth but refined through a luxury lens. 

- **Primary Background (#FDFBF7):** A breathable, off-white "Cream" that prevents eye strain and feels more organic than pure white.
- **Secondary Background (#F5E6D3):** "Cashew Beige," used for section blocking and subtle depth.
- **Typography & Details (#3C2A21):** "Dark Brown" replaces pure black to maintain warmth and an organic feel while ensuring high accessibility.
- **Accents:** "Muted Gold" is reserved for high-value calls to action and premium badges. "Deep Forest Green" is used sparingly to signify organic certification and natural origins.

## Typography
The typography strategy pairs editorial elegance with functional clarity. **Playfair Display** provides the high-contrast, sophisticated "Voice" of the brand, used for all major storytelling headings.

**Inter** serves as the "System" font, handling all functional data, body copy, and UI labels. To maintain the luxury feel, headings should utilize generous tracking (letter spacing) when in uppercase, while body copy remains tight and legible. Line heights are intentionally airy to support the Scandinavian minimal layout.

## Layout & Spacing
The design system follows a **Fixed-Fluid Hybrid Grid**. On desktop, content is contained within a 1280px maximum width to ensure readability, while background elements (like glassmorphic sections) may bleed to the edges.

A strict 8px rhythm governs all internal spacing. Layouts should favor "Asymmetric Balance"—grouping text to one side while allowing product imagery to occupy the majority of the visual field. 

**Breakpoints:**
- **Desktop (1200px+):** 12 columns, 64px margins. 
- **Tablet (768px - 1199px):** 8 columns, 40px margins.
- **Mobile (Under 767px):** 4 columns, 20px margins. Headlines scale down significantly to maintain visual hierarchy without breaking words.

## Elevation & Depth
Depth is created through "Material Logic" rather than traditional heavy shadows. 

1.  **Glassmorphism:** Navigation bars and floating product cards use a backdrop filter (`blur: 12px`) with a high-transparency off-white fill (`rgba(253, 251, 247, 0.7)`).
2.  **Soft Ambient Shadows:** Instead of dark shadows, use low-opacity, large-radius blurs tinted with the Dark Brown palette color to simulate natural, soft lighting.
3.  **Tonal Stacking:** Use the Cashew Beige (#F5E6D3) to lift elements off the Cream (#FDFBF7) background without needing any shadow at all.

## Shapes
The shape language is "Organic Geometric." Elements use a base 0.5rem (8px) corner radius to feel approachable and smooth, echoing the curved nature of a cashew nut. 

- **Standard Elements:** 8px (Buttons, Input Fields).
- **Large Containers:** 16px (Product Cards, Modal windows).
- **Interactive Triggers:** Smaller buttons or tags may use 24px (Pill-shape) to distinguish them from structural containers.

## Components

### Buttons
- **Primary:** Dark Brown (#3C2A21) background with Cream text. Sharp, precise corners (8px) and a subtle "Gold" border on hover.
- **Secondary:** Thin 1px border in Dark Brown, no background fill. High-transparency beige hover state.

### Cards
- Utilizes the glassmorphic style for product listings. Borders are 0.5px "Gold" at 30% opacity to give a metallic, premium glimmer when scrolling.

### Form Fields
- Minimalist design: Bottom-border only or very light "Soft Gray" outlines. Floating labels using the `label-caps` typography style to maintain a clean, architectural look.

### Trust Badges
- Certification icons (Organic, Fair Trade) should be rendered in "Deep Forest Green" or "Muted Gold" as monochromatic line-art to avoid clashing with product photography.

### Sticky Navigation
- A persistent glassmorphic bar at the top of the viewport with a subtle 1px bottom border in #E5E7EB. The logo remains centered to anchor the Scandinavian symmetry.