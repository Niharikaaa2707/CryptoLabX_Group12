"""
Brute-Force Cryptanalysis using Dictionary Scoring
"""

import os
from shift_cipher import decrypt_shift_cipher

def load_dictionary(dict_path: str) -> set:
    """Loads a text dictionary file into a set of uppercase words."""
    if not os.path.exists(dict_path):
        raise FileNotFoundError(f"Dictionary file not found: {dict_path}")
    with open(dict_path, 'r', encoding='utf-8') as f:
        words = set(f.read().strip().upper().split())
    return words

def dictionary_score(text: str, dictionary: set) -> int:
    """Calculates how many words in the decrypted text exist in the dictionary."""
    words = text.upper().split()
    score = sum(1 for word in words if word.strip(".,!?;:\"'") in dictionary)
    return score

def brute_force_dictionary_attack(ciphertext: str, dict_path: str):
    """Tries all 26 keys and selects the key with the highest dictionary match count."""
    dictionary = load_dictionary(dict_path)
    best_key = 0
    max_score = -1
    best_plaintext = ""

    for key in range(26):
        decrypted = decrypt_shift_cipher(ciphertext, key)
        score = dictionary_score(decrypted, dictionary)
        if score > max_score:
            max_score = score
            best_key = key
            best_plaintext = decrypted

    return best_key, best_plaintext, max_score

if __name__ == "__main__":
    # Quick Test
    dict_file = "attacks/shift_cipher_attack/dictionary/english_words.txt"
    sample_cipher = "Olssv dvysk" # "Hello world" with shift 7
    predicted_k, dec_msg, score = brute_force_dictionary_attack(sample_cipher, dict_file)
    print(f"Predicted Key: {predicted_k} | Decrypted: {dec_msg} | Score: {score}")
