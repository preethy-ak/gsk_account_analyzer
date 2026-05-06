# GSK Ecommerce Operations Dashboard

An automated Streamlit + Plotly dashboard that pulls **live data from Graas (Snowflake)**
and renders an 8-section operations report — Orders, ROAS, SKU performance, Vouchers,
Traffic YoY, Inventory, and Recommendations.

---

## Quick Start

### 1 — Install dependencies

```bash
cd gsk_dashboard
pip install -r requirements.txt
```

### 2 — Set credentials

```bash
cp .env.example .env
# Edit .env with your Graas Snowflake credentials
```

Required env vars:
| Variable | Example |
|----------|---------|
| `GRAAS_SNOWFLAKE_ACCOUNT` | `abc123.ap-southeast-1` |
| `GRAAS_SNOWFLAKE_USER` | `preethy@graas.ai` |
| `GRAAS_SNOWFLAKE_PASSWORD` | `••••••••` |
| `GRAAS_SNOWFLAKE_WAREHOUSE` | `COMPUTE_WH` |
| `GRAAS_SNOWFLAKE_DATABASE` | `GP_PRD_DWH` |
| `GRAAS_SNOWFLAKE_SCHEMA` | `GSK` |

### 3 — Run the dashboard

```bash
streamlit run dashboard.py
```

Opens at **http://localhost:8501**

---

## Running with Claude Code

Claude Code can automate this dashboard end-to-end. Drop this into your
Claude Code session after installing:

```
Run the GSK Ecommerce Dashboard and open it in the browser.
```

Claude Code will:
1. Check requirements are installed
2. Start the Streamlit server
3. Open the browser to `localhost:8501`
4. Auto-reload on code changes

---

## Project Structure

```
gsk_dashboard/
├── dashboard.py            ← Main Streamlit app (8 tabs)
├── src/
│   ├── __init__.py
│   └── data_loader.py      ← All Snowflake queries
├── .streamlit/
│   └── config.toml         ← Dark theme config
├── requirements.txt
├── .env.example            ← Credential template
└── README.md
```

---

## Dashboard Sections

| Tab | Contents |
|-----|----------|
| 01 Executive Summary | KPIs, revenue by channel, health scorecard, daily trend |
| 02 Orders & Revenue | Order volume, revenue vs voucher, YoY bar chart |
| 03 Ad Spend & ROAS | ROAS by channel, spend vs revenue bubble chart |
| 04 SKU Performance | Top 10 & Bottom 10 SKUs, loss-leader table |
| 05 Voucher Performance | Voucher %, promo type breakdown |
| 06 Traffic YoY | Visitor comparison Q1 2025 vs Q1 2026, conversion rate |
| 07 Store Operations | Listing health, inventory summary, ops checklist |
| 08 Recommendations | Prioritized P1/P2/P3 action cards |

---

## Sidebar Controls

- **Date range** — pick any period (defaults to Q1 2026)
- **Channel filter** — Shopee / Lazada / TikTok
- **YoY toggle** — compare against same period last year
- **Refresh button** — clears cache and reloads from Snowflake

---

## Automation / Scheduling

To auto-generate a daily report email or Slack message, run:

```bash
# Headless export to PDF (requires playwright)
pip install playwright
playwright install chromium
python export_report.py --date-from 2026-01-01 --date-to 2026-03-31
```

Or schedule with cron:

```cron
0 8 * * 1 cd /path/to/gsk_dashboard && python export_report.py
```

---

## Data Sources (Graas Snowflake Views)

| View | Used For |
|------|----------|
| `ORD_FCT_REPORT_DAILY_AGG` | Orders, revenue, promotions |
| `ORD_FCT_PRODUCT_REPORT_DAILY_AGG` | SKU-level performance |
| `TRF_FCT_SESSIONS_AGG` | Traffic & conversion |
| `MKG_FCT_CAMPAIGN_PERFORMANCE_AGG` | Ad spend & ROAS |
| `INV_DIM_PRODUCTS_AGG` | Inventory & listing health |

---

## Troubleshooting

**Connection error:** Check your `.env` file and ensure the Snowflake account
string includes the region (e.g. `abc123.ap-southeast-1`).

**No data returned:** Verify your Snowflake role has SELECT access on the GSK schema.

**Slow first load:** Initial query hits Snowflake cold cache — subsequent loads use
Streamlit's 1-hour cache (`@st.cache_data(ttl=3600)`).
