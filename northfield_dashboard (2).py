# ============================================================
# NORTHFIELD & CO.
# BUSINESS PERFORMANCE DASHBOARD 
# ============================================================

import pandas as pd
import numpy as np

from dash import Dash, dcc, html, Input, Output
import plotly.graph_objects as go


# ============================================================
# 1. LOAD DATA
# ============================================================

FILE_PATH = "Northfield_Co_Case_Study.xlsx"
SHEET_NAME = "Master data"

df = pd.read_excel(FILE_PATH, sheet_name=SHEET_NAME)
df["Date"] = pd.to_datetime(df["Date"])
df["Year"] = df["Date"].dt.year
df["Year_Month"] = df["Date"].dt.to_period("M").astype(str)


# ============================================================
# 2. CREATE TOTAL PAID MEDIA
# ============================================================

# spend_Google and spend_Meta are already roll-ups.
other_media = [
    "influencer_spend",
    "Awin_spend",
    "microsoft_spend",
    "criteo_spend",
    "cost_outbrain"
]

df["Total_Paid_Media"] = (
    df["spend_Google"]
    + df["spend_Meta"]
    + df[other_media].sum(axis=1)
)


# ============================================================
# 3. DASH APP
# ============================================================

app = Dash(__name__)
app.title = "Northfield & Co. | Business Dashboard"


# ============================================================
# 4. STYLES
# ============================================================

PAGE = {
    "fontFamily": "Arial, sans-serif",
    "backgroundColor": "#F3F6FA",
    "minHeight": "100vh",
    "padding": "24px 34px"
}

HEADER = {
    "background": "linear-gradient(135deg, #111827, #374151)",
    "color": "white",
    "padding": "28px 32px",
    "borderRadius": "16px",
    "marginBottom": "18px",
    "boxShadow": "0 4px 14px rgba(0,0,0,0.10)"
}

PANEL = {
    "backgroundColor": "white",
    "padding": "12px",
    "borderRadius": "14px",
    "boxShadow": "0 2px 10px rgba(0,0,0,0.07)",
    "marginBottom": "18px"
}

FILTER_PANEL = {
    "backgroundColor": "white",
    "padding": "20px",
    "borderRadius": "14px",
    "boxShadow": "0 2px 10px rgba(0,0,0,0.07)",
    "marginBottom": "18px"
}

CARD = {
    "backgroundColor": "white",
    "padding": "18px 16px",
    "borderRadius": "14px",
    "boxShadow": "0 2px 10px rgba(0,0,0,0.07)",
    "textAlign": "center",
    "flex": "1",
    "minWidth": "175px"
}

CARD_TITLE = {
    "fontSize": "12px",
    "fontWeight": "700",
    "letterSpacing": "0.5px",
    "color": "#6B7280",
    "marginBottom": "8px"
}

CARD_VALUE = {
    "fontSize": "25px",
    "fontWeight": "700",
    "color": "#111827"
}

SECTION_TITLE = {
    "fontSize": "18px",
    "fontWeight": "700",
    "color": "#111827",
    "margin": "4px 4px 10px 4px"
}


# ============================================================
# 5. HELPER FUNCTIONS
# ============================================================

def money(value):
    if pd.isna(value):
        return "$0"
    return f"${value:,.0f}"


def pct(value):
    if pd.isna(value):
        return "0.0%"
    return f"{value:.1f}%"


def comparison(grouped, label_col, value_col, name_a, name_b):
    """Return means for two binary groups, safely."""
    a = grouped.loc[grouped[label_col] == 1, value_col]
    b = grouped.loc[grouped[label_col] == 0, value_col]
    return (
        a.iloc[0] if len(a) else np.nan,
        b.iloc[0] if len(b) else np.nan
    )


def make_card(title, value):
    return [
        html.Div(title, style=CARD_TITLE),
        html.Div(value, style=CARD_VALUE)
    ]


def base_layout(fig, title, height=390):
    fig.update_layout(
        title={"text": title, "x": 0.02, "xanchor": "left"},
        template="plotly_white",
        height=height,
        margin={"l": 55, "r": 25, "t": 55, "b": 55},
        font={"family": "Arial, sans-serif", "color": "#374151"},
        hoverlabel={"bgcolor": "white"}
    )
    return fig


# ============================================================
# 6. LAYOUT
# ============================================================

years = sorted(df["Year"].unique())

app.layout = html.Div(
    style=PAGE,
    children=[

        # Header
        html.Div(
            style=HEADER,
            children=[
                html.H1(
                    "Northfield & Co.",
                    style={"margin": "0", "fontSize": "32px"}
                ),
                html.Div(
                    "Business Performance Dashboard",
                    style={
                        "fontSize": "20px",
                        "marginTop": "5px",
                        "color": "#E5E7EB"
                    }
                ),
                html.P(
                    "Revenue performance, customer acquisition, promotions, media and seasonal patterns",
                    style={
                        "margin": "10px 0 0 0",
                        "color": "#D1D5DB"
                    }
                )
            ]
        ),

        # Filters
        html.Div(
            style=FILTER_PANEL,
            children=[
                html.Div("FILTERS", style={
                    "fontSize": "13px",
                    "fontWeight": "700",
                    "color": "#6B7280",
                    "marginBottom": "12px"
                }),
                html.Div(
                    style={
                        "display": "flex",
                        "gap": "18px",
                        "flexWrap": "wrap"
                    },
                    children=[
                        html.Div(
                            style={"flex": "1", "minWidth": "210px"},
                            children=[
                                html.Label("Year", style={"fontWeight": "600"}),
                                dcc.Dropdown(
                                    id="year-filter",
                                    options=[{"label": "All Years", "value": "All"}] + [
                                        {"label": str(y), "value": int(y)} for y in years
                                    ],
                                    value="All",
                                    clearable=False
                                )
                            ]
                        ),
                        html.Div(
                            style={"flex": "1", "minWidth": "210px"},
                            children=[
                                html.Label("Promotion", style={"fontWeight": "600"}),
                                dcc.Dropdown(
                                    id="promotion-filter",
                                    options=[
                                        {"label": "All", "value": "All"},
                                        {"label": "Promotion", "value": "Promotion"},
                                        {"label": "No Promotion", "value": "No Promotion"}
                                    ],
                                    value="All",
                                    clearable=False
                                )
                            ]
                        ),
                        html.Div(
                            style={"flex": "1", "minWidth": "210px"},
                            children=[
                                html.Label("UWG Mailing", style={"fontWeight": "600"}),
                                dcc.Dropdown(
                                    id="mailing-filter",
                                    options=[
                                        {"label": "All", "value": "All"},
                                        {"label": "UWG Mailing", "value": "UWG Mailing"},
                                        {"label": "No Mailing", "value": "No Mailing"}
                                    ],
                                    value="All",
                                    clearable=False
                                )
                            ]
                        )
                    ]
                )
            ]
        ),

        # KPI cards
        html.Div(
            style={
                "display": "flex",
                "gap": "16px",
                "flexWrap": "wrap",
                "marginBottom": "18px"
            },
            children=[
                html.Div(id="kpi-total-revenue", style=CARD),
                html.Div(id="kpi-new-customer", style=CARD),
                html.Div(id="kpi-average-revenue", style=CARD),
                html.Div(id="kpi-paid-media", style=CARD),
                html.Div(id="kpi-media-share", style=CARD)
            ]
        ),

        # Daily revenue - full width
        html.Div(
            style=PANEL,
            children=[dcc.Graph(id="daily-revenue-chart")]
        ),

        # Monthly + media
        html.Div(
            style={
                "display": "grid",
                "gridTemplateColumns": "repeat(auto-fit, minmax(420px, 1fr))",
                "gap": "18px"
            },
            children=[
                html.Div(style=PANEL, children=[dcc.Graph(id="monthly-revenue-chart")]),
                html.Div(style=PANEL, children=[dcc.Graph(id="media-chart")])
            ]
        ),

        # Promotions + mailing
        html.Div(
            style={
                "display": "grid",
                "gridTemplateColumns": "repeat(auto-fit, minmax(420px, 1fr))",
                "gap": "18px"
            },
            children=[
                html.Div(style=PANEL, children=[dcc.Graph(id="promotion-chart")]),
                html.Div(style=PANEL, children=[dcc.Graph(id="mailing-chart")])
            ]
        ),

        # BFCM + holiday
        html.Div(
            style={
                "display": "grid",
                "gridTemplateColumns": "repeat(auto-fit, minmax(420px, 1fr))",
                "gap": "18px"
            },
            children=[
                html.Div(style=PANEL, children=[dcc.Graph(id="bfcm-chart")]),
                html.Div(style=PANEL, children=[dcc.Graph(id="holiday-chart")])
            ]
        ),

        # New customer + media relationship
        html.Div(
            style={
                "display": "grid",
                "gridTemplateColumns": "repeat(auto-fit, minmax(420px, 1fr))",
                "gap": "18px"
            },
            children=[
                html.Div(style=PANEL, children=[dcc.Graph(id="new-customer-chart")]),
                html.Div(style=PANEL, children=[dcc.Graph(id="scatter-chart")])
            ]
        ),

        # Key findings and recommendations
        html.Div(
            style={
                "display": "grid",
                "gridTemplateColumns": "repeat(auto-fit, minmax(420px, 1fr))",
                "gap": "18px"
            },
            children=[
                html.Div(
                    style={
                        **PANEL,
                        "padding": "22px 25px"
                    },
                    children=[
                        html.H3("Key Findings", style=SECTION_TITLE),
                        html.Div(id="key-findings")
                    ]
                ),
                html.Div(
                    style={
                        **PANEL,
                        "padding": "22px 25px"
                    },
                    children=[
                        html.H3("Business Recommendations", style=SECTION_TITLE),
                        html.Div(id="recommendations")
                    ]
                )
            ]
        ),

        # Interpretation note
        html.Div(
            style={
                "backgroundColor": "#EEF2F7",
                "padding": "16px 22px",
                "borderRadius": "12px",
                "color": "#4B5563",
                "fontSize": "13px",
                "marginTop": "2px"
            },
            children=[
                html.Strong("Important: "),
                "Promotion, mailing, BFCM, holiday and paid-media comparisons show observed associations. ",
                "They do not by themselves establish that these factors caused changes in revenue."
            ]
        )
    ]
)


# ============================================================
# 7. CALLBACK
# ============================================================

@app.callback(
    [
        Output("kpi-total-revenue", "children"),
        Output("kpi-new-customer", "children"),
        Output("kpi-average-revenue", "children"),
        Output("kpi-paid-media", "children"),
        Output("kpi-media-share", "children"),
        Output("daily-revenue-chart", "figure"),
        Output("monthly-revenue-chart", "figure"),
        Output("media-chart", "figure"),
        Output("promotion-chart", "figure"),
        Output("mailing-chart", "figure"),
        Output("bfcm-chart", "figure"),
        Output("holiday-chart", "figure"),
        Output("new-customer-chart", "figure"),
        Output("scatter-chart", "figure"),
        Output("key-findings", "children"),
        Output("recommendations", "children")
    ],
    [
        Input("year-filter", "value"),
        Input("promotion-filter", "value"),
        Input("mailing-filter", "value")
    ]
)
def update_dashboard(selected_year, selected_promotion, selected_mailing):

    filtered = df.copy()

    if selected_year != "All":
        filtered = filtered[filtered["Year"] == int(selected_year)]

    if selected_promotion == "Promotion":
        filtered = filtered[filtered["Promotion_Discount"] == 1]
    elif selected_promotion == "No Promotion":
        filtered = filtered[filtered["Promotion_Discount"] == 0]

    if selected_mailing == "UWG Mailing":
        filtered = filtered[filtered["UWG_Mailing"] == 1]
    elif selected_mailing == "No Mailing":
        filtered = filtered[filtered["UWG_Mailing"] == 0]

    # --------------------------------------------------------
    # Empty result
    # --------------------------------------------------------
    if filtered.empty:
        empty_fig = go.Figure()
        empty_fig.update_layout(
            template="plotly_white",
            title="No data available for the selected filters",
            xaxis={"visible": False},
            yaxis={"visible": False}
        )
        empty_card = make_card("NO DATA", "—")
        empty_text = [html.P("No observations match the selected filters.")]
        return (
            empty_card, empty_card, empty_card, empty_card, empty_card,
            empty_fig, empty_fig, empty_fig, empty_fig, empty_fig,
            empty_fig, empty_fig, empty_fig, empty_fig,
            empty_text, empty_text
        )

    # --------------------------------------------------------
    # KPIs
    # --------------------------------------------------------
    total_revenue = filtered["Total_Revenue"].sum()
    new_customer_revenue = filtered["Revenue_New_Customer"].sum()
    average_daily_revenue = filtered["Total_Revenue"].mean()
    total_paid_media = filtered["Total_Paid_Media"].sum()
    media_share = total_paid_media / total_revenue * 100 if total_revenue else 0

    # --------------------------------------------------------
    # Aggregations
    # --------------------------------------------------------
    daily = filtered.sort_values("Date")

    monthly = (
        filtered.groupby("Year_Month", as_index=False)
        .agg(
            Total_Revenue=("Total_Revenue", "sum"),
            New_Customer_Revenue=("Revenue_New_Customer", "sum")
        )
        .sort_values("Year_Month")
    )

    media_data = pd.DataFrame({
        "Channel": ["Google", "Meta", "Other Media"],
        "Spend": [
            filtered["spend_Google"].sum(),
            filtered["spend_Meta"].sum(),
            filtered[other_media].sum().sum()
        ]
    })

    def binary_average(column):
        result = (
            filtered.groupby(column, as_index=False)["Total_Revenue"]
            .mean()
            .rename(columns={"Total_Revenue": "Average_Revenue"})
        )
        return result

    promotion_data = binary_average("Promotion_Discount")
    promotion_data["Label"] = promotion_data["Promotion_Discount"].map({
        0: "No Promotion",
        1: "Promotion"
    })

    mailing_data = binary_average("UWG_Mailing")
    mailing_data["Label"] = mailing_data["UWG_Mailing"].map({
        0: "No Mailing",
        1: "UWG Mailing"
    })

    bfcm_data = binary_average("BFCM_Promo_Effect")
    bfcm_data["Label"] = bfcm_data["BFCM_Promo_Effect"].map({
        0: "Non-BFCM",
        1: "BFCM"
    })

    holiday_data = binary_average("holiday_list")
    holiday_data["Label"] = holiday_data["holiday_list"].map({
        0: "Non-Holiday",
        1: "Holiday"
    })

    # --------------------------------------------------------
    # 1. Daily revenue
    # --------------------------------------------------------
    daily_fig = go.Figure()
    daily_fig.add_trace(go.Scatter(
        x=daily["Date"],
        y=daily["Total_Revenue"],
        mode="lines",
        name="Daily Revenue",
        line={"width": 1.8},
        hovertemplate=(
            "<b>%{x|%d %b %Y}</b><br>"
            "Revenue: $%{y:,.0f}<extra></extra>"
        )
    ))
    daily_fig = base_layout(daily_fig, "Daily Total Revenue Over Time", 470)
    daily_fig.update_layout(hovermode="x unified")
    daily_fig.update_xaxes(title="Date")
    daily_fig.update_yaxes(title="Revenue ($)")

    # --------------------------------------------------------
    # 2. Monthly revenue
    # --------------------------------------------------------
    monthly_fig = go.Figure()
    monthly_fig.add_trace(go.Scatter(
        x=monthly["Year_Month"],
        y=monthly["Total_Revenue"],
        mode="lines+markers",
        name="Revenue",
        hovertemplate=(
            "<b>%{x}</b><br>Revenue: $%{y:,.0f}<extra></extra>"
        )
    ))
    monthly_fig = base_layout(monthly_fig, "Monthly Revenue Trend")
    monthly_fig.update_xaxes(title="Month", tickangle=-45)
    monthly_fig.update_yaxes(title="Revenue ($)")

    # --------------------------------------------------------
    # 3. Media
    # --------------------------------------------------------
    media_fig = go.Figure()
    media_fig.add_trace(go.Bar(
        x=media_data["Channel"],
        y=media_data["Spend"],
        text=[money(x) for x in media_data["Spend"]],
        textposition="auto",
        hovertemplate=(
            "<b>%{x}</b><br>Spend: $%{y:,.0f}<extra></extra>"
        )
    ))
    media_fig = base_layout(media_fig, "Paid Media Spend by Channel")
    media_fig.update_xaxes(title="Channel")
    media_fig.update_yaxes(title="Spend ($)")

    # --------------------------------------------------------
    # 4. Promotion
    # --------------------------------------------------------
    promotion_fig = go.Figure()
    promotion_fig.add_trace(go.Bar(
        x=promotion_data["Label"],
        y=promotion_data["Average_Revenue"],
        text=[money(x) for x in promotion_data["Average_Revenue"]],
        textposition="auto",
        hovertemplate=(
            "<b>%{x}</b><br>Average Daily Revenue: $%{y:,.0f}<extra></extra>"
        )
    ))
    promotion_fig = base_layout(
        promotion_fig,
        "Average Daily Revenue: Promotion vs No Promotion"
    )
    promotion_fig.update_xaxes(title="Promotion Status")
    promotion_fig.update_yaxes(title="Average Revenue ($)")

    # --------------------------------------------------------
    # 5. Mailing
    # --------------------------------------------------------
    mailing_fig = go.Figure()
    mailing_fig.add_trace(go.Bar(
        x=mailing_data["Label"],
        y=mailing_data["Average_Revenue"],
        text=[money(x) for x in mailing_data["Average_Revenue"]],
        textposition="auto",
        hovertemplate=(
            "<b>%{x}</b><br>Average Daily Revenue: $%{y:,.0f}<extra></extra>"
        )
    ))
    mailing_fig = base_layout(
        mailing_fig,
        "Average Daily Revenue: UWG Mailing vs No Mailing"
    )
    mailing_fig.update_xaxes(title="Mailing Status")
    mailing_fig.update_yaxes(title="Average Revenue ($)")

    # --------------------------------------------------------
    # 6. BFCM
    # --------------------------------------------------------
    bfcm_fig = go.Figure()
    bfcm_fig.add_trace(go.Bar(
        x=bfcm_data["Label"],
        y=bfcm_data["Average_Revenue"],
        text=[money(x) for x in bfcm_data["Average_Revenue"]],
        textposition="auto",
        hovertemplate=(
            "<b>%{x}</b><br>Average Daily Revenue: $%{y:,.0f}<extra></extra>"
        )
    ))
    bfcm_fig = base_layout(
        bfcm_fig,
        "Average Daily Revenue: BFCM vs Non-BFCM"
    )
    bfcm_fig.update_xaxes(title="BFCM Status")
    bfcm_fig.update_yaxes(title="Average Revenue ($)")

    # --------------------------------------------------------
    # 7. Holiday
    # --------------------------------------------------------
    holiday_fig = go.Figure()
    holiday_fig.add_trace(go.Bar(
        x=holiday_data["Label"],
        y=holiday_data["Average_Revenue"],
        text=[money(x) for x in holiday_data["Average_Revenue"]],
        textposition="auto",
        hovertemplate=(
            "<b>%{x}</b><br>Average Daily Revenue: $%{y:,.0f}<extra></extra>"
        )
    ))
    holiday_fig = base_layout(
        holiday_fig,
        "Average Daily Revenue: Holiday vs Non-Holiday"
    )
    holiday_fig.update_xaxes(title="Holiday Status")
    holiday_fig.update_yaxes(title="Average Revenue ($)")

    # --------------------------------------------------------
    # 8. New customer revenue
    # --------------------------------------------------------
    new_customer_fig = go.Figure()
    new_customer_fig.add_trace(go.Scatter(
        x=monthly["Year_Month"],
        y=monthly["New_Customer_Revenue"],
        mode="lines+markers",
        name="New Customer Revenue",
        hovertemplate=(
            "<b>%{x}</b><br>New-Customer Revenue: $%{y:,.0f}<extra></extra>"
        )
    ))
    new_customer_fig = base_layout(
        new_customer_fig,
        "Monthly New-Customer Revenue"
    )
    new_customer_fig.update_xaxes(title="Month", tickangle=-45)
    new_customer_fig.update_yaxes(title="New-Customer Revenue ($)")

    # --------------------------------------------------------
    # 9. Revenue vs paid media
    # --------------------------------------------------------
    scatter_fig = go.Figure()
    scatter_fig.add_trace(go.Scatter(
        x=filtered["Total_Paid_Media"],
        y=filtered["Total_Revenue"],
        mode="markers",
        marker={"size": 7, "opacity": 0.60},
        hovertemplate=(
            "Paid Media: $%{x:,.0f}<br>Revenue: $%{y:,.0f}<extra></extra>"
        )
    ))
    scatter_fig = base_layout(
        scatter_fig,
        "Daily Revenue vs Paid Media Spend"
    )
    scatter_fig.update_xaxes(title="Total Paid Media Spend ($)")
    scatter_fig.update_yaxes(title="Total Revenue ($)")

    # --------------------------------------------------------
    # KEY FINDINGS - generated from the currently filtered data
    # --------------------------------------------------------
    findings = []

    # Promotion comparison
    if len(promotion_data) == 2:
        promo_mean = promotion_data.loc[
            promotion_data["Promotion_Discount"] == 1,
            "Average_Revenue"
        ].iloc[0]
        no_promo_mean = promotion_data.loc[
            promotion_data["Promotion_Discount"] == 0,
            "Average_Revenue"
        ].iloc[0]
        diff = (promo_mean - no_promo_mean) / no_promo_mean * 100 if no_promo_mean else np.nan
        direction = "higher" if diff >= 0 else "lower"
        findings.append(
            f"Average daily revenue on promotion days was {abs(diff):.1f}% {direction} than on non-promotion days."
        )

    # BFCM comparison
    if len(bfcm_data) == 2:
        bfcm_mean = bfcm_data.loc[
            bfcm_data["BFCM_Promo_Effect"] == 1,
            "Average_Revenue"
        ].iloc[0]
        non_bfcm_mean = bfcm_data.loc[
            bfcm_data["BFCM_Promo_Effect"] == 0,
            "Average_Revenue"
        ].iloc[0]
        diff = (bfcm_mean - non_bfcm_mean) / non_bfcm_mean * 100 if non_bfcm_mean else np.nan
        direction = "higher" if diff >= 0 else "lower"
        findings.append(
            f"Average daily revenue on BFCM days was {abs(diff):.1f}% {direction} than on non-BFCM days."
        )

    # Holiday comparison
    if len(holiday_data) == 2:
        holiday_mean = holiday_data.loc[
            holiday_data["holiday_list"] == 1,
            "Average_Revenue"
        ].iloc[0]
        non_holiday_mean = holiday_data.loc[
            holiday_data["holiday_list"] == 0,
            "Average_Revenue"
        ].iloc[0]
        diff = (holiday_mean - non_holiday_mean) / non_holiday_mean * 100 if non_holiday_mean else np.nan
        direction = "higher" if diff >= 0 else "lower"
        findings.append(
            f"Average daily revenue on holiday days was {abs(diff):.1f}% {direction} than on non-holiday days."
        )

    # Mailing comparison
    if len(mailing_data) == 2:
        mailing_mean = mailing_data.loc[
            mailing_data["UWG_Mailing"] == 1,
            "Average_Revenue"
        ].iloc[0]
        no_mailing_mean = mailing_data.loc[
            mailing_data["UWG_Mailing"] == 0,
            "Average_Revenue"
        ].iloc[0]
        diff = (mailing_mean - no_mailing_mean) / no_mailing_mean * 100 if no_mailing_mean else np.nan
        direction = "higher" if diff >= 0 else "lower"
        findings.append(
            f"Average daily revenue on UWG mailing days was {abs(diff):.1f}% {direction} than on non-mailing days."
        )

    # Highest revenue day
    peak = filtered.loc[filtered["Total_Revenue"].idxmax()]
    findings.append(
        f"The highest observed revenue day was {peak['Date'].strftime('%d %b %Y')}, with revenue of {money(peak['Total_Revenue'])}."
    )

    findings.append(
        f"Paid media represented {media_share:.1f}% of total revenue over the selected period."
    )

    findings_list = [
        html.Li(
            item,
            style={"marginBottom": "10px", "lineHeight": "1.5"}
        )
        for item in findings
    ]

    # --------------------------------------------------------
    # RECOMMENDATIONS - decision-support, not causal claims
    # --------------------------------------------------------
    recommendations = [
        "Use BFCM and other high-revenue periods as priority periods for campaign planning, while evaluating incremental revenue and profitability before increasing spend.",
        "Compare promotion and mailing performance with campaign cost, customer acquisition and margin measures to determine whether observed revenue differences translate into business value.",
        "Investigate the largest daily revenue spikes individually and cross-check promotions, mailings, holidays and media activity before drawing conclusions about their drivers.",
        "Use the dashboard filters to examine whether the observed patterns are consistent across years rather than relying only on the overall period average."
    ]

    recommendations_list = [
        html.Li(
            item,
            style={"marginBottom": "10px", "lineHeight": "1.5"}
        )
        for item in recommendations
    ]

    return (
        make_card("TOTAL REVENUE", money(total_revenue)),
        make_card("NEW-CUSTOMER REVENUE", money(new_customer_revenue)),
        make_card("AVERAGE DAILY REVENUE", money(average_daily_revenue)),
        make_card("TOTAL PAID MEDIA", money(total_paid_media)),
        make_card("PAID MEDIA / REVENUE", pct(media_share)),
        daily_fig,
        monthly_fig,
        media_fig,
        promotion_fig,
        mailing_fig,
        bfcm_fig,
        holiday_fig,
        new_customer_fig,
        scatter_fig,
        html.Ul(findings_list, style={"paddingLeft": "22px", "marginBottom": "0"}),
        html.Ul(recommendations_list, style={"paddingLeft": "22px", "marginBottom": "0"})
    )


# ============================================================
# 8. RUN APPLICATION
# ============================================================

if __name__ == "__main__":
    app.run(debug=True)


