import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# Force light mode and ensure overflow is clean
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

# Fund data (unchanged)
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
    "Aggressive": {
        "AMP Aggressive Fund": {"Avg Return": 0.071, "Annual Fee": 65, "Mgmt Fee %": 0.010, "Buy/Sell Fee": 0.0025},
        "Booster High Growth": {"Avg Return": 0.085, "Annual Fee": 70, "Mgmt Fee %": 0.0105, "Buy/Sell Fee": 0.0028},
        "Generate Focused Growth Fund": {"Avg Return": 0.085, "Annual Fee": 70, "Mgmt Fee %": 0.0105, "Buy/Sell Fee": 0.0028},
        "Milford Aggressive": {"Avg Return": 0.11, "Annual Fee": 70, "Mgmt Fee %": 0.0105, "Buy/Sell Fee": 0.0028},
    },
    # Add the rest of the fund categories as before...
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

# Build Plotly chart
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
    hovermode="x unified",
    dragmode="pan",
    xaxis=dict(fixedrange=True),
    yaxis=dict(fixedrange=True),
    hoverlabel=dict(
        bgcolor="white",
        font_size=14,
        font_family="Arial"
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
