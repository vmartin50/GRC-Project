# NIST 800-171 Automated Compliance Scanner

An automated compliance scanning tool designed to audit systems against **NIST 800-171** security controls. This project uses a Python-based engine to execute system checks and a Streamlit dashboard to visualize the compliance status in real-time.

The scanner supports **Windows, macOS, and Linux**, automatically runs security checks for each NIST control, and generates **CSV and JSON reports** summarizing compliance status.  

---

## The Problem

Organizations handling sensitive data often struggle with:

- Ensuring compliance with NIST SP 800-171  
- Tracking hundreds of security controls manually  
- Generating reports and POA&M (Plan of Action & Milestones) for failed controls  
- Visualizing compliance results in an intuitive way  

Manual auditing is **time-consuming, error-prone, and inconsistent**.  

This tool automates these tasks, providing **fast, repeatable, and accurate compliance assessments**.

---

## Overview

The `scanner.py` script performs the following steps:

1. **Package Setup**  
   Automatically installs missing Python packages (`pandas` and `streamlit`) for ease of use.

2. **Administrator/Root Check**  
   Ensures the script is run with proper privileges to perform system-level checks.

3. **Load Controls**  
   Reads `controls.csv`, which contains all NIST SP 800-171 controls with **OS-specific commands**.

4. **Operating System Detection**  
   Determines the running OS (Windows/macOS/Linux) and selects appropriate commands for each control.

5. **Execute Security Checks**  
   Iterates through all controls, runs commands, and determines compliance:
   - **Compliant** if the command succeeds  
   - **Non-Compliant** if the command fails  
   - **Not Applicable** if no automated check is available  

6. **Generate Reports**  
   Saves results to:
   - `reports/audit_results.csv` (tabular format)  
   - `reports/audit_results.json` (structured format)  

7. **Summary**  
   Prints a terminal summary of:
   - Total controls  
   - Compliant vs Non-Compliant controls  

8. **POA&M Generation**  
   Automatically generates a Plan of Action & Milestones for any non-compliant controls in:
   - `reports/POAM_Report.csv`  

9. **Streamlit Dashboard**  
   Launch the dashboard for interactive visualization and downloading of POA&M.

---

## Features

- **Cross-platform:** Supports Windows, macOS, and Linux  
- **Automatic dependency installation** (`pandas` and `streamlit`)  
- **Audit reporting:** Generates CSV and JSON reports  
- **POA&M Ready:** Automatic Plan of Action & Milestones for failed controls  
- **User-friendly:** Prints real-time scan status and summary  

---

## Requirements

- Python 3.8+  
- Administrator/Root privileges to run system-level commands  

No manual installation of dependencies is required — the script handles it automatically.

---

## Quick Start

Follow these steps to run the NIST 800-171 Compliance Scanner:

### Clone the Repository

```bash
git clone https://github.com/vmartin50/GRC-project.git
cd GRC-project
```

### Run the Scanner

Open your terminal (**PowerShell** or **CMD**) as Administrator and execute:

```bash
python scanner.py
```

The script will:

- Install required packages if missing
- Detect your operating system
- Perform compliance checks for all NIST 800-171 controls
- Generate CSV and JSON reports in `reports/`
- Generate POA&M if any controls fail


---

## Launch Streamlit Dashboard

Launch the interactive dashboard:

```bash
streamlit run app.py
```

The dashboard allows you to:

- View live compliance scores
- Filter controls by family or status
- Download the POA&M for auditors


---

## Project Structure

```
project-folder/
│
├── scanner.py        # The engine that executes Windows/Mac/Linux commands
├── app.py            # Streamlit dashboard UI
├── controls.csv      # Library containing the NIST families, IDs, and commands
│
└── reports/          # Output folder
    ├── audit_results.csv
    └── audit_results.json
    └── reports/POAM_Report.csv
```


---

## Disclaimer

This tool is intended for **educational and auditing purposes**. It provides a technical snapshot of system settings but does **not guarantee full legal compliance** with NIST 800-171 standards.








