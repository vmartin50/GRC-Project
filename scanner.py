import ctypes
import sys
import pandas as pd
import subprocess
import json
import csv
from pathlib import Path
from datetime import datetime

# ADMIN CHECK
def is_admin():
    """Verifies the script has permission to check system security settings."""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

# Stops the script immediately if not run as Administrator
if not is_admin():
    print("❌ ERROR: Please run as Administrator.")
    sys.exit(1)

# Create a 'reports' folder if it doesn't already exist
Path("reports").mkdir(exist_ok=True)
# Record the exact time this scan started
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# --- STEP 1: LOAD THE MASTER LIBRARY ---
# Ensure the controls.csv file we created on GitHub is present
if not Path("controls.csv").exists():
    print("❌ ERROR: controls.csv not found! Run 'git pull' first.")
    sys.exit(1)

# Read the CSV into a Pandas DataFrame 
df_controls = pd.read_csv("controls.csv", quoting=csv.QUOTE_MINIMAL)

print("DEBUG: Controls Loaded")
print(df_controls)
print("Total Controls:", len(df_controls))

# --- STEP 2: INITIALIZE THE RESULTS LIST ---
# This acts as a 'bucket' that will hold every single check result.
audit_results = []

print(f"🚀 Starting NIST Audit of {len(df_controls)} controls...")

# --- STEP 3: THE EXECUTION LOOP ---
# This loop goes through the CSV row by row (3.1.1, then 3.1.2, etc.)
for index, row in df_controls.iterrows():
    
    # Run the Windows command listed in the CSV
    # shell=True allows us to use 'pipes' like | findstr
    process = subprocess.run(row['command'], shell=True, capture_output=True, text=True)
    
    # If the command finishes with exit code 0, it passed.
    status = "Compliant" if process.returncode == 0 else "Non-Compliant"
    
  
    audit_results.append({
        "family": row['family'],
        "control_id": row['id'],
        "requirement": row['name'],
        "status": status,
        "check_time": timestamp
    })
    
    # Print progress to the terminal so we know it's working
    print(f"[{row['id']}] {row['name']}: {status}")

# --- STEP 4: SAVE THE REPORT ---
results_df = pd.DataFrame(audit_results)

# Save the full list of results to one file
results_df.to_csv("reports/audit_results.csv", index=False)

# Save a JSON version for other apps to use
with open("reports/audit_results.json", "w") as jf:
    json.dump({"scan_time": timestamp, "results": audit_results}, jf, indent=4)

print(f"\n✅ Audit Complete!")
print(f"Created a report with {len(results_df)} controls in the /reports folder.")
