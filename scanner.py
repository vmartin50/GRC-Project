import ctypes
import sys
import pandas as pd
import subprocess
from pathlib import Path
from datetime import datetime

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if not is_admin():
    print("❌ ERROR: Please run as Administrator.")
    sys.exit(1)

# Initialize paths and data
Path("reports").mkdir(exist_ok=True)
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Load your 110+ controls
if not Path("controls.csv").exists():
    print("❌ ERROR: controls.csv not found!")
    sys.exit(1)

df_controls = pd.read_csv("controls.csv")
audit_results = []

print(f"🚀 Starting NIST Audit: {timestamp}")

# --- THE CORRECTED LOOP ---
for index, row in df_controls.iterrows():
    # 1. Run the command
    process = subprocess.run(row['command'], shell=True, capture_output=True, text=True)
    
    # 2. Determine status
    status = "Compliant" if process.returncode == 0 else "Non-Compliant"
    
    # 3. APPEND INSIDE THE LOOP (Crucial fix!)
    audit_results.append({
        "family": row['family'],
        "control_id": row['id'],
        "name": row['name'],
        "status": status,
        "check_time": timestamp
    })
    
    print(f"Checked [{row['id']}]: {status}")

# --- SAVE AFTER LOOP FINISHES ---
results_df = pd.DataFrame(audit_results)
results_df.to_csv("reports/audit_results.csv", index=False)
print(f"\n✅ Done! {len(results_df)} controls processed.")
