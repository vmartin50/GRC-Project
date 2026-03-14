import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="NIST 800-171 Dashboard", layout="wide")

st.title("🛡️ NIST 800-171 Compliance Dashboard")

RESULTS_FILE = 'reports/audit_results.csv'

if os.path.exists(RESULTS_FILE):
    # Read the data
    df = pd.read_csv(RESULTS_FILE)

    # Metric calculations
    total = len(df)
    passed = len(df[df['status'] == 'Compliant'])
    failed = total - passed
    score = (passed / total) * 100

    # Display Metrics
    c1, c2, c3 = st.columns(3)
    c1.metric("Compliance Score", f"{score:.1f}%")
    c2.metric("Passed", passed)
    c3.metric("Failed", failed, delta_color="inverse")

    st.divider()

    # --- SHOW ALL DATA ---
    st.subheader(f"All Scanned Controls ({total})")
    
    # Apply color styling
    def style_status(val):
        color = 'green' if val == 'Compliant' else 'red'
        return f'color: {color}; font-weight: bold'

    # Displaying the full table
    st.dataframe(
        df.style.applymap(style_status, subset=['status']),
        use_container_width=True,
        hide_index=True
    )

else:
    st.warning("No audit data found. Please run 'python scanner.py' first.")

if st.button("Force Refresh Data"):
    st.cache_data.clear()
    st.rerun()

# 4. Footer
st.sidebar.info(f"Last Scan: {df['check_time'].iloc[0] if os.path.exists(RESULTS_FILE) else 'N/A'}")
