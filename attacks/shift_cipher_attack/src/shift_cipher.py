"""
Shift Cipher Implementation (Encrypt & Decrypt)
"""

def encrypt_shift_cipher(plaintext: str, key: int) -> str:
    """Encrypts text using a Shift Cipher with a key from 0 to 25."""
    ciphertext = []
    key = key % 26
    for char in plaintext:
        if char.isalpha():
            start = ord('A') if char.isupper() else ord('a')
            shifted = chr((ord(char) - start + key) % 26 + start)
            ciphertext.append(shifted)
        else:
            ciphertext.append(char)
    return "".join(ciphertext)

def decrypt_shift_cipher(ciphertext: str, key: int) -> str:
    """Decrypts text using a Shift Cipher given the key."""
    return encrypt_shift_cipher(ciphertext, -key)

if __name__ == "__main__":
    # Sanity Check
    msg = "Hello, World! CryptoLabX 2026."
    k = 7
    enc = encrypt_shift_cipher(msg, k)
    dec = decrypt_shift_cipher(enc, k)
    print(f"Original:  {msg}")
    print(f"Encrypted: {enc}")
    print(f"Decrypted: {dec}")
    assert msg == dec, "Decryption failed!"
