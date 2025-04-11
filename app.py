import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.io as pio

# Force all Plotly charts to use light mode
pio.templates.default = "plotly_white"

# Force Streamlit app into light mode
st.markdown(
    """
    <style>
        html, body, [class*="st-"] {
            background-color: white !important;
            color: black !important;
        }
        section.main > div {
            overflow-x: hidden;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Fund data
funds = {
    "Conservative": {
        "AMP Defensive Conservative": {"Avg Return": 0.032, "Annual Fee": 0, "Mgmt Fee %": 0.0, "Buy/Sell Fee": 0.00},
        "ANZ Conservative": {"Avg Return": 0.024, "Annual Fee": 0, "Mgmt Fee %": 0.0, "Buy/Sell Fee": 0.00},
        "ASB Scheme's Cnsrv": {"Avg Return": 0.025, "Annual Fee": 0, "Mgmt Fee %": 0.0, "Buy/Sell Fee": 0.00},
        "BNZ Consrv": {"Avg Return": 0.024, "Annual Fee": 0, "Mgmt Fee %": 0.0, "Buy/Sell Fee": 0.00},
        "Booster Consrv Fund": {"Avg Return": 0.028, "Annual Fee": 0, "Mgmt Fee %": 0.0, "Buy/Sell Fee": 0.00},
        "Fisher Funds Plan Def Conserv": {"Avg Return": 0.039, "Annual Fee": 0, "Mgmt Fee %": 0.0, "Buy/Sell Fee": 0.00},
        "Milford Conservative Fund": {"Avg Return": 0.037, "Annual Fee": 0, "Mgmt Fee %": 0.0, "Buy/Sell Fee": 0.00},
        "Simplicity Conservative Fund": {"Avg Return": 0.023, "Annual Fee": 0, "Mgmt Fee %": 0.0, "Buy/Sell Fee": 0.00},
        "Westpac Defensive Conservative": {"Avg Return": 0.029, "Annual Fee": 0, "Mgmt Fee %": 0.0, "Buy/Sell Fee": 0.00},
    },
    "Moderate": {
        "AMP LS Moderate Fund": {"Avg Return": 0.032, "Annual Fee": 0, "Mgmt Fee %": 0.0, "Buy/Sell Fee": 0.00},
        "ASB Scheme's Moderate": {"Avg Return": 0.036, "Annual Fee": 0, "Mgmt Fee %": 0.0, "Buy/Sell Fee": 0.00},
        "BNZ Moderate Fund": {"Avg Return": 0.041, "Annual Fee": 0, "Mgmt Fee %": 0.0, "Buy/Sell Fee": 0.00},
        "Booster Moderate": {"Avg Return": 0.032, "Annual Fee": 0, "Mgmt Fee %": 0.0, "Buy/Sell Fee": 0.00},
        "Generate Moderate": {"Avg Return": 0.047, "Annual Fee": 0, "Mgmt Fee %": 0.0, "Buy/Sell Fee": 0.00},
        "Westpac Moderate": {"Avg Return": 0.041, "Annual Fee": 0, "Mgmt Fee %": 0.0, "Buy/Sell Fee": 0.00}
    },
    "Balanced": {
        "AMP LS Balanced Fund": {"Avg Return": 0.05, "Annual Fee": 0, "Mgmt Fee %": 0.0, "Buy/Sell Fee": 0.00},
        "ANZ Balanced": {"Avg Return": 0.041, "Annual Fee": 0, "Mgmt Fee %": 0.0, "Buy/Sell Fee": 0.00},
        "ASB Scheme's Balanced": {"Avg Return": 0.055, "Annual Fee": 0, "Mgmt Fee %": 0.0, "Buy/Sell Fee": 0.00},
        "BNZ Balanced Fund": {"Avg Return": 0.057, "Annual Fee": 0, "Mgmt Fee %": 0.0, "Buy/Sell Fee": 0.00},
        "Booster Balanced": {"Avg Return": 0.054, "Annual Fee": 0, "Mgmt Fee %": 0.0, "Buy/Sell Fee": 0.00},
        "Fisher Funds Plan Balanced": {"Avg Return": 0.065, "Annual Fee": 0, "Mgmt Fee %": 0.0, "Buy/Sell Fee": 0.00},
        "Milford Balanced Fund": {"Avg Return": 0.071, "Annual Fee": 0, "Mgmt Fee %": 0.0, "Buy/Sell Fee": 0.00},
        "Pathfinder Balanced Fund": {"Avg Return": 0.078, "Annual Fee": 0, "Mgmt Fee %": 0.0, "Buy/Sell Fee": 0.00},
        "QuayStreet Balanced": {"Avg Return": 0.082, "Annual Fee": 0, "Mgmt Fee %": 0.0, "Buy/Sell Fee": 0.00},
        "Simplicity Balanced Fund": {"Avg Return": 0.060, "Annual Fee": 0, "Mgmt Fee %": 0.0, "Buy/Sell Fee": 0.00},
        "Westpac Balanced Fund": {"Avg Return": 0.052, "Annual Fee": 0, "Mgmt Fee %": 0.0, "Buy/Sell Fee": 0.00}
    },
    "Growth": {
        "AMP LS Growth Fund": {"Avg Return": 0.065, "Annual Fee": 0, "Mgmt Fee %": 0.0, "Buy/Sell Fee": 0.00},
        "ANZ Growth": {"Avg Return": 0.059, "Annual Fee": 0, "Mgmt Fee %": 0.0, "Buy/Sell Fee": 0.00},
        "ASB Scheme's Growth": {"Avg Return": 0.069, "Annual Fee": 0, "Mgmt Fee %": 0.0, "Buy/Sell Fee": 0.00},
        "BNZ Growth Fund": {"Avg Return": 0.074, "Annual Fee": 0, "Mgmt Fee %": 0.0, "Buy/Sell Fee": 0.00},
        "Booster Growth": {"Avg Return": 0.07, "Annual Fee": 0, "Mgmt Fee %": 0.0, "Buy/Sell Fee": 0.00},
        "Generate Growth Fund": {"Avg Return": 0.074, "Annual Fee": 0, "Mgmt Fee %": 0.0, "Buy/Sell Fee": 0.00},
        "Milford Active Growth Fund": {"Avg Return": 0.093, "Annual Fee": 0, "Mgmt Fee %": 0.0, "Buy/Sell Fee": 0.00},
        "Pathfinder Growth Fund": {"Avg Return": 0.1, "Annual Fee": 0, "Mgmt Fee %": 0.0, "Buy/Sell Fee": 0.00},
        "QuayStreet Growth": {"Avg Return": 0.099, "Annual Fee": 0, "Mgmt Fee %": 0.0, "Buy/Sell Fee": 0.00},
        "Simplicity Growth Fund": {"Avg Return": 0.081, "Annual Fee": 0, "Mgmt Fee %": 0.0, "Buy/Sell Fee": 0.00},
        "Westpac Growth Fund": {"Avg Return": 0.063, "Annual Fee": 0, "Mgmt Fee %": 0.0, "Buy/Sell Fee": 0.00}
    },
    "Aggressive": {
        "AMP Aggressive Fund": {"Avg Return": 0.071, "Annual Fee": 0, "Mgmt Fee %": 0.0, "Buy/Sell Fee": 0.00},
        "Booster High Growth": {"Avg Return": 0.085, "Annual Fee": 0, "Mgmt Fee %": 0.0, "Buy/Sell Fee": 0.00},
        "Generate Focused Growth Fund": {"Avg Return": 0.085, "Annual Fee": 0, "Mgmt Fee %": 0.0, "Buy/Sell Fee": 0.00},
        "Milford Aggressive": {"Avg Return": 0.11, "Annual Fee": 0, "Mgmt Fee %": 0.0, "Buy/Sell Fee": 0.00},
    }
}



# UI
st.title("KiwiSaver Fund Comparison Calculator")

starting_balance = st.number_input("Starting KiwiSaver Balance ($)", min_value=0, value=0, step=1000)
income = st.number_input("Annual Income ($)", min_value=1000, value=70000, step=1000)
contribution_rate = st.slider("Your Contribution Rate (%)", 3, 10, 3) / 100
employer_contribution_rate = st.slider("Employer Contribution Rate (%)", 3, 10, 3) / 100
investment_years = st.slider("Investment Period (Years)", 1, 40, 20)

govt_contribution = 521

recommendation = "Conservative" if investment_years <= 3 else \
                "Moderate" if investment_years <= 5 else \
                "Balanced" if investment_years == 6 else \
                "Growth" if investment_years <= 10 else "Aggressive"

color = "green" if recommendation in funds else "red"
st.markdown(f"**Recommended Fund Type:** <span style='color:{color}; font-weight:bold;'>{recommendation}</span>", unsafe_allow_html=True)

fund_type = st.selectbox("Select Fund Type", list(funds.keys()))

monthly_employee = (income * contribution_rate) / 12
monthly_employer = (income * employer_contribution_rate) / 12

years = list(range(1, investment_years + 1))
results = pd.DataFrame({"Year": years})

selected_funds = funds[fund_type]
for fund, data in selected_funds.items():
    balance = starting_balance
    yearly_balances = []
    for year in years:
        annual_contribution = (monthly_employee + monthly_employer) * 12 + govt_contribution
        balance += annual_contribution
        balance *= (1 + data["Avg Return"])
        balance -= data["Annual Fee"]
        balance *= (1 - data["Mgmt Fee %"])
        balance *= (1 - data["Buy/Sell Fee"])
        yearly_balances.append(balance)
    results[fund] = yearly_balances

results_display = results.set_index("Year")

st.subheader(f"Projected KiwiSaver Balances - {fund_type} Funds")
st.dataframe(results_display.style.format({col: "${:,.2f}" for col in results_display.columns}))

sorted_funds = sorted(selected_funds.keys(), key=lambda f: results[f].iloc[-1], reverse=True)

# Build Plotly chart with light template and hover label fix
fig = go.Figure()
for fund in sorted_funds:
    fig.add_trace(go.Scatter(
        x=results["Year"],
        y=results[fund],
        mode='lines+markers',
        name=fund,
        hovertemplate=f'<b>Fund</b>: {fund}<br><b>Balance</b>: $%{{y:,.2f}}<extra></extra>'
    ))

fig.update_layout(
    template="plotly_white",
    xaxis_title="Years",
    yaxis_title="Projected Balance ($)",
    title=f"KiwiSaver Growth Comparison ({fund_type} Funds)",
    hovermode="x unified",
    dragmode="pan",
    xaxis=dict(fixedrange=True),
    yaxis=dict(fixedrange=True),
    hoverlabel=dict(
        bgcolor="#f0f0f0",
        font_color="black",
        font_size=14,
        font_family="Arial",
        bordercolor="black"
    )
)

# Show chart only on desktop via JS detection
st.subheader("Balance Growth Over Time")
st.markdown('<div id="chart-container">', unsafe_allow_html=True)
st.plotly_chart(fig, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# JS to hide chart on mobile and show a message instead
st.markdown(
    """
    <div id="mobile-msg" style="display: none; color: red; font-style: italic;">
        📱 Chart hidden on mobile for a better experience.
    </div>

    <script>
    const chart = window.parent.document.getElementById("chart-container") || document.getElementById("chart-container");
    const msg = document.getElementById("mobile-msg");
    if (window.innerWidth < 768) {
        if (chart) chart.style.display = "none";
        if (msg) msg.style.display = "block";
    }
    </script>
    """,
    unsafe_allow_html=True
)
