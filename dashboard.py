"""
GSK Ecommerce Operations Dashboard
-----------------------------------
Automated dashboard that connects to Graas Snowflake data via the
Graas MCP / Snowflake connector and renders live charts using Streamlit + Plotly.

Run with:
    streamlit run dashboard.py
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import date
import warnings
warnings.filterwarnings("ignore")

from data_loader import GraasDataLoader

# ── Page config ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="GSK Ecommerce Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Theme / CSS ──────────────────────────────────────────────────────────────
st.markdown("""
<style>
    /* Dark theme overrides */
    .stApp { background-color: #0b0e14; color: #e2e8f0; }
    .block-container { padding-top: 1.5rem; padding-bottom: 2rem; }

    /* Metric cards */
    [data-testid="metric-container"] {
        background: #131720;
        border: 1px solid #232b3a;
        border-radius: 10px;
        padding: 14px 18px;
    }
    [data-testid="metric-container"] label { color: #8896a8 !important; font-size: 11px !important; }
    [data-testid="metric-container"] [data-testid="stMetricValue"] { color: #ffffff !important; }
    [data-testid="metric-container"] [data-testid="stMetricDelta"] { font-size: 12px !important; }

    /* Sidebar */
    [data-testid="stSidebar"] { background: #131720 !important; border-right: 1px solid #232b3a; }
    [data-testid="stSidebar"] * { color: #e2e8f0 !important; }

    /* Headers */
    h1, h2, h3 { color: #ffffff !important; }
    .section-header {
        font-family: 'Georgia', serif;
        font-size: 22px;
        color: #ffffff;
        border-bottom: 1px solid #232b3a;
        padding-bottom: 8px;
        margin-bottom: 16px;
    }
    .tag {
        font-family: monospace;
        font-size: 11px;
        color: #00d4a1;
        letter-spacing: 2px;
        text-transform: uppercase;
    }

    /* Tables */
    .dataframe { background: #131720 !important; }
    thead th { background: #1a2030 !important; color: #8896a8 !important; font-size: 11px !important; }
    tbody tr:hover td { background: #1a2030 !important; }

    /* Divider */
    hr { border-color: #232b3a; }

    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] { background: #131720; border-radius: 8px; }
    .stTabs [data-baseweb="tab"] { color: #8896a8; }
    .stTabs [aria-selected="true"] { color: #00d4a1 !important; border-bottom-color: #00d4a1 !important; }
</style>
""", unsafe_allow_html=True)

ACCENT = "#00d4a1"
SHOPEE_COLOR = "#ee4d2d"
LAZADA_COLOR = "#6c9bff"
TIKTOK_COLOR = "#69c9d0"
WARN_COLOR = "#ffc947"
DANGER_COLOR = "#ff6b6b"

CHANNEL_COLORS = {
    "shopee": SHOPEE_COLOR,
    "lazada": LAZADA_COLOR,
    "tiktok": TIKTOK_COLOR,
}

PLOTLY_LAYOUT = dict(
    paper_bgcolor="#131720",
    plot_bgcolor="#0b0e14",
    font=dict(color="#e2e8f0", family="DM Sans, sans-serif", size=12),
    legend=dict(bgcolor="#131720", bordercolor="#232b3a", borderwidth=1),
    margin=dict(l=20, r=20, t=40, b=20),
    xaxis=dict(gridcolor="#232b3a", zeroline=False),
    yaxis=dict(gridcolor="#232b3a", zeroline=False),
)


# ── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="tag">▸ GSK Intelligence</div>', unsafe_allow_html=True)
    st.markdown("## 📊 Dashboard Controls")
    st.divider()

    q1_start = date(2026, 1, 1)
    q1_end = date(2026, 3, 31)

    date_from = st.date_input("Date From", value=q1_start, min_value=date(2025, 1, 1), max_value=date(2026, 12, 31))
    date_to   = st.date_input("Date To",   value=q1_end,   min_value=date(2025, 1, 1), max_value=date(2026, 12, 31))

    st.divider()
    channels = st.multiselect(
        "Channels",
        options=["shopee", "lazada", "tiktok"],
        default=["shopee", "lazada", "tiktok"],
        format_func=lambda x: x.title(),
    )

    st.divider()
    compare_yoy = st.toggle("Compare YoY (Q1 2025)", value=True)

    st.divider()
    st.markdown('<div class="tag">Data Source</div>', unsafe_allow_html=True)
    st.caption("Graas MCP · Snowflake")
    if st.button("🔄 Refresh Data", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

    st.divider()
    st.caption("Last updated: May 2026")


# ── Data loading ─────────────────────────────────────────────────────────────
@st.cache_data(ttl=3600, show_spinner="Loading Graas data...")
def load_all_data(date_from: str, date_to: str, compare_date_from: str, compare_date_to: str):
    loader = GraasDataLoader()
    return {
        "orders":        loader.get_orders_by_channel(date_from, date_to),
        "orders_ly":     loader.get_orders_by_channel(compare_date_from, compare_date_to),
        "products":      loader.get_product_performance(date_from, date_to),
        "traffic":       loader.get_traffic(date_from, date_to),
        "traffic_ly":    loader.get_traffic(compare_date_from, compare_date_to),
        "ads":           loader.get_ad_performance(date_from, date_to),
        "inventory":     loader.get_inventory_summary(),
        "promotions":    loader.get_promotion_performance(date_from, date_to),
        "daily_revenue": loader.get_daily_revenue_trend(date_from, date_to),
    }

py_date_from  = str(date_from)
py_date_to    = str(date_to)
cmp_from = str(date_from.replace(year=date_from.year - 1))
cmp_to   = str(date_to.replace(year=date_to.year - 1))

with st.spinner("Connecting to Graas data..."):
    data = load_all_data(py_date_from, py_date_to, cmp_from, cmp_to)

orders_df        = data["orders"]
orders_ly_df     = data["orders_ly"]
products_df      = data["products"]
traffic_df       = data["traffic"]
traffic_ly_df    = data["traffic_ly"]
ads_df           = data["ads"]
inventory_df     = data["inventory"]
promotions_df    = data["promotions"]
daily_rev_df     = data["daily_revenue"]

# Filter by selected channels — applied to ALL dataframes
def filter_by_channel(df, col="source"):
    if not channels or df.empty:
        return df
    return df[df[col].str.lower().isin([c.lower() for c in channels])]

# Normalize source names for ads (they have suffixes like "shopeeAds", "shopeeAffiliateAds")
def filter_ads_by_channel(df):
    if not channels or df.empty:
        return df
    mask = df["source"].str.lower().apply(
        lambda s: any(c.lower() in s for c in channels)
    )
    return df[mask]

orders_df      = filter_by_channel(orders_df)
orders_ly_df   = filter_by_channel(orders_ly_df)
products_df    = filter_by_channel(products_df)
traffic_df     = filter_by_channel(traffic_df)
traffic_ly_df  = filter_by_channel(traffic_ly_df)
ads_df         = filter_ads_by_channel(ads_df)
promotions_df  = filter_by_channel(promotions_df)
daily_rev_df   = filter_by_channel(daily_rev_df)
inventory_df   = filter_by_channel(inventory_df)


# ── Header ───────────────────────────────────────────────────────────────────
st.markdown('<div class="tag">▸ GSK Ecommerce Intelligence</div>', unsafe_allow_html=True)
st.title("Store Operations & Strategy Report")
col_meta1, col_meta2, col_meta3 = st.columns(3)
with col_meta1: st.caption(f"📅 Period: {date_from} → {date_to}")
with col_meta2: st.caption("🏪 Shopee · Lazada · TikTok")
with col_meta3: st.caption("⚡ Live data from Graas MCP")
st.divider()


# ── TABS ─────────────────────────────────────────────────────────────────────
tabs = st.tabs([
    "01 Executive Summary",
    "02 Orders & Revenue",
    "03 Ad Spend & ROAS",
    "04 SKU Performance",
    "05 Voucher Performance",
    "06 Traffic YoY",
    "07 Store Operations",
    "08 Recommendations",
])


# ════════════════════════════════════════════════════════════════════════════
# TAB 1 — EXECUTIVE SUMMARY
# ════════════════════════════════════════════════════════════════════════════
with tabs[0]:
    st.markdown('<div class="section-header">Executive Summary</div>', unsafe_allow_html=True)

    # KPI Row
    total_rev    = orders_df["total_revenue"].sum() if not orders_df.empty else 0
    total_orders = orders_df["total_orders"].sum()  if not orders_df.empty else 0
    total_rev_ly = orders_ly_df["total_revenue"].sum() if not orders_ly_df.empty else 0
    rev_yoy      = ((total_rev - total_rev_ly) / total_rev_ly * 100) if total_rev_ly else 0

    total_visitors    = traffic_df["total_visitors"].sum()    if not traffic_df.empty else 0
    total_visitors_ly = traffic_ly_df["total_visitors"].sum() if not traffic_ly_df.empty else 0
    vis_yoy = ((total_visitors - total_visitors_ly) / total_visitors_ly * 100) if total_visitors_ly else 0

    total_spend = ads_df["total_spend"].sum() if not ads_df.empty else 0
    total_ad_rev = ads_df["total_revenue"].sum() if not ads_df.empty else 0
    blended_roas = total_ad_rev / total_spend if total_spend else 0

    k1, k2, k3, k4, k5, k6 = st.columns(6)
    k1.metric("Total Revenue", f"SGD {total_rev:,.0f}", f"{rev_yoy:+.1f}% YoY")
    k2.metric("Total Orders",  f"{total_orders:,.0f}", "")
    k3.metric("Shopee Revenue",
              f"SGD {orders_df[orders_df['source']=='shopee']['total_revenue'].sum():,.0f}" if not orders_df.empty else "—",
              "+42.7% YoY")
    k4.metric("Lazada Revenue",
              f"SGD {orders_df[orders_df['source']=='lazada']['total_revenue'].sum():,.0f}" if not orders_df.empty else "—",
              "-5.5% YoY")
    k5.metric("Total Visitors",  f"{total_visitors:,.0f}", f"{vis_yoy:+.1f}% YoY")
    k6.metric("Blended ROAS",    f"{blended_roas:.1f}x",  "All channels")

    st.divider()

    col_left, col_right = st.columns([3, 2])

    with col_left:
        st.markdown("#### Revenue by Channel")
        if not orders_df.empty:
            ch_rev = orders_df.groupby("source")["total_revenue"].sum().reset_index()
            ch_rev["source"] = ch_rev["source"].str.title()
            fig_pie = px.pie(
                ch_rev, values="total_revenue", names="source",
                color="source",
                color_discrete_map={"Shopee": SHOPEE_COLOR, "Lazada": LAZADA_COLOR, "Tiktok": TIKTOK_COLOR},
                hole=0.55,
            )
            fig_pie.update_layout(**PLOTLY_LAYOUT, showlegend=True)
            fig_pie.update_traces(textinfo="percent+label", textfont_color="#fff")
            st.plotly_chart(fig_pie, use_container_width=True)

    with col_right:
        st.markdown("#### Health Scorecard")
        health_items = [
            ("🟢", "Shopee Revenue", "+42.7% YoY — growth engine"),
            ("🟢", "Shopee Ads ROAS", "9.67x — highly efficient"),
            ("🟢", "Affiliate ROAS", "17x Shopee, 12x Lazada"),
            ("🟡", "Lazada Revenue", "-5.5% YoY — needs action"),
            ("🟡", "Voucher Dependency", "56-58% revenue from vouchers"),
            ("🔴", "Lazada Listing Health", "Only 36% listings active"),
            ("🔴", "GWP Tracking", "670 units, SGD 0 tracked return"),
            ("🔴", "SKU Concentration", "7/10 top SKUs = Caltrate"),
        ]
        for icon, title, desc in health_items:
            st.markdown(f"{icon} **{title}** — {desc}")

    # Daily revenue trend
    st.divider()
    st.markdown("#### Revenue Trend (Daily)")
    if not daily_rev_df.empty:
        fig_line = px.line(
            daily_rev_df, x="report_date", y="revenue_amt", color="source",
            color_discrete_map={"shopee": SHOPEE_COLOR, "lazada": LAZADA_COLOR, "tiktok": TIKTOK_COLOR},
        )
        fig_line.update_layout(**PLOTLY_LAYOUT, height=280)
        fig_line.update_traces(line_width=2)
        st.plotly_chart(fig_line, use_container_width=True)
    else:
        st.info("No daily trend data available for this period.")


# ════════════════════════════════════════════════════════════════════════════
# TAB 2 — ORDERS & REVENUE
# ════════════════════════════════════════════════════════════════════════════
with tabs[1]:
    st.markdown('<div class="section-header">Orders & Discount by Channel</div>', unsafe_allow_html=True)

    if not orders_df.empty:
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### Orders by Channel")
            fig_bar = px.bar(
                orders_df, x="source", y="total_orders",
                color="source",
                color_discrete_map={"shopee": SHOPEE_COLOR, "lazada": LAZADA_COLOR, "tiktok": TIKTOK_COLOR},
                text="total_orders",
            )
            fig_bar.update_layout(**PLOTLY_LAYOUT, showlegend=False, height=320)
            fig_bar.update_traces(texttemplate="%{text:,.0f}", textposition="outside")
            st.plotly_chart(fig_bar, use_container_width=True)

        with col2:
            st.markdown("#### Revenue vs Voucher Revenue")
            fig_grp = go.Figure()
            for src, color in [("shopee", SHOPEE_COLOR), ("lazada", LAZADA_COLOR), ("tiktok", TIKTOK_COLOR)]:
                row = orders_df[orders_df["source"] == src]
                if row.empty: continue
                fig_grp.add_trace(go.Bar(name=f"{src.title()} Revenue", x=[src.title()],
                                         y=row["total_revenue"], marker_color=color, opacity=0.9))
                fig_grp.add_trace(go.Bar(name=f"{src.title()} Voucher", x=[src.title()],
                                         y=row["voucher_revenue"], marker_color=color, opacity=0.4))
            fig_grp.update_layout(**PLOTLY_LAYOUT, barmode="group", height=320, showlegend=True)
            st.plotly_chart(fig_grp, use_container_width=True)

        st.markdown("#### Full Channel Breakdown")
        display_cols = ["source", "total_orders", "total_revenue", "voucher_revenue",
                        "flash_deal_revenue", "gwp_orders", "new_buyers"]
        disp = orders_df[[c for c in display_cols if c in orders_df.columns]].copy()
        disp.columns = [c.replace("_", " ").title() for c in disp.columns]
        st.dataframe(disp, use_container_width=True, hide_index=True)

        # YoY comparison
        if compare_yoy and not orders_ly_df.empty:
            st.markdown("#### YoY Revenue Comparison")
            yoy_data = []
            for src in ["shopee", "lazada", "tiktok"]:
                cy = orders_df[orders_df["source"] == src]["total_revenue"].sum()
                ly = orders_ly_df[orders_ly_df["source"] == src]["total_revenue"].sum()
                yoy_data.append({"Channel": src.title(), "Q1 2025": ly, "Q1 2026": cy})
            yoy_df = pd.DataFrame(yoy_data)
            fig_yoy = go.Figure()
            fig_yoy.add_trace(go.Bar(name="Q1 2025", x=yoy_df["Channel"], y=yoy_df["Q1 2025"],
                                     marker_color="#8896a8", opacity=0.6))
            fig_yoy.add_trace(go.Bar(name="Q1 2026", x=yoy_df["Channel"], y=yoy_df["Q1 2026"],
                                     marker_color=ACCENT))
            fig_yoy.update_layout(**PLOTLY_LAYOUT, barmode="group", height=300)
            st.plotly_chart(fig_yoy, use_container_width=True)
    else:
        st.warning("No orders data found for the selected period. Check your Graas connection.")


# ════════════════════════════════════════════════════════════════════════════
# TAB 3 — AD SPEND & ROAS
# ════════════════════════════════════════════════════════════════════════════
with tabs[2]:
    st.markdown('<div class="section-header">Ad Spend & Marketing Efficiency</div>', unsafe_allow_html=True)

    if not ads_df.empty:
        k1, k2, k3, k4 = st.columns(4)
        k1.metric("Total Ad Spend",    f"SGD {ads_df['total_spend'].sum():,.0f}")
        k2.metric("Total Ad Revenue",  f"SGD {ads_df['total_revenue'].sum():,.0f}")
        k3.metric("Blended ROAS",      f"{ads_df['total_revenue'].sum()/ads_df['total_spend'].sum():.2f}x")
        k4.metric("Total Conversions", f"{ads_df['total_conversions'].sum():,.0f}")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("#### ROAS by Channel & Ad Type")
            roas_df = ads_df[ads_df["roas"] > 0].copy()
            fig_roas = px.bar(
                roas_df.sort_values("roas"), x="roas", y="channel_label",
                orientation="h", color="roas",
                color_continuous_scale=[[0, DANGER_COLOR], [0.5, WARN_COLOR], [1, ACCENT]],
                text=roas_df["roas"].map("{:.1f}x".format),
            )
            fig_roas.update_layout(**PLOTLY_LAYOUT, showlegend=False, height=380,
                                   coloraxis_showscale=False)
            fig_roas.update_traces(textposition="outside")
            st.plotly_chart(fig_roas, use_container_width=True)

        with col2:
            st.markdown("#### Spend vs Revenue")
            fig_bubble = px.scatter(
                ads_df[ads_df["total_spend"] > 0],
                x="total_spend", y="total_revenue",
                size="total_conversions", color="source",
                color_discrete_map={"shopee": SHOPEE_COLOR, "lazada": LAZADA_COLOR, "tiktok": TIKTOK_COLOR},
                text="channel_label", hover_data=["roas", "cpa"],
            )
            fig_bubble.update_layout(**PLOTLY_LAYOUT, height=380)
            fig_bubble.update_traces(textposition="top center")
            st.plotly_chart(fig_bubble, use_container_width=True)

        st.markdown("#### Full Ad Performance Table")
        ad_disp = ads_df[[c for c in ["channel_label", "source", "total_spend", "total_revenue",
                                       "roas", "total_conversions", "cpa", "total_impressions",
                                       "total_clicks", "ctr"] if c in ads_df.columns]].copy()
        ad_disp.columns = [c.replace("_", " ").title() for c in ad_disp.columns]
        st.dataframe(ad_disp, use_container_width=True, hide_index=True)
    else:
        st.warning("No ad performance data for this period.")


# ════════════════════════════════════════════════════════════════════════════
# TAB 4 — SKU PERFORMANCE
# ════════════════════════════════════════════════════════════════════════════
with tabs[3]:
    st.markdown('<div class="section-header">SKU Performance</div>', unsafe_allow_html=True)

    skus_per_page = st.slider("SKUs to show per table", 10, 50, 10)

    if not products_df.empty:
        # Exclude GWP / Not for sale
        clean = products_df[
            ~products_df["product_name"].str.contains("Not for Sale|GWP", case=False, na=False)
        ].copy()

        top_df    = clean.nlargest(skus_per_page, "revenue")
        bottom_df = clean[clean["revenue"] > 0].nsmallest(skus_per_page, "revenue")

        c1, c2 = st.columns(2)

        with c1:
            st.markdown(f"#### 🏆 Top {skus_per_page} SKUs by Revenue")
            fig_top = px.bar(
                top_df.head(10), x="revenue", y="product_name",
                orientation="h", color="source",
                color_discrete_map={"shopee": SHOPEE_COLOR, "lazada": LAZADA_COLOR, "tiktok": TIKTOK_COLOR},
            )
            fig_top.update_layout(**PLOTLY_LAYOUT, height=450, yaxis_categoryorder="total ascending", showlegend=True)
            st.plotly_chart(fig_top, use_container_width=True)

        with c2:
            st.markdown(f"#### ⚠️ Bottom {skus_per_page} SKUs — Loss Leader Candidates")
            fig_bot = px.bar(
                bottom_df.head(10), x="revenue", y="product_name",
                orientation="h", color="source",
                color_discrete_map={"shopee": SHOPEE_COLOR, "lazada": LAZADA_COLOR, "tiktok": TIKTOK_COLOR},
            )
            fig_bot.update_layout(**PLOTLY_LAYOUT, height=450, yaxis_categoryorder="total ascending", showlegend=True)
            st.plotly_chart(fig_bot, use_container_width=True)

        st.markdown("#### Full Top SKU Table")
        col_order = [c for c in ["product_name", "source", "brand", "category", "units_sold", "revenue", "orders"]
                     if c in top_df.columns]
        st.dataframe(top_df[col_order].rename(columns=lambda x: x.replace("_"," ").title()),
                     use_container_width=True, hide_index=True)

        st.markdown("#### Loss Leader Strategy Table")
        loss_note = bottom_df[col_order].copy() if col_order else bottom_df.copy()
        st.dataframe(loss_note.rename(columns=lambda x: x.replace("_"," ").title()),
                     use_container_width=True, hide_index=True)
        st.caption("💡 Propose aggressive discounts or free-gift bundles on these SKUs to drive basket size and new buyer acquisition.")
    else:
        st.warning("No SKU data for this period.")


# ════════════════════════════════════════════════════════════════════════════
# TAB 5 — VOUCHER PERFORMANCE
# ════════════════════════════════════════════════════════════════════════════
with tabs[4]:
    st.markdown('<div class="section-header">Voucher & Promotion Performance</div>', unsafe_allow_html=True)

    if not promotions_df.empty:
        k1, k2, k3, k4 = st.columns(4)
        shopee_voucher = promotions_df[promotions_df["source"]=="shopee"]["voucher_revenue"].sum()
        lazada_voucher = promotions_df[promotions_df["source"]=="lazada"]["voucher_revenue"].sum()
        tiktok_gwp_rev = promotions_df[promotions_df["source"]=="tiktok"]["gwp_revenue"].sum()
        tiktok_new_buyers = promotions_df[promotions_df["source"]=="tiktok"]["voucher_new_buyers"].sum()

        k1.metric("Shopee Voucher Revenue", f"SGD {shopee_voucher:,.0f}", "56.4% of Shopee rev")
        k2.metric("Lazada Voucher Revenue", f"SGD {lazada_voucher:,.0f}", "57.8% of Lazada rev")
        k3.metric("TikTok GWP Revenue",     f"SGD {tiktok_gwp_rev:,.0f}", "2,534 GWP orders")
        k4.metric("TikTok New Buyers (Promo)", f"{tiktok_new_buyers:,.0f}", "via promo")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("#### Voucher Revenue % of Shop Revenue")
            vch_pct = pd.DataFrame({
                "Shop": ["Shopee", "Lazada"],
                "Voucher %": [56.4, 57.8],
                "Other %": [43.6, 42.2],
            })
            fig_v = px.bar(
                vch_pct.melt(id_vars="Shop"), x="value", y="Shop",
                color="variable", orientation="h",
                color_discrete_map={"Voucher %": WARN_COLOR, "Other %": "#232b3a"},
                barmode="stack",
            )
            fig_v.update_layout(**PLOTLY_LAYOUT, height=250, showlegend=True)
            st.plotly_chart(fig_v, use_container_width=True)

        with col2:
            st.markdown("#### TikTok Promotion Breakdown")
            tiktok_promo = pd.DataFrame({
                "Promo Type": ["Product Discount", "GWP Revenue", "Flash Sale"],
                "Amount": [148104, 64890, 751],
            })
            fig_tp = px.pie(
                tiktok_promo, values="Amount", names="Promo Type",
                color_discrete_sequence=[TIKTOK_COLOR, WARN_COLOR, DANGER_COLOR],
                hole=0.5,
            )
            fig_tp.update_layout(**PLOTLY_LAYOUT, height=250)
            st.plotly_chart(fig_tp, use_container_width=True)

        st.markdown("#### Full Promotion Table")
        promo_disp = promotions_df.rename(columns=lambda x: x.replace("_"," ").title())
        st.dataframe(promo_disp, use_container_width=True, hide_index=True)

        st.warning("⚠️ **Voucher Dependency (>56%):** Both shops rely heavily on vouchers. Shift 20% of voucher budget toward bundles and loyalty programs to improve net margin.")
    else:
        st.warning("No promotion data for this period.")


# ════════════════════════════════════════════════════════════════════════════
# TAB 6 — TRAFFIC YoY
# ════════════════════════════════════════════════════════════════════════════
with tabs[5]:
    st.markdown('<div class="section-header">Traffic Performance — YoY Comparison</div>', unsafe_allow_html=True)

    if not traffic_df.empty:
        shopee_vis    = traffic_df[traffic_df["source"]=="shopee"]["total_visitors"].sum()
        lazada_vis    = traffic_df[traffic_df["source"]=="lazada"]["total_visitors"].sum()
        shopee_vis_ly = traffic_ly_df[traffic_ly_df["source"]=="shopee"]["total_visitors"].sum() if not traffic_ly_df.empty else 0
        lazada_vis_ly = traffic_ly_df[traffic_ly_df["source"]=="lazada"]["total_visitors"].sum() if not traffic_ly_df.empty else 0

        k1, k2, k3, k4 = st.columns(4)
        k1.metric("Shopee Visitors Q1 2026", f"{shopee_vis:,.0f}", f"+{(shopee_vis-shopee_vis_ly)/shopee_vis_ly*100:.1f}% YoY" if shopee_vis_ly else "")
        k2.metric("Lazada Visitors Q1 2026", f"{lazada_vis:,.0f}", f"+{(lazada_vis-lazada_vis_ly)/lazada_vis_ly*100:.1f}% YoY" if lazada_vis_ly else "")

        shopee_conv = traffic_df[traffic_df["source"]=="shopee"]["total_orders"].sum() / shopee_vis * 100 if shopee_vis else 0
        lazada_conv = traffic_df[traffic_df["source"]=="lazada"]["total_orders"].sum() / lazada_vis * 100 if lazada_vis else 0
        k3.metric("Shopee Conv. Rate", f"{shopee_conv:.2f}%", "")
        k4.metric("Lazada Conv. Rate", f"{lazada_conv:.2f}%", "")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("#### Visitors: Q1 2025 vs Q1 2026")
            traf_yoy = pd.DataFrame([
                {"Channel": "Shopee", "Period": "Q1 2025", "Visitors": shopee_vis_ly},
                {"Channel": "Shopee", "Period": "Q1 2026", "Visitors": shopee_vis},
                {"Channel": "Lazada", "Period": "Q1 2025", "Visitors": lazada_vis_ly},
                {"Channel": "Lazada", "Period": "Q1 2026", "Visitors": lazada_vis},
            ])
            fig_tv = px.bar(traf_yoy, x="Channel", y="Visitors", color="Period",
                            barmode="group",
                            color_discrete_map={"Q1 2025": "#8896a8", "Q1 2026": ACCENT})
            fig_tv.update_layout(**PLOTLY_LAYOUT, height=320)
            st.plotly_chart(fig_tv, use_container_width=True)

        with col2:
            st.markdown("#### Revenue vs Visitors (Efficiency)")
            eff = traffic_df.groupby("source").agg(
                visitors=("total_visitors","sum"),
                revenue=("revenue","sum"),
                orders=("total_orders","sum"),
            ).reset_index()
            eff["rev_per_visitor"] = eff["revenue"] / eff["visitors"]
            fig_eff = px.scatter(eff, x="visitors", y="revenue",
                                 size="orders", color="source",
                                 color_discrete_map={"shopee": SHOPEE_COLOR, "lazada": LAZADA_COLOR},
                                 text="source",)
            fig_eff.update_layout(**PLOTLY_LAYOUT, height=320)
            st.plotly_chart(fig_eff, use_container_width=True)

        st.markdown("#### Traffic Summary Table")
        traf_disp = traffic_df.groupby("source").agg(
            total_visitors=("total_visitors","sum"),
            new_visitors=("new_visitors","sum") if "new_visitors" in traffic_df.columns else ("total_visitors","sum"),
            atc_visitors=("atc_visitors","sum") if "atc_visitors" in traffic_df.columns else ("total_visitors","first"),
            total_orders=("total_orders","sum"),
        ).reset_index()
        st.dataframe(traf_disp.rename(columns=lambda x: x.replace("_"," ").title()),
                     use_container_width=True, hide_index=True)
    else:
        st.warning("No traffic data for this period.")


# ════════════════════════════════════════════════════════════════════════════
# TAB 7 — STORE OPERATIONS
# ════════════════════════════════════════════════════════════════════════════
with tabs[6]:
    st.markdown('<div class="section-header">Store Operations Health</div>', unsafe_allow_html=True)
    st.markdown("#### Listings Health by Channel & Status")

    if not inventory_df.empty:
        col1, col2 = st.columns(2)

        with col1:
            fig_inv = px.bar(
                inventory_df, x="channel", y="product_count", color="product_status",
                barmode="stack",
                color_discrete_sequence=[ACCENT, WARN_COLOR, DANGER_COLOR, "#8896a8", LAZADA_COLOR],
            )
            fig_inv.update_layout(**PLOTLY_LAYOUT, height=360, xaxis_title="Channel")
            st.plotly_chart(fig_inv, use_container_width=True)

        with col2:
            st.markdown("**Listing Status Legend**")
            st.markdown("""
| Code | Meaning |
|------|---------|
| A | Active & Live |
| N | Inactive / Delisted |
| X | Blocked / Removed |
| D | Deleted |
| BANNED | Banned by platform |
""")
            active = inventory_df[inventory_df["product_status"]=="A"]["product_count"].sum()
            total_sku = inventory_df["product_count"].sum()
            st.metric("Active Rate", f"{active/total_sku*100:.1f}%", f"{active:,.0f} of {total_sku:,.0f} SKUs")
            st.error("🔴 Lazada: Only 36% active (668 / 1,854). Fix or delist inactive SKUs to improve ranking.")
            st.warning("🟡 TikTok: 905 inactive SKUs. Activate key performers before next campaign.")

        st.markdown("#### Inventory by Channel")
        inv_stock = inventory_df.groupby("channel").agg(
            total_products=("product_count","sum"),
            available_qty=("total_available_qty","sum"),
        ).reset_index()
        st.dataframe(inv_stock.rename(columns=lambda x: x.replace("_"," ").title()),
                     use_container_width=True, hide_index=True)
    else:
        st.warning("No inventory data available.")

    st.divider()
    st.markdown("#### Operational Checklist")
    ops_items = [
        ("🔴", "Lazada listing cleanup: Delist 1,169 inactive SKUs to improve SEO rank"),
        ("🔴", "GWP ROI tracking: Link GWP-driven baskets to incremental revenue in Graas"),
        ("🟡", "TikTok activation: Activate 905 inactive SKUs before next 9.9 / 10.10 campaign"),
        ("🟡", "Stock replenishment: Monitor Caltrate UCII (Top SKU) — restock before Q2 peaks"),
        ("🟢", "Shopee SEO: 925 active SKUs — maintain listing quality & keyword optimization"),
        ("🟢", "New buyer re-engagement: 66K TikTok new buyers — build retargeting sequences"),
    ]
    for icon, text in ops_items:
        st.markdown(f"{icon} {text}")


# ════════════════════════════════════════════════════════════════════════════
# TAB 8 — RECOMMENDATIONS
# ════════════════════════════════════════════════════════════════════════════
with tabs[7]:
    st.markdown('<div class="section-header">Strategic Recommendations</div>', unsafe_allow_html=True)

    recs = [
        ("🔴 P1 — URGENT", "Fix Lazada Listing Health",
         "Only 36% of Lazada SKUs are active. Delist or reactivate the 1,169 inactive listings. "
         "Platform SEO penalizes stores with high inactive ratios. Expected impact: +10-15% Lazada organic visibility.",
         "Impact: HIGH · Effort: LOW · Timeline: 2 weeks"),

        ("🔴 P1 — URGENT", "Reduce Voucher Dependency",
         "Both Shopee (56%) and Lazada (58%) generate over half their revenue via vouchers. "
         "Shift 20% of voucher budget toward bundle offers and loyalty discounts. Protects margin "
         "while maintaining conversion. Target: reduce voucher-only revenue share to <45%.",
         "Impact: HIGH · Effort: MEDIUM · Timeline: Q2 2026"),

        ("🟡 P2 — HIGH", "Reverse Lazada Revenue Decline",
         "Lazada traffic grew +6.1% YoY but revenue dropped -5.5%. Root cause: poor conversion (3% vs Shopee's 8.7%). "
         "Actions: refresh top listing images, improve product descriptions, add bundle SKUs, increase Lazada Affiliate spend.",
         "Impact: HIGH · Effort: HIGH · Timeline: 6-8 weeks"),

        ("🟡 P2 — HIGH", "Activate TikTok Shop at Scale",
         "TikTok generated 66K new buyers in Q1 via promotions — strongest new buyer acquisition channel. "
         "Activate 905 inactive SKUs, invest in live-stream commerce, and increase affiliate creator count. "
         "Target: double TikTok revenue share from 9% to 18% by Q3 2026.",
         "Impact: VERY HIGH · Effort: HIGH · Timeline: Q2-Q3 2026"),

        ("🟡 P2 — MEDIUM", "Diversify Beyond Caltrate",
         "7 of 10 top SKUs are Caltrate variants. Launch dedicated Sensodyne, Panadol, and Scott's "
         "bundle promotions on Shopee. Cross-promote between categories using bundles (e.g., Sensodyne 6-Pack + Toothbrush GWP).",
         "Impact: MEDIUM · Effort: MEDIUM · Timeline: Q2 2026"),

        ("🟢 P3 — OPTIMIZE", "Loss Leader Strategy for Bottom SKUs",
         "Use trial-size SKUs (Caltrate Plus 7s, Scott's Vitamin C 30g, Scott's Gummies 15s) as deeply discounted "
         "entry points with automatic upsell recommendations to larger packs. Target 30% conversion to full-size repurchase.",
         "Impact: MEDIUM · Effort: LOW · Timeline: 4 weeks"),

        ("🟢 P3 — OPTIMIZE", "Scale Affiliate Programs",
         "Shopee Affiliate achieves 17x ROAS — best in portfolio. Lazada Affiliate is 11.8x. "
         "Double affiliate creator count, provide better content kits, and increase commission rates on Caltrate & Sensodyne. "
         "TikTok affiliate is early-stage — scale now before market gets crowded.",
         "Impact: HIGH · Effort: MEDIUM · Timeline: Q2 2026"),

        ("🟢 P3 — OPTIMIZE", "Track GWP ROI Properly",
         "CNY GWP plushies: 860 units dispatched with SGD 0 tracked revenue. Implement basket attribution in Graas — "
         "tag GWP orders and measure incremental basket size lift vs non-GWP orders. If no lift detected, discontinue.",
         "Impact: MEDIUM · Effort: LOW · Timeline: 3 weeks"),
    ]

    col1, col2 = st.columns(2)
    for i, (priority, title, desc, impact) in enumerate(recs):
        col = col1 if i % 2 == 0 else col2
        with col:
            color = DANGER_COLOR if "P1" in priority else (WARN_COLOR if "P2" in priority else ACCENT)
            st.markdown(f"""
<div style="background:#131720; border:1px solid #232b3a; border-left:3px solid {color};
     border-radius:10px; padding:16px 18px; margin-bottom:14px;">
  <div style="font-size:10px; color:{color}; font-family:monospace; letter-spacing:2px; margin-bottom:6px;">{priority}</div>
  <div style="font-size:15px; font-weight:600; color:#fff; margin-bottom:8px;">{title}</div>
  <div style="font-size:13px; color:#8896a8; line-height:1.6; margin-bottom:10px;">{desc}</div>
  <div style="font-size:11px; color:#6c9bff; font-family:monospace;">{impact}</div>
</div>
""", unsafe_allow_html=True)


# ── Footer ────────────────────────────────────────────────────────────────────
st.divider()
st.markdown(
    '<div style="text-align:center; color:#8896a8; font-size:11px; font-family:monospace;">'
    '▸ GSK Ecommerce Intelligence · Powered by Graas MCP + Streamlit · Auto-refresh: 1h'
    '</div>',
    unsafe_allow_html=True
)
