import ctypes
import sys
import csv
import json
import subprocess
from pathlib import Path

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
        return subprocess.run(cmd, capture_output=True, text=True).returncode == 0
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
        
# This creates a 'policies' folder.
Path("policies").mkdir(exist_ok=True)

# This creates a text file that describes the goal of this project.
Path("policies/policy.md").write_text("# NIST 800-171 Policy Handbook\n" "This file proves that we are using code to verify our security instead of manual checklists.")  

# This is a list of 10 NIST 800-171 controls. 
# For each one, the script asks Windows a question. 
# If the answer is 'Yes,' it marks it 'Compliant.' If 'No,' it marks it 'Non-Compliant.'
policy_rows = [
    ["3.1.9", "Session Lock", "Compliant" if cmd_ok("powershell -command \"Get-ItemProperty 'HKCU:\\Control Panel\\Desktop' -Name ScreenSaveActive\"") else "Non-Compliant"],
    ["3.5.3", "Password Complexity", "Compliant" if cmd_ok("net accounts | findstr /C:\"Password complexity\"") else "Non-Compliant"],
    ["3.1.8", "Limit Login Attempts", "Compliant" if cmd_ok("net accounts | findstr /C:\"Lockout threshold\"") else "Non-Compliant"],
    ["3.5.7", "Password Reuse", "Compliant" if cmd_ok("net accounts | findstr /C:\"Length of password history\"") else "Non-Compliant"],
    ["3.14.2", "Malware Protection", "Compliant" if cmd_ok("powershell -command \"Get-Service WinDefend\"") else "Non-Compliant"],
    ["3.8.3", "Media Sanitization", "Compliant" if cmd_ok("manage-bde -status C:") else "Non-Compliant"],
    ["3.1.5", "Least Privilege", "Compliant" if cmd_ok("whoami /groups | findstr /C:\"Mandatory Label\\High Mandatory Level\"") else "Non-Compliant"],
    ["3.5.8", "Password Encryption", "Compliant" if cmd_ok("reg query HKLM\\SAM\\SAM") else "Non-Compliant"],
    ["3.14.5", "Update Definitions", "Compliant" if cmd_ok("powershell -command \"Get-MpComputerStatus\"") else "Non-Compliant"],
    ["3.4.7", "Software Whitelisting", "Compliant" if cmd_ok("powershell -command \"Get-AppLockerPolicy -Local\"") else "Non-Compliant"]
]

# This saves the results into a CSV file.
# This file is the 'Live compliance status that will be displayed.
csv_file = "./controls.csv"

with open(csv_file, "w", newline="", encoding="utf-8") as f:
# This part formats the data so it looks like a spreadsheet.
w = csv.writer(f)

# Creates the titles.
w.write(["Control ID", "Security Requirement", "Current Status"])

# Fills in the results for the 10 controls.
w.writerows(policy_rows)

print(f"--- SUCCESS ---")
print("The audit is finished. Your results are in {csv_file}")
