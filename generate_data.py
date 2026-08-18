"""
Generates a synthetic partner performance dataset for a
Partner Pricing & Performance dashboard (Metabase project).

Columns:
    month, partner_id, partner_name, region, pricing_tier,
    leads, conversion_rate, funded_deals, avg_deal_size,
    funded_amount, forecast_funded_amount, variance

Run:
    python generate_data.py

Output:
    partner_performance.csv
"""

import numpy as np
import pandas as pd
from datetime import date

np.random.seed(42)

# ---- Config ----
N_MONTHS = 24
START_MONTH = date(2024, 9, 1)
REGIONS = ["UK", "EU", "US"]
TIERS = ["Standard", "Preferred", "Premium"]

PARTNERS = [
    {"partner_id": f"P{i:03d}", "partner_name": name, "region": region, "pricing_tier": tier}
    for i, (name, region, tier) in enumerate([
        ("Amber Retail", "UK", "Standard"),
        ("Northfield Traders", "UK", "Preferred"),
        ("Solstice Commerce", "UK", "Premium"),
        ("Berlin Marketplace", "EU", "Standard"),
        ("Lumen Goods", "EU", "Preferred"),
        ("Vantage EU", "EU", "Premium"),
        ("Cascade Retail US", "US", "Standard"),
        ("Union Square Goods", "US", "Preferred"),
        ("Pinnacle Commerce", "US", "Premium"),
        ("Harborline Traders", "UK", "Standard"),
        ("Meridian Supply", "EU", "Standard"),
        ("Crestpoint US", "US", "Preferred"),
    ], start=1)
]

months = pd.date_range(START_MONTH, periods=N_MONTHS, freq="MS")

rows = []
for partner in PARTNERS:
    # Each partner has its own baseline scale and trend so the dataset
    # has real variation to explain, not just noise.
    base_leads = np.random.randint(150, 900)
    trend = np.random.uniform(-0.01, 0.03)  # monthly growth/decline
    base_conversion = np.random.uniform(0.15, 0.35)
    avg_deal_size = np.random.uniform(3000, 15000)

    tier_multiplier = {"Standard": 1.0, "Preferred": 1.08, "Premium": 1.15}[partner["pricing_tier"]]

    for i, month in enumerate(months):
        seasonal = 1 + 0.08 * np.sin(2 * np.pi * i / 12)
        leads = max(10, int(base_leads * (1 + trend) ** i * seasonal * np.random.normal(1, 0.07)))

        conversion_rate = np.clip(base_conversion * np.random.normal(1, 0.10), 0.05, 0.6)
        funded_deals = int(leads * conversion_rate)
        funded_amount = round(funded_deals * avg_deal_size * tier_multiplier * np.random.normal(1, 0.05), 2)

        # Forecast is the "plan" set at the start of the month: close to actual
        # most of the time, but with realistic miss patterns (over and under).
        forecast_bias = np.random.normal(0, 0.12)
        forecast_funded_amount = round(funded_amount * (1 - forecast_bias), 2)
        variance = round(funded_amount - forecast_funded_amount, 2)

        rows.append({
            "month": month.strftime("%Y-%m-%d"),
            "partner_id": partner["partner_id"],
            "partner_name": partner["partner_name"],
            "region": partner["region"],
            "pricing_tier": partner["pricing_tier"],
            "leads": leads,
            "conversion_rate": round(conversion_rate, 4),
            "funded_deals": funded_deals,
            "avg_deal_size": round(avg_deal_size, 2),
            "funded_amount": funded_amount,
            "forecast_funded_amount": forecast_funded_amount,
            "variance": variance,
        })

df = pd.DataFrame(rows)
df.to_csv("partner_performance.csv", index=False)

print(f"Generated {len(df)} rows across {len(PARTNERS)} partners and {N_MONTHS} months.")
print(f"Saved to partner_performance.csv")
print()
print(df.head())