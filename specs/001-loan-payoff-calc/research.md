# Research: Student Loan Payoff Calculator

**Phase**: 0 - Outline & Research
**Purpose**: Resolve all NEEDS CLARIFICATION items from Technical Context
**Date**: 2026-01-26

## Research Tasks

From Technical Context, we identified these unknowns:

1. JavaScript charting library selection (Chart.js vs Plotly vs D3.js)
2. Production database choice (PostgreSQL vs SQLite)
3. Production deployment platform
4. UK tax data storage approach

---

## 1. JavaScript Charting Library Selection

**Question**: Which library best supports line graphs with uncertainty bands (shaded regions) and responsive design?

### Options Evaluated

#### Chart.js

**Pros:**
- Lightweight (~60KB minified)
- Simple API, quick setup
- Native support for line charts with fill regions (uncertainty bands)
- Responsive by default
- Good Bootstrap integration
- Active community, well-documented
- Free and MIT licensed

**Cons:**
- Limited interactivity compared to Plotly
- Basic annotation features (may need plugins)
- Less powerful for complex scientific visualizations

**Uncertainty Band Implementation:**
- Use `fill: '+1'` or `fill: '-1'` to fill between datasets
- Create 3 datasets: optimistic, realistic, pessimistic
- Fill region between optimistic and pessimistic for uncertainty band

**Code Example:**
```javascript
// Chart.js supports fill between lines natively
datasets: [
  { label: 'Optimistic', data: [...], borderColor: 'green', fill: false },
  { label: 'Realistic', data: [...], borderColor: 'blue', fill: false },
  { label: 'Pessimistic', data: [...], borderColor: 'red', fill: '+1' } // Fills to next dataset
]
```

#### Plotly.js

**Pros:**
- Powerful interactive features (zoom, pan, hover tooltips)
- Native support for filled areas and error bands
- Scientific-grade visualizations
- Excellent for complex data

**Cons:**
- Large bundle size (~3MB minified, ~1MB with partial bundle)
- More complex API
- Overkill for simple line graph with bands
- Steeper learning curve

**Uncertainty Band Implementation:**
- Use `fill: 'tonexty'` to fill between traces
- Rich tooltip customization

#### D3.js

**Pros:**
- Maximum flexibility and customization
- Complete control over every aspect
- Industry standard for custom visualizations

**Cons:**
- Steepest learning curve
- Requires significantly more code
- Manual responsive design implementation
- Overkill for standard line chart
- Higher maintenance burden

### Decision: Chart.js

**Rationale:**
- **YAGNI Principle**: Chart.js provides everything needed without over-engineering
- **Performance**: 60KB vs 1-3MB (Plotly/D3) - critical for mobile users
- **Bootstrap Integration**: Works seamlessly with Bootstrap responsive grid
- **Simplicity**: Minimal code to achieve requirements (line graph + uncertainty bands)
- **Uncertainty Bands**: Native support via `fill` property between datasets
- **Time to Market**: Fastest implementation, well-documented patterns

**Alternatives Considered:**
- Plotly.js: Rejected due to bundle size and complexity for simple use case
- D3.js: Rejected due to development time and YAGNI violation

---

## 2. Production Database Choice

**Question**: PostgreSQL vs SQLite for production deployment?

### Analysis

**Application Characteristics:**
- Stateless calculator (no user accounts, no persistence between sessions)
- UK tax threshold data is read-only configuration (rarely changes)
- No concurrent writes (only reads of tax data)
- Single-page application with no data storage requirements
- Performance-critical calculations happen in Python (not database)

### SQLite Approach

**Pros:**
- Zero configuration, file-based
- No separate database server to manage
- Perfect for read-only reference data
- Reduces deployment complexity
- Sufficient for UK tax threshold lookups (< 100 rows)
- Included with Python/Django

**Cons:**
- Not suitable for high-concurrency writes (not applicable here)
- Limited user management features (not needed - no auth)

### PostgreSQL Approach

**Pros:**
- Production-grade for multi-user applications
- Better for concurrent writes and complex queries

**Cons:**
- Requires separate database server
- Additional configuration and maintenance
- Overkill for read-only config data
- Increased deployment complexity

### Decision: SQLite for Production

**Rationale:**
- **YAGNI Principle**: No database features needed beyond simple config lookup
- **Stateless Application**: No user data storage = no database scaling concerns
- **Read-Only Data**: UK tax thresholds are configuration, not dynamic data
- **Deployment Simplicity**: Single file deployment, no DB server management
- **Performance**: SQLite more than sufficient for <100 row lookups

**Alternatives Considered:**
- PostgreSQL: Rejected as over-engineering for stateless calculator with read-only config
- JSON File: Considered but SQLite provides better query capability if needed later

**Migration Path**: If application evolves to require user accounts or data persistence, Django makes PostgreSQL migration straightforward.

---

## 3. Production Deployment Platform

**Question**: Where to deploy Django application for production?

### Options Evaluated

#### Heroku

**Pros:**
- Simple git-based deployment
- Free tier available (with limitations)
- Django-friendly with buildpacks
- Automatic SSL
- Easy scaling

**Cons:**
- Free tier has sleep timeout (30 min inactivity)
- More expensive than alternatives for 24/7 uptime
- Vendor lock-in concerns

#### PythonAnywhere

**Pros:**
- Designed specifically for Python/Django
- Free tier with always-on
- Simple web-based configuration
- Good for learning and MVPs

**Cons:**
- Limited customization on free tier
- Less professional for production
- Scaling limitations

#### DigitalOcean App Platform

**Pros:**
- Affordable ($5/month for basic app)
- Good Django support
- Predictable pricing
- Better performance than Heroku free tier

**Cons:**
- Requires more configuration than Heroku
- No free tier

#### Railway

**Pros:**
- Modern deployment platform
- Free tier with $5/month credit
- Git-based deployment
- Better free tier than Heroku
- Good Django support

**Cons:**
- Newer platform (less mature ecosystem)
- Free tier credit may be insufficient for heavy usage

### Decision: Railway (MVP), with DigitalOcean path

**Rationale:**
- **MVP Phase**: Railway free tier ($5 credit/month) is perfect for initial deployment and user testing
- **Cost-Effective**: Free tier sufficient for low-traffic calculator
- **Simple Deployment**: Git push to deploy (like Heroku)
- **Django Support**: Native Django buildpack support
- **Migration Path**: Easy to migrate to DigitalOcean App Platform when scaling needed

**Alternatives Considered:**
- Heroku: Rejected due to sleep timeout on free tier (poor UX for calculator)
- PythonAnywhere: Considered but Railway offers better developer experience
- DigitalOcean: Reserved for post-MVP when consistent traffic justifies $5/month

---

## 4. UK Tax Data Storage Approach

**Question**: How to structure and store UK Plan 2 student loan repayment thresholds?

### Options Evaluated

#### Option A: JSON Configuration File

**Approach:**
```json
{
  "plan_2": {
    "repayment_threshold_2023": 27295,
    "repayment_rate": 0.09,
    "inflation_adjustment": 0.025,
    "threshold_history": [
      {"year": 2021, "threshold": 27295},
      {"year": 2022, "threshold": 27295},
      {"year": 2023, "threshold": 27295}
    ]
  }
}
```

**Pros:**
- Simple, no database queries needed
- Version controlled in git
- Easy to update (edit file, redeploy)
- Transparent (developers can see values)

**Cons:**
- Not queryable with complex logic
- Requires app restart to update (not issue for annual updates)

#### Option B: Database Model

**Approach:**
```python
class TaxThreshold(models.Model):
    year = models.IntegerField()
    threshold = models.DecimalField()
    repayment_rate = models.DecimalField()
```

**Pros:**
- Queryable with Django ORM
- Can add admin interface for updates

**Cons:**
- Overkill for ~10 data points
- Requires database migration for schema changes
- Adds unnecessary complexity

#### Option C: Django Settings

**Approach:**
```python
# settings.py
UK_PLAN_2_REPAYMENT = {
    'threshold_2023': 27295,
    'rate': 0.09,
    'inflation': 0.025
}
```

**Pros:**
- Django-native approach
- Centralized configuration

**Cons:**
- Settings file becomes cluttered
- Harder to maintain historical data
- Not version controlled separately

### Decision: JSON Configuration File (Option A)

**Rationale:**
- **YAGNI Principle**: Simplest solution that meets requirements
- **Transparency**: Tax thresholds visible in version control
- **Annual Updates**: Threshold changes once per year - file update acceptable
- **No Complexity**: No database queries, migrations, or admin interface needed
- **Testability**: Easy to mock/override in unit tests

**Implementation:**
- Store at `data/uk_tax_thresholds.json`
- Load once at application startup (cache in memory)
- Service layer reads from cached config
- Document update process in README

**Alternatives Considered:**
- Database model: Rejected as over-engineering for static annual configuration
- Django settings: Rejected to keep settings.py clean and separate concerns

---

## Summary of Decisions

| Research Area | Decision | Rationale |
|--------------|----------|-----------|
| **Charting Library** | Chart.js | Lightweight (60KB), native uncertainty bands, Bootstrap compatible, YAGNI compliant |
| **Production Database** | SQLite | Stateless app with read-only config, no scaling concerns, deployment simplicity |
| **Deployment Platform** | Railway (MVP) → DigitalOcean (scale) | Free tier for MVP, simple git deployment, clear scaling path |
| **UK Tax Data** | JSON config file | Simplest solution, version controlled, annual updates acceptable, YAGNI compliant |

All decisions align with constitution principles: YAGNI, simplicity, avoid over-engineering.

---

## Technology Stack Summary

**Confirmed Decisions:**

- **Backend**: Django 5.1 + Python 3.13
- **Frontend**: Bootstrap 5.3 + Chart.js 4.x
- **Database**: SQLite (dev and production)
- **Testing**: pytest + pytest-django
- **Linting**: Ruff
- **Deployment**: Railway (MVP phase)
- **UK Tax Data**: JSON configuration file

**Dependencies to Add:**

```txt
Django>=5.1,<5.2
pytest>=8.0
pytest-django>=4.8
ruff>=0.2
```

**Frontend CDN (Bootstrap + Chart.js):**

```html
<!-- Bootstrap 5.3 -->
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>

<!-- Chart.js 4.x -->
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.min.js"></script>
```

---

## Next Steps

Phase 0 complete. All NEEDS CLARIFICATION items resolved. Ready to proceed to Phase 1:

1. Generate data-model.md (calculator entities and validation)
2. Generate contracts/ (API endpoint specification)
3. Generate quickstart.md (developer setup guide)
4. Update agent context with new technologies
