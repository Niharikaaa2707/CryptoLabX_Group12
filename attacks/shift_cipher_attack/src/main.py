"""
Main Driver Script - Cryptanalysis Comparison Engine
"""

from shift_cipher import encrypt_shift_cipher
from brute_force_dictionary import brute_force_dictionary_attack
from chi_square_attack import chi_square_attack

def run_experiments():
    dict_path = "attacks/shift_cipher_attack/dictionary/english_words.txt"
    
    test_cases = [
        ("The quick brown fox jumps over the lazy dog", 12),
        ("CryptoLabX security testing protocol", 3),
        ("Attack at dawn", 7),                       # Short text
        ("Zzz qqq xxx rrr", 19)                       # Non-standard / gibberish text
    ]

    print(f"{'Test Case':<35} | {'Actual Key':<10} | {'Dict Key':<8} | {'Chi2 Key':<8} | {'Dict Correct?':<13} | {'Chi2 Correct?'}")
    print("-" * 95)

    for plaintext, actual_key in test_cases:
        ciphertext = encrypt_shift_cipher(plaintext, actual_key)
        
        dict_k, _, _ = brute_force_dictionary_attack(ciphertext, dict_path)
        chi2_k, _, _ = chi_square_attack(ciphertext)

        dict_ok = "YES" if dict_k == actual_key else "NO"
        chi2_ok = "YES" if chi2_k == actual_key else "NO"

        print(f"{plaintext[:33]:<35} | {actual_key:<10} | {dict_k:<8} | {chi2_k:<8} | {dict_ok:<13} | {chi2_ok}")

if __name__ == "__main__":
    run_experiments()
