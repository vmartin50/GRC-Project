from pathlib import Path
import csv, subprocess, json

def cmd_ok(cmd):
    try:
        return subprocess.run(cmd, capture_output=True, text=True).returncode == 0
    except Exception:
        return False

Path("policies").mkdir(exist_ok=True)
# Add whatever policies you want here to run it against
Path("policies/policy.md")write_text( " " ) 

with open("./dummy.csv", "w", newline="", encoding="utf-8" as f: 
        w = csv,writer(f); w.writerow(["Control", "Name", "Validation"]); w.writerows(policy_rows)

