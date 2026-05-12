"""
Neil Sutera site - Phase 3a SEO injection.

Idempotent. Run once or many times.

Adds, per page:
- Twitter Card meta + og:image:width/height/alt + geo meta (wrapped in OG_TWITTER_START/END)
- Consolidated @graph JSON-LD: LocalBusiness + WebSite + BreadcrumbList + page-type node
  (wrapped in JSONLD_START/END, replaces any prior JSON-LD blocks)
- Skip-to-content link as first body child
- <main id="main"> wrapper from after </nav> through to before <footer>
- In-body breadcrumb nav above hero on inner pages

Drops:
- legacy <meta name="keywords">
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).parent
SITE = "https://neilsutera.com"

# Page registry: file -> (title, og:image url + dims, page-type schema dict, breadcrumb trail or None)
# Breadcrumb trail: list of (label, url) excluding Home (added implicitly)

OG_IMAGE = f"{SITE}/images/og-share.jpg"
OG_IMAGE_W = "1200"
OG_IMAGE_H = "630"

PAGES = {
    "index.html": {
        "url": f"{SITE}/",
        "page_type": None,  # home: WebSite + LocalBusiness only
        "breadcrumb": None,
    },
    "about.html": {
        "url": f"{SITE}/about.html",
        "page_type": {"@type": "AboutPage", "name": "About Neil Sutera"},
        "breadcrumb": [("About", f"{SITE}/about.html")],
    },
    "my-story.html": {
        "url": f"{SITE}/my-story.html",
        "page_type": {"@type": "AboutPage", "name": "My Story"},
        "breadcrumb": [("My Story", f"{SITE}/my-story.html")],
    },
    "coaching.html": {
        "url": f"{SITE}/coaching.html",
        "page_type": {"@type": "CollectionPage", "name": "Coaching Pathways"},
        "breadcrumb": [("Coaching", f"{SITE}/coaching.html")],
    },
    "your-future-self-12-week-individual-program.html": {
        "url": f"{SITE}/your-future-self-12-week-individual-program.html",
        "page_type": {
            "@type": "Service",
            "name": "Your Future Self - 12-Week Coaching Program",
            "serviceType": "Life Coaching",
            "provider": {"@id": f"{SITE}/#business"},
            "areaServed": [{"@type": "Place", "name": "Melbourne"}, {"@type": "Place", "name": "Victoria"}],
        },
        "breadcrumb": [("Coaching", f"{SITE}/coaching.html"), ("Your Future Self", f"{SITE}/your-future-self-12-week-individual-program.html")],
    },
    "wisdom-for-life-12-month-transformational-program.html": {
        "url": f"{SITE}/wisdom-for-life-12-month-transformational-program.html",
        "page_type": {
            "@type": "Service",
            "name": "Wisdom for Life - 12-Month Coaching Program",
            "serviceType": "Life Coaching",
            "provider": {"@id": f"{SITE}/#business"},
            "areaServed": [{"@type": "Place", "name": "Melbourne"}, {"@type": "Place", "name": "Victoria"}],
        },
        "breadcrumb": [("Coaching", f"{SITE}/coaching.html"), ("Wisdom for Life", f"{SITE}/wisdom-for-life-12-month-transformational-program.html")],
    },
    "1-1-coaching-deep-work-for-real-change.html": {
        "url": f"{SITE}/1-1-coaching-deep-work-for-real-change.html",
        "page_type": {
            "@type": "Service",
            "name": "Breakthrough Coaching - One-off Session",
            "serviceType": "Life Coaching",
            "provider": {"@id": f"{SITE}/#business"},
            "areaServed": [{"@type": "Place", "name": "Melbourne"}, {"@type": "Place", "name": "Victoria"}],
        },
        "breadcrumb": [("Coaching", f"{SITE}/coaching.html"), ("Breakthrough Coaching", f"{SITE}/1-1-coaching-deep-work-for-real-change.html")],
    },
    "estate-planning.html": {
        "url": f"{SITE}/estate-planning.html",
        "page_type": {
            "@type": "Service",
            "name": "Estate Planning Guidance",
            "serviceType": "Estate Planning Guidance",
            "provider": {"@id": f"{SITE}/#business"},
            "areaServed": {"@type": "Country", "name": "Australia"},
        },
        "breadcrumb": [("Estate Planning", f"{SITE}/estate-planning.html")],
    },
    "other-services.html": {
        "url": f"{SITE}/other-services.html",
        "page_type": {"@type": "CollectionPage", "name": "Other Services"},
        "breadcrumb": [("Other Services", f"{SITE}/other-services.html")],
    },
    "speaking-engagements-writing.html": {
        "url": f"{SITE}/speaking-engagements-writing.html",
        "page_type": {
            "@type": "Service",
            "name": "Speaking Engagements and Writing",
            "serviceType": "Speaking Engagements",
            "provider": {"@id": f"{SITE}/#business"},
            "areaServed": [{"@type": "Place", "name": "Melbourne"}, {"@type": "Place", "name": "Victoria"}, {"@type": "Country", "name": "Australia"}],
        },
        "breadcrumb": [("Other Services", f"{SITE}/other-services.html"), ("Speaking and Writing", f"{SITE}/speaking-engagements-writing.html")],
    },
    "workshops-corporate-programs.html": {
        "url": f"{SITE}/workshops-corporate-programs.html",
        "page_type": {
            "@type": "Service",
            "name": "Corporate Workshops and Programs",
            "serviceType": "Corporate Workshops",
            "provider": {"@id": f"{SITE}/#business"},
            "areaServed": [{"@type": "Place", "name": "Melbourne"}, {"@type": "Place", "name": "Victoria"}, {"@type": "Country", "name": "Australia"}],
        },
        "breadcrumb": [("Other Services", f"{SITE}/other-services.html"), ("Workshops and Programs", f"{SITE}/workshops-corporate-programs.html")],
    },
    "here-i-am.html": {
        "url": f"{SITE}/here-i-am.html",
        "page_type": {
            "@type": "Book",
            "name": "Here I Am",
            "author": {"@id": f"{SITE}/#person"},
            "bookFormat": "https://schema.org/Paperback",
            "inLanguage": "en-AU",
        },
        "breadcrumb": [("Here I Am", f"{SITE}/here-i-am.html")],
    },
    "contact-discovery-call.html": {
        "url": f"{SITE}/contact-discovery-call.html",
        "page_type": {"@type": "ContactPage", "name": "Book a Discovery Call"},
        "breadcrumb": [("Book a Discovery Call", f"{SITE}/contact-discovery-call.html")],
    },
}

BUSINESS_CORE = {
    "@type": "ProfessionalService",
    "@id": f"{SITE}/#business",
    "name": "Neil Sutera",
    "alternateName": "Neil Sutera Life Coaching",
    "description": "Melbourne-based life coach helping people transform across the three realms - Health, Relationships, and Money.",
    "url": SITE,
    "telephone": "+61407485408",
    "email": "info@neilsutera.com",
    "image": OG_IMAGE,
    "logo": f"{SITE}/brand_assets/logo-monogram.svg",
    "address": {
        "@type": "PostalAddress",
        "addressLocality": "Melbourne",
        "addressRegion": "VIC",
        "addressCountry": "AU",
    },
    "geo": {"@type": "GeoCoordinates", "latitude": "-37.8136", "longitude": "144.9631"},
    "areaServed": [
        {"@type": "Place", "name": "Melbourne"},
        {"@type": "Place", "name": "Victoria"},
    ],
    "serviceType": [
        "Life Coaching",
        "Personal Development Coaching",
        "Corporate Workshops",
        "Estate Planning Guidance",
        "Speaking Engagements",
    ],
    "priceRange": "$$",
    "openingHoursSpecification": {
        "@type": "OpeningHoursSpecification",
        "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
        "opens": "09:00",
        "closes": "17:00",
    },
}

PERSON_CORE = {
    "@type": "Person",
    "@id": f"{SITE}/#person",
    "name": "Neil Sutera",
    "jobTitle": "Life Coach",
    "url": SITE,
    "image": OG_IMAGE,
    "worksFor": {"@id": f"{SITE}/#business"},
    "address": {
        "@type": "PostalAddress",
        "addressLocality": "Melbourne",
        "addressRegion": "VIC",
        "addressCountry": "AU",
    },
}

WEBSITE_CORE = {
    "@type": "WebSite",
    "@id": f"{SITE}/#website",
    "url": f"{SITE}/",
    "name": "Neil Sutera",
    "inLanguage": "en-AU",
    "publisher": {"@id": f"{SITE}/#business"},
}


def build_breadcrumb(trail):
    items = [{"@type": "ListItem", "position": 1, "name": "Home", "item": f"{SITE}/"}]
    for i, (label, url) in enumerate(trail, start=2):
        items.append({"@type": "ListItem", "position": i, "name": label, "item": url})
    return {"@type": "BreadcrumbList", "itemListElement": items}


def extract_meta(html, name_or_prop, value_attr=None):
    # Returns content of <meta name="..." content="..."> or property variant
    pattern = rf'<meta\s+(?:name|property)="{re.escape(name_or_prop)}"\s+content="([^"]*)"'
    m = re.search(pattern, html, re.IGNORECASE)
    return m.group(1) if m else None


def build_graph(filename):
    cfg = PAGES[filename]
    nodes = [BUSINESS_CORE, PERSON_CORE, WEBSITE_CORE]
    if cfg["breadcrumb"] is not None:
        nodes.append(build_breadcrumb(cfg["breadcrumb"]))
    if cfg["page_type"]:
        pt = dict(cfg["page_type"])
        # Add @id and url for page-type node
        pt.setdefault("@id", cfg["url"] + "#page")
        pt.setdefault("url", cfg["url"])
        nodes.append(pt)
    import json
    return json.dumps({"@context": "https://schema.org", "@graph": nodes}, indent=2)


# Markers
OG_START = "<!-- OG_TWITTER_START -->"
OG_END = "<!-- OG_TWITTER_END -->"
JSONLD_START = "<!-- JSONLD_START -->"
JSONLD_END = "<!-- JSONLD_END -->"
BC_START = "<!-- BREADCRUMBS_START -->"
BC_END = "<!-- BREADCRUMBS_END -->"
SKIP_START = "<!-- SKIP_LINK_START -->"
SKIP_END = "<!-- SKIP_LINK_END -->"
MAIN_START = "<!-- MAIN_OPEN -->"
MAIN_END_C = "<!-- MAIN_CLOSE -->"


def strip_block(html, start, end):
    pattern = re.escape(start) + r".*?" + re.escape(end) + r"\n?"
    return re.sub(pattern, "", html, flags=re.DOTALL)


def inject_og_twitter_geo(html, page_url, page_title, page_desc):
    # Remove any existing block first
    html = strip_block(html, OG_START, OG_END)
    block = f"""{OG_START}
  <meta property="og:image:width" content="{OG_IMAGE_W}">
  <meta property="og:image:height" content="{OG_IMAGE_H}">
  <meta property="og:image:alt" content="Neil Sutera - Life Coach Melbourne">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{page_title}">
  <meta name="twitter:description" content="{page_desc}">
  <meta name="twitter:image" content="{OG_IMAGE}">
  <meta name="twitter:image:alt" content="Neil Sutera - Life Coach Melbourne">
  <meta name="geo.region" content="AU-VIC">
  <meta name="geo.placename" content="Melbourne">
  <meta name="ICBM" content="-37.8136, 144.9631">
  {OG_END}
"""
    # Insert after the og:locale meta line
    pattern = r'(<meta\s+property="og:locale"[^>]*>)\n'
    if re.search(pattern, html):
        html = re.sub(pattern, r"\1\n" + block, html, count=1)
    else:
        # Fallback: insert before </head>
        html = html.replace("</head>", block + "</head>")
    return html


def drop_keywords(html):
    return re.sub(r'\s*<meta\s+name="keywords"[^>]*>\n?', "\n", html, flags=re.IGNORECASE)


def inject_jsonld(html, filename):
    # Remove any existing JSON-LD block (with or without our markers)
    html = strip_block(html, JSONLD_START, JSONLD_END)
    # Strip any standalone <script type="application/ld+json"> ... </script>
    html = re.sub(
        r'\s*<script\s+type="application/ld\+json">.*?</script>\n?',
        "\n",
        html,
        flags=re.DOTALL | re.IGNORECASE,
    )
    graph_json = build_graph(filename)
    block = f"""{JSONLD_START}
  <script type="application/ld+json">
{graph_json}
  </script>
  {JSONLD_END}
"""
    # Insert just before </head>
    html = re.sub(r"(\s*)</head>", "\n  " + block + r"\1</head>", html, count=1)
    return html


def inject_skip_link(html):
    html = strip_block(html, SKIP_START, SKIP_END)
    block = f"""{SKIP_START}
  <a href="#main" class="sr-only focus:not-sr-only focus:fixed focus:top-4 focus:left-4 focus:z-[100] focus:bg-brand-charcoal focus:text-white focus:px-4 focus:py-2 focus:rounded">Skip to main content</a>
  {SKIP_END}"""
    # Insert immediately after <body...>
    html = re.sub(r"(<body[^>]*>)", r"\1\n  " + block, html, count=1)
    return html


def wrap_main(html):
    # Idempotent: only insert markers if not already present
    if MAIN_START in html and MAIN_END_C in html:
        return html
    # Open <main id="main"> after first </nav>
    html = re.sub(r"(</nav>)\n", r"\1\n\n  " + MAIN_START + '\n  <main id="main">\n', html, count=1)
    # Close </main> before <footer (the first occurrence after the open marker)
    html = re.sub(r"\n(\s*<footer)", "\n  </main>\n  " + MAIN_END_C + r"\n\1", html, count=1)
    return html


def inject_breadcrumbs(html, filename):
    cfg = PAGES[filename]
    if cfg["breadcrumb"] is None:
        return html  # no breadcrumb on home
    html = strip_block(html, BC_START, BC_END)
    trail = cfg["breadcrumb"]
    # Build visual breadcrumb list
    parts = ['<a href="' + SITE + '/" class="hover:text-brand-charcoal transition-colors">Home</a>']
    for i, (label, url) in enumerate(trail):
        if i == len(trail) - 1:
            parts.append(f'<span aria-current="page" class="text-brand-charcoal">{label}</span>')
        else:
            parts.append(f'<a href="{url}" class="hover:text-brand-charcoal transition-colors">{label}</a>')
    sep = '<span class="text-brand-warm/60" aria-hidden="true">/</span>'
    inner = ("\n      " + sep + "\n      ").join(parts)
    block = f"""{BC_START}
  <nav aria-label="Breadcrumb" class="bg-brand-cream pt-24 lg:pt-28">
    <div class="max-w-7xl mx-auto px-6 lg:px-8 py-3 flex items-center gap-2 text-sm text-brand-warm">
      {inner}
    </div>
  </nav>
  {BC_END}
"""
    # Insert directly after the MAIN_START marker line
    if MAIN_START in html:
        html = html.replace(MAIN_START + '\n  <main id="main">\n',
                            MAIN_START + '\n  <main id="main">\n  ' + block, 1)
    return html


def process(path: Path):
    html = path.read_text(encoding="utf-8")
    title = extract_meta(html, "og:title") or ""
    desc = extract_meta(html, "og:description") or ""
    page_url = PAGES[path.name]["url"]
    html = drop_keywords(html)
    html = inject_og_twitter_geo(html, page_url, title, desc)
    html = inject_jsonld(html, path.name)
    html = inject_skip_link(html)
    html = wrap_main(html)
    html = inject_breadcrumbs(html, path.name)
    path.write_text(html, encoding="utf-8")
    print(f"OK  {path.name}")


def main():
    for fname in PAGES:
        p = ROOT / fname
        if not p.exists():
            print(f"SKIP {fname} (missing)")
            continue
        process(p)


if __name__ == "__main__":
    main()
