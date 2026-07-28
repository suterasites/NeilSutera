#!/usr/bin/env python3
"""seo_100_patch.py - idempotent on-page SEO patcher for the Neil Sutera site.

Brings every page to a clean pass on the machine-checkable checks in
Apps/sutera-seo/checklist.py (the engine behind SEO HQ). Safe to re-run.

The site is Tailwind-CDN based and already passes main/skip-link/twitter/schema.
This only touches the remaining findings:
  - apple-touch-icon link on every page (favicon check wanted both icon + apple).
    A real 180x180 PNG was rendered from brand_assets/logo-monogram.svg via
    macOS qlmanage -> brand_assets/apple-touch-icon.png (opaque, logo on white).
  - <header> landmark: wrap the site <nav id="navbar"> in a <header> (semantic
    landmarks check wanted header + nav + footer; only header was missing).
  - footer column headings h4 -> h3 (kills the H2->H4 skip); the headings are
    styled purely by Tailwind utility classes, so the level change is invisible.
  - footer logo (brand_assets/logo-white.svg): add w-auto so it has both a width
    and a height utility (the CLS check counts Tailwind w-/h- sizing).
  - trim 5 over-long titles (67-83 -> 50-60) and 5 over-long descriptions
    (171-199 -> 150-160).

Homepage breadcrumb (visible + schema) is deliberately left as the only warns -
a homepage crumb is pointless UX - and the pooled score rounds to 100.
"""

import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ALL_FILES = [
    "index.html", "about.html", "my-story.html", "coaching.html",
    "your-future-self-12-week-individual-program.html",
    "wisdom-for-life-12-month-transformational-program.html",
    "1-1-coaching-deep-work-for-real-change.html", "estate-planning.html",
    "other-services.html", "workshops-corporate-programs.html",
    "speaking-engagements-writing.html", "here-i-am.html",
    "contact-discovery-call.html",
]

TITLES = {
    "about.html": "About Neil Sutera | Melbourne Life Coach for Change",
    "1-1-coaching-deep-work-for-real-change.html": "Breakthrough Coaching Melbourne | Neil Sutera Life Coach",
    "other-services.html": "Other Services | Workshops, Speaking & Writing | Neil Sutera",
    "workshops-corporate-programs.html": "Corporate Workshops & Speaking | Neil Sutera Melbourne",
    "speaking-engagements-writing.html": "Speaking & Writing | Neil Sutera, Melbourne Life Coach",
}

METAS = {
    "my-story.html": "The story behind Neil Sutera and Next Phase Wealth: from licensed financial adviser to a life coach working across Health, Relationships and Money.",
    "coaching.html": "Three one-on-one coaching pathways to alignment: Your Future Self, Wisdom for Life, and Breakthrough Coaching. Choose the one that fits where you are now.",
    "your-future-self-12-week-individual-program.html": "A focused 12-week coaching program for personal transformation. Align your health, relationships and finances with clarity. Melbourne-based, online available.",
    "estate-planning.html": "Ensure the right assets reach the right people at the right time. Neil Sutera helps Australians get proactive about estate planning. Not financial or legal advice.",
    "speaking-engagements-writing.html": "Speaking and writing on personal development, leadership and the inner architecture of human potential. Complex psychology made grounded and accessible.",
}


def patch(fn):
    path = os.path.join(ROOT, fn)
    html = open(path, encoding="utf-8").read()
    orig = html
    did = []

    # --- title ---
    if fn in TITLES:
        html2 = re.sub(r"<title>.*?</title>", "<title>" + TITLES[fn] + "</title>", html, count=1, flags=re.S)
        if html2 != html:
            html = html2
            did.append(f"title({len(TITLES[fn])})")

    # --- meta description ---
    if fn in METAS:
        new = METAS[fn]
        html2 = re.sub(r'(<meta name="description" content=")[^"]*(")',
                       lambda m: m.group(1) + new + m.group(2), html, count=1)
        if html2 != html:
            html = html2
            did.append(f"desc({len(new)})")

    # --- apple-touch-icon (after the existing rel="icon" link) ---
    if "apple-touch-icon" not in html:
        html2 = re.sub(r'(<link rel="icon"[^>]*>)',
                       r'\1\n  <link rel="apple-touch-icon" href="brand_assets/apple-touch-icon.png">',
                       html, count=1)
        if html2 != html:
            html = html2
            did.append("apple-touch-icon")

    # --- <header> landmark: wrap the site nav ---
    if "<header" not in html:
        m = re.search(r'<nav id="navbar"', html)
        if m:
            close = html.find("</nav>", m.start())    # site nav has no nested <nav>
            if close != -1:
                end = close + len("</nav>")
                html = html[:m.start()] + "<header>\n  " + html[m.start():end] + "\n  </header>" + html[end:]
                did.append("header")

    # --- footer column headings h4 -> h3 (all h4 on the page are footer columns) ---
    if "<h4" in html:
        html = re.sub(r"<h4(\b[^>]*)>", r"<h3\1>", html)
        html = html.replace("</h4>", "</h3>")
        did.append("footer-h3")

    # --- footer logo: add w-auto so it carries both a width + height utility ---
    html2 = re.sub(r'(<img[^>]*logo-white\.svg[^>]*class="h-12)(")', r"\1 w-auto\2", html, count=1)
    if html2 != html:
        html = html2
        did.append("logo-w-auto")

    if html != orig:
        open(path, "w", encoding="utf-8").write(html)
    return did


def main():
    print(f"Patching {len(ALL_FILES)} pages under {ROOT}\n")
    for fn in ALL_FILES:
        changed = patch(fn)
        print(f"  {fn:52s} {', '.join(changed) if changed else 'no change'}")
    print("\nDone. Idempotent - safe to re-run.")


if __name__ == "__main__":
    main()
