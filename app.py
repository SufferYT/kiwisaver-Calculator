import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go

# Force light mode with CSS
st.markdown(
    """
    <style>
        html, body, [class*="st-"] {
            background-color: white !important;
            color: black !important;
        }
        div.stButton > button, div.stTextInput > div, div.stSelectbox > div, div.stNumberInput > div, div.stSlider > div {
            background-color: white !important;
            color: black !important;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# KiwiSaver providers with categorized funds
funds = {
    "Conservative": {
        "AMP Defensive Conservative": {"Avg Return": 0.024, "Annual Fee": 0, "Mgmt Fee %": 0.0079, "Buy/Sell Fee": 0.00},
        "ANZ Conservative": {"Avg Return": 0.024, "Annual Fee": 0, "Mgmt Fee %": 0.0064, "Buy/Sell Fee": 0.00},
        "ASB Scheme's Cnsrv": {"Avg Return": 0.025, "Annual Fee": 0, "Mgmt Fee %": 0.004, "Buy/Sell Fee": 0.00},
        "BNZ Consrv": {"Avg Return": 0.024, "Annual Fee": 0, "Mgmt Fee %": 0.0045, "Buy/Sell Fee": 0.00},
        "Booster Consrv Fund": {"Avg Return": 0.028, "Annual Fee": 36, "Mgmt Fee %": 0.0038, "Buy/Sell Fee": 0.0012},
        "Fisher Funds Plan Def Conserv": {"Avg Return": 0.039, "Annual Fee": 0, "Mgmt Fee %": 0.0093, "Buy/Sell Fee": 0.00},
        "Milford Conservative Fund": {"Avg Return": 0.037, "Annual Fee": 0, "Mgmt Fee %": 0.0085, "Buy/Sell Fee": 0.00},
        "Simplicity Conservative Fund": {"Avg Return": 0.023, "Annual Fee": 0, "Mgmt Fee %": 0.0025, "Buy/Sell Fee": 0.00},
        "Westpac Defensive Conservative": {"Avg Return": 0.029, "Annual Fee": 0, "Mgmt Fee %": 0.004, "Buy/Sell Fee": 0.00}
    },
    "Moderate": {
        "AMP Moderate Fund": {"Avg Return": 0.032, "Annual Fee": 40, "Mgmt Fee %": 0.007, "Buy/Sell Fee": 0.0015},
        "ANZ Conservative Balanced": {"Avg Return": 0.033, "Annual Fee": 45, "Mgmt Fee %": 0.0072, "Buy/Sell Fee": 0.0017},
        "ASB Moderate": {"Avg Return": 0.036, "Annual Fee": 45, "Mgmt Fee %": 0.0072, "Buy/Sell Fee": 0.0017},
        "BNZ Moderate Fund": {"Avg Return": 0.041, "Annual Fee": 45, "Mgmt Fee %": 0.0072, "Buy/Sell Fee": 0.0017},
        "Booster Moderate": {"Avg Return": 0.032, "Annual Fee": 45, "Mgmt Fee %": 0.0072, "Buy/Sell Fee": 0.0017},
        "Generate Moderate": {"Avg Return": 0.047, "Annual Fee": 45, "Mgmt Fee %": 0.0072, "Buy/Sell Fee": 0.0017},
        "Westpac Moderate": {"Avg Return": 0.040, "Annual Fee": 45, "Mgmt Fee %": 0.0072, "Buy/Sell Fee": 0.0017},
    },
    "Balanced": {
        "AMP Balanced Fund": {"Avg Return": 0.05, "Annual Fee": 50, "Mgmt Fee %": 0.008, "Buy/Sell Fee": 0.002},
        "ANZ Balanced": {"Avg Return": 0.041, "Annual Fee": 48, "Mgmt Fee %": 0.0078, "Buy/Sell Fee": 0.0019},
        "ASB Balanced": {"Avg Return": 0.055, "Annual Fee": 48, "Mgmt Fee %": 0.0078, "Buy/Sell Fee": 0.0019},
        "BNZ Balanced Fund": {"Avg Return": 0.057, "Annual Fee": 48, "Mgmt Fee %": 0.0078, "Buy/Sell Fee": 0.0019},
        "Booster Balanced": {"Avg Return": 0.054, "Annual Fee": 48, "Mgmt Fee %": 0.0078, "Buy/Sell Fee": 0.0019},
        "Fisher Funds Plan Balanced": {"Avg Return": 0.065, "Annual Fee": 48, "Mgmt Fee %": 0.0078, "Buy/Sell Fee": 0.0019},
        "Milford Balanced Fund": {"Avg Return": 0.071, "Annual Fee": 48, "Mgmt Fee %": 0.0078, "Buy/Sell Fee": 0.0019},
        "Simplicity Balanced Fund": {"Avg Return": 0.06, "Annual Fee": 48, "Mgmt Fee %": 0.0078, "Buy/Sell Fee": 0.0019},
        "Westpac Balanced Fund": {"Avg Return": 0.052, "Annual Fee": 48, "Mgmt Fee %": 0.0078, "Buy/Sell Fee": 0.0019},
    },
    "Growth": {
        "AMP Growth Fund": {"Avg Return": 0.065, "Annual Fee": 55, "Mgmt Fee %": 0.009, "Buy/Sell Fee": 0.0022},
        "ANZ Growth": {"Avg Return": 0.059, "Annual Fee": 55, "Mgmt Fee %": 0.009, "Buy/Sell Fee": 0.0022},
        "ASB Growth": {"Avg Return": 0.069, "Annual Fee": 55, "Mgmt Fee %": 0.009, "Buy/Sell Fee": 0.0022},
        "BNZ Growth Fund": {"Avg Return": 0.074, "Annual Fee": 55, "Mgmt Fee %": 0.009, "Buy/Sell Fee": 0.0022},
        "Booster Growth": {"Avg Return": 0.07, "Annual Fee": 55, "Mgmt Fee %": 0.009, "Buy/Sell Fee": 0.0022},
        "Fisher Funds Growth Fund": {"Avg Return": 0.074, "Annual Fee": 55, "Mgmt Fee %": 0.009, "Buy/Sell Fee": 0.0022},
        "Generate Growth Fund": {"Avg Return": 0.074, "Annual Fee": 55, "Mgmt Fee %": 0.009, "Buy/Sell Fee": 0.0022},
        "Milford Active Growth Fund": {"Avg Return": 0.093, "Annual Fee": 55, "Mgmt Fee %": 0.009, "Buy/Sell Fee": 0.0022},
        "Pathfinder Growth Fund": {"Avg Return": 0.1, "Annual Fee": 55, "Mgmt Fee %": 0.009, "Buy/Sell Fee": 0.0022},
        "Simplicity Growth Fund": {"Avg Return": 0.081, "Annual Fee": 55, "Mgmt Fee %": 0.009, "Buy/Sell Fee": 0.0022},
        "Westpac Growth Fund": {"Avg Return": 0.063, "Annual Fee": 60, "Mgmt Fee %": 0.0092, "Buy/Sell Fee": 0.0023},
    },
    "Aggressive": {
        "AMP Aggressive Fund": {"Avg Return": 0.071, "Annual Fee": 65, "Mgmt Fee %": 0.010, "Buy/Sell Fee": 0.0025},
        "Booster High Growth": {"Avg Return": 0.085, "Annual Fee": 70, "Mgmt Fee %": 0.0105, "Buy/Sell Fee": 0.0028},
        "Generate Focused Growth Fund": {"Avg Return": 0.085, "Annual Fee": 70, "Mgmt Fee %": 0.0105, "Buy/Sell Fee": 0.0028},
        "Milford Aggressive": {"Avg Return": 0.11, "Annual Fee": 70, "Mgmt Fee %": 0.0105, "Buy/Sell Fee": 0.0028},
    }
}

# Streamlit UI
st.title("KiwiSaver Fund Comparison Calculator")

# User Inputs
starting_balance = st.number_input("Starting KiwiSaver Balance ($)", min_value=0, value=0, step=1000)
income = st.number_input("Annual Income ($)", min_value=1000, value=70000, step=1000)
contribution_rate = st.slider("Your Contribution Rate (%)", 3, 10, 3) / 100
employer_contribution_rate = st.slider("Employer Contribution Rate (%)", 3, 10, 3) / 100
investment_years = st.slider("Investment Period (Years)", 1, 40, 20)

govt_contribution = 521  # Max annual government contribution

# Fund recommendation logic
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

# Calculate projections for selected fund type
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

# Plotly chart with mobile-friendly hover
st.subheader("Balance Growth Over Time")
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
    xaxis_title="Years",
    yaxis_title="Projected Balance ($)",
    title=f"KiwiSaver Growth Comparison ({fund_type} Funds)",
    hovermode="x unified",  # Mobile-friendly group hover
    dragmode="pan",         # Mobile drag interaction
    hoverlabel=dict(
        bgcolor="white",
        font_size=14,
        font_family="Arial"
    )
)

st.plotly_chart(fig, use_container_width=True)
