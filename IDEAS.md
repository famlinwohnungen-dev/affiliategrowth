# Germany Affiliate Niche Intelligence — MVP Specification

**Version:** 0.1  
**Date:** 2026-09-09  
**Scope:** Germany / German-language Affiliate Market Discovery  
**Objective:** Minimum-cost validation of an automated system that discovers profitable Affiliate Niches before investing in large-scale content production.

---

## 1. Background

The proposed business model is a data-driven Affiliate website in Germany. Instead of selecting a niche based only on intuition, search volume, or the highest advertised commission, the system should combine:

1. German search demand
2. SEO/SERP competition
3. Affiliate network availability
4. Actual Affiliate programs
5. Commission model and economics
6. Recurring vs. one-time revenue
7. Average order/customer value
8. Commercial search intent
9. SERP competitor strength
10. Estimated revenue at different traffic levels

The central hypothesis is:

> A niche is attractive only when sufficient German search demand, commercially valuable search intent, attainable SERPs, and sufficiently attractive affiliate economics overlap.

The MVP is deliberately smaller than the eventual platform. It is intended to determine whether this hypothesis can produce one or more niches with credible and eventually measurable Affiliate revenue.

### Important principle

The system must distinguish **prediction** from **validation**.

Predicted revenue is a model output. Actual Affiliate clicks, leads, sales, and commissions are the eventual ground truth.

---

# 2. Purpose

The purpose of this MVP is to build a repeatable research pipeline that can answer:

> **“Which German Affiliate niches and keywords are worth investing content-production effort in?”**

The MVP shall:

- discover an initial pool of 50–100 candidate niches;
- identify relevant Affiliate programs;
- collect German search-demand data;
- identify commercially relevant keywords;
- collect and analyze SERP competitors;
- normalize Affiliate commission models;
- estimate revenue under conservative/base/optimistic assumptions;
- calculate an Opportunity Score;
- produce a ranked list of niches and keywords;
- provide a recommendation: `BUILD`, `RESEARCH`, `BACKLOG`, or `IGNORE`.

The MVP is **not** intended to:

- build a full Affiliate website network;
- automatically publish hundreds of articles;
- maximize SEO traffic at any cost;
- build a sophisticated SaaS dashboard;
- support every Affiliate network;
- guarantee revenue.

---

# 3. Requirements

## 3.1 Step 1 — Generate the First 50–100 Candidate Niches

### Objective

Create a broad but structured candidate universe before selecting the first niche.

### Sources

The candidate universe should be generated from multiple sources:

1. Affiliate network categories
2. Affiliate merchant/program categories
3. Search keyword seeds
4. Commercial product/service categories
5. Google Ads Keyword Planner keyword ideas
6. Public market/category taxonomies
7. Optional later sources: Google Trends, Reddit, forums, marketplaces

Google Ads API's `KeywordPlanIdeaService` supports keyword ideas from keyword seeds, URLs, or sites and allows targeting by location and language. Historical metrics such as search volume can then be used to filter candidates. citeturn0search6turn0search7

### Candidate-generation rule

Do not start with a manually chosen list of only 5–10 niches.

Generate at least:

```text
50 minimum
100 preferred
200 optional
```

Then normalize them into a hierarchical taxonomy:

```text
Home & Energy
├── Photovoltaik
├── Stromspeicher
├── Wärmepumpe
├── Wallbox
└── Smart Home

Software
├── AI Tools
├── Developer Tools
├── CRM
├── Project Management
└── Accounting Software

Travel
├── Hotels
├── Family Travel
├── Car Rental
└── Travel Insurance
```

### Niche-generation output

Every candidate must have:

- `niche_id`
- `parent_category`
- `niche_name`
- `description`
- `seed_keywords`
- `candidate_source`
- `initial_affiliate_count`
- `initial_search_signal`

---

# 4. Step 2 — Affiliate Networks and Data Sources

## 4.1 MVP Network Priority

The MVP should begin with:

### Tier 1

- Awin
- ADCELL

### Tier 2 — only if required by the selected niche

- Impact
- CJ
- TradeTracker
- Amazon PartnerNet
- specialist networks such as finance/insurance networks

The objective is not to integrate every network. The objective is to obtain enough program coverage to validate whether attractive economics exist.

## 4.2 Awin

Awin's Publisher API supports program discovery, including filtering program lists by country, and provides program details and commission information. citeturn0search5turn0search4

Awin also provides commission-group information for joined programs. citeturn0search1

Awin's publisher APIs use OAuth 2.0 access tokens. citeturn0search12

### Required Awin fields

At minimum:

```text
program_id
program_name
advertiser_name
advertiser_url
country
currency
status
category
valid_domains
relationship_status
commission_groups
commission_type
commission_value
program_description
data_feed_available
deep_link_available
last_updated
```

## 4.3 Affiliate Commission Normalization

Different networks use different terminology. Internally normalize into:

```text
CPS_PERCENT
CPS_FIXED
CPL
CPA
CPC
RECURRING_PERCENT
RECURRING_FIXED
HYBRID
UNKNOWN
```

Awin currently documents CPA, CPL and CPC as commission models, with CPA supporting either a percentage of order value or a fixed amount. citeturn0search3

### Critical requirement

Never assume:

```text
commission = actual realized revenue
```

The database must distinguish:

```text
advertised_commission
estimated_effective_commission
actual_commission
```

Actual commission becomes available only after the Affiliate program generates real performance data.

---

# 5. Step 3 — Google Keyword API for Germany

## 5.1 Primary source

Use Google Ads API Keyword Planning as the primary structured search-demand source.

Google's API supports:

- keyword ideas;
- historical metrics;
- location targeting;
- language targeting;
- search-network settings;
- historical date ranges. citeturn0search6turn0search7

Historical metrics include:

- average monthly searches;
- monthly search volume;
- competition level;
- competition index;
- bid percentiles;
- optional average CPC. citeturn0search8

## 5.2 Germany configuration

The MVP shall use:

```text
Country / Geo:
Germany

Language:
German

Network:
Google Search / configured search network

Adult keywords:
false

Date:
latest available historical period
```

### Important

The system must store the exact:

```text
geo_target
language
network
date_range
data_source
retrieval_timestamp
```

Search volume is not a timeless constant.

Google states that historical metrics refresh monthly and recommends caching/storing keyword-planning responses because the data does not change frequently. citeturn0search9

## 5.3 Keyword fields

```text
keyword_id
keyword
normalized_keyword
language
country
search_volume_avg
search_volume_monthly[]
competition_level
competition_index
cpc_low
cpc_high
cpc_average
trend
seasonality
source
retrieved_at
```

---

# 6. Step 4 — SERP Data: Required Fields

SERP analysis is required because search volume alone does not tell us whether a new website can realistically rank.

For each keyword, retrieve the first 10 organic results.

## 6.1 SERP Result Schema

```text
serp_id
keyword_id
position
domain
url
title
snippet
content_type
domain_authority
page_authority
backlinks
referring_domains
estimated_traffic
publication_date
last_modified
brand_indicator
affiliate_indicator
forum_indicator
reddit_indicator
video_indicator
query_match_score
retrieved_at
```

Not every field needs to be available from the first SERP provider. Fields that cannot be obtained reliably should be nullable rather than fabricated.

## 6.2 Content Type Classification

Each result should be classified:

```text
commercial
affiliate
manufacturer
publisher
review
comparison
forum
reddit
video
marketplace
government
encyclopedia
other
```

This enables detection of SERP weaknesses.

## 6.3 SERP Opportunity Signals

Positive signals:

```text
forum results
Reddit results
small publishers
outdated content
poor query match
thin content
missing comparison/review content
weak affiliate coverage
```

Negative signals:

```text
strong brands
Stiftung Warentest / authoritative institutions
large established publishers
high-authority domains
strong specialized affiliate sites
high-quality exact-match content
```

### Weak SERP Ratio

Define:

```text
WeakSERPRatio =
number_of_weak_results / 10
```

Example:

```text
6 weak results / 10
= 0.60
```

This should become an important component of the SEO Opportunity Score.

---

# 7. Step 5 — Affiliate Program Schema

The normalized Affiliate Program entity shall be:

```text
AffiliateProgram
-------------------------
program_id
network
merchant_id
merchant_name
merchant_domain
merchant_category
country
currency

commission_type
commission_value
commission_min
commission_max
commission_currency

recurring
recurring_period
recurring_duration

cookie_duration
aov_estimate
epc_estimate
conversion_estimate

lead_value
new_customer_only
existing_customer_allowed

approval_required
relationship_status
deep_link_available
product_feed_available

program_status
source_url
source_last_updated
retrieved_at
```

## 7.1 Why these fields matter

### `commission_type`

Distinguishes:

```text
5% sale
€40 CPA
€80 CPL
€20/month recurring
```

### `recurring`

Boolean:

```text
true / false / unknown
```

### `aov_estimate`

Average Order Value.

For percentage-based CPS:

```text
ExpectedCommission =
AOV × CommissionRate
```

### `epc_estimate`

Earnings Per Click.

If provided by the network, use it as a measured signal.

If not provided, estimate it only when sufficient data exists.

---

# 8. Step 6 — Keyword Schema

Keywords need to connect three domains:

```text
Keyword
   │
   ├── Niche
   ├── SERP
   └── Affiliate economics
```

Recommended schema:

```text
Keyword
-------------------------
keyword_id
niche_id
keyword
language
country

search_volume
cpc
competition_index

intent
intent_score

keyword_type
funnel_stage

affiliate_relevance
affiliate_program_count

serp_opportunity_score
serp_weak_ratio

estimated_ctr
estimated_traffic

estimated_conversion_rate
estimated_epc
estimated_revenue

opportunity_score

status
created_at
updated_at
```

## 8.1 Commercial Intent Classification

Initial rule-based classifier:

```text
100 = transactional
90  = best / comparison
85  = test / review
75  = pricing / cost
65  = alternatives
50  = experience / rating
30  = informational
10  = purely informational
```

This should later be replaced or augmented by an LLM/classifier trained against manually labeled examples.

---

# 9. Step 7 — Niche Schema

The Niche entity aggregates keywords and Affiliate programs.

```text
Niche
-------------------------
niche_id
name
parent_category
description

keyword_count
commercial_keyword_count
total_search_volume
commercial_search_volume

affiliate_program_count
active_program_count
recurring_program_count

avg_commission
median_commission
estimated_epc
estimated_aov

seo_opportunity_score
commercial_intent_score
affiliate_quality_score
content_feasibility_score

revenue_10k
revenue_50k
revenue_100k

opportunity_score

recommendation
recommendation_reason

created_at
updated_at
```

---

# 10. Step 8 — Revenue Calculation

Revenue estimation must be scenario-based.

Never output a single deterministic number.

## 10.1 Basic model

For a traffic level `T`:

```text
AffiliateClicks =
T × AffiliateCTR
```

```text
Conversions =
AffiliateClicks × ConversionRate
```

```text
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

## 10.2 Percentage commission

For CPS percentage:

```text
EffectiveCommission =
AOV × CommissionRate
```

Example:

```text
AOV = €500
Commission = 5%

EffectiveCommission = €25
```

## 10.3 Lead model

For CPL:

```text
Revenue =
Traffic
× AffiliateCTR
× LeadConversionRate
× CPL
```

## 10.4 Recurring model

For recurring programs:

```text
ExpectedLifetimeRevenue =
InitialCommission
+
ExpectedRecurringPayments
```

However, recurring revenue must not be treated as guaranteed.

Store:

```text
retention_months_estimate
recurring_probability
```

and calculate:

```text
ExpectedRecurringRevenue =
monthly_commission
× expected_retention_months
× probability_of_retention
```

## 10.5 Three scenarios

Every niche must produce:

```text
Conservative
Base
Optimistic
```

Example:

```text
Affiliate CTR:
5% / 10% / 15%

Conversion:
2% / 5% / 8%
```

The assumptions must be stored, not hard-coded.

---

# 11. Opportunity Score

The primary objective is not to find the largest search volume.

The objective is to find the best **risk-adjusted economic opportunity**.

## 11.1 Proposed initial formula

```text
OpportunityScore =

0.25 × RevenuePotential
+ 0.20 × SearchDemand
+ 0.20 × CommercialIntent
+ 0.20 × SEOOpportunity
+ 0.10 × AffiliateQuality
+ 0.05 × ContentFeasibility
```

All components are normalized to:

```text
0–100
```

## 11.2 Revenue Potential

Normalize expected revenue:

```text
RevenuePotential =
normalized(BaseRevenuePotential)
```

Do not use absolute revenue directly because one extremely large niche would dominate all results.

Recommended normalization:

```text
log1p(revenue)
```

followed by min-max or percentile normalization.

## 11.3 Search Demand

Use:

```text
commercial_search_volume
```

rather than total search volume wherever possible.

Recommended:

```text
SearchDemand =
70% commercial volume
30% total volume
```

## 11.4 Commercial Intent

Aggregate keyword intent weighted by search volume:

```text
CommercialIntent =
Σ(keyword_volume × keyword_intent)
/
Σ(keyword_volume)
```

## 11.5 SEO Opportunity

Initial formula:

```text
SEOOpportunity =

35% WeakSERPRatio
+ 20% QueryMismatch
+ 15% ContentWeakness
+ 15% FreshnessGap
+ 15% LowAuthorityPresence
```

This is deliberately a heuristic MVP score.

The model should later be calibrated against actual ranking results.

## 11.6 Affiliate Quality

Initial formula:

```text
AffiliateQuality =

30% program_count
+ 30% effective_commission
+ 20% recurring_ratio
+ 10% EPC
+ 10% program_stability
```

## 11.7 Content Feasibility

Consider:

```text
research difficulty
technical complexity
update frequency
fact-checking requirements
expertise requirement
content production cost
```

For the MVP:

```text
Easy      = 80–100
Medium    = 50–79
Hard      = 20–49
Very Hard = 0–19
```

---

# 12. Recommendation Engine

The final output must be more useful than a numerical score.

Each Niche receives:

```text
BUILD
RESEARCH
BACKLOG
IGNORE
```

## BUILD

Conditions:

```text
OpportunityScore >= 75
AND
Affiliate coverage sufficient
AND
Commercial demand sufficient
AND
SERP opportunity acceptable
```

## RESEARCH

Conditions:

```text
60 <= OpportunityScore < 75
```

or insufficient data.

## BACKLOG

Conditions:

```text
45 <= OpportunityScore < 60
```

## IGNORE

Conditions:

```text
OpportunityScore < 45
```

These thresholds are MVP defaults and must be calibrated against actual results.

---

# 13. Data Pipeline

The minimum pipeline should be:

```text
Affiliate Networks
       │
       ▼
Affiliate Collector
       │
       ▼
AffiliateProgram DB
       │
       ├──────────────┐
       │              │
       ▼              ▼
Niche Seeds      Merchant Data
       │              │
       └──────┬───────┘
              ▼
       Keyword Discovery
              │
              ▼
       Google Keyword Data
              │
              ▼
        Commercial Filter
              │
              ▼
           SERP API
              │
              ▼
        SERP Analysis
              │
              ▼
       Revenue Estimator
              │
              ▼
       Opportunity Scoring
              │
              ▼
      Ranked Niches/Keywords
```

---

# 14. Minimum Technical Architecture

The MVP should remain deliberately simple.

```text
Python
├── affiliate collectors
├── keyword collector
├── SERP collector
├── normalization
├── scoring
└── revenue simulation

SQLite (or other free engine, important easy to use)
├── niches
├── keywords
├── affiliate_programs
├── serp_results
├── revenue_assumptions
└── scores

Optional:
Streamlit
└── research dashboard
```

Do **not** start with:

- Kubernetes
- microservices
- complex event-driven architecture
- vector databases
- autonomous agents
- automated publishing

The first objective is economic validation.

---

# 15. Data Quality Requirements

Every external metric must carry:

```text
source
retrieved_at
country
language
time_period
confidence
```

Never mix:

```text
Germany search volume
with
global search volume
```

or:

```text
German keyword
with
English SERP
```

without explicitly recording the difference.

## Confidence

Each calculated metric should have:

```text
HIGH
MEDIUM
LOW
```

For example:

```text
Commission:
HIGH — directly supplied by network

AOV:
LOW — estimated from external data

Conversion:
LOW — modeled assumption

Revenue:
LOW — derived from assumptions
```

---

# 16. Result Expectation

At the end of the MVP discovery phase, the system should produce:

## 16.1 Candidate Niche Report

```text
Top 50–100 niches
```

For each:

```text
Niche
Opportunity Score
Search Demand
Commercial Demand
Affiliate Programs
Commission
Recurring Ratio
AOV
Estimated EPC
Revenue @ 10k
Revenue @ 50k
Revenue @ 100k
SEO Opportunity
Recommendation
```

## 16.2 Keyword Report

At least:

```text
500–2,000 candidate keywords
```

with:

```text
keyword
volume
CPC
commercial intent
SERP opportunity
affiliate relevance
estimated traffic
estimated revenue
opportunity score
```

## 16.3 SERP Report

For the highest-priority keywords:

```text
Top 10 competitors
domain
URL
content type
authority indicators
affiliate indicator
weakness indicators
SERP opportunity
```

## 16.4 Affiliate Report

At least:

```text
all discovered relevant programs
commission
commission type
recurring
AOV
EPC if available
network
country
approval status
```

---

# 17. Validation

Validation occurs at three levels.

## 17.1 Level 1 — Data Validation

Question:

> Can we reliably collect enough data to rank niches?

Pass criteria:

- ≥50 candidate niches
- ≥500 usable keywords
- ≥10 relevant Affiliate programs for at least some niches
- SERP data available for priority keywords
- no major Germany/language mismatch
- commission data normalized successfully

---

## 17.2 Level 2 — Model Validation

Question:

> Does the Opportunity Score identify opportunities that look genuinely attractive to a human expert?

Procedure:

1. Select top 20 niches automatically.
2. Manually review top 20.
3. Review the 20 lowest-ranked candidates.
4. Compare system ranking with expert judgment.
5. Identify false positives and false negatives.
6. Adjust weights.

Target:

```text
Top 20 precision >= 70%
```

for the initial manual validation.

This is not a business KPI; it is an MVP model-quality target.

---

## 17.3 Level 3 — Real Market Validation

This is the decisive test.

Select the top 3 niches.

For each:

```text
10–15 high-value pages
```

Total:

```text
30–45 pages
```

Then observe:

```text
Google impressions
Google clicks
ranking positions
affiliate clicks
leads
sales
commission
revenue/article
```

### The ultimate validation chain

```text
SEO impression
      ↓
Organic click
      ↓
Commercial page visit
      ↓
Affiliate click
      ↓
Lead / sale
      ↓
Commission
```

If this chain repeatedly occurs, the business hypothesis has evidence.

---

# 18. MVP Go / No-Go Criteria

## GO

Proceed to automation and scale if:

- at least one niche produces meaningful organic impressions;
- commercial keywords begin ranking;
- affiliate clicks occur;
- at least one conversion/lead is generated;
- revenue is repeatable rather than a single accidental transaction;
- estimated content economics are positive;
- the niche has enough additional keywords to scale.

## ITERATE

Continue experimentation if:

- impressions exist;
- rankings improve;
- affiliate clicks exist;
- conversion is not yet sufficient.

Optimize pages and offers before changing the niche.

## NO-GO

Stop or change niche if:

- no meaningful impressions after reasonable indexing time;
- SERP competition is substantially higher than predicted;
- relevant Affiliate programs are unavailable;
- Affiliate clicks occur but there is consistently no conversion;
- revenue potential is clearly below content production cost;
- the niche requires expertise or compliance effort disproportionate to its economics.

---

# 19. What Must NOT Be Automated in MVP

The following should initially remain human-controlled:

```text
Final niche selection
Final Affiliate program approval
Final content approval
Legal review
Fact checking for high-risk topics
Revenue assumption approval
```

Automation should support decisions, not conceal uncertainty.

---

# 20. Evolution Path

Once the MVP is validated:

```text
V0 — Manual research
      ↓
V1 — API-based data collection
      ↓
V2 — Automated niche scoring
      ↓
V3 — Automated keyword clustering
      ↓
V4 — Automated content briefs
      ↓
V5 — AI-assisted content production
      ↓
V6 — Search Console feedback loop
      ↓
V7 — Multi-niche expansion
```

The key rule is:

> **Only automate the next layer after the previous layer has demonstrated economic value.**

---

# 21. Final MVP Definition

The MVP is successful when a low-cost pipeline can answer, with traceable data:

> **“For the German market, these are the most attractive Affiliate niches, these are the keywords that create the opportunity, these are the Affiliate programs that monetize it, these are the current SERP competitors, this is the estimated revenue under multiple scenarios, and this is why the system recommends BUILD or IGNORE.”**

The MVP does not need perfect predictions.

It needs to be:

- repeatable;
- data-backed;
- inexpensive;
- explainable;
- falsifiable;
- connected to eventual real revenue.

The most important design principle is therefore:

```text
Prediction → Experiment → Actual Data → Calibration → Scale
```

rather than:

```text
Prediction → Massive Content Production
```

---

# 22. Recommended First Implementation Order

The first implementation should follow exactly this sequence:

```text
1. Candidate Niche Generator
        ↓
2. Affiliate Program Collector
        ↓
3. Google Keyword Collector
        ↓
4. Commercial Intent Classifier
        ↓
5. SERP Collector
        ↓
6. Revenue Simulator
        ↓
7. Opportunity Scoring
        ↓
8. Ranked Niche Report
```

Only after this pipeline produces a credible Top 10–20 should content production begin.

