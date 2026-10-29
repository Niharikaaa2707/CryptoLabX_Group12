
import csv
import json
import math
from pathlib import Path
from collections import Counter

DATA_DIR = Path("outputs/data")
RESULTS_DIR = Path("outputs")
BLOCK_SIZE = 4


def load_data(path):
    with open(path, "rb") as file:
        return file.read()


def byte_frequency(data):
    counts = Counter(data)

    return [
        counts.get(value, 0)
        for value in range(256)
    ]


def bit_distribution(data):
    ones = sum(byte.bit_count() for byte in data)
    total = len(data) * 8
    zeros = total - ones

    return {
        "zero_bits": zeros,
        "one_bits": ones,
        "zero_percentage": zeros * 100 / total,
        "one_percentage": ones * 100 / total
    }


def repeated_blocks(data):
    blocks = [
        data[i:i + BLOCK_SIZE]
        for i in range(0, len(data) - BLOCK_SIZE + 1, BLOCK_SIZE)
    ]

    counts = Counter(blocks)

    return {
        "total_blocks": len(blocks),
        "unique_blocks": len(counts),
        "repeated_block_types": sum(
            1 for count in counts.values() if count > 1
        ),
        "extra_duplicate_occurrences": sum(
            count - 1 for count in counts.values() if count > 1
        )
    }


def serial_correlation(data):
    if len(data) < 2:
        return None

    values = list(data)
    mean = sum(values) / len(values)

    numerator = sum(
        (values[i] - mean) * (values[i + 1] - mean)
        for i in range(len(values) - 1)
    )

    denominator = sum(
        (value - mean) ** 2
        for value in values
    )

    if denominator == 0:
        return None

    return numerator / denominator


def analyze_file(path):
    data = load_data(path)

    if len(data) == 0:
        raise ValueError(f"{path} is empty")

    frequencies = byte_frequency(data)

    expected = len(data) / 256

    chi_square = sum(
        (count - expected) ** 2 / expected
        for count in frequencies
    )

    return {
        "file": path.name,
        "bytes": len(data),
        "byte_frequency_min": min(frequencies),
        "byte_frequency_max": max(frequencies),
        "byte_frequency_chi_square": chi_square,
        "bit_distribution": bit_distribution(data),
        "repeated_4_byte_blocks": repeated_blocks(data),
        "serial_correlation": serial_correlation(data)
    }, frequencies


def main():
    RESULTS_DIR.mkdir(exist_ok=True)

    files = sorted(DATA_DIR.glob("*.bin"))

    if not files:
        print("No data files found in", DATA_DIR)
        print("Generate the Linux files and copy the Windows file first.")
        return

    results = []

    for path in files:
        result, frequencies = analyze_file(path)
        results.append(result)

        csv_path = RESULTS_DIR / (path.stem + "_byte_frequency.csv")

        with open(csv_path, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Byte", "Frequency"])

            for value, count in enumerate(frequencies):
                writer.writerow([value, count])

        print("\nFile:", result["file"])
        print("Bytes:", result["bytes"])
        print(
            "Byte frequency range:",
            result["byte_frequency_min"],
            "to",
            result["byte_frequency_max"]
        )
        print(
            "Byte frequency chi-square:",
            round(result["byte_frequency_chi_square"], 3)
        )
        print("Bit distribution:", result["bit_distribution"])
        print("Repeated blocks:", result["repeated_4_byte_blocks"])
        print(
            "Serial correlation:",
            result["serial_correlation"]
        )

    with open(RESULTS_DIR / "analysis_results.json", "w") as file:
        json.dump(results, file, indent=4)

    print("\nResults saved in", RESULTS_DIR)


if __name__ == "__main__":
    main()

