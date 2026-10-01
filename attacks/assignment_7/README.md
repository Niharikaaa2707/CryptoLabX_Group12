# Assignment 7 - Padding Oracle Attack

## Objective

This assignment demonstrates a Padding Oracle Attack against AES in CBC mode with PKCS#7 padding.

The attack recovers the plaintext without directly using the AES key during the attack. It uses only the padding oracle's response indicating whether the decrypted ciphertext has valid padding.

## Implementation

The program is implemented in:

```text
src/padding_oracle.py
```

It performs the following tasks:

1. Encrypts a plaintext using AES-CBC.
2. Implements PKCS#7 padding.
3. Implements a padding oracle that returns `True` for valid padding and `False` for invalid padding.
4. Splits the ciphertext into 16-byte blocks.
5. Modifies the previous ciphertext block to attack each target block.
6. Tries all 256 possible byte values.
7. Recovers plaintext bytes from right to left.
8. Recovers all ciphertext blocks.
9. Removes the final PKCS#7 padding.
10. Counts the total number of oracle queries.

## CBC Principle

For AES-CBC decryption:

```text
Pi = D(Ci) XOR C(i-1)
```

For the first block:

```text
P1 = D(C1) XOR IV
```

Therefore, modifying the previous ciphertext block changes the resulting plaintext of the target block.

## Padding Oracle Attack

The attack starts from the last byte of a block.

For each byte, the program tries all 256 possible values for the corresponding byte in the previous block. When the oracle returns `True`, the modification has produced valid PKCS#7 padding.

The intermediate value is then calculated as:

```text
Intermediate = ModifiedByte XOR PaddingValue
```

The original plaintext byte is calculated as:

```text
PlaintextByte = Intermediate XOR OriginalPreviousByte
```

The same process is repeated from right to left for every block.

## Result

Original plaintext:

```text
This is a secret message.
```

Recovered plaintext:

```text
This is a secret message.
```

Total oracle queries:

```text
2539
```

## Why the Attack Works

CBC mode XORs the decrypted ciphertext block with the previous ciphertext block. Therefore, an attacker who can modify the previous block can control the resulting plaintext bytes of the target block.

The padding oracle leaks information because it tells the attacker whether the resulting plaintext has valid PKCS#7 padding. Repeating this process allows the attacker to recover the complete plaintext.

## Prevention

Padding oracle attacks can be prevented by using authenticated encryption such as:

* AES-GCM
* ChaCha20-Poly1305

If CBC mode is used, authentication should be applied before accepting or processing the decrypted plaintext. Error messages should also avoid revealing whether padding specifically was invalid.

## Files

```text
assignment_7/
└── src/
    └── padding_oracle.py
```

## Conclusion

The experiment demonstrates that an AES-CBC implementation can leak plaintext when an attacker has access to a padding-validity oracle. The AES key does not need to be known by the attacker; the oracle responses are sufficient to recover the plaintext.

