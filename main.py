import os
from collections import Counter
from utils.logger import write_log

DATASET_FOLDER = "datasets"


def analyze_file():
    files = os.listdir(DATASET_FOLDER)

    if len(files) == 0:
        print("\nNo files found.")
        return

    print("\nAvailable Files:")
    for i, file in enumerate(files, start=1):
        print(f"{i}. {file}")

    try:
        choice = int(input("\nEnter file number: "))
        if choice < 1 or choice > len(files):
            print("Invalid file number!")
            return
    except ValueError:
        print("Please enter a valid number!")
        return

    filename = os.path.join(DATASET_FOLDER, files[choice - 1])

    with open(filename, "r", encoding="utf-8") as f:
        text = f.read()

    characters = len(text)
    words = len(text.split())
    lines = len(text.splitlines())
    unique_characters = len(set(text))

    letters = [c.lower() for c in text if c.isalpha()]
    frequency = Counter(letters)

    print("\n========== FILE ANALYSIS ==========")
    print(f"Characters       : {characters}")
    print(f"Words            : {words}")
    print(f"Lines            : {lines}")
    print(f"Unique Characters: {unique_characters}")

    print("\nLetter Frequency:")
    for letter in sorted(frequency):
        print(f"{letter} : {frequency[letter]}")


def menu():
    while True:
        print("\n===================================")
        print("        CryptoLabX Toolkit")
        print("===================================")
        print("1. Encrypt")
        print("2. Decrypt")
        print("3. Attack")
        print("4. Analyze")
        print("5. Exit")

        choice = input("\nEnter your choice: ")

        if choice == "1":
            print("\nEncrypt feature coming soon...")
            write_log("Encrypt")

        elif choice == "2":
            print("\nDecrypt feature coming soon...")
            write_log("Decrypt")

        elif choice == "3":
            print("\nAttack feature coming soon...")
            write_log("Attack")

        elif choice == "4":
            write_log("Analyze")
            analyze_file()

        elif choice == "5":
            write_log("Exit")
            print("\nThank you for using CryptoLabX!")
            break

        else:
            print("\nInvalid choice! Please try again.")


if __name__ == "__main__":
    menu()