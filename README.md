# Partner Pricing & Performance Dashboard

A commercial performance dashboard built in Metabase, connected to a PostgreSQL
database, modelling the kind of partner-level pricing and forecasting analysis
used in commercial/strategy teams (leads → conversion → funded amount, forecast
vs actual variance, and partner-level breakdowns).

---

## Problem Statement

Commercial and strategy teams need to answer three recurring questions every
month: which partners are driving the most value, how is performance trending
over time, and where is actual performance diverging from forecast (and by how
much). This project builds a small but realistic dataset and a dashboard that
answers all three.

---

## Dataset

Generated synthetically in Python (`generate_data.py`) rather than sourced from
a real company, since this is a portfolio project. The generator produces
realistic, non-trivial patterns on purpose (per-partner growth trends,
seasonality, and forecast bias) so the dashboard has genuine variance to
explain, not flat lines.

- 12 partners across UK, EU, and US regions
- 3 pricing tiers (Standard, Preferred, Premium)
- 24 months of history per partner (288 rows total)
- Columns: month, partner, region, pricing tier, leads, conversion rate,
  funded deals, average deal size, funded amount, forecast funded amount,
  variance

---

## Stack

- **Python** (pandas, numpy) — synthetic data generation
- **PostgreSQL** — data storage
- **Metabase** — dashboarding and analysis

---

## Dashboard

![Dashboard overview](screenshots/dashboard-overview.png)

The dashboard combines four views:

1. **Total Variance (All Partners)** — headline number, total forecast vs
   actual variance across all partners and months
2. **Funded Amount by Partner** — bar chart ranking partners by total funded
   amount
3. **Funded Amount Trend by Month** — line chart of total funded amount over
   time
4. **Forecast vs Actual Funded Amount by Month** — two-line chart showing
   where actual performance diverges from forecast

---

## How to Run

**1. Generate the dataset**
```bash
pip install pandas numpy
python generate_data.py
```
This produces `partner_performance.csv`.

**2. Load into PostgreSQL**
```sql
CREATE DATABASE partner_pricing_demo;

CREATE TABLE partner_performance (
    month DATE,
    partner_id TEXT,
    partner_name TEXT,
    region TEXT,
    pricing_tier TEXT,
    leads INTEGER,
    conversion_rate NUMERIC(5,4),
    funded_deals INTEGER,
    avg_deal_size NUMERIC(12,2),
    funded_amount NUMERIC(14,2),
    forecast_funded_amount NUMERIC(14,2),
    variance NUMERIC(14,2)
);
```
Then import `partner_performance.csv` into the table (via `psql \copy` or
pgAdmin's Import/Export tool).

**3. Connect Metabase**
Run Metabase locally, connect it to `partner_pricing_demo` as a PostgreSQL
data source, and build the four questions described above.

---

## Author

Isha Atif
MRes Applied Artificial Intelligence, University of Greater Manchester
Data Operations Analyst, BeautyZone London
GitHub: github.com/isha-atif-dev
LinkedIn: linkedin.com/in/isha-atif