import streamlit as st
import pandas as pd
import os
import subprocess
import json

st.markdown("""
<style>

html, body, [class*="css"]  {
    background-color: #0e1117 !important;
    color: #e0e0e0 !important;
    font-family: "Inter", sans-serif;
}

/* Title */
h1 {
    color: #ffffff !important;
    text-align: center;
    font-weight: 800;
    letter-spacing: -1px;
    margin-bottom: 10px;
}

/* Section headers */
h2, h3 {
    color: #c9d1d9 !important;
    font-weight: 700;
    margin-top: 30px;
}

/* Metric cards */
div[data-testid="metric-container"] {
    background: #161b22;
    border: 1px solid #30363d;
    border-radius: 12px;
    padding: 20px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.4);
}

/* Buttons */
.stButton>button {
    background-color: #238636 !important;
    color: white !important;
    border-radius: 8px;
    border: 1px solid #2ea043;
    font-weight: 600;
    padding: 0.6rem 1.2rem;
}

.stButton>button:hover {
    background-color: #2ea043 !important;
    border-color: #3fb950;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #161b22 !important;
    border-right: 1px solid #30363d;
}

/* Dataframe styling */
.dataframe {
    color: #e0e0e0 !important;
}

.dataframe th {
    background-color: #21262d !important;
    color: #e6edf3 !important;
}

.dataframe td {
    background-color: #0e1117 !important;
    color: #e6edf3 !important;
}

/* Scrollbars */
::-webkit-scrollbar {
    width: 8px;
}
::-webkit-scrollbar-thumb {
    background: #30363d;
    border-radius: 4px;
}
::-webkit-scrollbar-thumb:hover {
    background: #484f58;
}

</style>
""", unsafe_allow_html=True)



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
