# Technical Architecture: NIST 800-171 Automated Compliance Scanner

This document describes the technical design, data flow, and logical evaluation framework of the **NIST 800-171 Automated Compliance Scanner**.

---

# 1. System Design Phases

## Phase I: Environment Guard (Security Check)

The script begins by verifying the **Execution Context**. Because NIST controls involve sensitive registry hives (`HKLM\SAM`) and system-wide security policies, the script utilizes the Windows **shell32 API**.

**Mechanism:** `is_admin()` function  

**Logic:**  
If the process token lacks **Administrative elevation**, the script terminates immediately to prevent **false negatives**.

---

## Phase II: The Core Evaluation Engine

This is the central logic of the application. It uses a **Standardized Assessment Framework** to iterate through a list of NIST controls.

### Components

**The Inspector (`cmd_ok`)**

- A subprocess wrapper that executes shell commands (PowerShell/CMD).

**Exit Code Validation**

- The engine relies on **Boolean logic**.
- An **Exit Code of 0** from the OS is interpreted as **Compliant**.

**The Tripwire Model**

The architecture assumes an initial state of:

```python
overall_compliant = True
```

If any single control fails, the global state is permanently flipped to **False**, reflecting a strict **binary compliance stance**.

---

# 2. Data Flow & Normalization

The script transforms raw system responses into **structured data objects**.

| Step | Action | Outcome |
|-----|------|------|
| 1 | Raw Query: Execute `net accounts` or `reg query` | System Output / Exit Code |
| 2 | Normalization: Map results to a Python dictionary (`{}`) | Key-Value Data Pair |
| 3 | Aggregation: Append objects to the `audit_results` list | In-Memory Database |
| 4 | Serialization: Write to JSON and CSV | Persistent Audit Artifacts |

---

# 3. Storage & Reporting Strategy

The architecture separates data based on its **intended audience**.

## Standardized File Logging

The script utilizes **ISO 8601 timestamping**:

```
%Y-%m-%d %H:%M:%S
```

This ensures that all generated reports in the `/reports` folder are:

- Chronologically sortable
- Aligned with **regulatory non-repudiation requirements**

---

## Dual-Format Output

### JSON (Machine-Readable)

Designed for ingestion into:

- **SIEM tools** 
- **Dashboards** 

### CSV (Human-Readable)

Designed for **manual review by auditors** using spreadsheet software such as:

- Excel
- Google Sheets

---

# 4. Technical Control Summary

The scanner evaluates **10 key NIST 800-171 requirements**, including:

## Access Control (3.1.x)

- Session locks
- Least privilege enforcement

## Identification & Authentication (3.5.x)

- Password complexity
- Password reuse restrictions

## System & Information Integrity (3.14.x)

- Malware protection
- Security definition updates
