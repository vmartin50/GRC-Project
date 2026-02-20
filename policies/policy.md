# NIST 800-171 Security Policy Handbook
**Author:** [Vanessa Martin]  
**Date:** February 20, 2026

## 1. Overview
This policy handbook defines the mandatory technical security standards for workstations handling sensitive information. To ensure high-integrity security, we utilize "NIST-as-Code" to automate the verification of these controls.

## 2. Scope
This policy applies to all Windows-based assets. Compliance is measured against the **NIST SP 800-171** framework, specifically focusing on the following 10 critical security areas.

## 3. Control Standards 

### 3.1 Access Control
* **3.1.9 Session Lock:** Systems must be configured to automatically trigger a screen lock after a period of inactivity to prevent unauthorized physical access.
* **3.1.5 Least Privilege:** Users shall operate with the minimum level of privileges necessary to perform their duties. Administrative accounts should not be used for daily tasks.
* **3.1.8 Limit Login Attempts:** To prevent brute-force attacks, the system must lockout users after a specified number of failed login attempts.

### 3.2 Identification & Authentication
* **3.5.3 Password Complexity:** System passwords must meet complexity requirements (length, character types) to resist cracking.
* **3.5.7 Password Reuse:** Systems must remember previous passwords to prevent users from rotating between the same two or three passwords.
* **3.5.8 Password Encryption:** All stored passwords and credentials must be protected using FIPS-validated cryptography.

### 3.3 System & Information Integrity
* **3.14.2 Malware Protection:** Local antivirus (Windows Defender) must be active and running at all times.
* **3.14.5 Update Definitions:** Security definitions for malware protection must be updated daily.

### 3.4 Configuration Management & Media Protection
* **3.8.3 Media Sanitization:** Full-disk encryption (BitLocker) is required to protect data at rest on all portable and workstation drives.
* **3.4.7 Software Whitelisting:** Only authorized software is permitted to run on the system (monitored via AppLocker policies).

## 4. Compliance Auditing
The `scanner.py` utility is authorized to perform read-only audits of these settings. The resulting `controls.csv` serves as the official record of compliance.
