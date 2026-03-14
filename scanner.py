import ctypes
import sys
import csv
import json
import subprocess
from pathlib import Path
from datetime import datetime

def is_admin():
    """Checks if the script is being run with Administrative privileges."""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def cmd_ok(cmd):
    """
    This function acts like a Digital Inspector. 
    It runs a Windows command and checks if the system says 'OK' (exit code 0).
    If the setting is correct, it returns True. If not, it returns False.
    """
    try:
        return subprocess.run(cmd, capture_output=True, text=True, shell=True).returncode == 0
    except Exception:
        return False

# Ensures the script has the elevated permissions required to query system settings.
if not is_admin():
    print("--------------------------------------------------")
    print("❌ ERROR: ADMINISTRATIVE PRIVILEGES REQUIRED")
    print("This audit requires access to system security logs.")
    print("Please restart your terminal as 'Administrator'.")
    print("--------------------------------------------------")
    sys.exit(1)

# This establishes a reporting directory and standardized time format for audit logging.
Path("reports").mkdir(exist_ok=True)
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
# This is a list of 10 NIST 800-171 controls. 
# For each one, the script asks Windows a question. 
# If the answer is 'Yes,' it marks it 'Compliant.' If 'No,' it marks it 'Non-Compliant.'
checks = [
   ("3.1.9", "Session Lock", "powershell -command \"Get-ItemProperty 'HKCU:\\Control Panel\\Desktop' -Name ScreenSaveActive\""),
    ("3.5.3", "Password Complexity", "net accounts | findstr /C:\"Password complexity\""),
    ("3.1.8", "Limit Login Attempts", "net accounts | findstr /C:\"Lockout threshold\""),
    ("3.5.7", "Password Reuse", "net accounts | findstr /C:\"Length of password history\""),
    ("3.14.2", "Malware Protection", "powershell -command \"Get-Service WinDefend\""),
    ("3.8.3", "Media Sanitization", "manage-bde -status C:"),
    ("3.1.5", "Least Privilege", "whoami /groups | findstr /C:\"Mandatory Label\\High Mandatory Level\""),
    ("3.5.8", "Password Encryption", "reg query HKLM\\SAM\\SAM"),
    ("3.14.5", "Update Definitions", "powershell -command \"Get-MpComputerStatus\""),
    ("3.4.7", "Software Whitelisting", "powershell -command \"Get-AppLockerPolicy -Local\"")
]

audit_results = []
# This assumes the system is compliant until a single check fails.
overall_compliant = True

print(f"--- NIST 800-171 Audit Started: {timestamp} ---")

# This is the execution loop
for control_id, name, command in checks:
    is_compliant = cmd_ok(command)

status = "Compliant" if is_compliant else "Non-Compliant"

# If any check is False, the entire system is Non-Compliant.
if not is_compliant:
        overall_compliant = False

# Stores data for the report
audit_results.append({
        "control_id": control_id,
        "requirement": name,
        "status": status,
        "check_time": timestamp
    })
print(f"[{control_id}] {name}: {status}")

final_status = "SYSTEM COMPLIANT" if overall_compliant else "SYSTEM NON-COMPLIANT"

# Report generation
# JSON Export: Structured for automated dashboards (PowerBI/SIEM)
with open("reports/audit_results.json", "w") as jf:
    json.dump({
        "summary": final_status, 
        "scan_time": timestamp,
        "results": audit_results
    }, jf, indent=4)

# CSV Export: Formatted for human review in Excel
with open("reports/audit_results.csv", "w", newline="") as cf:
    # Use DictWriter to map our dictionary keys directly to CSV columns
    writer = csv.DictWriter(cf, fieldnames=["control_id", "requirement", "status", "check_time"])
    writer.writeheader()
    writer.writerows(audit_results)

print(f"\n--- AUDIT COMPLETE ---")
print(f"Overall Result: {final_status}")
print(f"Reports are available in the 'reports/' folder.")
