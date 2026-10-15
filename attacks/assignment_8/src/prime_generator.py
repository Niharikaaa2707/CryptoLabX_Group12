import json
import os
import secrets
import time

from miller_rabin import miller_rabin


BITS = 512
ROUNDS = 20


def generate_prime():
    candidates_tested = 0
    total_rounds = 0

    start_time = time.perf_counter()

    while True:
        candidate = secrets.randbits(BITS)

        # Set the highest bit to ensure 512-bit length.
        candidate |= 1 << (BITS - 1)

        # Set the lowest bit to ensure an odd candidate.
        candidate |= 1

        candidates_tested += 1

        is_prime, rounds_used, bases = miller_rabin(
            candidate, ROUNDS
        )

        total_rounds += rounds_used

        if is_prime:
            break

    execution_time = time.perf_counter() - start_time

    return {
        "assigned_bit_length": BITS,
        "prime": str(candidate),
        "actual_bit_length": candidate.bit_length(),
        "candidates_tested": candidates_tested,
        "rounds_per_candidate": ROUNDS,
        "total_rounds_executed": total_rounds,
        "execution_time_seconds": execution_time,
        "bases": bases
    }


if __name__ == "__main__":
    results = generate_prime()

    output_dir = os.path.join(
        os.path.dirname(__file__), "..", "outputs"
    )

    os.makedirs(output_dir, exist_ok=True)

    output_file = os.path.join(output_dir, "run_data.json")

    with open(output_file, "w") as file:
        json.dump(results, file, indent=4)

    print("\n512-BIT PRIME GENERATION")
    print("-" * 45)
    print("Generated prime:", results["prime"])
    print("Actual bit length:", results["actual_bit_length"])
    print("Candidates tested:", results["candidates_tested"])
    print("Rounds per candidate:", ROUNDS)
    print("Total rounds executed:", results["total_rounds_executed"])
    print(
        "Execution time:",
        round(results["execution_time_seconds"], 6),
        "seconds"
    )
    print("Results saved to:", output_file)
