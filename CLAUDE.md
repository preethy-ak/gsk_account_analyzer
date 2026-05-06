# CLAUDE.md — GSK Ecommerce Dashboard

## Project Overview
Streamlit dashboard for GSK ecommerce operations. Connects to Graas Snowflake.
Main app: `dashboard.py`. Data layer: `src/data_loader.py`.

## Running the App
```bash
pip install -r requirements.txt
streamlit run dashboard.py
```

## Environment
Credentials go in `.env` (copy from `.env.example`).
Never commit `.env` to git.

## Key Files
- `dashboard.py` — 8-tab Streamlit app with all charts
- `src/data_loader.py` — All Snowflake SQL queries
- `.streamlit/config.toml` — Dark theme config

## Adding a New Chart
1. Add query method to `GraasDataLoader` in `src/data_loader.py`
2. Call it in `load_all_data()` in `dashboard.py`
3. Render in the relevant tab using `st.plotly_chart()`

## Refreshing Data
Hit "🔄 Refresh Data" in the sidebar, or clear Streamlit cache:
```python
st.cache_data.clear()
```

## Dependencies
- streamlit: UI framework
- plotly: Charts
- snowflake-connector-python: Graas data
- pandas: Data wrangling
