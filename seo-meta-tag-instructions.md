# SEO meta tag optimisation — neilsutera.com

## Context

The site is currently near-invisible on Google. Over the last 3 months it received only 16 impressions and 5 clicks total. The Google Search Console "Queries" report is completely empty, meaning Google isn't associating the site with any searchable terms. Searching "neil sutera life coach melbourne" returns zero results for neilsutera.com.

The most impactful first step is optimising the meta title and description tags on every page so Google knows what the site is about and can match it to relevant searches.

---

## Homepage

### Title tag (keep under 60 characters)

```
Neil Sutera | Life Coach Melbourne — Personal Transformation
```

### Meta description (keep under 155 characters)

```
Melbourne life coach helping you align health, relationships, and money. Explore the 12-week Your Future Self program or book a free discovery call today.
```

### Implementation

Add or update these two tags inside the `<head>` of the homepage:

```html
<title>Neil Sutera | Life Coach Melbourne — Personal Transformation</title>
<meta name="description" content="Melbourne life coach helping you align health, relationships, and money. Explore the 12-week Your Future Self program or book a free discovery call today.">
```

---

## Service pages

Each service page needs its own unique title and description. If these pages don't exist yet, they should be created as separate pages (not just sections on the homepage). Here are the recommended tags for each:

### Your Future Self — 12-week program

```html
<title>Your Future Self Program | 12-Week Life Coaching — Neil Sutera</title>
<meta name="description" content="A focused 12-week coaching program for personal transformation. Align your health, relationships, and finances with clarity and purpose. Melbourne-based, online available.">
```

### Wisdom for Life — 12-month program

```html
<title>Wisdom for Life Program | 12-Month Deep Coaching — Neil Sutera</title>
<meta name="description" content="An immersive 12-month coaching journey for lasting personal change. Go deeper into self-awareness, resilience, and life alignment with Neil Sutera in Melbourne.">
```

### Breakthrough coaching

```html
<title>Breakthrough Coaching Melbourne | Overcome Challenges — Neil Sutera</title>
<meta name="description" content="Stuck on a specific challenge or recurring life issue? Breakthrough coaching with Neil Sutera helps you get clarity and move forward. Book a free discovery call.">
```

### Estate planning

```html
<title>Estate Planning Help Australia | Get Proactive — Neil Sutera</title>
<meta name="description" content="Ensure the right assets go to the right people at the right time. Neil Sutera helps Australian residents get proactive about estate planning. Not financial or legal advice.">
```

### Corporate workshops and speaking

```html
<title>Corporate Workshops & Speaking | Leadership & Resilience — Neil Sutera</title>
<meta name="description" content="Tailored workshops for organisations on communication, resilience, and emotional intelligence. Book Neil Sutera for your next corporate event or speaking engagement.">
```

### Book — "Here I Am"

```html
<title>Here I Am — Book by Neil Sutera | Personal Development</title>
<meta name="description" content="Discover 'Here I Am' by Neil Sutera. A book on personal transformation blending psychology, self-awareness, and practical action for a more purposeful life.">
```

---

## Additional SEO tags to add on every page

### Open Graph tags (for social sharing)

Add these to the `<head>` of every page, updating the content values per page:

```html
<meta property="og:type" content="website">
<meta property="og:site_name" content="Neil Sutera">
<meta property="og:title" content="[same as title tag]">
<meta property="og:description" content="[same as meta description]">
<meta property="og:url" content="https://neilsutera.com/[page-path]">
<meta property="og:image" content="https://neilsutera.com/images/og-share.jpg">
```

Create an OG image (`og-share.jpg`) at 1200×630px with Neil's name, title ("Life Coach Melbourne"), and branding.

### Canonical URL

Add a canonical tag to every page to prevent duplicate content issues:

```html
<link rel="canonical" href="https://neilsutera.com/[page-path]">
```

### Structured data (JSON-LD)

Add this to the homepage `<head>` to help Google understand the business:

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "ProfessionalService",
  "name": "Neil Sutera — Life Coach",
  "description": "Melbourne-based life coach focused on personal transformation across health, relationships, and money.",
  "url": "https://neilsutera.com",
  "telephone": "[phone number]",
  "address": {
    "@type": "PostalAddress",
    "addressLocality": "Melbourne",
    "addressRegion": "VIC",
    "addressCountry": "AU"
  },
  "geo": {
    "@type": "GeoCoordinates",
    "latitude": "[latitude]",
    "longitude": "[longitude]"
  },
  "sameAs": [
    "[LinkedIn URL]",
    "[Facebook URL]",
    "[Instagram URL]"
  ],
  "priceRange": "$$",
  "openingHoursSpecification": {
    "@type": "OpeningHoursSpecification",
    "dayOfWeek": ["Monday","Tuesday","Wednesday","Thursday","Friday"],
    "opens": "09:00",
    "closes": "17:00"
  }
}
</script>
```

Replace placeholder values (`[phone number]`, `[latitude]`, URLs) with real data.

---

## On-page content requirements

Meta tags alone won't rank if the page body doesn't support them. Make sure the homepage includes these elements in visible text (not hidden or image-only):

1. **H1 heading** containing "Life Coach Melbourne" or a close variant (only one H1 per page)
2. **A paragraph early on the page** that naturally mentions: life coaching, Melbourne, personal transformation, health, relationships, and money
3. **H2 headings** for each service section (e.g. "12-Week Coaching Program", "Breakthrough Coaching", "Corporate Workshops")
4. **A clear call-to-action** mentioning the free discovery call with a link/button
5. **Alt text on all images** that describes what's shown and includes relevant terms where natural (e.g. `alt="Neil Sutera, life coach based in Melbourne"`)

---

## Technical checklist

- [ ] Every page has a unique title tag (no duplicates across pages)
- [ ] Every page has a unique meta description (no duplicates)
- [ ] No title tag exceeds 60 characters
- [ ] No meta description exceeds 155 characters
- [ ] Canonical URLs are set on all pages
- [ ] Open Graph tags are present on all pages
- [ ] JSON-LD structured data is on the homepage
- [ ] All images have descriptive alt text
- [ ] The site has a `sitemap.xml` submitted to Google Search Console
- [ ] The site has a `robots.txt` that doesn't block important pages
