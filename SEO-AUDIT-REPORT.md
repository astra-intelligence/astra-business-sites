# SEO/SEM Initial Setup — Audit & Recommendations

**Issue:** AST-624  
**Date:** 2026-06-26  
**Scope:** The Sights, HoldQuarter, Astra Intelligence Corp (main), Account Guardian, AstraWatch

---

## 1. Sites & Deployment Status

| Site | URL | Status | Notes |
|------|-----|--------|-------|
| **The Sights** | thesights.astraintelligence.co | ✅ Live (Netlify) | Published, needs redeploy |
| **HoldQuarter** | holdquarter.astraintelligence.co | ✅ Live (Netlify) | Published, needs redeploy |
| **Astra Intelligence Corp** | astraintelligence.co | ✅ Live (Netlify) | Published, needs redeploy |
| **Account Guardian** | — | 🔲 Not deployed | No web front-end found |
| **AstraWatch** | — | 🔲 No web front-end | Slack bot, infra-only |

**Critical Finding:** Local code at `astra-business-sites/` contains schema markup, sitemaps, and robots.txt that are NOT deployed to any of the 3 live Netlify sites. Each site was deployed as a separate Netlify service (not from the monorepo), so the local files need to be deployed individually or the architecture unified.

---

## 2. Live Site Audit Summary

### Meta Tags (Current Live State)

| Element | The Sights | HoldQuarter | Main Corp |
|---------|-----------|-------------|-----------|
| **Title** | ✅ "The Sights — Cryptids, Dragons & the Paranormal" | ✅ "HoldQuarter — Automated Quarterly Tax Withholding" | ✅ "Astra Intelligence Corporation | AI Research & Applied Intelligence" |
| **Meta Description** | ✅ Present | ✅ Present | ✅ Present |
| **Canonical URL** | ❌ Missing | ❌ Missing | ❌ Missing |
| **OG:Title** | ✅ Present | ✅ Present | ❌ Missing |
| **OG:Description** | ✅ Present | ✅ Present | ❌ Missing |
| **OG:Image** | ✅ Present | ❌ Missing | ❌ Missing |
| **OG:URL** | ❌ Missing | ❌ Missing | ❌ Missing |
| **OG:Type** | ❌ Missing | ✅ website | ❌ Missing |
| **Twitter Card** | ❌ Missing | ❌ Missing | ❌ Missing |
| **Schema (ld+json)** | ❌ Missing live (✅ in source) | ❌ Missing live (✅ in source) | ❌ Missing |
| **Robots meta tag** | ❌ Missing | ❌ Missing | ❌ Missing |
| **Hreflang** | ❌ N/A (en-only) | ❌ N/A (en-only) | ❌ N/A (en-only) |

### Technical SEO (Current Live State)

| Item | The Sights | HoldQuarter | Main Corp |
|------|-----------|-------------|-----------|
| **robots.txt** | ❌ 404 | ❌ 404 | ❌ 404 |
| **sitemap.xml** | ❌ 404 | ❌ 404 | ❌ 404 |
| **GA4 Tag** | ❌ Missing | ❌ Missing | ❌ Missing |
| **SSL** | ✅ Let's Encrypt | ✅ Let's Encrypt | ✅ Let's Encrypt |
| **Page speed** | ⚠️ Not measured | ⚠️ Not measured | ⚠️ Not measured |

### Source Code (on disk at `astra-business-sites/`)

| Item | The Sights | HoldQuarter | Main Corp |
|------|-----------|-------------|-----------|
| **Schema** | ✅ WebSite + SearchAction | ✅ SoftwareApplication | ❌ Missing |
| **robots.txt** | ✅ (root-level, shared) | ✅ (root-level, shared) | ✅ (root-level, shared) |
| **Sitemap index** | ✅ (per-subdomain) | ✅ (per-subdomain) | ✅ (root index) |
| **OG tags** | ✅ 3 tags | ✅ 3 tags | ❌ Missing |
| **GA4** | ❌ Missing | ❌ Missing | ❌ Missing |

### Word Count (Content Depth)

| Site | Words | Assessment |
|------|-------|------------|
| The Sights | ~659 | Light — could use more body content for SEO value |
| HoldQuarter | ~846 | Light — needs expanded landing page copy |
| Main Corp | ~875 | Light — thin for a corporate site homepage |

---

## 3. Keyword Research [PENDING — Research Agents Running]

*Research dispatched to subagents. Results will be appended once returned.*

### Draft Keywords for The Sights (Expected)
- Cryptid sticker sheet, Bigfoot sticker, Mothman art, paranormal stickers, dragon sticker art, unique kids gifts, weird stickers, 9-year-old artist, creature stickers, cryptozoology decor

### Draft Keywords for HoldQuarter (Expected)
- Freelancer tax withholding, quarterly tax automation, self-employment tax, 1099 tax withholding, automatic IRS payments, independent contractor taxes, gig worker tax software

### Draft Keywords for Main Corp (Expected)
- AI research lab, ethical AI company, applied intelligence systems, AI for media

---

## 4. Schema Markup Recommendations

### The Sights — Recommended Schema
```json
{
  "@context": "https://schema.org",
  "@type": "WebSite",
  "name": "The Sights",
  "description": "Weird, wonderful sticker art by a 9-year-old creator. Cryptids, dragons, and creatures that go bump in the night.",
  "url": "https://thesights.astraintelligence.co",
  "potentialAction": {
    "@type": "SearchAction",
    "target": "https://thesights.astraintelligence.co/?search={search_term_string}",
    "query-input": "required name=search_term_string"
  }
}
```
✅ Already in source — needs redeploy.
Add `Organization` schema:
```json
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "The Sights",
  "url": "https://thesights.astraintelligence.co",
  "logo": "https://thesights.astraintelligence.co/logo.png",
  "foundingDate": "2026",
  "parentOrganization": {
    "@type": "Organization",
    "name": "Astra Intelligence Corporation",
    "url": "https://astraintelligence.co"
  }
}
```

### HoldQuarter — Recommended Schema
```json
{
  "@context": "https://schema.org",
  "@type": "SoftwareApplication",
  "name": "HoldQuarter",
  "applicationCategory": "FinanceApplication",
  "operatingSystem": "Web",
  "description": "Automated quarterly tax withholding for freelancers and independent contractors.",
  "url": "https://holdquarter.astraintelligence.co",
  "offers": {
    "@type": "Offer",
    "price": "0",
    "priceCurrency": "USD"
  }
}
```
✅ SoftwareApplication schema already in source — needs redeploy.
Add `Organization` schema for HoldQuarter as well.

### Main Corp — Recommended Schema
```json
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "Astra Intelligence Corporation",
  "description": "AI research lab building ethical, human-aligned systems that solve real problems in media, mental health, and everyday life.",
  "url": "https://astraintelligence.co",
  "email": "founders@astraintelligence.co",
  "foundingDate": "2025",
  "knowsAbout": ["Artificial Intelligence", "Machine Learning", "Applied AI", "Agentic Systems"],
  "memberOf": [
    {
      "@type": "Organization",
      "name": "Astra Intelligence Labs"
    }
  ]
}
```

---

## 5. Robots.txt & Sitemap Fix

### Problem
Current live sites return **404** for `/robots.txt` and `/sitemap.xml`. Source files exist on disk but were deployed to separate Netlify sites that don't have them.

### Fix (per site)
Each Netlify site needs its own `robots.txt` and `sitemap.xml`:

**robots.txt** (all sites):
```
User-agent: *
Allow: /
Disallow: /assets/

Sitemap: https://SITE_URL/sitemap.xml
```

**sitemap.xml (per site):**
```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://SITE_URL/</loc>
    <changefreq>weekly</changefreq>
    <priority>1.0</priority>
  </url>
</urlset>
```

### Deployment Strategy (Option A — Recommended)
Deploy each site independently to its own Netlify site:
- `thesights-astraintelligence-co` → index.html + robots.txt + sitemap.xml
- `holdquarter-astraintelligence-co` → index.html + robots.txt + sitemap.xml  
- `astraintelligence-co` → index.html + robots.txt + sitemap.xml

### Deployment Strategy (Option B — Architecture Change)
Consolidate into single Netlify site with subdirectory routing (already configured in `netlify.toml`), using `thesights.astraintelligence.co` = `SITE/thesights/`.

---

## 6. GA4 Conversion Goals (Proposed)

Once GA4 is set up (AST-623), configure these conversion events:

### The Sights (Ecommerce)
1. `view_item` — Product page view
2. `add_to_cart` — Cart addition
3. `purchase` — Completed checkout
4. `view_promotion` — Viewed featured/sale items
5. `sign_up` — Email newsletter signup

### HoldQuarter (SaaS/Fintech)
1. `sign_up` — Account creation
2. `start_onboarding` — Began tax setup flow
3. `connect_payment_account` — Connected Stripe/payment processor
4. `schedule_withholding` — Configured first quarterly withholding
5. `referral_click` — Referral program click

### Main Corp (Corporate/Brand)
1. `page_view` — 2+ pages per session
2. `outbound_click` — Clicked to venture site
3. `contact_click` — Clicked contact/email
4. `form_submit` — Contact form submission
5. `download_whitepaper` — Research download

---

## 7. SEM / Google Ads Draft Campaigns

### HoldQuarter — "Freelancer Tax Season" Campaign
- **Budget:** $500-1000/mo (TBD)
- **Keywords:** "freelancer taxes", "quarterly estimated tax", "self employment tax filing", "1099 tax withholding"
- **Ad copy:** *"Stop guessing quarterly taxes. HoldQuarter automatically withholds + pays the IRS for you."*
- **Landing page:** holdquarter.astraintelligence.co

### The Sights — "Unique Sticker Gifts" Campaign  
- **Budget:** $200-500/mo (TBD)
- **Keywords:** "cryptid stickers", "paranormal gifts", "unique kids art", "dragon sticker sheet"
- **Ad copy:** *"Cryptid & dragon stickers by a 9-year-old artist. Perfect unique gift."*
- **Landing page:** thesights.astraintelligence.co

### Astra Corp — "AI Research Brand" Campaign
- **Budget:** Minimal (brand awareness)
- **Keywords:** "AI research lab", "applied intelligence", "ethical AI company"
- **Ad copy:** *"Building truth-seeking AI systems. Astra Intelligence Corporation."*

---

## 8. Competitive Landscape [PENDING — Research Running]

*Competitor research dispatched to subagents. Results will be appended.*

---

## 9. Deployment Checklist

- [ ] **AST-623 (Blocked):** GA4 + Search Console setup for each site
- [ ] **Redeploy** thesights site with schema + sitemap + robots.txt
- [ ] **Redeploy** holdquarter site with schema + sitemap + robots.txt
- [ ] **Redeploy** main corp site with schema + sitemap + robots.txt + OG tags
- [ ] **Add Organization schema** to all 3 sites
- [ ] **Add canonical URLs** to all 3 sites
- [ ] **Add Twitter Card tags** to all 3 sites
- [ ] **Configure GA4 conversion events** (after GA4 live)
- [ ] **Launch SEM campaigns** (after keywords finalized)
- [ ] **Expand content depth** (target 1500+ words per homepage)
- [ ] **Set up Google Search Console** (AST-623 dependency)

---

## 10. Issues Found

### 🔴 Critical (Blocks Indexing)
1. **No robots.txt on live sites** — crawlers have no guidance → 404 on discovery
2. **No sitemaps on live sites** — Google/Bing can't discover pages
3. **No canonical URLs** — potential duplicate content issues
4. **Main corp site has zero OG/schema** — zero social share preview, zero rich results

### 🟡 High
5. **Schema not deployed** — source files have it, but live sites don't
6. **No GA4 tracking** — can't measure conversions or user behavior
7. **Local code ≠ live deployment** — `astra-business-sites/` monorepo not synced to separate Netlify sites

### 🟢 Medium
8. **No Twitter Card tags** — poor previews on X/Twitter shares
9. **Thin content** — all sites under 1000 words on homepage
10. **No internal linking between ventures** — main corp site doesn't link to HoldQuarter or The Sights
## 3. Keyword Research — 10-15 per Site

### The Sights (Cryptids, Dragons & Paranormal Stickers)

| Keyword | Intent | Est. Monthly Volume | Notes |
|---------|--------|-------------------|-------|
| cryptid sticker sheet | Commercial | 1K-3K | High purchase intent |
| Bigfoot stickers | Commercial | 5K-10K | Evergreen, seasonal spikes |
| Mothman art print | Commercial | 1K-3K | Niche, loyal audience |
| paranormal stickers | Commercial | 3K-5K | Broad, good top-of-funnel |
| dragon sticker art | Commercial | 5K-10K | Competitive but high volume |
| unique kids gifts | Informational | 10K-50K | Broad, use as category page |
| sticker sheet for kids | Commercial | 3K-5K | Parent target |
| cryptozoology gift | Commercial | 1K-3K | High intent |
| 9-year-old artist | Informational | 500-1K | Story angle, PR value |
| weird stickers online | Commercial | 1K-3K | Niche discovery |
| creature sticker pack | Commercial | 5K-10K | Solid B2C volume |
| Loch Ness sticker | Commercial | 500-1K | Iconic cryptid |
| paranormal collector gift | Commercial | 500-1K | Small but high-value |
| mythical creature art | Informational | 10K-20K | Brand awareness |
| handmade sticker shop | Commercial | 1K-3K | Etsy competition |

### HoldQuarter (Freelance Tax Withholding)

| Keyword | Intent | Est. Monthly Volume | Competition |
|---------|--------|-------------------|-------------|
| quarterly tax filing freelancer | Commercial | 3K-5K | Medium |
| self employment tax calculator | Informational | 10K-20K | High |
| automatic tax withholding | Commercial | 1K-3K | Low |
| 1099 tax withholding software | Commercial | 500-1K | Low |
| freelancer tax software | Commercial | 5K-10K | High |
| independent contractor taxes | Informational | 10K-20K | High |
| quarterly estimated tax payment | Informational | 5K-10K | Medium |
| gig worker tax withholding | Commercial | 1K-3K | Low |
| irs quarterly payment automation | Commercial | 500-1K | Very Low |
| how to pay quarterly taxes | Informational | 10K-20K | High |
| tax withholding for freelancers | Commercial | 3K-5K | Medium |
| save for tax season | Informational | 5K-10K | Medium |
| stripe tax withholding | Commercial | 1K-3K | Low (Stripe Tax) |
| interest on tax savings | Informational | 500-1K | Very Low |
| freelance financial planning | Informational | 3K-5K | Medium |

### Astra Intelligence Corp (AI Research Lab)

| Keyword | Intent | Est. Monthly Volume | Notes |
|---------|--------|-------------------|-------|
| AI research lab | Informational | 5K-10K | Brand awareness |
| ethical AI company | Informational | 3K-5K | Differentiation |
| applied AI systems | Commercial | 1K-3K | B2B audience |
| AI for media | Commercial | 1K-3K | Niche |
| autonomous AI agents | Informational | 5K-15K | Growing |
| truth-seeking AI | Informational | 500-1K | Unique positioning |
| human-aligned AI | Informational | 1K-3K | Academic audience |
| AI venture studio | Commercial | 500-1K | Niche |
| machine learning research | Informational | 10K-20K | Very competitive |
| AI product development | Commercial | 3K-5K | B2B |

---

## 8. Competitive Landscape

### HoldQuarter Competitors

| Competitor | URL | Model | Key Differentiator | Est. Traffic |
|-----------|-----|-------|-------------------|-------------|
| **Keeper Tax** | keepertax.com | $199/yr subscription | Automatic 1099 deduction finder | ~500K/mo |
| **FlyFin** | flyfin.ai | $199/yr AI-powered | AI-based deduction categorization | ~200K/mo |
| **QuickBooks Self-Employed** | quickbooks.intuit.com/self-employed | $15/mo + $7.50/mo | Big brand, integrations with TurboTax | ~5M/mo |
| **Stride Tax** | strideinsurance.com/tax | Free deduction tracking + paid filing | Insurance + tax bundle | ~300K/mo |

**HoldQuarter Differentiation:** Automatic withholding + interest-bearing account. No competitor offers automated IRS remittance from payment inflow. Keeper and FlyFin focus on deductions, QBSE focuses on tracking — HoldQuarter owns the *withholding at source* niche.

### The Sights Competitors

| Competitor | URL | Pricing | Differentiator |
|-----------|-----|--------|---------------|
| **Etsy** (cryptid stickers category) | etsy.com | $3-8/sheet | Giant marketplace, huge traffic |
| **Redbubble** (paranormal art) | redbubble.com | $10-20/print | Print-on-demand, artist uploads |
| **Stickermule** (custom) | stickermule.com | $25+/sheet | Professional/bulk, not art-focused |
| **DeviousPlan** (small shops) | various | $5-15/sheet | Small batch artists |

**The Sights Differentiation:** Original art by a 9-year-old creator. Story-driven brand. Cryptids + dragons + paranormal all in one shop. Parent-child creator story is PR gold.

### Astra Intelligence Corp Competitors

| Competitor | URL | Focus |
|-----------|-----|-------|
| **Anthropic** | anthropic.com | AI safety research, Claude |
| **OpenAI** | openai.com | General AI, GPT models |
| **Adept** | adept.ai | AI agents for enterprise |
| **Cognition Labs** | cognition.ai | AI coding agents (Devin) |

**Differentiation:** Venture studio model + applied AI products + research. Most AI labs do one or the other, not both.

---
*Report generated 2026-06-26 by SEO/SEM Manager (AST-624)*
