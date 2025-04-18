
import streamlit as st
import pandas as pd
import plotly.express as px

# Load cleaned data
df = pd.read_csv("Large Cap Cleaned.csv")

# Sidebar Filters
st.sidebar.title("Filters")

# SEBI Classification Filter
with st.sidebar.expander("SEBI Classification Filter", expanded=True):
    sebi_classes = df["SEBI Classification"].unique().tolist()
    selected_sebi_class = st.multiselect("Select SEBI Classification", sebi_classes, default=sebi_classes)

# Filter by Performance (Top N Funds) with additional options for 3 and All
with st.sidebar.expander("Performance Filter (Top N Funds)", expanded=True):
    performance_filter = st.selectbox("Filter top N funds based on 1Y returns", options=[3, 5, 10, 15, 20, "All"], index=2)  # Default 10 funds
    if performance_filter == "All":
        # When "All" is selected, display all funds without performance filter
        top_performers = df[df["SEBI Classification"].isin(selected_sebi_class)]
    else:
        # Sort the data by 1Y returns and select top N
        top_performers = df[df["SEBI Classification"].isin(selected_sebi_class)].sort_values(by="1Y", ascending=False).head(performance_filter)

# Fund selection via searchable multiselect dropdown
with st.sidebar.expander("Fund Selection", expanded=True):
    fund_names = top_performers["Fund Name"].unique().tolist()
    selected_funds = st.multiselect("Select Funds:", fund_names, default=fund_names[:performance_filter])  # Default to selected top N funds

# Main content layout
st.title("Large Cap Mutual Fund Dashboard")

# Table at the top - Sorted by 1Y returns (or selected metric)
st.subheader("Selected Funds Overview")
st.markdown("<small><i>Data is sorted by 1-year returns.</i></small>", unsafe_allow_html=True)

# Display the 1Y, 3Y, and 5Y returns in the table and sort by 1Y returns
fund_table = top_performers[top_performers["Fund Name"].isin(selected_funds)][
    ["Fund Name", "NAV", "AUM Cr.", "TER", "Sharpe", "Sortino", "St Dev", "1Y", "3Y", "5Y"]
]
fund_table_sorted = fund_table.sort_values(by="1Y", ascending=False)  # Sort by 1Y returns

# Adjust the index to start from 1
fund_table_sorted.index = range(1, len(fund_table_sorted) + 1)

# Hide the index column (row numbers) in the table
st.dataframe(fund_table_sorted)

# Add a horizontal line to demarcate the sections
st.markdown("---")

# Dropdown for period selection (1Y, 3Y, 5Y)
period = st.selectbox("Select Return Period", options=["1Y", "3Y", "5Y"], index=0)

# Return Comparison Section with Dynamic Period Selection
st.subheader(f"Return Comparison ({period})")

# Sort funds by the selected period (Descending Order)
chart_df = top_performers[top_performers["Fund Name"].isin(selected_funds)][["Fund Name", period]].dropna()
chart_df_sorted = chart_df.sort_values(by=period, ascending=False)

if not chart_df_sorted.empty:
    # Create Plotly bar chart based on selected period
    fig = px.bar(
        chart_df_sorted,
        x="Fund Name",
        y=period,
        color="Fund Name",
        title=f"{period} Return Comparison",
        labels={period: "Return (%)", "Fund Name": "Fund"},
        hover_data=["Fund Name", period],  # Hover data shows detailed info
    )  # Rotate labels for better readability
    fig.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig)
else:
    st.info("No data to display for selected funds.")

# Add a horizontal line to demarcate the sections
st.markdown("---")

# Dropdown for selecting Risk Metric (Sharpe, Sortino, or St Dev)
metric = st.selectbox("Select Risk Metric", options=["Sharpe", "Sortino", "St Dev"], index=0)

# Display the corresponding info for the selected metric
if metric == "Sharpe":
    st.markdown(
        "<small><i>Sharpe Ratio: Measures the risk-adjusted return of a fund. A higher Sharpe ratio indicates a better return for the level of risk taken.</i></small>",
        unsafe_allow_html=True,
    )
elif metric == "Sortino":
    st.markdown(
        "<small><i>Sortino Ratio: A variation of the Sharpe ratio that only considers downside volatility. A higher Sortino ratio is preferred.</i></small>",
        unsafe_allow_html=True,
    )
elif metric == "St Dev":
    st.markdown(
        "<small><i>Standard Deviation: Measures the volatility of a fund’s returns. A higher standard deviation indicates higher volatility and risk.</i></small>",
        unsafe_allow_html=True,
    )

# Simple Bar Chart for Selected Metric (without "Bar Chart" term)
st.subheader(f"{metric} Comparison")

# Sort funds by the selected metric (Descending Order)
metrics_df = top_performers[top_performers["Fund Name"].isin(selected_funds)][["Fund Name", "Sharpe", "Sortino", "St Dev"]].dropna()
metrics_df_sorted = metrics_df.sort_values(by=metric, ascending=False)

# Create a simple bar chart for the selected metric
fig = px.bar(
    metrics_df_sorted,
    x="Fund Name",
    y=metric,
    title=f"{metric} Comparison",
    labels={"Fund Name": "Fund", "value": "Raw Value"},
    color="Fund Name",
)

# Show plot
st.plotly_chart(fig)

# Add a horizontal line to demarcate the sections
st.markdown("---")

# Footer with developer info
st.markdown("Interactive MF Dashboard developed by Divanshu Kapoor")


import base64

# Path to the logo file
logo_path = "new_logo.png"  # Logo path

# Add custom CSS for positioning the logo at the bottom-right corner with an off-white background
st.markdown(
    """ 
    <style>
    .logo {
        position: fixed;
        bottom: 10px;
        right: 10px;
        z-index: 9999;
        width: 100px;  # Adjusted size of the logo
        background-color: #f8f8f8;  # Off-white background for better visibility
        padding: 5px;
        border-radius: 10px;  # Rounded corners for the background
    }
    </style>
    """, 
    unsafe_allow_html=True
)

# Display the logo
st.markdown(f'<img class="logo" src="data:image/webp;base64,{base64.b64encode(open(logo_path, "rb").read()).decode()}" />', unsafe_allow_html=True)
