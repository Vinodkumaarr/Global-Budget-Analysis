# import streamlit as st
# import pandas as pd
# from sqlalchemy import create_engine
# import urllib.parse
# import plotly.express as px
# import plotly.graph_objects as go
# import numpy as np

# st.set_page_config(page_title="Global Budget Analysis", layout="wide")



# def get_engine():
#     # Reads from .streamlit/secrets.toml locally, or from Streamlit Cloud's
#     # Secrets manager when deployed. Falls back to local defaults if no
#     # secrets file is found at all (useful for quick local testing) —
#     # accessing st.secrets raises an error when no secrets.toml exists,
#     # so we guard the whole block with try/except.
#     try:
#         db_user = st.secrets.get("DB_USER", "root")
#         db_password = st.secrets.get("DB_PASSWORD", "1243")
#         db_host = st.secrets.get("DB_HOST", "localhost")
#         db_port = st.secrets.get("DB_PORT", "3306")
#         db_name = st.secrets.get("DB_NAME", "global_budget_db")
#     except Exception:
#         db_user = "root"
#         db_password = "1243"
#         db_host = "localhost"
#         db_port = "3306"
#         db_name = "global_budget_db"

#     password_quoted = urllib.parse.quote_plus(db_password)
#     return create_engine(
#         f"mysql+mysqlconnector://{db_user}:{password_quoted}@{db_host}:{db_port}/{db_name}"
# )


# st.title("🌍 Global Government Budget Analysis")
# st.markdown("An interactive platform exploring public finance shifts, sector dominance, and predictive trajectories.")

# # SIDEBAR REGIONAL FILTERS
# engine = get_engine()
# countries_df = pd.read_sql_query("SELECT country_name FROM countries ORDER BY country_name", engine)
# engine.dispose()

# selected_country = st.sidebar.selectbox("Select a Country to Filter", countries_df['country_name'].tolist())

# # NAVIGATION TABS FOR CLEAN PROCESS SEPARATION
# tab_macro, tab_sectors, tab_anomalies, tab_research_lab = st.tabs([
#     "📈 Macro Historical Trends",
#     "🥧 Sector Structural Spreads",
#     "🔍 Statistical Anomalies",
#     "🔬 Macro Economic Research Lab"
# ])

# with tab_macro:
#     st.header("Global Spending Growth Pathways")
#     engine = get_engine()
#     q = """
#         SELECT b.year, b.total_budget_billions_usd
#         FROM budgets b JOIN countries c ON b.country_id = c.country_id
#         WHERE c.country_name = %s ORDER BY b.year
#     """
#     df_macro = pd.read_sql_query(q, engine, params=(selected_country,))
#     engine.dispose()

#     if not df_macro.empty:
#         fig = px.line(df_macro, x="year", y="total_budget_billions_usd",
#                       title=f"Historical Expenditure Strategy: {selected_country}",
#                       template="plotly_dark", labels={"total_budget_billions_usd": "Total Budget (Billions USD)"})
#         st.plotly_chart(fig, width='stretch')
#     else:
#         st.info("No records found for the selection.")

# with tab_sectors:
#     st.header("Allocation Distribution Analysis")
#     engine = get_engine()
#     q_sec = """
#         SELECT b.year, sa.sector_name, sa.allocated_percentage, sa.allocated_amount_billions_usd
#         FROM sector_allocations sa
#         JOIN budgets b ON sa.budget_id = b.budget_id
#         JOIN countries c ON b.country_id = c.country_id
#         WHERE c.country_name = %s
#     """
#     df_sec = pd.read_sql_query(q_sec, engine, params=(selected_country,))
#     engine.dispose()

#     if not df_sec.empty:
#         col_c1, col_c2 = st.columns(2)
#         with col_c1:
#             fig_area = px.area(df_sec, x="year", y="allocated_percentage", color="sector_name",
#                                 title="Structural Budget Shifts Over Time", template="plotly_dark")
#             st.plotly_chart(fig_area, width='stretch')
#         with col_c2:
#             fig_box = px.box(df_sec, x="sector_name", y="allocated_percentage", color="sector_name",
#                               title="Variance and Spread Across Sectors", template="plotly_dark")
#             st.plotly_chart(fig_box, width='stretch')
#     else:
#         st.info("No sector records found.")

# with tab_anomalies:
#     st.header("Descriptive Outlier Detection")
#     st.markdown("Identifies fiscal years where spending shifted sharply outside normal historical baselines.")

#     if not df_macro.empty:
#         mean_val = df_macro['total_budget_billions_usd'].mean()
#         std_val = df_macro['total_budget_billions_usd'].std()

#         df_macro['z_score'] = (df_macro['total_budget_billions_usd'] - mean_val) / std_val
#         anomalies = df_macro[df_macro['z_score'].abs() > 1.96]

#         st.write("### Flagged Fiscal Outlier Periods (Z-Score > 1.96):")
#         if not anomalies.empty:
#             st.dataframe(anomalies.style.background_gradient(cmap='Reds', subset=['total_budget_billions_usd']), width='stretch')
#         else:
#             st.success("Excellent budget structural stability! No extreme statistical outliers discovered.")

# with tab_research_lab:
#     st.header("🔬 Deep Exploratory Research Workspace")
#     st.markdown("Advanced analytical modules calculating structural correlation shifts and spending volatility.")

#     # Render Analysis C (Correlation Matrix) visually as an interactive heatmap
#     st.subheader("Cross-Sector Allocation Correlation Matrix")
#     engine = get_engine()
#     q_corr = """
#         SELECT b.year, sa.sector_name, sa.allocated_percentage
#         FROM sector_allocations sa
#         JOIN budgets b ON sa.budget_id = b.budget_id
#         JOIN countries c ON b.country_id = c.country_id
#         WHERE c.country_name = %s;
#     """
#     df_corr_raw = pd.read_sql(q_corr, engine, params=(selected_country,))
#     engine.dispose()

#     if not df_corr_raw.empty:
#         pivot_df = df_corr_raw.pivot(index='year', columns='sector_name', values='allocated_percentage')
#         corr_matrix = pivot_df.corr()

#         # Build an interactive Plotly Heatmap chart layout
#         fig_heat = px.imshow(
#             corr_matrix,
#             text_auto=".2f",
#             aspect="auto",
#             color_continuous_scale="RdBu",  # Red-Blue scale highlights positive vs negative relationships clearly
#             labels=dict(color="Correlation Coefficient"),
#             template="plotly_dark"
#         )
#         st.plotly_chart(fig_heat, width='stretch')

#     # --- Volatility Index & Rolling Statistics ---
#     st.subheader("Volatility Index & Rolling Statistics")
#     engine = get_engine()
#     q_vol = """
#         SELECT b.year, b.total_budget_billions_usd
#         FROM budgets b JOIN countries c ON b.country_id = c.country_id
#         WHERE c.country_name = %s ORDER BY b.year ASC
#     """
#     df_vol = pd.read_sql(q_vol, engine, params=(selected_country,))
#     engine.dispose()

#     if not df_vol.empty:
#         df_vol = df_vol.sort_values('year')
#         df_vol['rolling_mean'] = df_vol['total_budget_billions_usd'].rolling(window=10).mean()
#         df_vol['rolling_std'] = df_vol['total_budget_billions_usd'].rolling(window=10).std()
#         df_vol['volatility_index'] = (df_vol['rolling_std'] / df_vol['rolling_mean']) * 100

#         st.markdown("Rolling 10-year Volatility Index (Coefficient of Variation)")
#         fig_vol = go.Figure()
#         fig_vol.add_trace(go.Scatter(x=df_vol['year'], y=df_vol['volatility_index'], mode='lines+markers', name='Volatility Index', line=dict(color='#FFA500')))
#         fig_vol.update_layout(template='plotly_dark', yaxis_title='Volatility Index (%)')
#         st.plotly_chart(fig_vol, width='stretch')

#         st.write("Recent rolling statistics (non-null rows):")
#         st.dataframe(df_vol.dropna().tail(10), width='stretch')
#     else:
#         st.info("Not enough historical data to compute volatility metrics for this country.")

#     # --- Polynomial Projection (Analytical) ---
#     st.subheader("Polynomial Projection (Analytical)")
#     col_p1, col_p2 = st.columns(2)
#     with col_p1:
#         proj_degree = st.selectbox("Projection degree", [1, 2, 3], index=1)
#         proj_horizon = st.number_input("Forecast horizon year", min_value=2025, max_value=2050, value=2035)
#     with col_p2:
#         apply_scenario = st.checkbox("Apply scenario shock to projection")
#         shock_pct = st.slider("Shock %", -50, 100, 0)

#     if not df_vol.empty:
#         x = df_vol['year'].astype(int).values
#         y = df_vol['total_budget_billions_usd'].astype(float).values
#         if len(x) > proj_degree:
#             coeffs = np.polyfit(x, y, deg=proj_degree)
#             poly = np.poly1d(coeffs)
#             years_future = np.arange(int(x.max()) + 1, int(proj_horizon) + 1)
#             proj_vals = poly(years_future)
#             if apply_scenario and shock_pct != 0:
#                 proj_vals = proj_vals * (1 + shock_pct / 100.0)

#             fig_proj = go.Figure()
#             fig_proj.add_trace(go.Scatter(x=x, y=y, mode='markers+lines', name='Historical', marker=dict(color='#888888')))
#             fig_proj.add_trace(go.Scatter(x=years_future, y=proj_vals, mode='lines', name='Projection', line=dict(color='#00FFAA', dash='dash')))
#             fig_proj.update_layout(title=f"Polynomial Projection (deg {proj_degree}) for {selected_country}", template='plotly_dark', xaxis_title='Year', yaxis_title='Budget (Billions USD)')
#             st.plotly_chart(fig_proj, width='stretch')

#             df_proj_out = pd.DataFrame({'year': years_future, 'projected_budget': proj_vals})
#             st.dataframe(df_proj_out.style.format({'projected_budget': '${:,.2f}'}), width='stretch')
#         else:
#             st.warning("Not enough historical points for the selected polynomial degree.")


import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import urllib.parse
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Global Budget Intelligence",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background:
        radial-gradient(
            circle at 10% 10%,
            rgba(128, 0, 0, 0.20),
            transparent 35%
        ),
        radial-gradient(
            circle at 90% 10%,
            rgba(0, 0, 255, 0.18),
            transparent 35%
        ),
        linear-gradient(
            135deg,
            #080812 0%,
            #100916 45%,
            #080b18 100%
        );

    color: #f5f5f7;
}

/* Main container */

.block-container {
    max-width: 1450px;
    padding-top: 2rem;
    padding-bottom: 4rem;
}


/* ============================================================
   SIDEBAR
   ============================================================ */

section[data-testid="stSidebar"] {
    background:
        linear-gradient(
            180deg,
            #10070d 0%,
            #0b0b17 60%,
            #060611 100%
        );

    border-right: 1px solid rgba(255,255,255,0.08);
}

section[data-testid="stSidebar"] > div {
    padding: 1.5rem 1rem;
}

.sidebar-title {
    font-size: 1.35rem;
    font-weight: 800;

    background: linear-gradient(
        90deg,
        #ff5c70,
        #667cff
    );

    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;

    margin-bottom: 0.2rem;
}

.sidebar-subtitle {
    color: #9ca3af;
    font-size: 0.82rem;
    margin-bottom: 1.8rem;
}


/* ============================================================
   HERO
   ============================================================ */

.hero {
    padding: 2.4rem 2.6rem;

    border-radius: 24px;

    background:
        linear-gradient(
            120deg,
            rgba(128,0,0,0.85),
            rgba(48,0,100,0.70),
            rgba(0,0,255,0.75)
        );

    border: 1px solid rgba(255,255,255,0.13);

    box-shadow:
        0 25px 70px rgba(0,0,0,0.45),
        inset 0 1px rgba(255,255,255,0.12);

    margin-bottom: 2rem;

    position: relative;
    overflow: hidden;
}

.hero::after {
    content: "";

    position: absolute;

    width: 350px;
    height: 350px;

    right: -120px;
    top: -160px;

    background: rgba(255,255,255,0.08);

    border-radius: 50%;

    filter: blur(10px);
}

.hero h1 {
    font-size: 2.5rem;
    font-weight: 800;
    margin: 0;

    letter-spacing: -1px;
}

.hero p {
    color: rgba(255,255,255,0.82);

    font-size: 1rem;

    margin-top: 0.8rem;

    max-width: 850px;
}


/* ============================================================
   SECTION HEADINGS
   ============================================================ */

.section-title {
    font-size: 1.45rem;
    font-weight: 700;

    margin-top: 1.2rem;
    margin-bottom: 0.25rem;
}

.section-description {
    color: #9ca3af;
    font-size: 0.9rem;

    margin-bottom: 1.3rem;
}


/* ============================================================
   KPI CARDS
   ============================================================ */

.kpi-container {
    display: flex;
    gap: 1rem;
    margin: 1.2rem 0 2rem 0;
}

.kpi-card {
    flex: 1;

    padding: 1.25rem;

    border-radius: 18px;

    background:
        linear-gradient(
            145deg,
            rgba(255,255,255,0.075),
            rgba(255,255,255,0.025)
        );

    border: 1px solid rgba(255,255,255,0.09);

    box-shadow:
        0 12px 35px rgba(0,0,0,0.22);

    backdrop-filter: blur(14px);

    transition: all 0.25s ease;
}

.kpi-card:hover {
    transform: translateY(-3px);

    border-color: rgba(100,120,255,0.4);

    box-shadow:
        0 18px 45px rgba(0,0,0,0.35);
}

.kpi-label {
    color: #9ca3af;
    font-size: 0.78rem;

    text-transform: uppercase;

    letter-spacing: 0.7px;
}

.kpi-value {
    font-size: 1.65rem;

    font-weight: 800;

    margin-top: 0.3rem;

    background:
        linear-gradient(
            90deg,
            #ff6577,
            #6577ff
        );

    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}


/* ============================================================
   CARDS
   ============================================================ */

.dashboard-card {
    padding: 1.3rem;

    border-radius: 18px;

    background:
        rgba(255,255,255,0.035);

    border:
        1px solid rgba(255,255,255,0.08);

    box-shadow:
        0 15px 40px rgba(0,0,0,0.20);

    backdrop-filter: blur(12px);

    margin-bottom: 1.2rem;
}


/* ============================================================
   BUTTONS
   ============================================================ */

.stButton > button {
    width: 100%;

    border: none;

    border-radius: 12px;

    padding: 0.65rem 1rem;

    font-weight: 600;

    color: white;

    background:
        linear-gradient(
            90deg,
            #800000,
            #0000ff
        );

    transition: all 0.25s ease;
}

.stButton > button:hover {
    transform: translateY(-2px);

    box-shadow:
        0 8px 25px rgba(0,0,255,0.35);

    border: none;
}


/* ============================================================
   SELECTBOX / INPUTS
   ============================================================ */

div[data-baseweb="select"] > div {
    background: rgba(255,255,255,0.05);

    border:
        1px solid rgba(255,255,255,0.12);

    border-radius: 12px;
}

div[data-baseweb="input"] > div {
    background: rgba(255,255,255,0.05);

    border:
        1px solid rgba(255,255,255,0.12);

    border-radius: 12px;
}


/* ============================================================
   TABS
   ============================================================ */

.stTabs [data-baseweb="tab-list"] {
    gap: 8px;

    background:
        rgba(255,255,255,0.025);

    padding: 7px;

    border-radius: 16px;

    border:
        1px solid rgba(255,255,255,0.07);

    margin-bottom: 1.5rem;
}

.stTabs [data-baseweb="tab"] {
    border-radius: 11px;

    padding: 0.65rem 1rem;

    color: #9ca3af;

    font-weight: 600;
}

.stTabs [aria-selected="true"] {
    background:
        linear-gradient(
            90deg,
            rgba(128,0,0,0.8),
            rgba(0,0,255,0.8)
        );

    color: white !important;
}


/* ============================================================
   DATAFRAME
   ============================================================ */

[data-testid="stDataFrame"] {
    border-radius: 14px;
    overflow: hidden;

    border:
        1px solid rgba(255,255,255,0.08);
}


/* ============================================================
   ALERTS
   ============================================================ */

div[data-testid="stAlert"] {
    border-radius: 14px;
}


/* ============================================================
   DIVIDER
   ============================================================ */

hr {
    border-color: rgba(255,255,255,0.08);
}


/* ============================================================
   FOOTER
   ============================================================ */

.footer {
    text-align: center;

    margin-top: 3rem;

    padding-top: 1.5rem;

    border-top:
        1px solid rgba(255,255,255,0.08);

    color: #71717a;

    font-size: 0.78rem;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# DATABASE CONNECTION
# ============================================================

def get_engine():

    try:
        db_user = st.secrets.get("DB_USER", "root")
        db_password = st.secrets.get("DB_PASSWORD", "1243")
        db_host = st.secrets.get("DB_HOST", "localhost")
        db_port = st.secrets.get("DB_PORT", "3306")
        db_name = st.secrets.get("DB_NAME", "global_budget_db")

    except Exception:

        db_user = "root"
        db_password = "1243"
        db_host = "localhost"
        db_port = "3306"
        db_name = "global_budget_db"

    password_quoted = urllib.parse.quote_plus(db_password)

    return create_engine(
        f"mysql+mysqlconnector://"
        f"{db_user}:{password_quoted}@"
        f"{db_host}:{db_port}/{db_name}"
    )


# ============================================================
# PLOTLY THEME
# ============================================================

def apply_plotly_theme(fig):

    fig.update_layout(

        template="plotly_dark",

        paper_bgcolor="rgba(0,0,0,0)",

        plot_bgcolor="rgba(255,255,255,0.025)",

        font=dict(
            family="Inter, sans-serif",
            color="#E5E7EB"
        ),

        title=dict(
            font=dict(
                size=18,
                color="#F9FAFB"
            )
        ),

        margin=dict(
            l=40,
            r=30,
            t=60,
            b=40
        ),

        legend=dict(
            bgcolor="rgba(0,0,0,0)",
            borderwidth=0
        ),

        hoverlabel=dict(
            bgcolor="#111827",
            font_size=12
        ),

        xaxis=dict(
            gridcolor="rgba(255,255,255,0.06)",
            zerolinecolor="rgba(255,255,255,0.08)"
        ),

        yaxis=dict(
            gridcolor="rgba(255,255,255,0.06)",
            zerolinecolor="rgba(255,255,255,0.08)"
        )
    )

    return fig


# ============================================================
# HERO
# ============================================================

st.markdown("""
<div class="hero">

    <h1>🌍 Global Government Budget Intelligence</h1>

    <p>
        Explore government expenditure patterns, sector allocation,
        fiscal anomalies, volatility trends, correlations and
        analytical budget projections through an interactive
        research dashboard.
    </p>

</div>
""", unsafe_allow_html=True)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        '<div class="sidebar-title">Global Budget</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="sidebar-subtitle">'
        'Fiscal intelligence & analytics platform'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown("### 🌎 Regional Filter")

    engine = get_engine()

    countries_df = pd.read_sql_query(
        """
        SELECT country_name
        FROM countries
        ORDER BY country_name
        """,
        engine
    )

    engine.dispose()

    selected_country = st.selectbox(
        "Select Country",
        countries_df["country_name"].tolist()
    )

    st.markdown("---")

    st.markdown("### 📊 Dashboard Modules")

    st.markdown(
        """
        **Macro Trends**  
        Historical budget evolution

        **Sector Analysis**  
        Allocation & structural shifts

        **Anomaly Detection**  
        Statistical fiscal outliers

        **Research Lab**  
        Correlations, volatility & projections
        """
    )

    st.markdown("---")

    st.caption("Global Budget Intelligence Platform")
    st.caption("Data-driven public finance research")


# ============================================================
# LOAD BASIC MACRO DATA
# ============================================================

engine = get_engine()

q_macro = """
SELECT
    b.year,
    b.total_budget_billions_usd
FROM budgets b
JOIN countries c
    ON b.country_id = c.country_id
WHERE c.country_name = %s
ORDER BY b.year
"""

df_macro = pd.read_sql_query(
    q_macro,
    engine,
    params=(selected_country,)
)

engine.dispose()


# ============================================================
# KPI SECTION
# ============================================================

if not df_macro.empty:

    latest_budget = df_macro.iloc[-1]["total_budget_billions_usd"]

    highest_budget = df_macro[
        "total_budget_billions_usd"
    ].max()

    average_budget = df_macro[
        "total_budget_billions_usd"
    ].mean()

    latest_year = df_macro.iloc[-1]["year"]

    st.markdown(
        '<div class="section-title">Fiscal Snapshot</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-description">'
        f'Current analytical overview for <b>{selected_country}</b>'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <div class="kpi-container">

            <div class="kpi-card">
                <div class="kpi-label">Latest Budget</div>
                <div class="kpi-value">${latest_budget:,.2f}B</div>
            </div>

            <div class="kpi-card">
                <div class="kpi-label">Peak Budget</div>
                <div class="kpi-value">${highest_budget:,.2f}B</div>
            </div>

            <div class="kpi-card">
                <div class="kpi-label">Average Budget</div>
                <div class="kpi-value">${average_budget:,.2f}B</div>
            </div>

            <div class="kpi-card">
                <div class="kpi-label">Latest Fiscal Year</div>
                <div class="kpi-value">{latest_year}</div>
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# NAVIGATION
# ============================================================

tab_macro, tab_sectors, tab_anomalies, tab_research_lab = st.tabs(
    [
        "📈 Macro Historical Trends",
        "🥧 Sector Structural Spreads",
        "🔍 Statistical Anomalies",
        "🔬 Macro Economic Research Lab"
    ]
)


# ============================================================
# TAB 1 — MACRO
# ============================================================

with tab_macro:

    st.markdown(
        '<div class="section-title">'
        'Global Spending Growth Pathways'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-description">'
        'Historical evolution of government expenditure across fiscal years.'
        '</div>',
        unsafe_allow_html=True
    )

    if not df_macro.empty:

        fig = px.line(
            df_macro,
            x="year",
            y="total_budget_billions_usd",
            title=f"Historical Expenditure Strategy — {selected_country}",
            labels={
                "year": "Fiscal Year",
                "total_budget_billions_usd":
                    "Total Budget (Billions USD)"
            },
            markers=True
        )

        fig.update_traces(
            line=dict(
                color="#6677ff",
                width=3
            ),
            marker=dict(
                size=7,
                color="#ff5c70"
            )
        )

        fig = apply_plotly_theme(fig)

        st.markdown(
            '<div class="dashboard-card">',
            unsafe_allow_html=True
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        st.markdown("</div>", unsafe_allow_html=True)

    else:

        st.info(
            "No budget records found for the selected country."
        )


# ============================================================
# TAB 2 — SECTORS
# ============================================================

with tab_sectors:

    st.markdown(
        '<div class="section-title">'
        'Allocation Distribution Analysis'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-description">'
        'Understand how government spending is distributed across sectors.'
        '</div>',
        unsafe_allow_html=True
    )

    engine = get_engine()

    q_sec = """
    SELECT
        b.year,
        sa.sector_name,
        sa.allocated_percentage,
        sa.allocated_amount_billions_usd
    FROM sector_allocations sa
    JOIN budgets b
        ON sa.budget_id = b.budget_id
    JOIN countries c
        ON b.country_id = c.country_id
    WHERE c.country_name = %s
    """

    df_sec = pd.read_sql_query(
        q_sec,
        engine,
        params=(selected_country,)
    )

    engine.dispose()

    if not df_sec.empty:

        col_c1, col_c2 = st.columns(2)

        with col_c1:

            fig_area = px.area(
                df_sec,
                x="year",
                y="allocated_percentage",
                color="sector_name",
                title="Structural Budget Shifts",
                labels={
                    "allocated_percentage":
                        "Allocation (%)",
                    "year": "Fiscal Year"
                }
            )

            fig_area = apply_plotly_theme(fig_area)

            st.markdown(
                '<div class="dashboard-card">',
                unsafe_allow_html=True
            )

            st.plotly_chart(
                fig_area,
                use_container_width=True
            )

            st.markdown("</div>", unsafe_allow_html=True)

        with col_c2:

            fig_box = px.box(
                df_sec,
                x="sector_name",
                y="allocated_percentage",
                color="sector_name",
                title="Sector Allocation Variance",
                labels={
                    "sector_name": "Sector",
                    "allocated_percentage":
                        "Allocation (%)"
                }
            )

            fig_box = apply_plotly_theme(fig_box)

            st.markdown(
                '<div class="dashboard-card">',
                unsafe_allow_html=True
            )

            st.plotly_chart(
                fig_box,
                use_container_width=True
            )

            st.markdown("</div>", unsafe_allow_html=True)

    else:

        st.info(
            "No sector records found for this country."
        )


# ============================================================
# TAB 3 — ANOMALIES
# ============================================================

with tab_anomalies:

    st.markdown(
        '<div class="section-title">'
        'Descriptive Outlier Detection'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-description">'
        'Identify fiscal years where government spending moved '
        'significantly outside historical patterns.'
        '</div>',
        unsafe_allow_html=True
    )

    if not df_macro.empty:

        mean_val = df_macro[
            "total_budget_billions_usd"
        ].mean()

        std_val = df_macro[
            "total_budget_billions_usd"
        ].std()

        if std_val != 0 and not pd.isna(std_val):

            df_anomaly = df_macro.copy()

            df_anomaly["z_score"] = (
                df_anomaly["total_budget_billions_usd"]
                - mean_val
            ) / std_val

            anomalies = df_anomaly[
                df_anomaly["z_score"].abs() > 1.96
            ]

            col_a1, col_a2 = st.columns(2)

            with col_a1:

                st.markdown(
                    f"""
                    <div class="kpi-card">

                        <div class="kpi-label">
                            Mean Budget
                        </div>

                        <div class="kpi-value">
                            ${mean_val:,.2f}B
                        </div>

                    </div>
                    """,
                    unsafe_allow_html=True
                )

            with col_a2:

                st.markdown(
                    f"""
                    <div class="kpi-card">

                        <div class="kpi-label">
                            Detected Outliers
                        </div>

                        <div class="kpi-value">
                            {len(anomalies)}
                        </div>

                    </div>
                    """,
                    unsafe_allow_html=True
                )

            st.markdown("### 🚨 Flagged Fiscal Outlier Periods")

            if not anomalies.empty:

                st.dataframe(
                    anomalies,
                    use_container_width=True,
                    hide_index=True
                )

            else:

                st.success(
                    "Excellent budget structural stability! "
                    "No extreme statistical outliers were discovered."
                )

        else:

            st.warning(
                "Insufficient variation in budget data "
                "to calculate a meaningful Z-score."
            )

    else:

        st.info(
            "No historical data available for anomaly analysis."
        )


# ============================================================
# TAB 4 — RESEARCH LAB
# ============================================================

with tab_research_lab:

    st.markdown(
        '<div class="section-title">'
        '🔬 Deep Exploratory Research Workspace'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-description">'
        'Advanced analytical modules for structural correlation, '
        'volatility and forward-looking budget projections.'
        '</div>',
        unsafe_allow_html=True
    )


    # --------------------------------------------------------
    # CORRELATION MATRIX
    # --------------------------------------------------------

    st.markdown(
        '<div class="dashboard-card">',
        unsafe_allow_html=True
    )

    st.subheader(
        "Cross-Sector Allocation Correlation Matrix"
    )

    engine = get_engine()

    q_corr = """
        SELECT
            b.year,
            sa.sector_name,
            sa.allocated_percentage
        FROM sector_allocations sa
        JOIN budgets b
            ON sa.budget_id = b.budget_id
        JOIN countries c
            ON b.country_id = c.country_id
        WHERE c.country_name = %s
    """

    df_corr_raw = pd.read_sql_query(
        q_corr,
        engine,
        params=(selected_country,)
    )

    engine.dispose()

    if not df_corr_raw.empty:

        pivot_df = df_corr_raw.pivot(
            index="year",
            columns="sector_name",
            values="allocated_percentage"
        )

        corr_matrix = pivot_df.corr()

        fig_heat = px.imshow(
            corr_matrix,
            text_auto=".2f",
            aspect="auto",
            color_continuous_scale=[
                "#800000",
                "#ffffff",
                "#0000ff"
            ],
            labels={
                "color": "Correlation"
            }
        )

        fig_heat = apply_plotly_theme(fig_heat)

        st.plotly_chart(
            fig_heat,
            use_container_width=True
        )

    else:

        st.info(
            "Not enough sector data to calculate correlations."
        )

    st.markdown("</div>", unsafe_allow_html=True)


    # --------------------------------------------------------
    # VOLATILITY
    # --------------------------------------------------------

    st.markdown(
        '<div class="dashboard-card">',
        unsafe_allow_html=True
    )

    st.subheader(
        "📊 Volatility Index & Rolling Statistics"
    )

    engine = get_engine()

    q_vol = """
        SELECT
            b.year,
            b.total_budget_billions_usd
        FROM budgets b
        JOIN countries c
            ON b.country_id = c.country_id
        WHERE c.country_name = %s
        ORDER BY b.year ASC
    """

    df_vol = pd.read_sql_query(
        q_vol,
        engine,
        params=(selected_country,)
    )

    engine.dispose()

    if not df_vol.empty:

        df_vol = df_vol.sort_values("year")

        df_vol["rolling_mean"] = (
            df_vol[
                "total_budget_billions_usd"
            ].rolling(window=10).mean()
        )

        df_vol["rolling_std"] = (
            df_vol[
                "total_budget_billions_usd"
            ].rolling(window=10).std()
        )

        df_vol["volatility_index"] = (
            df_vol["rolling_std"]
            / df_vol["rolling_mean"]
        ) * 100

        fig_vol = go.Figure()

        fig_vol.add_trace(
            go.Scatter(
                x=df_vol["year"],
                y=df_vol["volatility_index"],
                mode="lines+markers",
                name="Volatility Index",
                line=dict(
                    color="#ff6577",
                    width=3
                ),
                marker=dict(
                    size=6
                )
            )
        )

        fig_vol.update_layout(
            title="Rolling 10-Year Volatility Index",
            xaxis_title="Year",
            yaxis_title="Volatility (%)"
        )

        fig_vol = apply_plotly_theme(fig_vol)

        st.plotly_chart(
            fig_vol,
            use_container_width=True
        )

        st.markdown("### Recent Rolling Statistics")

        st.dataframe(
            df_vol.dropna().tail(10),
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info(
            "Not enough historical data to compute volatility."
        )

    st.markdown("</div>", unsafe_allow_html=True)


    # --------------------------------------------------------
    # POLYNOMIAL PROJECTION
    # --------------------------------------------------------

    st.markdown(
        '<div class="dashboard-card">',
        unsafe_allow_html=True
    )

    st.subheader(
        "🔮 Polynomial Budget Projection"
    )

    st.markdown(
        "Configure the analytical projection model below."
    )

    col_p1, col_p2 = st.columns(2)

    with col_p1:

        proj_degree = st.selectbox(
            "Projection Degree",
            [1, 2, 3],
            index=1
        )

        proj_horizon = st.number_input(
            "Forecast Horizon",
            min_value=2025,
            max_value=2050,
            value=2035
        )

    with col_p2:

        apply_scenario = st.checkbox(
            "Apply Scenario Shock"
        )

        shock_pct = st.slider(
            "Scenario Shock (%)",
            -50,
            100,
            0
        )

    if not df_vol.empty:

        x = (
            df_vol["year"]
            .astype(int)
            .values
        )

        y = (
            df_vol[
                "total_budget_billions_usd"
            ]
            .astype(float)
            .values
        )

        if len(x) > proj_degree:

            coeffs = np.polyfit(
                x,
                y,
                deg=proj_degree
            )

            poly = np.poly1d(coeffs)

            years_future = np.arange(
                int(x.max()) + 1,
                int(proj_horizon) + 1
            )

            proj_vals = poly(years_future)

            if apply_scenario and shock_pct != 0:

                proj_vals = (
                    proj_vals
                    * (1 + shock_pct / 100.0)
                )

            fig_proj = go.Figure()

            fig_proj.add_trace(
                go.Scatter(
                    x=x,
                    y=y,
                    mode="markers+lines",
                    name="Historical",
                    line=dict(
                        color="#9CA3AF",
                        width=2
                    ),
                    marker=dict(
                        size=6
                    )
                )
            )

            fig_proj.add_trace(
                go.Scatter(
                    x=years_future,
                    y=proj_vals,
                    mode="lines",
                    name="Projection",
                    line=dict(
                        color="#6677ff",
                        width=3,
                        dash="dash"
                    )
                )
            )

            fig_proj.update_layout(
                title=(
                    f"Polynomial Projection "
                    f"(Degree {proj_degree}) — "
                    f"{selected_country}"
                ),
                xaxis_title="Year",
                yaxis_title="Budget (Billions USD)"
            )

            fig_proj = apply_plotly_theme(
                fig_proj
            )

            st.plotly_chart(
                fig_proj,
                use_container_width=True
            )

            df_proj_out = pd.DataFrame(
                {
                    "year": years_future,
                    "projected_budget":
                        proj_vals
                }
            )

            st.markdown(
                "### 📋 Projected Budget Values"
            )

            st.dataframe(
                df_proj_out.style.format(
                    {
                        "projected_budget":
                            "${:,.2f}"
                    }
                ),
                use_container_width=True,
                hide_index=True
            )

        else:

            st.warning(
                "Not enough historical points for "
                "the selected polynomial degree."
            )

    st.markdown("</div>", unsafe_allow_html=True)


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer">
        🌍 Global Budget Intelligence &nbsp;•&nbsp;
        Data Analytics Dashboard &nbsp;•&nbsp;
        Built with Streamlit, MySQL & Plotly
    </div>
    """,
    unsafe_allow_html=True
)

