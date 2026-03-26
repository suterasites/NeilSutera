# CLAUDE.md - Neil Sutera Life Coaching

## Business Context

**Business Name:** Neil Sutera
**Email:** info@neilsutera.com
**Phone:** +61 407 485 408
**Location:** Melbourne, Australia
**Copyright:** 2026

### About
- Melbourne-based life coach helping people transform their lives
- Core philosophy centres on "the three realms" - Health, Relationships, and Money
- When these three areas are aligned, people experience clarity and purpose. When they're out of balance, people feel fragmented
- Approach blends psychology, self-awareness, and practical action
- Focused on helping people close the gap between who they are now and who they want to become
- Melbourne is the primary service area - use this for local SEO targeting (e.g. "life coach Melbourne", "personal development coaching Melbourne")
- Target market: individuals seeking personal transformation, professionals wanting clarity, people navigating major life decisions, and corporate teams

### Services

**Your Future Self - 12-Week Intensive Program**
- Structured 12-week coaching program
- Designed for people ready to make meaningful change in a focused timeframe
- Works across the three realms (Health, Relationships, Money) to create alignment

**Wisdom For Life - 12-Month Deep Transformation Program**
- Long-term, deep transformation over 12 months
- For people committed to sustained, fundamental change
- Comprehensive work across all three realms with ongoing support

**Breakthrough Coaching Sessions**
- One-off sessions for people dealing with specific challenges or decisions
- Targeted support for immediate clarity on a particular issue
- Entry point for people not ready for a full program commitment

**Estate Planning Guidance**
- Helping Australians ensure assets go to the right people
- Practical guidance on estate planning decisions
- Complementary to the broader life coaching work (Money realm)

**Corporate Workshops**
- Focused on emotional intelligence and authentic communication
- Designed for teams and organisations
- Leadership development and workplace culture improvement

**Speaking & Writing**
- Speaking engagements on personal development and leadership
- Written content on personal growth, self-awareness, and the three realms

### CTAs and Navigation
- Multiple calls to action directing visitors to book a session or learn more via contact page

---

## Always Do First
- **Invoke the `frontend-design` skill** before writing any frontend code, every session, no exceptions.

## Reference Images
- If a reference image is provided: match layout, spacing, typography, and color exactly. Swap in placeholder content (images via `https://placehold.co/`, generic copy). Do not improve or add to the design.
- If no reference image: design from scratch with high craft (see guardrails below).
- Screenshot your output, compare against reference, fix mismatches, re-screenshot. Do at least 2 comparison rounds. Stop only when no visible differences remain or user says so.

## Local Server
- **Always serve on localhost** - never screenshot a `file:///` URL.
- Start the dev server: `node serve.mjs` (serves the project root at `http://localhost:3000`)
- `serve.mjs` lives in the project root. Start it in the background before taking any screenshots.
- If the server is already running, do not start a second instance.

## Screenshot Workflow
- Puppeteer is installed at `C:/Users/nateh/AppData/Local/Temp/puppeteer-test/`. Chrome cache is at `C:/Users/nateh/.cache/puppeteer/`.
- **Always screenshot from localhost:** `node screenshot.mjs http://localhost:3000`
- Screenshots are saved automatically to `./temporary screenshots/screenshot-N.png` (auto-incremented, never overwritten).
- Optional label suffix: `node screenshot.mjs http://localhost:3000 label` → saves as `screenshot-N-label.png`
- `screenshot.mjs` lives in the project root. Use it as-is.
- After screenshotting, read the PNG from `temporary screenshots/` with the Read tool - Claude can see and analyze the image directly.
- When comparing, be specific: "heading is 32px but reference shows ~24px", "card gap is 16px but should be 24px"
- Check: spacing/padding, font size/weight/line-height, colors (exact hex), alignment, border-radius, shadows, image sizing

## Output Defaults
- Single `index.html` file, all styles inline, unless user says otherwise
- Tailwind CSS via CDN: `<script src="https://cdn.tailwindcss.com"></script>`
- Placeholder images: `https://placehold.co/WIDTHxHEIGHT`
- Mobile-first responsive

## Brand Assets
- Always check the `brand_assets/` folder before designing. It may contain logos, color guides, style guides, or images.
- If assets exist there, use them. Do not use placeholders where real assets are available.
- If a logo is present, use it. If a color palette is defined, use those exact values - do not invent brand colors.

## Anti-Generic Guardrails
- **Colors:** Never use default Tailwind palette (indigo-500, blue-600, etc.). Pick a custom brand color and derive from it.
- **Shadows:** Never use flat `shadow-md`. Use layered, color-tinted shadows with low opacity.
- **Typography:** Never use the same font for headings and body. Pair a display/serif with a clean sans. Apply tight tracking (`-0.03em`) on large headings, generous line-height (`1.7`) on body.
- **Gradients:** Layer multiple radial gradients. Add grain/texture via SVG noise filter for depth.
- **Animations:** Only animate `transform` and `opacity`. Never `transition-all`. Use spring-style easing.
- **Interactive states:** Every clickable element needs hover, focus-visible, and active states. No exceptions.
- **Images:** Add a gradient overlay (`bg-gradient-to-t from-black/60`) and a color treatment layer with `mix-blend-multiply`.
- **Icons:** Use icons sparingly. Do not scatter icons throughout the page - only use them where they add genuine clarity (e.g. contact details, navigation). Prefer clean typography and whitespace over decorative icons.
- **Spacing:** Use intentional, consistent spacing tokens - not random Tailwind steps.
- **Depth:** Surfaces should have a layering system (base → elevated → floating), not all sit at the same z-plane.

## Deployment
- **Always deploy changes to GitHub and Cloudflare Pages** after making code changes. This must happen automatically at the end of every task without the user needing to ask.
- **Remote:** `origin` is set to `https://github.com/suterasites/AcceleratePerformanceFootball.git`
- Push to `main` branch. Cloudflare Pages auto-deploys from the repo.
- After completing any code changes, stage the modified files, commit with a clear message, and `git push` to deploy.

## Multi-Page Consistency
- **Navbar:** The navbar must be identical across all pages. If the navbar is modified on any page, apply the same change to every other page immediately.
- **Footer:** The footer must be identical across all pages. If the footer is modified on any page, apply the same change to every other page immediately.
- **Internal links:** All text links that reference a page on the site must link to the correct page URL. When a new page is created, scan all existing pages and update any mentions of that topic to link to the new page.

## Hard Rules
- Do not add sections, features, or content not in the reference
- Do not "improve" a reference design - match it
- Do not stop after one screenshot pass
- Do not use `transition-all`
- Do not use default Tailwind blue/indigo as primary color
- Do not use em dashes (—) anywhere in content, code, or comments. Use hyphens (-), commas, or periods instead
