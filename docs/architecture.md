# Technical Architecture: NIST 800-171 Automated Compliance Scanner

## System Design
This tool is built as a **LightWeight Compliance Engine**. It uses Python as an automation layer to query the Windows operating system and compare current settings against the **NIST 800-171** security framework.

### The Execution Pipeline
The script follows a linear four-stage process:

1.  **Privilege Validation:** Uses the `ctypes` library to verify the process is running with **Administrative Privileges**. This is critical because low-privilege users cannot see security settings like BitLocker status or Password Policies.
2.  **OS Interrogation:** The script loops through security controls, spawning sub-processes using Python's `subprocess` module to talk to Windows.
3.  **Result Evaluation:** The script captures the **Exit Code** of the command.
  * Exit Code 0: The system is configured correctly (Compliant).
  * Exit Code non-0: The setting is missing or incorrect (Non-Compliant).
4.  **Data Persistence:** Results are saved into a **CSV file** for an audit trail.


---

