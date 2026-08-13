# Secure Application Module - Online Banking System

## Overview
This module implements a console-based Online Banking Application as part of Lab Assignment 3 (Group 12). The objective is to demonstrate core banking functionalities while illustrating security vulnerabilities for SAST tool detection.

## Core Functionalities
1. **User Authentication:** Console login mechanism.
2. **Check Balance:** View account balances.
3. **Transfer Funds:** Move funds between user accounts.
4. **Manage Beneficiaries:** Add and list beneficiary information.
5. **Logging:** Record application activities to execution log files.

## Implemented Vulnerabilities
1. **Hardcoded Credentials & Sensitive Data Exposure in Logs:** Plaintext passwords stored in dictionaries and logged during authentication.
2. **Insufficient Input Validation:** The transfer feature does not restrict negative transfer values, allowing logical balance manipulation.
3. **Broken Access Control (IDOR):** Users can query balance information of arbitrary account IDs without authorization checks.

## SAST Analysis
- **Tool Used:** SonarQube (Community Edition / SonarScanner)
- **Report Location:** `reports/sast_report.txt` (or SonarQube dashboard export)
- **Screenshots:** `screenshots/sast_scan_results.png` (Screenshot of SonarQube dashboard scan)
- **Issues Found:** 2 Low-severity hardcoded credential vulnerabilities (`B105: CWE-259`).