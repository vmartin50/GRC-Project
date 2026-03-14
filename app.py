import streamlit as st
import pandas as pd
import os

# 1. Page Configuration
st.set_page_config(page_title="NIST 800-171 Compliance Dashboard", layout="wide")

# 2. Header Section
st.title("🛡️ NIST 800-171 Automated Auditor")
st.markdown("This dashboard displays the real-time compliance status of your Windows system based on the latest scan.")

# 3. Load Data
RESULTS_FILE = 'reports/audit_results.csv'

if os.path.exists(RESULTS_FILE):
    df = pd.read_csv(RESULTS_FILE)

    # --- TOP LEVEL METRICS ---
    total_checks = len(df)
    passed = len(df[df['status'] == 'Compliant'])
    failed = total_checks - passed
    score = (passed / total_checks) * 100

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Compliance Score", f"{score:.1f}%")
    col2.metric("Total Controls", total_checks)
    col3.metric("Pass", passed)
    col4.metric("Fail", failed, delta_color="inverse")

    st.divider()

    # --- FILTERING & DATA TABLE ---
    st.subheader("📋 Detailed Audit Findings")
    
    # Create two columns for the filter and the search
    f_col1, f_col2 = st.columns([1, 1])
    with f_col1:
        family_choice = st.multiselect("Filter by NIST Family:", options=df['family'].unique(), default=df['family'].unique())
    with f_col2:
        status_choice = st.radio("Status Filter:", ["All", "Compliant", "Non-Compliant"], horizontal=True)

    # Apply Filters
    filtered_df = df[df['family'].isin(family_choice)]
    if status_choice != "All":
        filtered_df = filtered_df[filtered_df['status'] == status_choice]

    # Color the status column (Green for Pass, Red for Fail)
    def color_status(val):
        color = '#2ecc71' if val == 'Compliant' else '#e74c3c'
        return f'background-color: {color}; color: white; font-weight: bold'

    st.dataframe(
        filtered_df.style.applymap(color_status, subset=['status']),
        use_container_width=True,
        hide_index=True
    )

    # --- VISUALIZATIONS ---
    st.divider()
    st.subheader("📊 Compliance Distribution")
    
    v_col1, v_col2 = st.columns(2)
    
    with v_col1:
        st.write("**Pass/Fail Count**")
        st.bar_chart(df['status'].value_counts())
        
    with v_col2:
        st.write("**Controls by Family**")
        family_counts = df.groupby('family')['status'].value_counts().unstack().fillna(0)
        st.bar_chart(family_counts)

else:
    # Handle the case where the user hasn't run the scanner yet
    st.warning("⚠️ No audit data found in `reports/audit_results.csv`.")
    st.info("Please run `python scanner.py` as Administrator to generate your results.")
    if st.button("I've run the scanner - Refresh Data"):
        st.rerun()

# 4. Footer
st.sidebar.info(f"Last Scan: {df['check_time'].iloc[0] if os.path.exists(RESULTS_FILE) else 'N/A'}")
