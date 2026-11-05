# Cryptography Lab Assignment 10
## MT19937 Stream Cipher and Predictable Token Attack

## 1. Objective

The objective of this assignment is to understand why a statistical pseudorandom number generator (PRNG), such as MT19937, is unsuitable for cryptographic applications.

The assignment demonstrates three main concepts:

1. Implementation of a toy stream cipher using MT19937.
2. Recovery of a weak 16-bit seed using a known-plaintext attack.
3. Prediction of password reset tokens generated using timestamp-based seeding.

Through these experiments, we understand the difference between statistical randomness and cryptographic security.

## 2. Requirements

- Python 3
- Basic understanding of XOR operations.
- Basic understanding of pseudorandom number generators.

No external Python packages are required because the implementation uses Python's built-in `random` module.

## 3. Project Structure

```text
assignment_10/
│
├── main.py
├── README.md
├── requirements.txt
│
├── src/
│   ├── __init__.py
│   ├── mt_stream_cipher.py
│   ├── known_plaintext_attack.py
│   └── predictable_token.py
│
├── notebooks/
│   └── assignment10_analysis.ipynb
│
└── outputs/
    └── assignment10_output.txt
```

## 4. Execution Instructions

Navigate to the assignment directory:

```bash
cd attacks/assignment_10
```

Run the complete assignment:

```bash
python3 main.py
```

Run individual components:

```bash
python3 -m src.mt_stream_cipher
python3 -m src.known_plaintext_attack
python3 -m src.predictable_token
```

Save the complete execution output:

```bash
mkdir -p outputs
python3 main.py | tee outputs/assignment10_output.txt
```

The Jupyter notebook can be opened using Jupyter Notebook or VS Code.

## 5. Part A: MT19937 Stream Cipher

### 5.1 Introduction

MT19937 is a pseudorandom number generator based on the Mersenne Twister algorithm.

Python provides an inbuilt implementation through the `random` module. The generator produces a deterministic sequence of pseudorandom numbers based on its initial seed.

In this assignment, MT19937 is used to generate an 8-bit keystream value for every byte of the input message.

The byte extraction procedure is:

```python
generator = random.Random(seed)
value = generator.getrandbits(8)
```

The same procedure is used throughout the assignment.

### 5.2 Encryption and Decryption

Let:

- P = Plaintext byte
- K = Keystream byte
- C = Ciphertext byte

Encryption is performed using XOR:

\[
C=P\oplus K
\]

Decryption is performed using:

\[
P=C\oplus K
\]

This works because XOR has the following properties:

\[
A\oplus 0=A
\]

\[
A\oplus A=0
\]

Therefore:

\[
C\oplus K=(P\oplus K)\oplus K=P
\]

The same function is used for encryption and decryption.

### 5.3 Verification

A sample message is encrypted using a fixed seed.

The ciphertext is then decrypted using the same seed.

The implementation verifies that the decrypted message is identical to the original plaintext.

This confirms that the XOR-based stream cipher implementation works correctly.

## 6. Part A: Known-Plaintext Attack

### 6.1 Plaintext Generation

A plaintext is generated with the following structure:

```text
Random printable prefix + AAAAAAAAAAAAAA
```

The prefix contains between 5 and 20 printable ASCII characters.

The plaintext is encrypted using a randomly selected 16-bit seed.

The attacker knows that the plaintext contains fourteen consecutive A characters but does not know their location.

### 6.2 Seed Search Space

The seed is selected from a 16-bit range.

The total number of possible seeds is:

\[
2^{16}=65,536
\]

The possible seed values are:

\[
0,1,2,\ldots,65535
\]

Since the search space is relatively small, all possible seeds can be tested.

### 6.3 Attack Methodology

The attack performs the following steps:

1. Obtain the ciphertext.
2. Initialize the candidate seed to zero.
3. Generate a keystream using the candidate seed.
4. Decrypt the ciphertext.
5. Search the resulting plaintext for fourteen consecutive A characters.
6. If the known sequence is found, record the candidate seed.
7. Continue until all 65,536 seeds have been tested.
8. Verify the recovered seed by decrypting the complete ciphertext.

### 6.4 Why the Attack Works

For a given seed, MT19937 generates the same keystream sequence.

Therefore, if the correct seed is found, the ciphertext decrypts into the original plaintext.

The known sequence provides a way to identify the correct candidate without knowing the complete plaintext beforehand.

The recovered plaintext is also compared with the original plaintext to verify the result.

## 7. Part B: Predictable Password Reset Tokens

### 7.1 Token Generation

In this experiment, a simulated application generates a password reset token using MT19937.

The current Unix timestamp is used as the seed.

A Unix timestamp represents the number of seconds elapsed since January 1, 1970 (UTC).

The generator produces sixteen consecutive 8-bit outputs.

These outputs are combined to form a 16-byte token.

The token is displayed in hexadecimal format.

### 7.2 Timestamp Prediction Attack

Assume an attacker observes a reset token and knows that it was generated within 300 seconds before or after the current timestamp.

Let the actual timestamp be T.

The attacker searches the following interval:

\[
[T-300,T+300]
\]

The number of possible timestamps is:

\[
300+300+1=601
\]

For every candidate timestamp:

1. Seed MT19937 with the candidate timestamp.
2. Generate sixteen 8-bit outputs.
3. Combine the outputs into a 16-byte token.
4. Compare the generated token with the observed token.
5. Record any matching timestamp.

### 7.3 Verification

After finding a matching timestamp, the program generates the token again using the recovered timestamp.

The regenerated token is compared with the observed token.

If both tokens match, the timestamp recovery is verified.

## 8. MT19937 Algorithm

MT19937 is a deterministic pseudorandom number generator developed using the Mersenne Twister algorithm.

Its internal state consists of:

- 624 words.
- Each word contains 32 bits.
- The generator uses state initialization and state transition operations.
- Bitwise XOR, shifts, and masks are used during state processing.
- A tempering stage improves the statistical distribution of generated values.

Its period is:

\[
2^{19937}-1
\]

This very large period makes it useful for simulations and statistical applications.

However, a large period does not guarantee cryptographic security.

## 9. Why MT19937 Is Not Cryptographically Secure

MT19937 is designed to produce statistically good pseudorandom sequences, not to resist malicious attackers.

Its major limitations include:

**1. Deterministic output**

The same seed always produces the same sequence of outputs.

**2. State reconstruction**

Sufficient observed output can allow an attacker to reconstruct the internal state and predict future outputs.

**3. Small seed space**

When the seed is selected from a small range, an attacker can test every possible seed.

**4. Predictable timestamps**

If the generator is seeded using the current time, an attacker can estimate the generation time and search a limited number of candidate timestamps.

**5. Lack of cryptographic security**

MT19937 does not provide the security properties required for encryption keys, authentication tokens, or password reset tokens.

Passing statistical randomness tests does not mean that a generator is cryptographically secure.

## 10. Pseudocode

### 10.1 Known-Plaintext Seed Recovery

```text
Input: Ciphertext
Known sequence: Fourteen consecutive A characters

for seed from 0 to 65535:

    Generate keystream using seed

    Decrypt ciphertext

    if plaintext contains known sequence:

        Record seed
        Record decrypted plaintext

Verify the recovered seed using the complete ciphertext
```

### 10.2 Timestamp Prediction

```text
Input: Observed token
Input: Approximate generation timestamp T

for timestamp from T-300 to T+300:

    Generate token using candidate timestamp

    if generated token equals observed token:

        Record matching timestamp

        Regenerate token using recovered timestamp

        Verify the regenerated token
```

## 11. Experimental Observations

The following observations are obtained from the implementation:

1. Encryption and decryption using the same seed successfully recover the original message.
2. The known-plaintext attack searches all 65,536 possible seeds.
3. The correct seed can be identified using the known fourteen-character sequence.
4. The complete plaintext can be recovered and verified.
5. The timestamp prediction attack searches 601 candidate timestamps.
6. The matching timestamp reproduces the observed 16-byte token.
7. The experiments demonstrate how weak or predictable seeds can compromise applications using MT19937.

The exact ciphertext, plaintext prefix, seed, timestamp, and token may change between executions because new random samples and timestamps are generated.

## 12. Security Recommendations

MT19937 should not be used for security-sensitive applications.

Instead, cryptographically secure pseudorandom number generators (CSPRNGs) should be used.

For example, Python provides the `secrets` module for generating security-sensitive random values.

Suitable applications include:

- Password reset tokens.
- Authentication tokens.
- Session identifiers.
- Cryptographic keys.

A CSPRNG is designed to make its output unpredictable to an attacker, unlike a statistical PRNG such as MT19937.

## 13. Conclusion

This assignment demonstrates the weaknesses of using a statistical pseudorandom number generator for cryptographic applications.

In Part A, a weak 16-bit seed is recovered through a known-plaintext brute-force attack.

In Part B, a timestamp-based password reset token is predicted by searching a limited range of possible timestamps.

Both experiments demonstrate that deterministic output and predictable seeds can make a pseudorandom generator vulnerable to attacks.

Although MT19937 has excellent statistical properties and a very large period, it is not suitable for cryptographic applications.

Therefore, security-sensitive applications must use cryptographically secure random number generators instead of ordinary statistical PRNGs.
```

### Update and commit

From your assignment directory:

```bash
cd ~/CryptoLabX_Group12/attacks/assignment_10
```

After replacing the README, return to the repository root:

```bash
cd ~/CryptoLabX_Group12
git add attacks/assignment_10/README.md
git commit -m "Expand assignment documentation"
```

**Note:** This creates a fifth commit if your original four commits are already complete. If you haven't made Commit 4 yet, include this README in Commit 4 instead.
