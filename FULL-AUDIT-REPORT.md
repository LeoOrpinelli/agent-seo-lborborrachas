# Full SEO Audit Report — lborborrachas.com.br
**Date:** 2026-03-24
**Audited URL:** https://www.lborborrachas.com.br/
**Business:** Lbor Borrachas — Distribuidora e Fabricante de Artefatos de Borracha Industrial
**Market:** Brazil (São Paulo, pt-BR)
**Auditor:** Claude SEO Audit System (claude-sonnet-4-6)

---

## Overall SEO Health Score: 39 / 100 — Needs Significant Work

| Category | Weight | Score | Weighted |
|---|---|---|---|
| Technical SEO | 22% | 54/100 | 11.9 |
| Content Quality & E-E-A-T | 23% | 38/100 | 8.7 |
| On-Page SEO | 20% | 30/100 | 6.0 |
| Schema / Structured Data | 10% | 31/100 | 3.1 |
| Performance (Core Web Vitals) | 10% | 44/100 | 4.4 |
| AI Search Readiness (GEO) | 10% | 31/100 | 3.1 |
| Images | 5% | 35/100 | 1.75 |
| **Total** | **100%** | — | **39 / 100** |

**Supplementary scores (informational):**

| Area | Score |
|---|---|
| Local SEO | 23/100 |
| Sitemap | 54/100 |
| Visual / Mobile | 64/100 |

---

## Business Type Detection

| Signal | Finding |
|---|---|
| Industry | Industrial Rubber Products (Borrachas Industriais) — B2B/B2C supplier |
| Location | São Paulo, SP, Brazil (DDD 11) |
| Model | Distributor + Manufacturer + Retailer hybrid |
| Platform | Custom PHP 7.4 + AngularJS 1.6.9 e-commerce CMS (MGMasters) |
| CDN | Cloudflare (GRU edge — São Paulo) |
| Catalog size | 230 products, 42 categories, 30 blog articles |
| Primary conversion | /cotacao (quote request form) |

---

## Executive Summary — Top 5 Critical Issues

1. **Physical address is completely absent from every page** — the business is invisible to Google's local systems and the local pack is unreachable.
2. **AngularJS 1.6.9 (EOL since December 2021) + PHP 7.4.33 (EOL since November 2022)** — both the frontend framework and server runtime are end-of-life security risks that also carry performance costs.
3. **Zero security headers (HSTS, CSP, X-Frame-Options, X-Content-Type-Options)** — critical security gap with direct implications for user trust signals.
4. **No "Quem Somos" / About page, no CNPJ publicly displayed, no team credentials** — E-E-A-T Trustworthiness failure for a B2B business requesting competitors' CNPJs on its own contact form.
5. **Homepage has ~80 words of editorial content** — the entire page is a product grid with no value proposition, no company narrative, no differentiators; this is the core driver of the 39/100 score.

## Executive Summary — Top 5 Quick Wins

1. **Add physical address to footer** (1 hour): enables GBP association, local pack eligibility, NAP consistency.
2. **Add security headers via Cloudflare** (30 minutes): Transform Rules → add HSTS, X-Content-Type-Options, X-Frame-Options, Referrer-Policy.
3. **Fix schema errors** (2 hours): WebSite `name: ""` → `"Lbor Borrachas"`, SearchAction `&s=` → `?s=`, remove incorrect `TollFree` contactOption.
4. **Add meta description + Open Graph tags to homepage** (30 minutes): one CMS field update that also feeds AI-generated summaries.
5. **Create `/llms.txt`** (1 hour): plain text file, zero coding required, immediately signals AI search readiness to GPTBot, ClaudeBot, PerplexityBot.

---

## 1. Technical SEO — Score: 54/100

### Infrastructure
- **CDN:** Cloudflare with GRU (São Paulo) edge — good
- **HTTPS:** Enforced via 301 — good
- **Compression:** Brotli (`Content-Encoding: br`) — good
- **HTTP/3:** Advertised via `alt-svc` — good
- **HTML cache:** `Cache-Control: no-store` forces all pages through origin — critical performance issue

### Crawlability
- **robots.txt:** Well-formed, correctly blocks `/admin/`, `/modules/`, `/search`, `/tmp/`. Sitemap declared at top.
- **Sitemap:** Accessible at `/sitemap.xml`, 303 URLs, correct XML format — but `lastmod` is dynamic (all today's date) and `changefreq: always` on every URL.
- **Crawl budget:** Wasted by no-cache HTML and unreliable lastmod signals.

### Issues Found

#### CRITICAL

| # | Issue | Detail |
|---|---|---|
| T1 | **3-hop redirect chain** | `http://lborborrachas.com.br/` → `https://lborborrachas.com.br/` → `https://www.lborborrachas.com.br/`. Should be a single 301. Wastes link equity and crawl budget. |
| T2 | **AngularJS 1.6.9 (EOL December 2021)** | SPA framework is end-of-life. JS rendering dependency creates risk for dynamic routes not in initial HTML payload. Search blocked in robots.txt. |
| T3 | **Zero security headers** | No HSTS, CSP, X-Content-Type-Options, X-Frame-Options, Referrer-Policy. HSTS absence leaves users exposed to SSL stripping before redirects fire. |
| T4 | **PHP 7.4.33 EOL + exposed in X-Powered-By** | PHP 7.4 reached end-of-life November 2022. Version string is visible in HTTP headers — set `expose_php = Off` immediately. |

#### HIGH

| # | Issue | Detail |
|---|---|---|
| T5 | **Title tag: "Lbor Borrachas" (14 chars)** | No product keyword, no location, no value proposition. |
| T6 | **Canonical vs og:url trailing-slash mismatch** | Canonical: no trailing slash. og:url: with trailing slash. Sitemap: no trailing slash. Must be consistent. |
| T7 | **WebSite schema: empty name + malformed SearchAction** | `"name": ""` and `target: "...search&s={...}"` (& instead of ?). Disqualifies Sitelinks Searchbox. |
| T8 | **Organization schema: TollFree misclassification** | `(11) 2167-5600` is a São Paulo landline, not a toll-free number. |
| T9 | **No LCP image preload or fetchpriority** | First product card image has no `<link rel="preload">` or `fetchpriority="high"`. |

#### MEDIUM

| # | Issue | Detail |
|---|---|---|
| T10 | **Meta description reads as keyword list** | Pipe-delimited terms, mixed capitalization, no CTA. |
| T11 | **Sitemap: all lastmod = today, changefreq = always, priority = 1.00** | All three values are dynamically generated and ignored by Google. Fix lastmod to real database timestamps. |
| T12 | **Static asset cache TTL: 4 hours** | CSS and JS already use versioned filenames — should be `max-age=31536000, immutable`. |
| T13 | **Numeric IDs in category URL slugs** | `/c/11-lencol-de-borracha` — ID prefix creates link rot risk if categories are reorganized. |

#### LOW

| # | Issue | Detail |
|---|---|---|
| T14 | **`meta name="revisit-after"` (deprecated)** | Ignored by all crawlers since early 2000s — remove. |
| T15 | **No IndexNow** | Not implemented. Low effort, accelerates Bing/Yandex re-indexing. |
| T16 | **Blog on external subdomain** | `blog.lborborrachas.com.br` (currently HTTP 500). Blog equity does not flow to main domain. |
| T17 | **Organization sameAs: empty array** | No social/directory profiles linked for entity corroboration. |

### What Is Working
- HTTPS enforced site-wide
- robots.txt is well-structured
- sitemap.xml accessible and valid format
- `meta robots: index,follow` correctly set
- `lang="pt-br"` on `<html>` element
- Google Search Console verification tag present
- GTM with consent-default-denied pattern (LGPD-aware)
- Alt text present on product images

---

## 2. Content Quality & E-E-A-T — Score: 38/100

### E-E-A-T Assessment

| Factor | Score | Notes |
|---|---|---|
| Experience | 18/40 | No case studies, no client testimonials, no project references. Sales rep names visible in WhatsApp buttons but zero bios or credentials. |
| Expertise | 22/40 | Product descriptions mention Shore A hardness, temperature ranges, polymer types (EPDM, SBR, Neoprene) — demonstrates domain knowledge. But no authorship, no certifications cited. |
| Authoritativeness | 12/40 | No external citations, no trade associations (ABAM, ABNT), no reviews, no social media linked. Blog subdomain returns HTTP 500. |
| Trustworthiness | 28/40 | HTTPS ✓. Phone visible ✓. Multi-channel WhatsApp by department ✓. But: no physical address, no About page (404), no CNPJ publicly displayed, no privacy policy. |

**E-E-A-T Total: 20.5/40 (51%)**

### Content Findings

#### CRITICAL

| # | Issue |
|---|---|
| C1 | **No "Quem Somos" page** — `/sobre`, `/sobre-nos`, `/empresa`, `/quem-somos` all return 404. Zero company history, founding year, team credentials, physical address, or CNPJ visible anywhere. |
| C2 | **Blog completely non-functional** — `blog.lborborrachas.com.br` returns HTTP 500. Footer blog link points to broken URL. A content channel for topical authority is dead. |
| C3 | **Homepage has ~80 words of editorial content** — page is a product grid only. No H1 with substantive text, no value proposition, no industries served, no geographic service area, no differentiators. |

#### HIGH

| # | Issue |
|---|---|
| C4 | **Brand-only title tag** — no keyword targeting |
| C5 | **OG tags incomplete; Twitter Cards absent entirely** — `og:type`, `og:locale` missing; zero Twitter Card tags on any page |
| C6 | **Organization schema `sameAs` empty** — Google cannot corroborate entity identity |
| C7 | **Product page canonical points to category with underscore vs hyphen inconsistency** — `/c/11_lencol-de-borracha` (underscore) vs `/c/11-lencol-de-borracha` (hyphen used in sitemap) |
| C8 | **Sitemap lastmod dynamic** — all dates show today, destroying crawl prioritization signal |

#### MEDIUM

| # | Issue |
|---|---|
| C9 | **Category descriptions ~90–120 words** — well below 600–800 word minimum for competitive B2B pages. All use identical Title Case template pattern. |
| C10 | **No pricing, lead time, or MOQ information** — forces all buyers to submit blind quote requests. Fails user intent satisfaction. |
| C11 | **No LGPD privacy policy** — contact and quote forms collect CNPJ, email, phone — no linked privacy policy anywhere. Legal risk under Lei 13.709/2018. |

### AI Citation Readiness: 18/100
The site has effectively zero citable passages. No definitional paragraphs (134–167 words), no FAQ blocks, no specification tables, no named authors, no publication dates. AI systems cannot extract or attribute content from this site.

---

## 3. On-Page SEO — Score: 30/100

| Element | Finding | Status |
|---|---|---|
| Title tag | "Lbor Borrachas" (14 chars, brand only) | FAIL |
| Meta description | Present but keyword-stuffed list, mixed capitalization | PARTIAL |
| H1 | "Todos os produtos" — zero keyword value | FAIL |
| H2 | None on homepage | FAIL |
| H3 | 24 product category names — correct depth | PASS |
| Heading hierarchy | Flat (H1 → H3, no H2) | FAIL |
| Internal linking | Category → product links present | PASS |
| Breadcrumbs | Absent on all pages | FAIL |
| Local keywords in headings | None | FAIL |
| Open Graph | Partial (og:title, og:description, og:image) | PARTIAL |
| Twitter Cards | Absent entirely | FAIL |
| `lang` attribute | `pt-br` — correct | PASS |
| Viewport meta | Present | PASS |

**Sitemap findings:**
- 303 URLs, good coverage of products/categories/articles
- `/cotacao` (primary conversion page) missing from sitemap
- 5 URL slugs malformed (trailing dashes, fused words: `borrachapara`)
- `<lastmod>` dynamically set to current date on all entries

---

## 4. Schema / Structured Data — Score: 31/100

### Schema Detected

**Homepage JSON-LD — WebSite (broken):**
```json
{
  "@context": "http://schema.org",  // ← should be https://
  "@type": "WebSite",
  "name": "",  // ← EMPTY — critical bug
  "alternateName": "Lbor Borrachas",
  "potentialAction": {
    "target": "https://www.lborborrachas.com.br/search&s={search_term_string}"
    // ← & should be ? — SearchAction non-functional
  }
}
```

**Homepage JSON-LD — Organization (broken):**
```json
{
  "@context": "http://schema.org",  // ← should be https://
  "@type": "Organization",  // ← should be LocalBusiness
  // name: missing entirely
  "contactPoint": [{
    "contactOption": "TollFree"  // ← WRONG — (11) 2167-5600 is a local landline
  }],
  "sameAs": []  // ← empty
}
```

**Category pages — Microdata ItemList (broken):**
- All 55 `ListItem` entries use relative URLs (`/c/11-lencol-de-borracha`) — must be absolute
- All image paths are relative — must be absolute
- One empty `<div itemscope itemtype="...ItemList">` container (generates Search Console error)
- `@context` uses `http://` — must be `https://`

### Schema Error Summary

| Error | Severity |
|---|---|
| `@context` uses `http://` not `https://` on all blocks | Critical |
| WebSite `name`: empty string | Critical |
| SearchAction target: `&s=` instead of `?s=` | Critical |
| Organization: `name` property missing | Critical |
| Organization: `contactOption: TollFree` — factually wrong | Warning |
| Organization: `sameAs` empty array | Warning |
| Microdata: all 55 ListItem URLs are relative | Critical |
| Empty ItemList container on category pages | Error |
| No `LocalBusiness` schema | Critical |
| No `BreadcrumbList` schema anywhere | High |
| No `Product` schema on product pages (230 pages) | Critical |

### Missing Schema Opportunities

| Schema Type | Priority | Impact |
|---|---|---|
| `LocalBusiness` (replace Organization) | Critical | Business panel, local pack, address display |
| `Product` + `Offer` on `/p/` pages | Critical | Product rich results, Shopping eligibility |
| `BreadcrumbList` on all inner pages | High | Breadcrumb trail in SERPs |
| `ItemList` in JSON-LD (replace broken Microdata) | High | Category page rich results |
| `Article` / `BlogPosting` on blog | Medium | Article rich results |
| `FAQPage` on category pages | Medium | AI citation benefit (GEO) |

---

## 5. Performance (Core Web Vitals) — Score: 44/100

### Estimated Core Web Vitals (75th percentile, Brazilian mobile)

| Metric | Estimate | Threshold | Status |
|---|---|---|---|
| LCP | 3.5s – 5.5s | 2.5s good / 4.0s poor | FAIL (Needs Improvement → Poor) |
| INP | 250ms – 400ms | 200ms good / 500ms poor | FAIL (Needs Improvement) |
| CLS | 0.05 – 0.12 | 0.1 good / 0.25 poor | BORDERLINE |

*Verify against real CrUX field data at https://cruxvis.withgoogle.com for authoritative 75th-percentile values.*

### Root Causes

| Issue | Impact | Detail |
|---|---|---|
| HTML not cached (Cache-Control: no-store) | TTFB ~450ms | Forces every anonymous page request through origin. Cloudflare bypasses CDN. |
| Google Fonts `@import` inside CSS | +300–600ms to critical path | Serial waterfall: HTML → CSS → then fonts. Move to `<link>` in `<head>` with `preconnect`. |
| No LCP image preload | Delayed FCP/LCP | LCP image (first product card) not preloaded and has no `fetchpriority="high"`. |
| 51 images, zero lazy loading | Full-page image load | All product category images load on init. Add `loading="lazy"` to below-fold images. |
| 442 KB JS bundle (no defer) | INP 250–400ms | AngularJS 1.6.9 + jQuery 1.9.1 in a single synchronous bundle. Neither deferred. |
| No WebP/AVIF delivery | ~30% excess image size | All images served as PNG/JPG. No content negotiation for modern formats. |
| Static asset TTL: 4 hours | Repeat-visit performance | CSS/JS already use versioned filenames — should be `max-age=31536000, immutable`. |
| Images: no width/height attributes | CLS risk | Browser cannot reserve layout space before images load. |

### Third-Party Script Load

| Script | Load Method | Risk |
|---|---|---|
| Google Tag Manager | `<script>` in `<head>` (async loader) | Fires Ads + consent tags — chain risk |
| Google AdSense | `<script async>` | Causes additional sub-requests at runtime |
| RD Station (CloudFront) | `<script async>` | Returns 13 bytes — likely broken/disabled |
| Cloudflare email decode | `<script data-cfasync="false">` | Loads synchronously before main JS |

---

## 6. Images — Score: 35/100

| Check | Status | Detail |
|---|---|---|
| Alt text present | PASS | All 26+ product category images have alt text |
| Alt text quality | PARTIAL | One image mismatch: Mangueira de Silicone image used for "Perfil de Silicone" category |
| Lazy loading | FAIL | Zero `loading="lazy"` attributes on any image |
| WebP / AVIF delivery | FAIL | All images served as PNG/JPG regardless of browser Accept header |
| Explicit width/height | FAIL | No `<img width="..." height="...">` attributes anywhere |
| LCP image preload | FAIL | No `<link rel="preload">` for first-visible product image |
| fetchpriority | FAIL | No `fetchpriority="high"` on any image |
| Responsive srcset | FAIL | Same image served regardless of viewport size |
| Image compression | PARTIAL | Thumbnails are 240px and moderate size (~15–40 KB each) |

---

## 7. AI Search Readiness (GEO) — Score: 31/100

### AI Crawler Access (robots.txt)
| Crawler | Status |
|---|---|
| GPTBot (ChatGPT) | ALLOWED (no explicit rule) |
| ClaudeBot (Anthropic) | ALLOWED |
| PerplexityBot | ALLOWED |
| Google-Extended (Gemini/AIO) | ALLOWED |
| OAI-SearchBot | ALLOWED |

Crawlers are technically allowed but there is no deliberate AI-readiness signal (`llms.txt`, explicit Allow rules).

### llms.txt
**Status: MISSING (404)** — No `llms.txt` file at the domain root. This is a high-impact, low-effort gap: a well-formed `llms.txt` signals AI readiness and guides crawlers toward high-value pages.

### Citability Score: 22/100
- Zero citable passages (134–167 word definitional blocks required)
- H1 = brand name only; H2 = "Todos os produtos" (navigation label)
- No statistics, no sourced claims, no specification tables
- No FAQ sections on any page
- No named authors, no publication dates
- Blog non-functional (HTTP 500)

### Authority & Brand Signals: 18/100
- Organization JSON-LD present but `sameAs` is empty
- No Wikipedia entity, no CNPJ publicly displayed
- No Google Business Profile linked in schema
- No YouTube presence detectable
- No external citations or industry association membership

### Platform-Specific Readiness

| Platform | Score | Key Gap |
|---|---|---|
| Google AI Overviews (pt-BR) | 28/100 | No FAQ schema, no answer-oriented headings, no meta descriptions on inner pages |
| ChatGPT / SearchGPT | 25/100 | No citable passages, entity not corroborated externally |
| Perplexity AI | 30/100 | SSR helps; zero passage-level content to extract |
| Bing Copilot | 35/100 | SSR + existing schema give slight edge; same content depth gap |

### Competitive GEO Context
GEO maturity among Brazilian B2B industrial rubber suppliers is extremely low in 2026. A site that implements `llms.txt`, FAQ schema, and answer-oriented category content within 60 days is likely to become the default AI-cited source for "borracha industrial São Paulo" queries — the competitive window is open now.

---

## 8. Local SEO — Score: 23/100

### NAP Consistency

| Element | Homepage | Contact Page | Footer | Schema |
|---|---|---|---|---|
| Business Name | Lbor Borrachas ✓ | Lbor Borrachas ✓ | LborBorrachas.com.br | Empty string ✗ |
| Address | MISSING ✗ | MISSING ✗ | MISSING ✗ | MISSING ✗ |
| Phone | (11) 2167-5600 ✓ | (11) 2167-5600 ✓ | MISSING ✗ | +55-11-2167-5600 ✓ |
| Email | [email protected] ✓ | [email protected] ✓ | MISSING ✗ | MISSING ✗ |

**Critical: The full street address (Rua, número, bairro, CEP) is absent from every single page on the site.**

### Google Business Profile Signals
- No Google Maps embed anywhere
- No GBP URL referenced in schema or content
- No review widget or star rating display
- **Score: 0/7 GBP signals detected**

### Local Schema
- `@type: Organization` used instead of `LocalBusiness`
- No `address` (PostalAddress) property
- No `geo` (GeoCoordinates)
- No `openingHoursSpecification`
- `areaServed: "BR"` — too broad for a São Paulo business

### Local Keyword Targeting
Zero local modifiers ("São Paulo", "SP", "ABCD Paulista") found in:
- Any heading tag (H1/H2/H3)
- Meta title
- Product category names
- Meta descriptions

### Location Pages
**Count: 0.** No location-specific landing pages exist. For a São Paulo B2B industrial supplier, pages targeting "borrachas industriais São Paulo" and "distribuidora de borracha SP" are high-priority opportunities.

---

## 9. Visual & Mobile — Score: 64/100

### Above-the-Fold Content

**Desktop (1920×1080):**
- Orange CTA button ("Solicite um orçamento online") — visible ✓
- Search bar — visible ✓
- H1 "Todos os produtos" — visible (but zero keyword value) ✗
- First 4 product category cards — visible ✓

**Mobile (375×812):**
- Three stacked CTA buttons consume first ~300px ✓/✗ (present but pushes products below fold)
- Zero products visible before first scroll ✗
- Cookie consent banner covers bottom 114px of viewport ✗
- Phone number hidden behind "Fale conosco" toggle ✗

### Mobile Issues

| Issue | Severity |
|---|---|
| All three primary CTA buttons: 38px tall (min 48px required) | HIGH |
| Cookie banner (114px) obscures product cards | HIGH |
| No `loading="lazy"` on any image | HIGH |
| No responsive `srcset` — mobile downloads desktop images | MEDIUM |
| WhatsApp floating buttons invisible on mobile viewport | MEDIUM |
| Tablet: CTA text clipped at 768px | MEDIUM |

### What Is Working
- Responsive layout (2-col mobile grid, 4-col desktop) ✓
- No horizontal scroll ✓
- Viewport meta tag correct ✓
- Logo clean across all viewports ✓
- Orange CTA button has good visual hierarchy ✓
- All product images have alt text ✓

---

## 10. Sitemap — Score: 54/100

| Check | Status | Detail |
|---|---|---|
| Discoverable (robots.txt + standard path) | PASS | Declared in robots.txt, accessible at /sitemap.xml |
| XML validity | PASS | Well-formed, correct namespace |
| Total URLs | 303 | 230 products, 42 categories, 30 articles, 1 homepage |
| lastmod accuracy | FAIL | All 303 URLs show today's date — dynamically generated |
| changefreq usage | FAIL | `always` on every URL — Google ignores |
| priority usage | FAIL | `1.00` on 230 products, `0.99` on 42 categories — blanket values ignored |
| /cotacao in sitemap | FAIL | Primary conversion page missing |
| Slug malformations | 5 errors | Trailing dashes, fused words (`borrachapara`), truncated slug (`tira-de-borrach`) |
| Sitemap index | Not needed | 303 URLs — single file is appropriate |

---

## Appendix: Key URLs Referenced

| URL | Status | Notes |
|---|---|---|
| https://www.lborborrachas.com.br/ | 200 | Homepage |
| https://www.lborborrachas.com.br/robots.txt | 200 | Well-formed |
| https://www.lborborrachas.com.br/sitemap.xml | 200 | 303 URLs, valid XML |
| https://www.lborborrachas.com.br/contato | 200 | No address |
| https://www.lborborrachas.com.br/cotacao | 200 | Not in sitemap |
| https://www.lborborrachas.com.br/llms.txt | 404 | Missing |
| https://www.blog.lborborrachas.com.br/ | 500 | Broken |
| https://www.lborborrachas.com.br/quem-somos | 404 | Missing entirely |
| https://www.lborborrachas.com.br/c/11-lencol-de-borracha | 200 | Category OK |
| https://www.lborborrachas.com.br/p/lencol-de-borracha-alta-abrasao | 200 | Product OK |
