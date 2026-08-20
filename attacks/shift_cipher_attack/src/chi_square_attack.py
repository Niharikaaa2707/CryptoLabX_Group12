"""
Chi-Square Cryptanalysis for Shift Cipher
"""

from collections import Counter
from shift_cipher import decrypt_shift_cipher

# Standard English letter frequencies (A-Z) in percentages
ENGLISH_FREQUENCIES = {
    'A': 8.167, 'B': 1.492, 'C': 2.782, 'D': 4.253, 'E': 12.702,
    'F': 2.228, 'G': 2.015, 'H': 6.094, 'I': 6.966, 'J': 0.153,
    'K': 0.772, 'L': 4.025, 'M': 2.406, 'N': 6.749, 'O': 7.507,
    'P': 1.929, 'Q': 0.095, 'R': 5.987, 'S': 6.327, 'T': 9.056,
    'U': 2.758, 'V': 0.978, 'W': 2.360, 'X': 0.150, 'Y': 1.974, 'Z': 0.074
}

def calculate_chi_square(text: str) -> float:
    """Calculates Chi-Square statistic comparing text letter counts to English distribution."""
    clean_text = [c.upper() for c in text if c.isalpha()]
    total_letters = len(clean_text)
    
    if total_letters == 0:
        return float('inf')

    counts = Counter(clean_text)
    chi_square = 0.0

    for letter, expected_pct in ENGLISH_FREQUENCIES.items():
        observed = counts.get(letter, 0)
        expected = (expected_pct / 100.0) * total_letters
        if expected > 0:
            chi_square += ((observed - expected) ** 2) / expected

    return chi_square

def chi_square_attack(ciphertext: str):
    """Evaluates all 26 shifts and returns key with lowest Chi-Square score."""
    best_key = 0
    min_score = float('inf')
    best_plaintext = ""

    for key in range(26):
        decrypted = decrypt_shift_cipher(ciphertext, key)
        score = calculate_chi_square(decrypted)
        if score < min_score:
            min_score = score
            best_key = key
            best_plaintext = decrypted

    return best_key, best_plaintext, min_score

if __name__ == "__main__":
    # Sanity Test
    sample_cipher = "Olssv dvysk" # "Hello world" with key 7
    predicted_k, dec_msg, score = chi_square_attack(sample_cipher)
    print(f"Predicted Key: {predicted_k} | Decrypted: {dec_msg} | Score: {score:.4f}")
