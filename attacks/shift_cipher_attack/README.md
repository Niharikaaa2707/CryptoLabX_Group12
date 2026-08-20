# Lab Assignment 4: Cryptanalysis of Shift Cipher

## 1. Overview
This project explores the cryptanalysis of the classical Shift (Caesar) Cipher using two distinct approaches:
1. **Brute-Force with Dictionary Scoring**
2. **Chi-Square ($\chi^2$) Frequency Analysis**

---

## 2. Algorithms Implemented

### Shift Cipher (`shift_cipher.py`)
Encrypted using:
$$C = (P + K) \pmod{26}$$

Decrypted using:
$$P = (C - K) \pmod{26}$$

Non-alphabetic characters remain untouched, and letter casing is preserved.

### Dictionary Scoring (`brute_force_dictionary.py`)
Iterates through all 26 possible keys ($0 \le K \le 25$), decrypts the ciphertext, and counts how many words match a predefined dictionary (`english_words.txt`). The key with the maximum matching word count is selected.

### Chi-Square Analysis (`chi_square_attack.py`)
Measures how closely the observed letter frequencies in a decrypted text match standard English distributions. The Chi-Square statistic is computed as:

$$\chi^2 = \sum_{c='A'}^{'Z'} \frac{(O_c - E_c)^2}{E_c}$$

Where:
* $O_c$: Observed count of letter $c$ in decrypted text.
* $E_c$: Expected count of letter $c$ based on English relative frequencies.

The key with the **lowest** $\chi^2$ value is selected as the correct key.

---

## 3. Experimental Results

| Test Case | Actual Key | Dict Key | Chi2 Key | Dict Correct? | Chi2 Correct? |
| :--- | :---: | :---: | :---: | :---: | :---: |
| `The quick brown fox jumps over the lazy dog` | 12 | 12 | 12 | YES | YES |
| `CryptoLabX security testing protocol` | 3 | 0 | 3 | NO | YES |
| `Attack at dawn` | 7 | 7 | 7 | YES | YES |
| `Zzz qqq xxx rrr` | 19 | 0 | 5 | NO | NO |

---

## 4. Failure Analysis

* **Dictionary Scoring Failure (`CryptoLabX...`):**  
  Failed because technical jargon, proper nouns, or unique compound terms like "CryptoLabX" were absent from `english_words.txt`.
* **Random/Non-Standard Text (`Zzz qqq...`):**  
  Both algorithms failed because the text contains no valid English words (failing Dictionary) and lacks standard English character distributions (failing Chi-Square).
* **Suggested Improvements:**  
  1. Expand the dictionary using N-gram frequency lists.  
  2. Fall back to Chi-Square analysis when Dictionary Scoring yields a low confidence score or tie.

---

## 5. Conclusion
Chi-Square analysis is generally more robust for arbitrary English text since it does not rely on exact word matches. However, Dictionary Scoring performs better on very short phrases where character statistics have high variance.
