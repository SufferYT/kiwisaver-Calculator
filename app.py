import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Sample KiwiSaver providers with historical returns and fees
providers = {
    "Provider A": {"Avg Return": 0.07, "Annual Fee": 50, "Mgmt Fee %": 0.009, "Buy/Sell Fee": 0.002},
    "Provider B": {"Avg Return": 0.065, "Annual Fee": 40, "Mgmt Fee %": 0.008, "Buy/Sell Fee": 0.0015},
    "Provider C": {"Avg Return": 0.08, "Annual Fee": 60, "Mgmt Fee %": 0.010, "Buy/Sell Fee": 0.0025},
}

# Streamlit UI
st.title("KiwiSaver Comparison Calculator")

# User Inputs
income = st.number_input("Annual Income ($)", min_value=1000, value=70000, step=1000)
contribution_rate = st.slider("Your Contribution Rate (%)", 3, 10, 3) / 100
employer_contribution_rate = st.slider("Employer Contribution Rate (%)", 3, 10, 3) / 100
investment_years = st.slider("Investment Period (Years)", 5, 40, 20)

govt_contribution = 521  # Max annual government contribution

# Monthly contributions
monthly_employee = (income * contribution_rate) / 12
monthly_employer = (income * employer_contribution_rate) / 12

years = list(range(1, investment_years + 1))
results = pd.DataFrame({"Year": years})

# Calculate projections for each provider
for provider, data in providers.items():
    balance = 0
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
    
    results[provider] = yearly_balances

# Display comparison table
st.subheader("Projected KiwiSaver Balances")
st.dataframe(results.style.format("${:,.2f}"))

# Plot growth over time
st.subheader("Balance Growth Over Time")
fig, ax = plt.subplots(figsize=(10, 5))
for provider in providers.keys():
    ax.plot(results["Year"], results[provider], label=provider)
ax.set_xlabel("Years")
ax.set_ylabel("Projected Balance ($)")
ax.set_title("KiwiSaver Growth Comparison")
ax.legend()
ax.grid()
st.pyplot(fig)
