# Vigenère Cipher Cryptanalysis using Kasiski Examination

## Aim

To perform cryptanalysis of a Vigenère cipher using **Kasiski Examination, Index of Coincidence, and Frequency Analysis**, and recover the probable key and plaintext.

**Group Number:** 12
**Ciphertext:** Ciphertext-2 (Even Group Numbers)

## Description

This program attempts to break a Vigenère cipher without knowing the encryption key.

The ciphertext is first cleaned by removing spaces and special characters. Repeated patterns are then identified and the distances between their occurrences are calculated. Factors of these distances are used by Kasiski Examination to estimate possible key lengths.

After selecting a probable key length, the ciphertext is divided into groups. Each group can be treated approximately as a Caesar cipher, allowing frequency analysis to estimate the shift corresponding to each character of the key.

The recovered key is then used to decrypt the ciphertext. Finally, the plaintext is encrypted again using the recovered key to verify that the original ciphertext is obtained.

## Main Steps

1. Clean and preprocess the ciphertext.
2. Find repeated patterns.
3. Calculate distances between repeated patterns.
4. Find factors of the distances.
5. Estimate candidate key lengths using Kasiski Examination.
6. Calculate the Index of Coincidence.
7. Split the ciphertext according to the estimated key length.
8. Perform frequency analysis on every group.
9. Find the probable Caesar shift for each group.
10. Combine the shifts to obtain the Vigenère key.
11. Decrypt the ciphertext.
12. Re-encrypt the plaintext for verification.

## Functions

| Function                   | Purpose                                                              |
| -------------------------- | -------------------------------------------------------------------- |
| `clean_ciphertext()`       | Removes spaces and special characters and converts text to uppercase |
| `find_repeated_patterns()` | Finds repeated sequences in the ciphertext                           |
| `calculate_distances()`    | Calculates distances between repeated occurrences                    |
| `find_factors()`           | Finds factors of the calculated distances                            |
| `kasiski_analysis()`       | Suggests candidate key lengths                                       |
| `calculate_ic()`           | Calculates the Index of Coincidence                                  |
| `split_into_groups()`      | Divides ciphertext according to the key length                       |
| `frequency_analysis()`     | Calculates A–Z frequency for each group                              |
| `find_shift()`             | Estimates the Caesar shift for a group                               |
| `find_key()`               | Combines shifts to obtain the probable key                           |
| `vigenere_decrypt()`       | Decrypts the ciphertext                                              |
| `vigenere_encrypt()`       | Encrypts plaintext using the recovered key                           |
| `verify()`                 | Checks whether re-encryption matches the original ciphertext         |

## Kasiski Examination

Kasiski Examination helps estimate the length of the Vigenère key.

The program searches for repeated sequences in the ciphertext. If the same plaintext sequence is encrypted using the same part of the repeating key, the resulting ciphertext sequence may also repeat.

The distance between repeated sequences is calculated, and the factors of these distances are examined. Factors that occur frequently can indicate possible key lengths.

## Index of Coincidence

The Index of Coincidence (IC) is used as an additional method for estimating the key length.

For a group containing `N` characters:

```text
IC = Σ fi(fi - 1) / N(N - 1)
```

where `fi` represents the frequency of each letter.

The ciphertext is tested using candidate key lengths, and the resulting groups are analyzed using their IC values.

## Frequency Analysis

Once a probable key length is obtained, the ciphertext is divided into groups.

For example, for a key length of 5:

```text
Group 1 → positions 1, 6, 11, 16, ...
Group 2 → positions 2, 7, 12, 17, ...
Group 3 → positions 3, 8, 13, 18, ...
Group 4 → positions 4, 9, 14, 19, ...
Group 5 → positions 5, 10, 15, 20, ...
```

Each group is approximately a Caesar cipher encrypted with one character of the Vigenère key.

Frequency analysis is performed on each group and the most probable Caesar shift is determined. These shifts are combined to form the complete key.

## Vigenère Decryption

The Vigenère cipher uses modular arithmetic over the alphabet.

Encryption:

```text
C = (P + K) mod 26
```

Decryption:

```text
P = (C - K) mod 26
```

where `P` is plaintext, `C` is ciphertext, and `K` is the key.

## Verification

After recovering the plaintext, the program encrypts it again using the recovered key.

The newly generated ciphertext is compared with the cleaned original ciphertext.

```text
Original Ciphertext
        ↓
     Decrypt
        ↓
Recovered Plaintext
        ↓
     Encrypt
        ↓
Re-encrypted Ciphertext
        ↓
      Compare
```

If both ciphertexts are identical, the result is successfully verified.

## Input

Since the group number is **12**, the program uses:

```text
Ciphertext-2 (Even Group Numbers)
```

The ciphertext is provided in the assignment and contains spaces and line breaks. These are removed during preprocessing.

## Output

The program displays:

* Estimated key length
* Frequency table for each group
* Recovered Vigenère key
* Recovered plaintext
* Verification result

Example:

```text
========================================
 VIGENERE CIPHER CRYPTANALYSIS
========================================

Estimated Key Length: <length>

Frequency Analysis
Group 1:
A: ...
B: ...
C: ...
...

Recovered Key: <KEY>

Recovered Plaintext:
<plaintext>

Verification: SUCCESS
```

## Compilation and Execution

For C++:

```bash
g++ vigenere_kasiski.cpp -o vigenere_kasiski
./vigenere_kasiski
```

For Python:

```bash
python vigenere_kasiski.py
```

## Project Structure

```text
vigenere_kasiski/
│
├── vigenere_kasiski.cpp
└── README.md
```

## Conclusion

This experiment demonstrates the cryptanalysis of the Vigenère cipher using classical cryptanalytic techniques. Kasiski Examination and the Index of Coincidence help estimate the key length, while frequency analysis is used to recover the individual key characters. The recovered key is then used to decrypt the ciphertext, and re-encryption confirms whether the recovered result is correct.

