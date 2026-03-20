import streamlit as st
import pandas as pd
import os

# ------------------------------
# PAGE CONFIG
# ------------------------------

st.set_page_config(
    page_title="NIST 800-171 Compliance Dashboard",
    layout="wide"
)

st.title("NIST 800-171 Compliance Dashboard")

RESULTS_FILE = "reports/audit_results.csv"

# ------------------------------
# POA&M GENERATOR
# ------------------------------

def generate_poam(df):

    poam = df[df["status"] == "Non-Compliant"].copy()

    if len(poam) == 0:
        return pd.DataFrame()

    poam["Weakness Description"] = "Control requirement not satisfied"
    poam["Remediation Plan"] = "Implement required security configuration or policy"
    poam["Milestone Date"] = "TBD"
    poam["Responsible Party"] = "IT Security Team"

    return poam


# ------------------------------
# LOAD RESULTS
# ------------------------------

if not os.path.exists(RESULTS_FILE):
    st.error("No audit results found. Run scanner.py first.")
    st.stop()

df = pd.read_csv(RESULTS_FILE)

# ------------------------------
# METRICS
# ------------------------------

total_controls = len(df)
passed = len(df[df["status"] == "Compliant"])
failed = len(df[df["status"] == "Non-Compliant"])
not_applicable = len(df[df["status"] == "Not Applicable"])

compliance_score = round((passed / total_controls) * 100, 2)

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Controls", total_controls)
col2.metric("Compliant", passed)
col3.metric("Non-Compliant", failed)
col4.metric("Compliance Score", f"{compliance_score}%")

st.progress(compliance_score / 100)

# ------------------------------
# CONTROL RESULTS TABLE
# ------------------------------

st.subheader("Control Assessment Results")

st.dataframe(
    df,
    use_container_width=True
)

# ------------------------------
# FAMILY BREAKDOWN
# ------------------------------

st.subheader("Compliance by Control Family")

family_summary = df.groupby(["family", "status"]).size().unstack(fill_value=0)

st.dataframe(family_summary)

# ------------------------------
# POA&M SECTION
# ------------------------------

st.subheader("Plan of Action & Milestones (POA&M)")

poam = generate_poam(df)

if len(poam) == 0:

    st.success("No failed controls. No POA&M required.")

else:

    st.dataframe(poam, use_container_width=True)

    poam_csv = poam.to_csv(index=False)

    st.download_button(
        label="Download POA&M Report",
        data=poam_csv,
        file_name="POAM_Report.csv",
        mime="text/csv"
    )

# ------------------------------
# FOOTER
# ------------------------------

st.markdown("---")
st.caption("NIST 800-171 Automated Compliance Dashboard")
