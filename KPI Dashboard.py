import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="KPI Dashboard", layout="wide")

st.title("📊 KPI Dashboard")

# =========================================
# UPLOAD CSV
# =========================================

uploaded_file = st.sidebar.file_uploader("Upload KPI CSV", type=["csv"])

if uploaded_file is None:
    st.warning("Please upload a CSV file to continue.")
    st.stop()

df = pd.read_csv(uploaded_file)

# =========================================
# VALIDATION
# =========================================

required_columns = ["site", "date", "availability", "traffic", "cssr"]

missing_cols = [col for col in required_columns if col not in df.columns]

if missing_cols:
    st.error(f"Missing required columns: {missing_cols}")
    st.stop()

# Convert date column
df["date"] = pd.to_datetime(df["date"])

# =========================================
# TABS
# =========================================

tab1, tab2 = st.tabs(["📋 Overview", "🏢 Filter by Site"])

# =========================================
# TAB 1 – OVERVIEW
# =========================================

with tab1:
    st.subheader("Overall KPI Summary")

    col1, col2, col3 = st.columns(3)

    col1.metric("Avg Availability", f"{df['availability'].mean():.2f}%")
    col2.metric("Avg Traffic", f"{df['traffic'].mean():.2f}")
    col3.metric("Avg CSSR", f"{df['cssr'].mean():.2f}%")

    st.divider()

    st.subheader("Availability Trend")

    daily = df.groupby("date")["availability"].mean()

    fig, ax = plt.subplots()
    ax.plot(daily.index, daily.values)
    ax.set_xlabel("Date")
    ax.set_ylabel("Availability (%)")
    st.pyplot(fig)

# =========================================
# TAB 2 – FILTER BY SITE
# =========================================

# Clean site column
df["site"] = df["site"].astype(str)

# Drop missing
df = df[df["site"].notna()]

# Generate site list
site_list = sorted(df["site"].unique())

# =========================================
# DATA PREVIEW
# =========================================

with st.expander("🔍 Preview Data"):

    st.dataframe(df)


