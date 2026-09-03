# Lab Assignment 5: Monoalphabetic Substitution Cipher & Cryptanalysis

**Group Number:** 12  
**Implementation Language:** C++ (`std=c++17`)  
**Dataset Reference:** *Modern Cryptography* by Katz & Lindell (Excerpt from Page 42, calculated using formula: $\text{Group Number} + 30$)

---

## 📌 Project Overview

This module provides a complete C++ framework for implementing a **Monoalphabetic Substitution Cipher** and executing statistical cryptanalysis without relying on external cryptographic libraries. 

Because monoalphabetic substitution ciphers preserve the underlying statistical properties of the language, an attacker can break the cipher by analyzing character frequencies, word lengths, and structural pattern repetitions. This project demonstrates the iterative recovery of both the plaintext message and the underlying substitution key through frequency analysis and $N$-gram pattern matching.

---

## 📁 Repository & File Structure

```text
attacks/assignment_5/
├── outputs/
│   ├── plaintext.txt      # 1-page text excerpt from Katz & Lindell (Page 42)
│   └── execution.log      # Complete output execution log captured from run
├── src/
│   └── monoalphabetic.cpp # Complete C++ cipher engine & cryptanalysis program
└── README.md              # Project documentation and experimental analysis
