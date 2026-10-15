import json
import os

from sympy import isprime
from miller_rabin import miller_rabin


BITS = 512
ROUNDS = 20


def verify_prime():
    base_dir = os.path.dirname(__file__)

    data_file = os.path.join(
        base_dir, "..", "outputs", "run_data.json"
    )

    with open(data_file, "r") as file:
        data = json.load(file)

    prime = int(data["prime"])

    # Verify the bit length.
    correct_length = prime.bit_length() == BITS

    # Run Miller-Rabin again.
    mr_result, rounds_used, verification_bases = miller_rabin(
        prime, ROUNDS
    )

    # Independent verification using SymPy.
    independent_result = isprime(prime)

    success = (
        correct_length
        and mr_result
        and independent_result
    )

    results_file = os.path.join(
        base_dir, "..", "outputs", "results.txt"
    )

    with open(results_file, "w") as file:
        file.write("CRYPTOGRAPHIC PRIME GENERATION\n")
        file.write("Miller-Rabin Primality Test\n")
        file.write("=" * 50 + "\n\n")

        file.write("EXPERIMENTAL RESULTS\n\n")
        file.write(
            f"Assigned bit length: {BITS}\n"
        )
        file.write(
            f"Generated prime: {prime}\n"
        )
        file.write(
            f"Actual bit length: {prime.bit_length()}\n"
        )
        file.write(
            f"Candidates tested: {data['candidates_tested']}\n"
        )
        file.write(
            f"Miller-Rabin rounds per candidate: {ROUNDS}\n"
        )
        file.write(
            f"Total generation rounds executed: "
            f"{data['total_rounds_executed']}\n"
        )
        file.write(
            f"Generation execution time: "
            f"{data['execution_time_seconds']:.6f} seconds\n\n"
        )

        file.write("BASES USED FOR GENERATION\n\n")

        for i, base in enumerate(data["bases"], start=1):
            file.write(f"Round {i}: {base}\n")

        file.write("\nVERIFICATION RESULTS\n\n")
        file.write(
            f"Correct bit length: {correct_length}\n"
        )
        file.write(
            f"Miller-Rabin verification: {mr_result}\n"
        )
        file.write(
            f"Verification rounds executed: {rounds_used}\n"
        )
        file.write(
            f"Independent SymPy verification: {independent_result}\n"
        )

        file.write("\nBASES USED FOR VERIFICATION\n\n")

        for i, base in enumerate(
            verification_bases, start=1
        ):
            file.write(f"Round {i}: {base}\n")

        file.write("\nFINAL RESULT\n\n")
        file.write(
            "SUCCESS: Prime candidate passed all verification checks.\n"
            if success
            else "FAILURE: One or more verification checks failed.\n"
        )

    print("Generated prime:", prime)
    print("Correct bit length:", correct_length)
    print("Miller-Rabin verification:", mr_result)
    print("Independent SymPy verification:", independent_result)
    print("Results saved to:", results_file)

    if not success:
        raise SystemExit("Verification failed.")


if __name__ == "__main__":
    verify_prime()
