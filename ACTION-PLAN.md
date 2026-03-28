# SEO Action Plan — lborborrachas.com.br
**Generated:** 2026-03-24
**Overall Score:** 39/100
**Target Score (12 months):** 72/100

---

## Priority Legend
- 🔴 **CRITICAL** — Blocks indexing, local visibility, or is a security risk (fix immediately)
- 🟠 **HIGH** — Significantly impacts rankings and CTR (fix within 1 week)
- 🟡 **MEDIUM** — Optimization opportunity (fix within 1 month)
- 🟢 **LOW** — Nice to have / future-proofing (backlog)

---

## PHASE 1 — This Week (No Code Deployment Required)

### 🔴 C1 — Add Physical Address to Footer and Contact Page
**Effort:** 1 hour | **Impact:** Local pack visibility, GBP association, NAP consistency
**Why:** The business is completely invisible to Google's local systems. This single fix enables GBP verification, local pack eligibility, and `LocalBusiness` schema.

**Action:** Add the complete address (Rua, número, bairro, cidade, estado, CEP) as visible text in the site footer and on `/contato`. Format:
```
Lbor Borrachas
[Rua/Av], [número]
[Bairro], São Paulo – SP, [CEP]
CNPJ: [XX.XXX.XXX/XXXX-XX]
```

---

### 🔴 C2 — Add Security Headers via Cloudflare
**Effort:** 30 minutes | **Impact:** Security, user trust signals
**Why:** Zero security headers currently. HSTS absence leaves users exposed to SSL stripping.

**Action:** In Cloudflare → Transform Rules → Modify Response Header, add:
```
Strict-Transport-Security: max-age=31536000; includeSubDomains; preload
X-Content-Type-Options: nosniff
X-Frame-Options: SAMEORIGIN
Referrer-Policy: strict-origin-when-cross-origin
```

---

### 🔴 C3 — Fix Redirect Chain
**Effort:** 30 minutes | **Impact:** Crawl budget, link equity, TTFB
**Why:** `http://lborborrachas.com.br/` currently makes 3 hops. Should be 1.

**Action:** In Cloudflare Page Rules, configure a single rule:
- Incoming: `http://lborborrachas.com.br/*`
- Action: 301 Redirect to `https://www.lborborrachas.com.br/$1`

---

### 🔴 C4 — Suppress PHP Version in Headers
**Effort:** 5 minutes | **Impact:** Security
**Why:** `X-Powered-By: PHP/7.4.33` (EOL) advertises an attack surface.

**Action:** Add to `php.ini`:
```
expose_php = Off
```
Then add PHP upgrade to PHP 8.2+ to the technical roadmap.

---

### 🔴 C5 — Fix Schema Errors (3 critical bugs, ~2 hours)
**Effort:** 2 hours | **Impact:** Sitelinks Searchbox, rich results, entity trust
**Why:** 3 critical schema bugs disqualify the site from Sitelinks Searchbox and corrupt entity data.

**Action — Fix 1:** Change `"name": ""` to `"name": "Lbor Borrachas"` in WebSite JSON-LD.

**Action — Fix 2:** Change `search&s=` to `search?s=` in SearchAction target URL.

**Action — Fix 3:** Remove `"contactOption": "TollFree"` from Organization contactPoint (number is a local São Paulo landline, not toll-free).

**Action — Fix 4:** Change all `"@context": "http://schema.org"` to `"@context": "https://schema.org"` across all templates.

---

### 🟠 H1 — Expand Homepage Title Tag
**Effort:** 15 minutes | **Impact:** Click-through rate, keyword ranking signal
**Why:** Current title "Lbor Borrachas" (14 chars) contains zero product keywords.

**Action:** Update title to 50–60 characters:
```
Lbor Borrachas | Manta, Lençol e Perfis de Borracha Industrial
```

---

### 🟠 H2 — Rewrite Homepage Meta Description
**Effort:** 15 minutes | **Impact:** CTR, AI summary quality
**Why:** Current description is a keyword-stuffed pipe list, not a value proposition.

**Action:** Replace with (≤155 chars):
```
Distribuidora e fabricante de manta, lençol e perfis de borracha industrial. Neoprene, EPDM, Silicone e mais. Solicite orçamento online.
```

---

### 🟠 H3 — Add Open Graph + Twitter Card Tags
**Effort:** 1 hour (CMS template edit) | **Impact:** Social sharing, AI metadata extraction
**Why:** `og:type`, `og:locale` missing; zero Twitter Cards on any page.

**Action:** Add to sitewide `<head>` template:
```html
<meta property="og:type" content="website" />
<meta property="og:locale" content="pt_BR" />
<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:title" content="[PAGE TITLE]" />
<meta name="twitter:description" content="[META DESCRIPTION]" />
<meta name="twitter:image" content="[OG IMAGE URL]" />
```

---

### 🟠 H4 — Create `/llms.txt`
**Effort:** 1 hour | **Impact:** AI search readiness (GEO), crawler guidance
**Why:** Missing entirely. Low effort, signals AI readiness to GPTBot, ClaudeBot, PerplexityBot, Google-Extended.

**Action:** Create at `https://www.lborborrachas.com.br/llms.txt`:
```
# Lbor Borrachas — llms.txt
# Distribuidora e fabricante de artefatos de borracha industrial em São Paulo, Brasil.

## Site
Name: Lbor Borrachas
URL: https://www.lborborrachas.com.br
Description: Fornecedor de lençol, manta, perfis, silicone, neoprene, EPDM e borrachas industriais.
Language: pt-BR

## Key Pages
- https://www.lborborrachas.com.br/cotacao
- https://www.lborborrachas.com.br/contato
- https://www.lborborrachas.com.br/c/11-lencol-de-borracha
- https://www.lborborrachas.com.br/c/365-manta-de-silicone
- https://www.lborborrachas.com.br/sitemap.xml

## AI Crawler Access
GPTBot: allow
ClaudeBot: allow
PerplexityBot: allow
Google-Extended: allow
```

---

## PHASE 2 — Week 2 (CMS Template Changes)

### 🔴 C6 — Claim and Optimize Google Business Profile
**Effort:** 2–4 hours | **Impact:** Local pack ranking (primary factor per Whitespark 2026)
**Why:** Zero GBP signals detected on the site. The local pack is unreachable without a verified GBP.

**Action:**
1. Go to google.com/business and claim the profile for the São Paulo address
2. Set primary category to "Distribuidora de Materiais Industriais" or nearest equivalent
3. Upload 10+ product/storefront photos
4. Add business hours, description (750 chars), and all product categories
5. Add website URL and phone number matching the site exactly

---

### 🔴 C7 — Upgrade Organization Schema to LocalBusiness
**Effort:** 3 hours | **Impact:** Business panel, local pack, rich results
**Why:** `Organization` type does not trigger local rich results. `LocalBusiness` with full address and geo enables the business panel.

**Action:** Replace the sitewide Organization JSON-LD with:
```json
{
  "@context": "https://schema.org",
  "@type": "LocalBusiness",
  "@id": "https://www.lborborrachas.com.br/#organization",
  "name": "Lbor Borrachas",
  "description": "Distribuidora e fabricante de artefatos de borracha industrial: lençol, manta, perfil, silicone, poliuretano e mais.",
  "url": "https://www.lborborrachas.com.br",
  "logo": "https://www.lborborrachas.com.br/uploads/img/d94b08b2510be5fedb4b41758485aa38.png",
  "telephone": "+55-11-2167-5600",
  "email": "vendas@lbor.com.br",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "[ENDEREÇO COMPLETO]",
    "addressLocality": "São Paulo",
    "addressRegion": "SP",
    "postalCode": "[CEP]",
    "addressCountry": "BR"
  },
  "geo": {
    "@type": "GeoCoordinates",
    "latitude": "[LATITUDE]",
    "longitude": "[LONGITUDE]"
  },
  "openingHoursSpecification": [{
    "@type": "OpeningHoursSpecification",
    "dayOfWeek": ["Monday","Tuesday","Wednesday","Thursday","Friday"],
    "opens": "08:00",
    "closes": "18:00"
  }],
  "sameAs": [
    "[GOOGLE BUSINESS PROFILE URL]",
    "[LINKEDIN COMPANY PAGE URL]"
  ]
}
```

---

### 🔴 C8 — Create "Quem Somos" Page
**Effort:** 4 hours (copywriting + CMS) | **Impact:** E-E-A-T Trustworthiness, Google entity signals
**Why:** All `/quem-somos`, `/sobre`, `/sobre-nos`, `/empresa` paths return 404. This is a direct E-E-A-T Trustworthiness failure.

**Action:** Create `/quem-somos` with:
- Company founding year and history narrative (400+ words)
- Full physical address + embedded Google Map
- CNPJ displayed publicly
- Named team members with roles (at minimum: directors, sales manager)
- Industry memberships (ABAM, Sindiborrachas if applicable)
- Any certifications (ISO, ABNT compliance)
- Link to LGPD privacy policy

---

### 🟠 H5 — Add BreadcrumbList Schema to Category and Product Pages
**Effort:** 4 hours | **Impact:** Breadcrumb display in SERPs, click-through rate
**Why:** Zero breadcrumb schema exists. Breadcrumbs are present in the visual UI but not marked up.

**Action:** Add to category page template `<head>`:
```json
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {"@type": "ListItem", "position": 1, "name": "Início", "item": "https://www.lborborrachas.com.br/"},
    {"@type": "ListItem", "position": 2, "name": "[CATEGORY NAME]", "item": "https://www.lborborrachas.com.br/c/[slug]"}
  ]
}
```
Add a third item for product pages.

---

### 🟠 H6 — Fix Microdata: Convert to JSON-LD with Absolute URLs
**Effort:** 3 hours | **Impact:** ItemList rich results
**Why:** 55 ListItem entries across homepage + category pages use relative URLs and relative image paths — both invalid. One empty container generates Search Console errors.

**Action:**
1. Remove the empty `<div itemscope itemtype="...ItemList">` container from category pages
2. Replace all relative `itemprop="url"` with absolute URLs (`https://www.lborborrachas.com.br/...`)
3. Replace all relative `itemprop="image"` with absolute URLs
4. Or migrate entirely to JSON-LD (recommended)

---

### 🟠 H7 — Fix Homepage H1 and Add H2 Headings
**Effort:** 2 hours | **Impact:** Keyword relevance, content hierarchy, on-page SEO
**Why:** H1 = "Todos os Produtos" (navigation label). Zero H2s on the entire homepage.

**Action:**
- H1: "Borrachas Industriais: Lençol, Manta, Perfis e Silicone em São Paulo"
- H2 (product family groupings): "Lençol e Manta de Borracha", "Perfis e Guarnições", "Pisos de Borracha", "Silicone Industrial"

---

### 🟠 H8 — Fix Canonical and og:url Trailing-Slash Consistency
**Effort:** 1 hour | **Impact:** Indexing signals
**Why:** Canonical: no trailing slash. og:url: trailing slash. Sitemap: no trailing slash. Mixed signals.

**Action:** Standardize on `https://www.lborborrachas.com.br/` (with trailing slash) across canonical, og:url, sitemap homepage entry, and all internal links.

---

### 🟠 H9 — Add Google Maps Embed to /contato
**Effort:** 30 minutes | **Impact:** GBP association, local trust signals
**Why:** No Maps embed exists anywhere. Links the website to the GBP entity.

**Action:** Get the embed code from Google Maps for the São Paulo business location and add an iframe to `/contato`.

---

### 🟠 H10 — Add Product Schema to All /p/ Pages
**Effort:** 1–2 days (requires CMS template modification) | **Impact:** Product rich results, Shopping eligibility
**Why:** 230 product pages have zero schema. `Product` + `Offer` is the highest-impact schema type for an e-commerce/catalog site.

**Action:** Add dynamically generated JSON-LD to each product page:
```json
{
  "@context": "https://schema.org",
  "@type": "Product",
  "name": "[PRODUCT NAME]",
  "description": "[PRODUCT DESCRIPTION]",
  "image": ["https://www.lborborrachas.com.br/uploads/img/[IMAGE PATH]"],
  "sku": "[SKU]",
  "brand": {"@type": "Brand", "name": "Lbor Borrachas"},
  "offers": {
    "@type": "Offer",
    "priceCurrency": "BRL",
    "availability": "https://schema.org/InStock",
    "url": "https://www.lborborrachas.com.br/p/[slug]"
  }
}
```

---

## PHASE 3 — Month 1 (Content & Performance)

### 🔴 C9 — Restore or Migrate Blog
**Effort:** 4–8 hours | **Impact:** Topical authority, E-E-A-T Authoritativeness, backlink target
**Why:** `blog.lborborrachas.com.br` returns HTTP 500. A content channel for 30 articles is completely dead.

**Action (preferred):** Migrate blog content to `https://www.lborborrachas.com.br/blog/` with 301 redirects from subdomain. All 30 article URLs in the sitemap (`/artigo/*.html`) already live on the main domain and return 200 — the issue may be limited to the blog index page.

**Action (quick fix):** Fix the HTTP 500 on the blog subdomain. Remove the footer blog link until repaired.

---

### 🟠 H11 — Enable Cloudflare Edge Caching for HTML Pages
**Effort:** 2 hours | **Impact:** TTFB reduction from ~450ms to ~20–50ms for cache hits
**Why:** `Cache-Control: no-store` + PHPSESSID on every request forces Cloudflare to mark all pages DYNAMIC, bypassing CDN.

**Action:** Create a Cloudflare Cache Rule:
- Match: URL path does NOT contain `/admin`, `/cotacao`, `/contato`, `/carrinho`, `/minha-conta`
- Action: Cache Everything, Edge TTL: 5 minutes
- Strip or ignore session cookies for anonymous GET requests

---

### 🟠 H12 — Add LCP Image Preload and Lazy Loading
**Effort:** 2 hours | **Impact:** LCP improvement — potential improvement from 4–5s to 2–3s range
**Why:** First product card image is the LCP element with no preload hint. All 51 images load eagerly.

**Action:**
1. Add to `<head>`: `<link rel="preload" as="image" href="/uploads/img/240/[FIRST-PRODUCT-IMAGE].png" fetchpriority="high">`
2. Add `fetchpriority="high"` to the first above-fold product `<img>` tag
3. Add `loading="lazy"` to all images below position 4 in the product grid

---

### 🟠 H13 — Fix Google Fonts @import → <link> with Preconnect
**Effort:** 1 hour | **Impact:** Removes 300–600ms from critical rendering path
**Why:** `@import url('https://fonts.googleapis.com/...')` inside the CSS file creates a serial waterfall.

**Action:**
1. Remove the `@import` from `style_6978.min.css`
2. Add to HTML `<head>`:
```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Roboto+Slab:wght@300;700&display=swap">
```

---

### 🟠 H14 — Add `defer` to Main JS Bundle
**Effort:** 30 minutes | **Impact:** Removes 442 KB JS from render-blocking critical path
**Why:** `<script src="/script_6978.min.js">` loads synchronously, blocking HTML parsing.

**Action:** Change to `<script src="/script_6978.min.js" defer></script>`

---

### 🟠 H15 — Increase Static Asset Cache TTL to 1 Year
**Effort:** 30 minutes | **Impact:** Repeat-visit performance
**Why:** CSS/JS already use versioned filenames (`_6978`). Cache-busting is in place. TTL should be immutable.

**Action:** In Cloudflare, add a Cache Rule for `*.css`, `*.js`, `/uploads/img/*`:
```
Cache-Control: public, max-age=31536000, immutable
```

---

### 🟠 H16 — Add width/height to All Images + Convert to WebP
**Effort:** 4 hours | **Impact:** CLS improvement, ~30% image size reduction
**Why:** Zero explicit dimensions = layout shifts on slow connections. PNG/JPG only = no modern format savings.

**Action:**
1. Add `width` and `height` attributes to all `<img>` tags
2. Configure the image pipeline to generate WebP variants and serve them via `<picture>` + `<source type="image/webp">`

---

### 🟡 M1 — Publish LGPD Privacy Policy
**Effort:** 2 hours | **Impact:** Legal compliance, Trust signals
**Why:** Contact and quote forms collect CNPJ, email, phone — no privacy policy exists. Lei 13.709/2018 requires it.

**Action:** Create `/politica-de-privacidade` addressing LGPD requirements. Link from footer, `/contato`, and `/cotacao` forms.

---

### 🟡 M2 — Expand Category Page Descriptions to 600–800 Words
**Effort:** 3–5 hours per category | **Impact:** Topical authority, thin content remediation
**Why:** Current descriptions are 90–120 words, all following the same templated Title Case pattern. 25 categories × 600 words = significant content investment.

**Priority categories to start:**
1. `/c/11-lencol-de-borracha` (highest volume likely)
2. `/c/26-pisos-de-borracha`
3. `/c/365-manta-de-silicone`
4. `/c/63-neoprene-fretado`

**Structure per category:**
- H1: "[Produto]: Tipos, Aplicações e Especificações Técnicas"
- Definitional paragraph (150 words)
- H2: "Tipos de [Produto]" with comparison table (material, dureza Shore A, temperatura, aplicação)
- H2: "Aplicações Industriais" with use case examples
- H2: "Como Escolher o [Produto] Certo?"
- H2: "Perguntas Frequentes" → FAQPage schema
- CTA: "Solicite um orçamento"

---

### 🟡 M3 — Fix Sitemap: Real lastmod Dates + Remove Deprecated Tags
**Effort:** 4 hours (CMS development) | **Impact:** Crawl budget efficiency
**Why:** All 303 URLs show today's date. `changefreq: always` and `priority: 1.00` blanket values are ignored by Google.

**Action:**
1. Store `updated_at` timestamp per product/category/article in the database
2. Emit actual timestamps in `<lastmod>` at sitemap generation time
3. Remove all `<changefreq>` and `<priority>` tags from the sitemap

---

### 🟡 M4 — Add /cotacao to Sitemap
**Effort:** 30 minutes | **Impact:** Ensures conversion page is indexed
**Why:** The primary conversion page (`/cotacao`) is missing from the sitemap.

**Action:** Add to sitemap.xml with an accurate lastmod date.

---

### 🟡 M5 — Create São Paulo Location/Service Page
**Effort:** 3 hours | **Impact:** Local organic ranking for geo-modified queries
**Why:** No location-specific landing page exists. This is the #1 local organic ranking factor (Whitespark 2026).

**Action:** Create `/borrachas-industriais-sao-paulo` with:
- H1: "Borrachas Industriais em São Paulo — Lbor Borrachas"
- Full address + Google Maps embed
- Service area description (São Paulo + ABCD Paulista + Grande SP)
- Key product categories with local angle
- Business hours
- CTA to /cotacao
- LocalBusiness schema referencing this page

---

### 🟡 M6 — Generate Review System
**Effort:** 2 hours | **Impact:** Stars in SERPs, GBP ranking velocity
**Why:** Zero reviews or ratings visible anywhere. For B2B industrial buyers, social proof is critical.

**Action:**
1. Create a GBP review link and add it to the post-quotation email/thank-you page
2. Add a "Deixe sua avaliação" CTA to `/contato`
3. Once reviews accumulate (10+), add `aggregateRating` to the LocalBusiness schema

---

### 🟡 M7 — Submit to Brazilian B2B Citation Directories
**Effort:** 3 hours | **Impact:** Citation signals, GBP verification support
**Why:** Citation presence is a top-3 local ranking factor. Brazilian B2B directories are underutilized.

**Priority directories:**
1. Reclame Aqui (reclameaqui.com.br) — primary Brazilian consumer/B2B trust platform
2. GuiaMais (guiamais.com.br) — Brazilian local directory
3. Telelistas (telelistas.net) — telecom directory
4. Empresas.com.br
5. ACSP (acsp.com.br) — Associação Comercial de São Paulo (high-authority local citation)

**Ensure:** Business name, address, and phone number are identical to the site across all listings.

---

## PHASE 4 — Quarter 1 (Strategic / Long-Term)

### 🟡 M8 — Add Homepage Editorial Content Block (400–600 words)
**Effort:** 1 day (copy + dev) | **Impact:** Content depth, keyword coverage, E-E-A-T
**Why:** Homepage currently has ~80 words. Minimum 400–500 words needed for competitive B2B category pages.

**Action:** Add above-the-fold editorial section covering:
- Who Lbor Borrachas is, years in operation
- Products and materials (EPDM, Neoprene, SBR, Silicone, Poliuretano)
- Industries served (automotive, construction, metallurgy, food processing, civil engineering)
- São Paulo service area
- Why choose Lbor (stock availability, custom cutting, B2B pricing, fast delivery)
- CTA linking to /cotacao and /contato

---

### 🟡 M9 — Create FAQPage Schema on Category Pages
**Effort:** 2 hours per category | **Impact:** AI citation (GEO), passage-level citability
**Why:** FAQ schema is the primary vehicle for passage extraction by Google AI Overviews and Perplexity.

**Action:** Add 4–6 Q&A blocks per major category page:
- "O que é lençol de borracha?"
- "Qual a diferença entre borracha SBR e Neoprene?"
- "Quais espessuras estão disponíveis?"
- "Como solicitar um orçamento de borracha industrial?"

Implement as `FAQPage` JSON-LD alongside the existing schema.

---

### 🟡 M10 — Add "Como Comprar" Section to Product Pages
**Effort:** 2 hours (CMS template) | **Impact:** User intent satisfaction, B2B conversion
**Why:** B2B industrial buyers need to understand the purchase process before requesting a quote.

**Action:** Add a standardized block to all product pages:
- Processo de cotação (how the quote form works)
- Prazo de entrega típico
- Quantidade mínima de pedido (MOQ)
- Condições de pagamento
- Área de entrega

---

### 🟢 L1 — Migrate Blog to Main Domain
**Effort:** 2–3 days | **Impact:** Topical authority consolidation (high value, high effort)
**Why:** Blog content on `blog.lborborrachas.com.br` builds authority for a subdomain, not the main site. After fixing the 500 error, plan migration to `www.lborborrachas.com.br/blog/`.

**Action:** 301 redirect each blog article URL to the new `/blog/[slug]` on the main domain. Update internal links. Preserve article URLs in the sitemap.

---

### 🟢 L2 — Plan PHP 8.2 Upgrade
**Effort:** 1–3 days (testing + deployment) | **Impact:** Security, performance (opcache improvements in PHP 8.x)
**Why:** PHP 7.4.33 has been end-of-life since November 28, 2022. No security patches.

---

### 🟢 L3 — Plan AngularJS Migration
**Effort:** 2–4 weeks | **Impact:** INP improvement, long-term security, maintainability
**Why:** AngularJS 1.6.9 (EOL December 2021) + jQuery 1.9.1 (2013) account for ~350 KB of the 442 KB JS bundle. Replacing with vanilla JS or a modern framework would reduce parse time from ~3s to <200ms on mid-range Android.

---

### 🟢 L4 — Implement IndexNow
**Effort:** 2 hours | **Impact:** Accelerated Bing/Yandex re-indexing
**Why:** Not implemented. Low effort, especially useful when product catalog updates occur.

**Action:** Generate a key, place at `https://www.lborborrachas.com.br/{key}.txt`, submit change notifications via POST on product/article updates.

---

### 🟢 L5 — Add YouTube Product Demonstration Videos
**Effort:** Ongoing | **Impact:** AI citation probability (+0.737 correlation with AI mentions in GEO research)
**Why:** YouTube mention signals are the strongest single indicator of AI citation likelihood. Even 3–5 short product demo videos would help.

**Action:** Create a YouTube channel. Publish "Como usar [produto]" and "Guia de seleção de borracha industrial" videos. Link from product pages and the Quem Somos page.

---

## Impact Summary

| Phase | Timeline | Estimated Score Gain | Priority Actions |
|---|---|---|---|
| Phase 1 (Quick wins) | Week 1 | +8–10 points | Security headers, address, schema fixes, title tag, llms.txt |
| Phase 2 (Template changes) | Week 2 | +10–12 points | GBP, LocalBusiness schema, Quem Somos, Product schema |
| Phase 3 (Content + Performance) | Month 1 | +8–10 points | Blog, edge caching, LCP fixes, category content |
| Phase 4 (Strategic) | Quarter 1 | +5–8 points | Homepage content, FAQ schema, YouTube, PHP upgrade |
| **Projected Total** | **3 months** | **~71–79/100** | — |

---

## Monitoring Checklist

After implementing Phase 1 and 2:

- [ ] Google Search Console: Submit sitemap after fixing lastmod, check for schema errors in Rich Results report
- [ ] Google Rich Results Test: Validate LocalBusiness, WebSite, Product schema at https://search.google.com/test/rich-results
- [ ] CrUX Dashboard: Monitor LCP, INP, CLS at https://cruxvis.withgoogle.com for origin
- [ ] PageSpeed Insights: Run before/after performance changes at https://pagespeed.web.dev
- [ ] Cloudflare Analytics: Verify cache hit rate increases after enabling edge caching
- [ ] GBP Insights: Track local pack impressions and direction requests after claiming/optimizing GBP
- [ ] Google Search Console: Monitor "Quem Somos" page for indexing after creation
- [ ] Schema validator: https://validator.schema.org — test all JSON-LD blocks after fixes
