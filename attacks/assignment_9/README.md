
# Crypto Lab Assignment 9
## Evaluation of Operating-System Random Number Generators

## 1. Objective

To evaluate operating-system random-number generation mechanisms
and investigate their suitability for cryptographic applications.

The experiment uses Linux `/dev/urandom`, OpenSSL's `rand` utility,
and the Windows .NET cryptographic random-number API.

## 2. Directory Structure

```text
assignment_9/
├── src/
│   ├── generate_linux.sh
│   ├── analyze_random.py
│   └── windows_cng.cs
├── outputs/
│   └── data/
├── assignment9_analysis.ipynb
├── requirements.txt
├── .gitignore
└── README.md
```

Generated binary data is kept locally and excluded from Git.

## 3. Random Data Generation

Each generator produces 1 MiB (1,048,576 bytes) of random data.

### Linux /dev/urandom

The Linux kernel maintains a cryptographic random-number generator
seeded and managed using available entropy sources.

The `/dev/urandom` device provides random bytes from this generator.
It is suitable for cryptographic use on modern Linux systems.

### OpenSSL rand

OpenSSL's `rand` command generates random bytes using OpenSSL's
cryptographic random-number subsystem.

The subsystem uses a cryptographic pseudorandom generator seeded
from appropriate random sources. Its exact implementation and
configuration depend on the OpenSSL version and provider setup.

### Windows CNG / .NET

The .NET `RandomNumberGenerator` API provides cryptographically
secure random bytes.

On Windows, the operating-system implementation uses Windows
cryptographic facilities. Windows CNG includes the
`BCryptGenRandom` interface.

The application uses the high-level .NET API instead of implementing
its own random-number generator.

## 4. Data Analysis

The Python program and Jupyter notebook analyze:

1. Byte-frequency distribution across all 256 byte values.
2. Distribution of zero-bits and one-bits.
3. Repeated non-overlapping four-byte patterns.
4. Serial correlation between adjacent byte values.
5. Chi-square test for byte-frequency uniformity.
6. Binomial test for bit balance.
7. Runs test for the sequence of zero-bits and one-bits.

The notebook reports the observed measurements and p-values.

## 5. Statistical Tests

### Byte-frequency chi-square test

The expected count for each byte value is:

E = N / 256

The chi-square statistic is:

X^2 = sum((O - E)^2 / E)

Here, O is an observed byte count, E is the expected count, and N
is the total number of bytes.

A large deviation from the expected counts can indicate a
non-uniform distribution.

### Bit-balance test

For N bits, the expected number of one-bits is N/2, assuming
independent unbiased bits.

The binomial test checks the observed number of one-bits against
a probability of 0.5.

### Runs test

A run is a consecutive sequence of identical bits. For example,
00111010 contains five runs: 00, 111, 0, 1, and 0.

The runs test checks whether the observed number of runs is
consistent with a random binary sequence under its assumptions.

### Serial correlation

Lag-one serial correlation measures the linear relationship
between each byte and the following byte.

Values close to zero indicate little observed linear dependence
at lag one. They do not rule out other dependencies.

### Repeated patterns

The program counts repeated non-overlapping four-byte blocks.

A repeated block does not automatically indicate a defective
generator. Repetitions can occur by chance, especially in large
datasets.

## 6. Interpretation of P-values

The significance level is 0.05.

A p-value below 0.05 indicates evidence against the particular
null hypothesis tested, under the test's assumptions.

A p-value above 0.05 means that the test did not detect sufficient
evidence against that hypothesis.

It does not prove that the generator is random or secure.

Multiple tests examine different properties. Results should be
interpreted together, and repeated experiments can provide
additional information.

## 7. Comparison of the Mechanisms

| Property | Linux /dev/urandom | OpenSSL rand | Windows .NET API |
|---|---|---|---|
| Interface | Kernel device | Command-line utility | Programming API |
| Main role | Kernel random bytes | Cryptographic random bytes | Cryptographic random bytes |
| Randomness management | Linux kernel | OpenSSL random subsystem | Windows cryptographic facilities |
| Application convenience | Simple file access | Simple command-line generation | Simple API call |
| Main consideration | Trust the kernel and system state | Trust the library, configuration, and seed management | Trust the OS provider and API implementation |

The interfaces are different, but all three can provide
cryptographically suitable random bytes when correctly implemented
and used in a properly initialized system.

## 8. Why Statistical Tests Do Not Guarantee Security

Statistical tests examine patterns in observed output. They cannot
establish that an attacker cannot predict future output.

A deterministic generator with a secret internal state can produce
excellent statistical results. If an attacker discovers that state,
the output may become predictable.

Similarly, a generator can produce statistically balanced output
while having insufficient entropy, a compromised seed, or a
vulnerable implementation.

Cryptographic security also depends on initialization, state
protection, reseeding, implementation quality, and resistance to
state compromise.

Therefore, statistical testing is useful for detecting some
defects but cannot replace cryptographic design and review.

## 9. Procedure

1. Run `src/generate_linux.sh` on Linux.
2. Generate the Windows data using `src/windows_cng.cs` on Windows.
3. Place all three `.bin` files in `outputs/data/`.
4. Install the dependencies using `pip install -r requirements.txt`.
5. Run `python3 src/analyze_random.py`.
6. Run all cells in `assignment9_analysis.ipynb`.
7. Record and interpret the actual results.

## 10. Conclusion

The experiment compares random-data generation interfaces and
examines their observable statistical properties.

The measurements help identify deviations in byte frequencies,
bit balance, repeated patterns, and serial dependence.

However, passing these tests does not prove unpredictability or
cryptographic security. Secure random generation ultimately
depends on a trustworthy operating system, correct cryptographic
implementations, and proper entropy and state management.

