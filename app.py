import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

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

# Sample KiwiSaver providers with categorized funds
funds = {
    "Conservative": {
        "Provider A Conservative": {"Avg Return": 0.04, "Annual Fee": 30, "Mgmt Fee %": 0.006, "Buy/Sell Fee": 0.001},
        "Provider B Conservative": {"Avg Return": 0.042, "Annual Fee": 25, "Mgmt Fee %": 0.0055, "Buy/Sell Fee": 0.0012},
    },
    "Moderate": {
        "Provider A Moderate": {"Avg Return": 0.05, "Annual Fee": 40, "Mgmt Fee %": 0.007, "Buy/Sell Fee": 0.0015},
        "Provider C Moderate": {"Avg Return": 0.052, "Annual Fee": 45, "Mgmt Fee %": 0.0072, "Buy/Sell Fee": 0.0017},
    },
    "Balanced": {
        "Provider A Balanced": {"Avg Return": 0.06, "Annual Fee": 50, "Mgmt Fee %": 0.008, "Buy/Sell Fee": 0.002},
        "Provider B Balanced": {"Avg Return": 0.062, "Annual Fee": 48, "Mgmt Fee %": 0.0078, "Buy/Sell Fee": 0.0019},
    },
    "Growth": {
        "Provider B Growth": {"Avg Return": 0.07, "Annual Fee": 55, "Mgmt Fee %": 0.009, "Buy/Sell Fee": 0.0022},
        "Provider C Growth": {"Avg Return": 0.072, "Annual Fee": 60, "Mgmt Fee %": 0.0092, "Buy/Sell Fee": 0.0023},
    },
    "Aggressive": {
        "Provider A Aggressive": {"Avg Return": 0.08, "Annual Fee": 65, "Mgmt Fee %": 0.010, "Buy/Sell Fee": 0.0025},
        "Provider C Aggressive": {"Avg Return": 0.085, "Annual Fee": 70, "Mgmt Fee %": 0.0105, "Buy/Sell Fee": 0.0028},
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

# Determine color based on recommendation match
color = "green" if recommendation in funds else "red"
st.markdown(f"**Recommended Fund Type:** <span style='color:{color}; font-weight:bold;'>{recommendation}</span>", unsafe_allow_html=True)

# Fund type selection (last input)
fund_type = st.selectbox("Select Fund Type", list(funds.keys()))

# Monthly contributions
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
        balance += annual_contribution  # Add contributions

        # Apply investment return
        balance *= (1 + data["Avg Return"])

        # Deduct fees
        balance -= data["Annual Fee"]
        balance *= (1 - data["Mgmt Fee %"])  # Management fee
        balance *= (1 - data["Buy/Sell Fee"])  # Buy/Sell fee

        yearly_balances.append(balance)
    
    results[fund] = yearly_balances

# Drop the index column to prevent duplicate numbering
results_display = results.set_index("Year")

# Display comparison table
st.subheader(f"Projected KiwiSaver Balances - {fund_type} Funds")
st.dataframe(results_display.style.format({col: "${:,.2f}" for col in results_display.columns}))

# Plot growth over time
st.subheader("Balance Growth Over Time")
fig, ax = plt.subplots(figsize=(10, 5))
for fund in selected_funds.keys():
    ax.plot(results["Year"], results[fund], label=fund)
ax.set_xlabel("Years")
ax.set_ylabel("Projected Balance ($)")
ax.set_title(f"KiwiSaver Growth Comparison ({fund_type} Funds)")
ax.legend()
ax.grid()
st.pyplot(fig)
