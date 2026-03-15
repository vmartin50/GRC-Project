import sys
import platform
import pandas as pd
import subprocess
import json
import csv
from pathlib import Path
from datetime import datetime

# ------------------------------
# ADMIN / ROOT CHECK
# ------------------------------
def is_admin():
    os_name = platform.system().lower()

    if os_name == "windows":
        import ctypes
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False

    elif os_name in ["linux", "darwin"]:
        # UID 0 = root
        return os.geteuid() == 0

    return False


if not is_admin():
    print("❌ ERROR: Script must be run with Administrator / root privileges.")
    sys.exit(1)

# ------------------------------
# SETUP
# ------------------------------
Path("reports").mkdir(exist_ok=True)
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

if not Path("controls.csv").exists():
    print("❌ ERROR: controls.csv not found!")
    sys.exit(1)

df_controls = pd.read_csv("controls.csv", quoting=csv.QUOTE_MINIMAL)

print("DEBUG: Controls Loaded")
print(df_controls)
print("Total Controls:", len(df_controls))

audit_results = []

current_os = platform.system().lower()
print(f"Detected OS: {current_os}")
print(f"Starting NIST Audit of {len(df_controls)} controls...")

# ------------------------------
# EXECUTION LOOP
# ------------------------------
for index, row in df_controls.iterrows():

    # Select correct command for OS
    if current_os == "windows":
        command = row["win_command"]
    elif current_os == "darwin":
        command = row["mac_command"]
    elif current_os == "linux":
        command = row["linux_command"]
    else:
        command = None

    if not command or str(command).lower() == "nan":
        status = "Not Applicable"
    else:
        process = subprocess.run(command, shell=True, capture_output=True, text=True)
        status = "Compliant" if process.returncode == 0 else "Non-Compliant"

    audit_results.append({
        "family": row["family"],
        "control_id": row["id"],
        "requirement": row["name"],
        "status": status,
        "check_time": timestamp
    })

    print(f"[{row['id']}] {row['name']}: {status}")

# ------------------------------
# SAVE REPORTS
# ------------------------------
results_df = pd.DataFrame(audit_results)
results_df.to_csv("reports/audit_results.csv", index=False)

with open("reports/audit_results.json", "w") as jf:
    json.dump({"scan_time": timestamp, "results": audit_results}, jf, indent=4)

print("\n✅ Audit Complete!")
print(f"Created a report with {len(results_df)} controls in the /reports folder.")

