# NIST 800-171 Automated Compliance Scanner

An automated compliance scanning tool designed to audit Windows systems against **NIST 800-171** security controls. This project uses a Python-based engine to execute system checks and a Streamlit dashboard to visualize the compliance status in real-time.

---

## Overview

This tool bridges the gap between complex security requirements and actionable data. It reads a library of security controls from a CSV file, queries the Windows environment (Registry, PowerShell, and CMD), and generates a structured report.

### Key Features

- **Data-Driven:** Easily add or edit controls by updating `controls.csv` without touching the code.
- **Automated Scanning:** Runs deep-system checks via `scanner.py`.
- **Visual Analytics:** Interactive dashboard via `app.py` for executive and technical reviews.
- **Multi-Format Reporting:** Generates results in both `.csv` and `.json`.

---

## Installation & Setup

### 1. Prerequisites

- **Windows 10/11** (Pro or Enterprise recommended for full feature support)
- **Python 3.10+**
- **Administrator Privileges** (required to query security logs and registry keys)

### 2. Clone the Repository

Open your terminal and run:

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
cd YOUR_REPO_NAME 
```

---


### 3. Install Dependencies

Open your terminal and run:

```bash
pip install pandas streamlit
```

---

## How to Use

### Step 1: Run the Audit

Open your terminal (**PowerShell** or **CMD**) as Administrator and execute:

```bash
python scanner.py
```

The script will loop through all controls in `controls.csv` and create a `reports/` folder containing your results.

---

### Step 2: Launch the Dashboard

Run the Streamlit application to visualize your data:

```bash
streamlit run app.py
```

---

## Project Structure

```
project-folder/
│
├── scanner.py        # The engine that executes Windows commands
├── app.py            # Streamlit dashboard UI
├── controls.csv      # Library containing the NIST families, IDs, and commands
│
└── reports/          # Output folder
    ├── audit_results.csv
    └── audit_results.json
```

---

## Security Controls Audited

The current version audits **20+ core controls** across these NIST families:

- **Access Control (AC)**
- **Identification & Authentication (IA)**
- **Configuration Management (CM)**
- **System & Information Integrity (SI)**
- **Media Protection (MP)**

---

## Disclaimer

This tool is intended for **educational and auditing purposes**. It provides a technical snapshot of system settings but does **not guarantee full legal compliance** with NIST 800-171 standards.








