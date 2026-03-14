import ctypes
import sys
import csv
import json
import subprocess
import pandas as pd # Make sure to run 'pip install pandas'
from pathlib import Path
from datetime import datetime

def is_admin():
    """Checks if the script is being run with Administrative privileges."""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def cmd_ok(cmd):
    """Runs a Windows command and checks if the system says 'OK' (exit code 0)."""
    try:
        # We use shell=True to handle the pipes (|) inside your CSV commands
        return subprocess.run(cmd, capture_output=True, text=True, shell=True).returncode == 0
    except Exception:
        return False

# 1. Privilege Check
if not is_admin():
    print("--------------------------------------------------")
    print("❌ ERROR: ADMINISTRATIVE PRIVILEGES REQUIRED")
    print("Please restart your terminal as 'Administrator'.")
    print("--------------------------------------------------")
    sys.exit(1)

# 2. Setup Reporting
Path("reports").mkdir(exist_ok=True)
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# 3. LOAD CONTROLS FROM CSV (Replacing the hard-coded list)
if not Path("controls.csv").exists():
    print("❌ ERROR: controls.csv not found! Please run 'git pull' to get it from GitHub.")
    sys.exit(1)

# Reading the CSV using Pandas
df_controls = pd.read_csv("controls.csv")

audit_results = []
overall_compliant = True

print(f"--- NIST 800-171 Audit Started: {timestamp} ---")
print(f"Loading {len(df_controls)} controls from CSV...\n")

# 4. EXECUTION LOOP
# We now iterate through the rows of your CSV file
for index, row in df_controls.iterrows():
    control_id = row['id']
    name = row['name']
    command = row['command']
    family = row['family']

    is_compliant = cmd_ok(command)
    status = "Compliant" if is_compliant else "Non-Compliant"

    if not is_compliant:
        overall_compliant = False

    # Stores data for the report (including the family name now!)
    audit_results.append({
        "family": family,
        "control_id": control_id,
        "requirement": name,
        "status": status,
        "check_time": timestamp
    })
    
    print(f"[{control_id}] {name}: {status}")

# 5. FINAL STATUS & EXPORT
final_status = "SYSTEM COMPLIANT" if overall_compliant else "SYSTEM NON-COMPLIANT"

# JSON Export
with open("reports/audit_results.json", "w") as jf:
    json.dump({
        "summary": final_status, 
        "scan_time": timestamp,
        "results": audit_results
    }, jf, indent=4)

# CSV Export (This is what app.py will read)
results_df = pd.DataFrame(audit_results)
results_df.to_csv("reports/audit_results.csv", index=False)

print(f"\n--- AUDIT COMPLETE ---")
print(f"Overall Result: {final_status}")
print(f"Reports available in 'reports/' folder.")
