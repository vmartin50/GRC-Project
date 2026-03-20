# AUTO-INSTALLS THE REQUIRED PACKAGES

import subprocess
import sys

required_packages = ["pandas", "streamlit"]

for package in required_packages:
    try:
        __import__(package)
    except ImportError:
        print(f" {package} not found. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# IMPORTS

import sys
import os
import platform
import pandas as pd
import subprocess
import json
import csv
from pathlib import Path
from datetime import datetime

# ADMIN / ROOT CHECK

def is_admin():

    os_name = platform.system().lower()

    if os_name == "windows":
        import ctypes
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False

    elif os_name in ["linux", "darwin"]:
        return os.geteuid() == 0

    return False


if not is_admin():
    print("ERROR: Script must be run with Administrator / root privileges.")
    sys.exit(1)

# SETUP

print("Starting NIST 800-171 Compliance Scan...\n")

Path("reports").mkdir(exist_ok=True)

timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# LOADS CONTROLS

if not Path("controls.csv").exists():
    print("ERROR: controls.csv not found!")
    sys.exit(1)

df_controls = pd.read_csv("controls.csv", quoting=csv.QUOTE_MINIMAL)

print(f"Loaded {len(df_controls)} controls.")

# DETECTS OS

current_os = platform.system().lower()

print(f"Detected Operating System: {current_os}\n")

# RESULTS STORAGE

audit_results = []

# EXECUTION LOOP

for index, row in df_controls.iterrows():

    control_id = row["id"]
    control_name = row["name"]
    family = row["family"]

    # Select command based on OS
    if current_os == "windows":
        command = row.get("win_command")

    elif current_os == "darwin":
        command = row.get("mac_command")

    elif current_os == "linux":
        command = row.get("linux_command")

    else:
        command = None

    
    if not command or str(command).lower() == "nan":

        status = "Not Applicable"
        output = "No automated check available"

    else:

        try:

            process = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True
            )

            output = process.stdout.strip()

            if process.returncode == 0:
                status = "Compliant"
            else:
                status = "Non-Compliant"

        except Exception as e:

            status = "Error"
            output = str(e)

    audit_results.append({

        "family": family,
        "control_id": control_id,
        "requirement": control_name,
        "status": status,
        "output": output,
        "check_time": timestamp

    })

    print(f"[{control_id}] {control_name} → {status}")

# SAVES CSV REPORT

results_df = pd.DataFrame(audit_results)

csv_path = "reports/audit_results.csv"

results_df.to_csv(csv_path, index=False)

print(f"\nCSV report saved: {csv_path}")

# SAVES JSON REPORT

json_path = "reports/audit_results.json"

with open(json_path, "w") as jf:

    json.dump(
        {
            "scan_time": timestamp,
            "results": audit_results
        },
        jf,
        indent=4
    )

print(f"JSON report saved: {json_path}")

# SUMMARY

total = len(results_df)
passed = len(results_df[results_df["status"] == "Compliant"])
failed = len(results_df[results_df["status"] == "Non-Compliant"])

print("\n-----------------------------")
print("SCAN SUMMARY")
print("-----------------------------")
print(f"Total Controls: {total}")
print(f"Compliant: {passed}")
print(f"Non-Compliant: {failed}")
print("-----------------------------")

print("\n NIST 800-171 Compliance Scan Complete.")
print("Reports saved in /reports folder.")
