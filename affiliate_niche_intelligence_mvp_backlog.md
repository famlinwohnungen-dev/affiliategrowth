# Germany Affiliate Niche Intelligence — MVP Implementation Backlog

**Version:** 1.0  
**Date:** 2026-09-09  
**Goal:** Validate whether a data-driven German affiliate website can generate repeatable revenue before investing in a full automation platform.

---

## 1. Executive Decision

Do **not** build the full automated affiliate platform yet.

Build a small research-and-validation pipeline that can answer:

> **Which German affiliate niches have enough search demand, commercial intent, achievable SERPs, and affiliate economics to justify publishing content?**

The MVP should prove the economics with real Google impressions, rankings, affiliate clicks, and ideally conversions.

### Recommended MVP stack

- Python 3.12+
- SQLite
- SQLAlchemy
- Pydantic
- Google Ads API
- Awin Publisher API
- ADCELL portal/export as a secondary source initially
- DataForSEO SERP API
- Streamlit or simple FastAPI + HTML for reporting
- GitHub Actions / cron for scheduled jobs
- No Kubernetes
- No microservices
- No vector database
- No agent framework
- No autonomous AI content generation in Phase 0/1

---

# 2. Validation Strategy

Use a funnel instead of building everything at once.

```text
50–100 candidate niches
        ↓
Affiliate availability
        ↓
500–2,000 commercial keywords
        ↓
Keyword economics
        ↓
SERP analysis
        ↓
Top 3–5 niches
        ↓
30–45 real pages
        ↓
Google Search Console
        ↓
Affiliate clicks
        ↓
Conversions / revenue
        ↓
GO / ITERATE / NO-GO
```

The critical principle is:

> **Every expensive automation step must be justified by evidence from the previous step.**

---

# 3. Phase 0 — Project Setup

## 3.1 Repository

Recommended structure:

```text
affiliate-intelligence/
├── pyproject.toml
├── README.md
├── .env.example
├── config/
│   ├── niches.yaml
│   ├── countries.yaml
│   └── scoring.yaml
├── src/
│   ├── config/
│   ├── db/
│   ├── models/
│   ├── sources/
│   │   ├── awin.py
│   │   ├── adcell.py
│   │   ├── google_ads.py
│   │   └── dataforseo.py
│   ├── pipelines/
│   │   ├── niche_discovery.py
│   │   ├── keyword_discovery.py
│   │   ├── serp_analysis.py
│   │   └── scoring.py
│   ├── analytics/
│   │   └── revenue.py
│   └── reports/
│       └── export.py
├── sql/
├── tests/
└── notebooks/
```

## 3.2 Environment variables

```text
DATABASE_URL=
AWIN_PUBLISHER_ID=
AWIN_ACCESS_TOKEN=
GOOGLE_ADS_CUSTOMER_ID=
GOOGLE_ADS_DEVELOPER_TOKEN=
GOOGLE_ADS_CLIENT_ID=
GOOGLE_ADS_CLIENT_SECRET=
GOOGLE_ADS_REFRESH_TOKEN=
DATAFORSEO_LOGIN=
DATAFORSEO_PASSWORD=
```

Never store API credentials in Git.

---

# 4. Phase 1 — Generate the First 50–100 Niches

## Objective

Create a broad candidate pool without prematurely deciding which niches are attractive.

The first version should generate approximately **100 candidates**, then let data eliminate most of them.

## 4.1 Candidate sources

Use four independent seed sources.

### Source A — Affiliate categories

Extract categories and subcategories from:

- Awin
- ADCELL
- other affiliate networks only if necessary

Awin's Publisher API can expose program lists and filter them by country/relationship. It also exposes program details and commission groups for publishers with the required relationships. 

ADCELL currently exposes more than 2,300 partner programs and supports filters such as lead events, sale events, lifetime remuneration, CSV products, SEM, PLA, etc.

### Source B — Merchant categories

Example:

```text
Insurance
Finance
Energy
Telecom
Software
SaaS
Hosting
VPN
Cybersecurity
Consumer electronics
Home appliances
Garden
Furniture
Baby products
Pet products
Travel
Hotels
Car rental
Education
Online courses
Professional services
```

### Source C — Commercial keyword seeds

Create seed templates:

```text
best {product}
{product} test
{product} vergleich
{product} erfahrung
{product} kaufen
{product} kosten
{product} preis
{product} günstig
{service} vergleich
{service} kosten
{service} anbieter
{service} test
{brand} alternative
{product} alternative
```

### Source D — Google Keyword Planner

Use Google Ads API keyword ideas to expand seeds.

Google's `KeywordPlanIdeaService` supports keyword, URL, and site seeds and allows location/language targeting. Historical metrics include average monthly searches, approximate monthly volume, competition, competition index and bid ranges. 

---

# 5. Niche Generation Algorithm

Initial implementation should be deterministic.

```python
candidate_niches = []

for category in affiliate_categories:
    candidate_niches.extend(
        create_niche_candidates(category)
    )

for merchant_category in merchant_categories:
    candidate_niches.extend(
        create_niche_candidates(merchant_category)
    )

for seed in keyword_seeds:
    candidate_niches.extend(
        infer_niches_from_keyword(seed)
    )

candidate_niches = normalize(candidate_niches)
candidate_niches = deduplicate(candidate_niches)
candidate_niches = rank_by_initial_affiliate_signal(candidate_niches)

top_100 = candidate_niches[:100]
```

Do **not** use LLMs for this initially.

The objective is to establish a reproducible baseline.

---

# 6. Niche Normalization

Every candidate needs:

```text
niche_id
name
parent_category
country
language
source
seed_terms[]
status
```

Example:

```text
niche:
    name: "Photovoltaik"
    parent_category: "Energy"
    language: "de"
    country: "DE"
```

Possible related niches:

```text
Photovoltaik
Photovoltaik Speicher
Balkonkraftwerk
Wärmepumpe
Stromtarife
Wallbox
Gasvergleich
```

Keep these separate initially.

Later, semantic clustering can determine whether they belong to one content/business cluster.

---

# 7. Phase 2 — Affiliate Program Discovery

## Priority

### Tier 1

1. Awin
2. ADCELL

### Tier 2

Only after MVP evidence:

- finance-specific networks
- travel networks
- software/SaaS programs
- direct merchant programs
- additional affiliate networks

## Important distinction

There are two different questions:

### Question A

> Does an affiliate program exist?

This can be researched broadly.

### Question B

> Can **my publisher account** actually participate and earn this commission?

This must be treated separately.

Awin's commission-group API returns the commission groups and values available to the publisher for programs with an active relationship. Commission values can therefore be publisher/program specific. 

---

# 8. Awin Collector

## API calls

Initial collector:

```text
GET /publishers/{publisherId}/programmes
GET /publishers/{publisherId}/programmedetails
GET /publishers/{publisherId}/commissiongroups
```

Awin documents that its Publisher API can provide programs, program details, commission information, transactions and aggregated reports. 

## Store raw response

Always store:

```text
source
endpoint
retrieved_at
request_hash
raw_json
```

Do not immediately discard fields.

This protects against changes in the API and allows later reprocessing.

---

# 9. ADCELL Collector

For the MVP:

### Preferred

Use an official publisher export/download if available in the account.

### Fallback

Use a controlled manual export from the ADCELL portal.

Do **not** spend weeks reverse-engineering undocumented endpoints.

The MVP question is whether ADCELL materially improves niche discovery and affiliate coverage—not whether ADCELL can be perfectly automated on day one.

ADCELL's public publisher pages expose program information such as sale/lead remuneration and program features, while the publisher platform provides program discovery and application functionality.

---

# 10. Affiliate Program Schema

```sql
affiliate_programs
------------------
id
network
external_program_id
merchant_name
merchant_domain
program_name

country
currency

commission_type
commission_value
commission_min
commission_max

recurring
recurring_period
recurring_probability

cookie_days

aov_estimate
conversion_rate_estimate
lead_value

epc
approval_required
approval_status

deep_link_supported
product_feed_supported

status

source_url
raw_data

first_seen_at
last_seen_at
updated_at
```

## Commission types

Normalize to:

```text
CPS_PERCENT
CPS_FIXED
CPL
CPA_FIXED
CPC
RECURRING
UNKNOWN
```

Never mix raw commission and normalized effective commission.

---

# 11. Effective Commission

For CPS:

```text
effective_commission = AOV × commission_rate
```

Example:

```text
AOV = €800
commission = 4%

effective_commission = €32
```

For fixed CPS:

```text
effective_commission = fixed_commission
```

For CPL:

```text
effective_commission = CPL
```

For recurring programs:

```text
expected_lifetime_value =
    initial_commission
    +
    expected_recurring_commission
```

But recurring revenue must be modeled probabilistically.

Do not assume:

```text
monthly recurring × 12
```

unless the retention data supports it.

---

# 12. Affiliate Quality Score

Initial formula:

```text
AffiliateQuality =
    30% ProgramAvailability
  + 30% EffectiveCommission
  + 20% RecurringPotential
  + 10% EPC
  + 10% ProgramStability
```

Normalize every component to 0–100.

Important:

> Commission alone must never determine niche attractiveness.

A 20% commission on a €20 product can be much worse than a 2% commission on a €2,000 product.

---

# 13. Phase 3 — Google Keyword Data

## Target

Germany + German language.

Google Ads API supports geo targeting and language targeting for keyword generation. Historical metrics include average monthly searches, monthly volume, competition, competition index and bid percentiles. 

## MVP calls

### First call

Generate keyword ideas from seeds.

### Second call

Request historical metrics for the shortlisted keyword set.

Use batches rather than requesting one keyword at a time.

Google supports up to 10,000 keywords in a historical-metrics request, although the practical MVP batch size should be much smaller for debugging and traceability.

---

# 14. Keyword Schema

```sql
keywords
--------
id
keyword
normalized_keyword

niche_id

country
language

source
seed

avg_monthly_searches
monthly_volume
competition
competition_index

bid_low
bid_high
average_cpc

intent
commercial_intent

affiliate_relevance

serp_opportunity_score

estimated_ctr
estimated_traffic
estimated_affiliate_ctr
estimated_conversion_rate
estimated_epc
estimated_revenue

opportunity_score

first_seen_at
last_updated_at
```

---

# 15. Keyword Intent Classification

Use deterministic rules first.

## Informational

```text
was ist
wie funktioniert
anleitung
ratgeber
erklärung
```

## Commercial investigation

```text
test
vergleich
erfahrung
bewertung
beste
top
alternative
```

## Transactional

```text
kaufen
preis
kosten
günstig
angebot
online bestellen
```

## Service/commercial lead

```text
anbieter
tarif
versicherung
berater
angebot
kosten
```

Later, LLM classification can improve edge cases.

---

# 16. Commercial Intent Score

Example:

```text
Informational       = 20
Commercial Research = 65
Transactional       = 90
Lead Intent          = 90
Brand Navigation    = 30
```

Then manually review the top opportunities.

Do not blindly trust an LLM intent classifier.

---

# 17. Phase 4 — SERP Analysis

## Recommended MVP provider

**DataForSEO**

Reason:

- pay-as-you-go
- low unit cost
- no monthly subscription for SERP API
- Germany/local targeting
- Google Organic SERP
- structured JSON
- suitable for batch analysis

Current published pricing starts at approximately **$0.0006 per Google organic SERP page containing 10 results** in the standard normal-priority queue; live mode is more expensive. DataForSEO also states a $1 trial credit and a $50 minimum deposit. 

For MVP, use:

```text
Standard
Normal priority
depth = 10
Germany
German
desktop
```

Do not use Live mode unless necessary.

---

# 18. SERP Collection Strategy

Do NOT collect SERPs for all keywords.

Use a funnel:

```text
2,000 keywords
      ↓
filter to 500
      ↓
filter to 150
      ↓
SERP analysis
      ↓
top 50–100 opportunities
```

This dramatically reduces cost.

---

# 19. SERP Schema

```sql
serp_snapshots
--------------
id
keyword_id

search_engine
country
language
device

retrieved_at

result_count
features_json
raw_json
```

```sql
serp_results
------------
id
serp_snapshot_id

position

domain
url
title
description

result_type

is_ad
is_featured_snippet
is_paa
is_video
is_shopping
is_local

domain_authority
page_authority
backlinks

brand_indicator
affiliate_indicator
forum_indicator
reddit_indicator

query_match_score
content_quality_score
freshness_score
```

---

# 20. SERP Result Classification

For each top-10 result calculate:

### Domain type

```text
BIG_BRAND
PUBLISHER
AFFILIATE
ECOMMERCE
FORUM
REDDIT
GOVERNMENT
NEWS
SPECIALIST
UNKNOWN
```

### Content type

```text
PRODUCT_PAGE
CATEGORY_PAGE
REVIEW
COMPARISON
GUIDE
BLOG
FORUM_THREAD
HOMEPAGE
SERVICE_PAGE
```

This classification is extremely important.

A SERP containing ten giant brands is fundamentally different from:

```text
2 strong brands
3 mediocre affiliates
2 outdated blogs
2 forums
1 weak niche site
```

---

# 21. SEO Opportunity Score

Initial formula:

```text
SEOOpportunity =
    35% WeakSERPRatio
  + 20% QueryMismatch
  + 15% ContentWeakness
  + 15% FreshnessGap
  + 15% LowAuthorityPresence
```

## Weak SERP

A result can be considered weak if one or more conditions apply:

```text
low authority
poor query match
thin content
outdated content
forum-generated result
generic page
poor UX
no dedicated answer
```

Do not reduce this to domain authority alone.

---

# 22. Phase 5 — Revenue Model

Revenue estimation must be scenario-based.

## Core equation

```text
AffiliateClicks =
    Traffic × AffiliateCTR

Conversions =
    AffiliateClicks × ConversionRate

Revenue =
    Conversions × EffectiveCommission
```

Therefore:

```text
Revenue =
    Traffic
    × AffiliateCTR
    × ConversionRate
    × EffectiveCommission
```

---

# 23. Traffic Scenarios

The user specifically wants:

```text
10,000 monthly visitors
50,000 monthly visitors
100,000 monthly visitors
```

Do not assume every visitor comes from the target keyword.

Create:

```text
Scenario
    traffic
    affiliate_ctr
    conversion_rate
    effective_commission
```

Example:

```text
Conservative:
affiliate CTR = 3%
conversion = 1%
commission = €20

Base:
affiliate CTR = 5%
conversion = 2%
commission = €25

Optimistic:
affiliate CTR = 8%
conversion = 4%
commission = €30
```

These are placeholders only.

Real program data must replace them.

---

# 24. Example Revenue

For 50,000 visitors:

```text
50,000 × 5% = 2,500 affiliate clicks

2,500 × 2% = 50 conversions

50 × €25 = €1,250/month
```

This is:

```text
€15,000/year
```

before costs and taxes.

The platform should always show:

```text
monthly revenue
annual revenue
revenue per 1,000 visitors
affiliate clicks
conversions
```

---

# 25. Confidence-Adjusted Revenue

This is an important addition to the MVP.

Every assumption should have:

```text
value
source
confidence
```

Example:

```text
AOV = €800
source = merchant/network
confidence = HIGH

conversion_rate = 2%
source = industry assumption
confidence = LOW
```

Then:

```text
ExpectedRevenue =
    EstimatedRevenue × ConfidenceFactor
```

Do not hide uncertainty behind a single precise number.

---

# 26. Opportunity Score

Recommended first version:

```text
OpportunityScore =
    25% RevenuePotential
  + 20% SearchDemand
  + 20% CommercialIntent
  + 20% SEOOpportunity
  + 10% AffiliateQuality
  + 5% ContentFeasibility
```

All components normalized to 0–100.

## Why RevenuePotential gets 25%

The goal is not traffic.

The goal is:

> profitable affiliate traffic.

---

# 27. Revenue Potential Score

Example normalization:

```text
RevenuePotential =
    percentile_rank(
        base_case_monthly_revenue
    )
```

Use percentile ranking rather than arbitrary € thresholds.

This makes the score robust across different niches.

---

# 28. Content Feasibility

Initial score:

```text
ContentFeasibility =
    40% topical breadth
  + 30% content differentiation
  + 20% available data
  + 10% production cost
```

A niche should be downgraded if producing useful content requires:

```text
expert certification
expensive testing
physical products
legal advice
medical expertise
proprietary data
```

This is especially relevant for YMYL niches.

---

# 29. Final Recommendation Classes

```text
BUILD
RESEARCH
BACKLOG
IGNORE
```

Suggested thresholds:

```text
>= 75  BUILD
60–74  RESEARCH
40–59  BACKLOG
< 40   IGNORE
```

Do not treat these thresholds as statistically validated yet.

They are operational thresholds for the MVP.

---

# 30. Database

Recommended initial tables:

```text
niches
affiliate_programs
affiliate_commissions
keywords
serp_snapshots
serp_results
revenue_assumptions
opportunity_scores
pipeline_runs
```

Optional:

```text
keyword_niche
program_niche
keyword_program
```

Use relationship tables when many-to-many relationships become necessary.

---

# 31. Pipeline Runs

Every pipeline execution should be traceable.

```sql
pipeline_runs
-------------
id
pipeline_name
started_at
finished_at
status

records_input
records_output

api_cost_estimate
error_count

parameters_json
```

This is important for controlling API costs.

---

# 32. ETL Schedule

## Affiliate programs

```text
weekly
```

## Commission groups

```text
weekly
```

## Keyword metrics

```text
monthly
```

Google's historical keyword metrics are not something that needs to be requested continuously; cache the data and refresh periodically.

## SERP

```text
on demand
```

Later:

```text
weekly for high-value keywords
monthly for lower-value keywords
```

## Opportunity score

```text
after every material data refresh
```

---

# 33. API Cost Control

Implement a hard budget.

```python
MAX_MONTHLY_API_COST = 50
MAX_SERP_COST_PER_RUN = 5
MAX_KEYWORDS_PER_SERP_RUN = 500
```

Before making requests:

```python
if estimated_cost > remaining_budget:
    raise BudgetExceeded()
```

This should be implemented before automation.

---

# 34. Cost Estimate for MVP

A reasonable target:

| Component | MVP target |
|---|---:|
| Domain | ~€10–20/year |
| Hosting | €0–10/month |
| SQLite | €0 initially |
| Awin | normally no research API charge |
| ADCELL | €0 initially |
| Google Ads API | primarily API/account setup dependent |
| SERP | only a few dollars for initial research |
| LLM | €0 initially or very small |
| Total | roughly €20–100 for first validation |

The exact Google Ads/affiliate-network account requirements should be verified during setup.

DataForSEO's published SERP pricing makes small experiments particularly inexpensive: 1,000 standard Google SERPs are currently listed at about $0.60, although account funding and any optional parameters must be considered. Before pay any services, please aks for my approval. At beginning, import is not generating any costs.

---

# 35. Phase 6 — First Experiment

Do NOT launch 100 niches.

Select:

```text
Top 3 niches
```

For each:

```text
10–15 pages
```

Total:

```text
30–45 pages
```

This is the first real business experiment.

---

# 36. Page Selection

Prioritize:

```text
commercial investigation
transactional
lead intent
```

Examples:

```text
{product} test
{product} vergleich
{product} erfahrung
{product} kosten
{service} vergleich
{service} anbieter
{service} kosten
{product} alternative
```

Avoid spending the first experiment on:

```text
what is X
history of X
definition of X
generic informational content
```

---

# 37. Content Production

For the validation experiment:

### Human-controlled content

Use AI for:

```text
research assistance
outline
data extraction
comparison tables
draft assistance
internal linking suggestions
```

But human-review every published page.

Do not build an autonomous content factory before knowing which pages actually make money.

---

# 38. Website Architecture

Minimum:

```text
Homepage
Category pages
Comparison pages
Review pages
Legal pages
```

Technology can be simple:

```text
WordPress
or
Astro / Next.js
```

For the first validation, use whichever lets you publish fastest.

The intelligence platform and website should be loosely coupled.

---

# 39. Tracking

Every affiliate link should contain a unique internal identifier.

Example:

```text
page_id
keyword_id
program_id
placement_id
```

Store:

```text
affiliate_click
timestamp
page_id
keyword_id
program_id
placement_id
```

This allows:

```text
keyword → page → affiliate program → click → conversion → revenue
```

Without this chain, later optimization becomes difficult.

---

# 40. Google Search Console Feedback Loop

After publishing:

```text
Google Search Console
        ↓
query
page
impressions
clicks
CTR
position
        ↓
database
        ↓
opportunity model
```

Search Console should eventually become the most valuable data source because it changes the model from:

```text
predicted demand
```

to:

```text
observed demand
```

---

# 41. Validation KPIs

## Level 1 — Data

Must validate:

```text
affiliate programs are real
commission data is correct
keyword volume is plausible
SERP data is current
```

## Level 2 — Model

Check:

```text
high score → better ranking potential?
high commission → better revenue?
commercial intent → better affiliate CTR?
weak SERP → faster ranking?
```

## Level 3 — Market

Measure:

```text
impressions
ranking
organic clicks
affiliate CTR
affiliate clicks
conversion rate
revenue
revenue/page
revenue/1,000 visitors
```

---

# 42. Go / Iterate / No-Go

## GO

Proceed to automation if:

```text
at least one niche generates impressions
AND
commercial keywords rank
AND
affiliate clicks occur
AND
at least one conversion occurs
AND
revenue is repeatable
AND
content economics look attractive
```

## ITERATE

If:

```text
impressions exist
but
rankings/clicks are weak
```

or:

```text
affiliate clicks exist
but
conversion is weak
```

Then optimize:

```text
SERP targeting
content
CTA
affiliate program
commercial keyword selection
```

## NO-GO

Stop or change niche if:

```text
no meaningful impressions
SERPs consistently dominated by unbeatable domains
no relevant affiliate programs
affiliate clicks without economically viable conversion
expected revenue < content cost
```

---

# 43. MVP Backlog

## P0 — Must Have

### P0.1 Repository

- [ ] Create Python project
- [ ] Add SQLite
- [ ] Add configuration management
- [ ] Add structured logging
- [ ] Add database migrations

### P0.2 Niche Discovery

- [ ] Define 100 initial seed categories
- [ ] Normalize categories
- [ ] Generate 100 candidate niches
- [ ] Store niche records

### P0.3 Awin

- [ ] Create publisher account
- [ ] Obtain API credentials
- [ ] Implement authentication
- [ ] Implement program collection
- [ ] Implement program details
- [ ] Implement commission collection
- [ ] Persist raw responses

### P0.4 ADCELL

- [ ] Create publisher account
- [ ] Identify export/API options
- [ ] Import first program dataset
- [ ] Normalize programs

### P0.5 Google Ads

- [ ] Create/configure Google Ads API access
- [ ] Configure Germany geo target
- [ ] Configure German language
- [ ] Implement keyword idea generation
- [ ] Implement historical metrics
- [ ] Cache results

### P0.6 SERP

- [ ] Create DataForSEO account
- [ ] Implement Google Organic endpoint
- [ ] Configure Germany
- [ ] Configure German
- [ ] Retrieve top 10
- [ ] Store raw JSON
- [ ] Parse SERP results

### P0.7 Scoring

- [ ] Implement commercial intent
- [ ] Implement SEO opportunity
- [ ] Implement affiliate quality
- [ ] Implement revenue model
- [ ] Implement opportunity score
- [ ] Implement confidence score

### P0.8 Reporting

- [ ] Export CSV
- [ ] Create niche ranking
- [ ] Create keyword ranking
- [ ] Create affiliate-program ranking
- [ ] Create revenue scenario report

---

# 44. P1 — Should Have

- [ ] Automatic keyword clustering
- [ ] Semantic niche clustering
- [ ] Competitor domain classification
- [ ] Domain authority/backlink enrichment
- [ ] Content freshness analysis
- [ ] Query-to-page matching
- [ ] Search Console ingestion
- [ ] Affiliate click ingestion
- [ ] Revenue dashboard
- [ ] API cost dashboard

---

# 45. P2 — Later

Do not build before validation.

- [ ] LLM-powered niche discovery
- [ ] LLM keyword classification
- [ ] Automatic content briefs
- [ ] Automatic article generation
- [ ] Automatic internal linking
- [ ] CMS publishing
- [ ] Automatic content refresh
- [ ] Agentic workflow
- [ ] Multi-network optimization
- [ ] Multi-country expansion

---

# 46. First Dashboard

The first dashboard should answer only five questions.

## 1. Which niches are attractive?

```text
Niche
Score
Revenue potential
Search demand
SEO opportunity
Affiliate quality
```

## 2. Which keywords should I target?

```text
Keyword
Volume
CPC
Intent
SERP opportunity
Revenue
Score
```

## 3. Which affiliate programs are attractive?

```text
Merchant
Network
Commission
AOV
Effective commission
Recurring
EPC
```

## 4. Why is a keyword attractive?

Show:

```text
high demand
high commercial intent
weak SERP
good commission
```

## 5. What should I build next?

```text
BUILD
RESEARCH
BACKLOG
IGNORE
```

---

# 47. Example Final Output

```text
Rank | Niche              | Score | Revenue | SEO   | Affiliate
-----|--------------------|-------|---------|-------|----------
1    | Wärmepumpe         | 84    | €4,800  | 86    | 78
2    | Photovoltaik        | 81    | €3,900  | 72    | 91
3    | Balkonkraftwerk     | 77    | €2,100  | 83    | 74
4    | Stromvergleich      | 73    | €5,600  | 54    | 93
5    | VPN                 | 69    | €2,800  | 49    | 88
```

The ranking is illustrative only.

---

# 48. Critical Design Principle

Do not build a model that says:

> "This niche has an Opportunity Score of 87.3."

without explaining why.

Every score should be decomposable:

```text
Opportunity = 82

RevenuePotential   91
SearchDemand       74
CommercialIntent   88
SEOOpportunity     81
AffiliateQuality   79
ContentFeasibility 76
```

And each number should be traceable to raw data.

This makes the system auditable and allows the scoring formula to evolve.

---

# 49. Recommended Implementation Order

The most efficient implementation sequence is:

```text
Week 1
------
SQLite
schemas
100 niches
Awin
ADCELL import

Week 2
------
Google Ads API
keyword discovery
keyword normalization
commercial intent

Week 3
------
DataForSEO
SERP collection
SERP classification
SEO opportunity

Week 4
------
revenue model
opportunity score
dashboard
top-20 niche report

Week 5
------
select top 3 niches
select 30–45 keywords
publish first content

Week 6–12
---------
Google indexing
Search Console
affiliate clicks
conversions
revenue
model calibration
```

The exact calendar can be compressed if implementation time is available.

---

# 50. Final MVP Success Criterion

The MVP is **not successful** because:

```text
the APIs work
the database works
the dashboard looks good
10,000 keywords were collected
```

The MVP is successful only if it demonstrates:

```text
DATA
  ↓
good niche identified
  ↓
commercial keyword identified
  ↓
SERP opportunity identified
  ↓
content published
  ↓
Google traffic
  ↓
affiliate clicks
  ↓
conversion
  ↓
revenue
```

The ultimate validation metric is:

```text
Expected lifetime affiliate gross profit
----------------------------------------
Content + infrastructure + acquisition cost
```

If this ratio is convincingly > 1 for a repeatable niche, then—and only then—invest in the fully automated affiliate intelligence and content-production platform.

---

# 51. Immediate Next Actions

The next concrete engineering tasks should be:

1. Create the SQLite schema.
2. Create the 100 initial niche seed list.
3. Create Awin publisher account/API access.
4. Create ADCELL publisher account and obtain the first program export.
5. Create/configure Google Ads API access.
6. Create DataForSEO account.
7. Implement four collectors:
   - `AwinCollector`
   - `AdcellImporter`
   - `GoogleKeywordCollector`
   - `DataForSeoSerpCollector`
8. Run the first pipeline.
9. Produce `top_100_niches.csv`.
10. Manually review the top 20.
11. Select 3 niches for the real-world content experiment.

---

# 52. Sources / Current API Notes

- Awin Publisher API supports program discovery, program details and commission groups; commission groups provide the commission values available to the publisher for eligible program relationships.
- Google Ads API's KeywordPlanIdeaService supports keyword ideas and historical metrics with location/language targeting.
- DataForSEO currently publishes Google Organic SERP pricing starting at $0.0006 per first-page SERP in the standard normal-priority queue. But ask for my approval before you have to pay any services.
- ADCELL currently lists more than 2,300 partner programs and exposes publisher-facing program information.

These API capabilities and prices should be rechecked immediately before production implementation because external providers can change quotas, access requirements and pricing.
