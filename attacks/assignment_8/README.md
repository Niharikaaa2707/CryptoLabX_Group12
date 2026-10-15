# Cryptographic Prime Generation Using Miller–Rabin

## 1. Objective

Generate a probable prime of exactly 512 bits using the Miller–Rabin
primality test. Record the experimental results and independently
verify the generated number.

## 2. Mathematical Background

Let \(n > 3\) be an odd integer. The Miller–Rabin test is based on
the decomposition:

\[
n-1=2^s d
\]

where \(s \geq 1\) and \(d\) is odd.

Choose a random base \(a\) satisfying:

\[
2 \leq a \leq n-2
\]

Calculate:

\[
x=a^d \bmod n
\]

The candidate passes the round if:

\[
x=1 \quad \text{or} \quad x=n-1
\]

Otherwise, repeatedly square \(x\) modulo \(n\):

\[
x=x^2 \bmod n
\]

If \(x\) becomes \(n-1\), the round passes. If this never happens
within the required iterations, \(n\) is composite.

A candidate that passes all 20 rounds is considered a probable prime.

For an odd composite number, the probability of passing 20 independent
Miller–Rabin rounds is at most:

\[
\left(\frac{1}{4}\right)^{20}=2^{-40}
\]

## 3. Prime Generation

The program generates random integers using Python's `secrets` module.

For a 512-bit candidate, the highest bit and lowest bit are set:

\[
n \gets n \;|\; 2^{511}
\]

\[
n \gets n \;|\; 1
\]

The first operation ensures that the integer has exactly 512 bits.
The second ensures that the candidate is odd.

Each candidate is tested using 20 randomly selected bases. If it fails,
a new candidate is generated. This process continues until a candidate
passes all rounds.

## 4. Algorithm

1. Generate a random 512-bit odd candidate \(n\).
2. Set \(n-1=2^s d\), where \(d\) is odd.
3. Select a random base \(a\) in the range \([2,n-2]\).
4. Calculate \(x=a^d \bmod n\).
5. Apply the Miller–Rabin conditions.
6. Reject the candidate if any round identifies it as composite.
7. Repeat with a new candidate if necessary.
8. Verify the final candidate independently.

## 5. Experimental Setup

| Parameter | Value |
|---|---|
| Programming language | Python |
| Assigned bit length | 512 |
| Miller–Rabin rounds | 20 |
| Candidate generation | `secrets` |
| Independent verification | SymPy |
| Execution-time measurement | `time.perf_counter()` |

## 6. Experimental Results

The program records the actual measurements in `outputs/results.txt`.

| Parameter | Observed Value |
|---|---|
| Assigned bit length | 512 |
| Generated prime candidate | See results file |
| Actual bit length | 512 |
| Number of candidates tested | See results file |
| Rounds per candidate | 20 |
| Total generation rounds | See results file |
| Execution time | See results file |

The observed candidate count and execution time vary between runs.

## 7. Verification

The generated number is verified using three checks.

**Bit length:**

\[
2^{511}\leq n<2^{512}
\]

Python's `n.bit_length()` must return 512.

**Miller–Rabin:** The candidate is tested again using 20 newly selected
random bases and must pass every round.

**Independent verification:** SymPy's `isprime(n)` function is used
to independently check the generated number.

The expected results are:

- Correct bit length: `True`
- Miller–Rabin verification: `True`
- Independent SymPy verification: `True`

## 8. Execution

Install the dependency:

```bash
python3 -m pip install sympy
