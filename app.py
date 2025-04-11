import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go

st.write("✅ Checkpoint: Imports loaded")

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

st.write("✅ Checkpoint: Light mode CSS applied")

# KiwiSaver providers with categorized funds
funds = {
    # ... (unchanged fund dictionary — no need to print here)
}

st.write("✅ Checkpoint: Funds dictionary loaded")

# Streamlit UI
st.title("KiwiSaver Fund Comparison Calculator")
st.write("✅ Checkpoint: Title rendered")

# User Inputs
starting_balance = st.number_input("Starting KiwiSaver Balance ($)", min_value=0, value=0, step=1000)
income = st.number_input("Annual Income ($)", min_value=1000, value=70000, step=1000)
contribution_rate = st.slider("Your Contribution Rate (%)", 3, 10, 3) / 100
employer_contribution_rate = st.slider("Employer Contribution Rate (%)", 3, 10, 3) / 100
investment_years = st.slider("Investment Period (Years)", 1, 40, 20)

st.write("✅ Checkpoint: Inputs collected")

govt_contribution = 521

# Fund recommendation logic
recommendation = "Conservative" if investment_years <= 3 else \
                "Moderate" if investment_years <= 5 else \
                "Balanced" if investment_years == 6 else \
                "Growth" if investment_years <= 10 else "Aggressive"

color = "green" if recommendation in funds else "red"
st.markdown(f"**Recommended Fund Type:** <span style='color:{color}; font-weight:bold;'>{recommendation}</span>", unsafe_allow_html=True)

st.write("✅ Checkpoint: Recommendation calculated")

fund_type = st.selectbox("Select Fund Type", list(funds.keys()))
st.write("✅ Checkpoint: Fund type selected")

monthly_employee = (income * contribution_rate) / 12
monthly_employer = (income * employer_contribution_rate) / 12

years = list(range(1, investment_years + 1))
results = pd.DataFrame({"Year": years})

st.write("✅ Checkpoint: Contribution + year range calculated")

# Projections for selected fund type
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

st.write("✅ Checkpoint: Projections calculated")

results_display = results.set_index("Year")
st.subheader(f"Projected KiwiSaver Balances - {fund_type} Funds")
st.dataframe(results_display.style.format({col: "${:,.2f}" for col in results_display.columns}))

st.write("✅ Checkpoint: Data table displayed")

# Plot chart
st.subheader("Balance Growth Over Time")
fig = go.Figure()

sorted_funds = sorted(selected_funds.keys(), key=lambda f: results[f].iloc[-1], reverse=True)
for fund in sorted_funds:
    fig.add_trace(go.Scatter(
        x=results["Year"],
        y=results[fund],
        mode='lines+markers',
        name=fund,
        hovertemplate=f'<b>Fund</b>: {fund}<br><b>Balance</b>: $%{{y:,.2f}}<extra></extra>'
    ))

fig.update_layout(
    autosize=True,
    xaxis_title="Years",
    yaxis_title="Projected Balance ($)",
    title=f"KiwiSaver Growth Comparison ({fund_type} Funds)",
    hovermode="x unified",
    margin=dict(l=20, r=20, t=40, b=20)
)

st.plotly_chart(fig, use_container_width=True)
st.write("✅ Checkpoint: Chart rendered")
