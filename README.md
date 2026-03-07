# NIST 800-171 Automated Compliance Scanner

## Project Overview  
This project demostrates **"Compliance-as-Code."** It uses a Python-based scanner to automatically audit a Windows system against 10 specific security controls from the **NIST 800-171** framework.

---

## The Problem
In many organizations, security auditing is a slow, manual process. IT teams often rely on checklists and "best guesses" to determine if their workstations are secure. This leads to:
* **Human Error:** Missing critical settings during manual checks.
* **Lack of Evidence:** No timestamped proof for auditors that a system was actually secure.
* **Consistency Gaps:** Different machines having different security levels

---

## The Solution
Instead of checking settings by hand, this tool scans the system to provide an instant "Compliant" or "Non-Compliant" report. This bridges the gap between our security goals and our actual settings, verifying that our computer configurations strictly follow our written security requirements. 

---

## Administrative Gatekeeper
Automatically verifies **elevated privileges** before querying sensitive system hives.

## Binary Compliance Model
Implements a **Strict Compliance logic**:  
If one sub-control fails, the system status is marked as **Non-Compliant**.

## Multi-Format Reporting
Generates both:

- **JSON** (for SIEM platforms and dashboards)
- **CSV** (for human auditors)

## Audit Logging
All reports are timestamped using **ISO 8601 standards** to provide a verifiable audit trail.

---  

## 🔍 The 10 NIST Controls Checked
The scanner verifies the following essential security areas:

### Control Mapping Table
| NIST ID | Security Requirement | Technical Check Method |
| :--- | :--- | :--- |
| **3.1.9** | **Session Lock** | Registry Key: `ScreenSaveActive` |
| **3.5.3** | **Password Complexity** | Windows `net accounts` policy |
| **3.1.8** | **Limit Login Attempts** | Windows `lockout threshold` |
| **3.5.7** | **Password Reuse** | Password history length check |
| **3.14.2**| **Malware Protection** | Windows Defender Service Status |
| **3.8.3** | **Media Sanitization** | `manage-bde` BitLocker Status |
| **3.1.5** | **Least Privilege** | User SID / Group Membership check |
| **3.5.8** | **Password Encryption** | Registry SAM protection check |
| **3.14.5**| **Update Definitions** | `Get-MpComputerStatus` via PowerShell |
| **3.4.7** | **Software Whitelisting** | `Get-AppLockerPolicy` check |

# Getting Started

## Prerequisites

- **Operating System:** Windows 10 / Windows 11 / Windows Server
- **Language:** Python 3.x
- **Permissions:** Terminal must be run as **Administrator**

     
---

## Installation

Clone the repository:

```bash
git clone https://github.com/yourusername/nist-800-171-scanner.git
cd nist-800-171-scanner
```

---

# Running the Audit

Execute the script from an **elevated terminal**:

```bash
python scanner.py
```

---

# Understanding Results

After execution, a **`reports/`** folder will be created containing:

### `audit_results.csv`

Open this file in **Excel or other spreadsheet tools** to view a row-by-row breakdown of each control.

### `audit_results.json`




