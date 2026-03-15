import streamlit as st
import pandas as pd
import os
import subprocess
import json

st.set_page_config(page_title="NIST 800-171 Dashboard", layout="wide")

st.title("🛡️ NIST 800-171 Compliance Dashboard")

RESULTS_FILE = "reports/audit_results.csv"
JSON_FILE = "reports/audit_results.json"

# -----------------------------
# RUN AUDIT BUTTON
# -----------------------------
if st.button("Run NIST Audit"):
    with st.spinner("Running system audit..."):
        # Use python3 when needed (Linux/macOS)
        python_cmd = "python3" if os.name != "nt" else "python"
        subprocess.run([python_cmd, "scanner.py"])
    st.success("Audit completed!")
    st.rerun()

st.divider()

# -----------------------------
# CHECK IF RESULTS EXIST
# -----------------------------
if os.path.exists(RESULTS_FILE):

    df = pd.read_csv(RESULTS_FILE)

    # -----------------------------
    # METRICS
    # -----------------------------
    total = len(df)
    compliant = (df["status"] == "Compliant").sum()
    non_compliant = (df["status"] == "Non-Compliant").sum()
    not_applicable = (df["status"] == "Not Applicable").sum()

    score = (compliant / total) * 100 if total > 0 else 0

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Compliance Score", f"{score:.1f}%")
    c2.metric("Compliant", compliant)
    c3.metric("Non-Compliant", non_compliant)
    c4.metric("Not Applicable", not_applicable)

    st.divider()

    # -----------------------------
    # COMPLIANCE CHART
    # -----------------------------
    st.subheader("Compliance Overview")

    status_counts = df["status"].value_counts()

    st.bar_chart(status_counts)

    st.divider()

    # -----------------------------
    # SHOW FULL CONTROL TABLE
    # -----------------------------
    st.subheader(f"All Scanned Controls ({total})")

    def style_status(val):
        if val == "Compliant":
            return "color: green; font-weight: bold"
        elif val == "Non-Compliant":
            return "color: red; font-weight: bold"
        else:
            return "color: gray; font-weight: bold"

    st.dataframe(
        df.style.applymap(style_status, subset=["status"]),
        use_container_width=True,
        hide_index=True
    )

    st.divider()

else:
    st.warning("⚠️ No audit data found. Click 'Run NIST Audit' to start a scan.")

# -----------------------------
# JSON REPORT VIEWER
# -----------------------------
st.subheader("Raw JSON Report")

if st.button("View JSON Report"):
    if os.path.exists(JSON_FILE):
        with open(JSON_FILE) as f:
            json_data = json.load(f)

        st.json(json_data)
    else:
        st.info("JSON report not found.")

    # -----------------------------
    # LAST SCAN INFO
    # -----------------------------
    if os.path.exists(RESULTS_FILE):
        df = pd.read_csv(RESULTS_FILE)
        if not df.empty:
            last_scan = df["check_time"].iloc[0]
            st.sidebar.info(f"Last Scan: {last_scan}")
