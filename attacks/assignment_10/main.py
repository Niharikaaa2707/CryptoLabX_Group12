from src.mt_stream_cipher import encrypt_decrypt
from src.known_plaintext_attack import demonstrate_attack
from src.predictable_token import demonstrate_token_attack


def demonstrate_stream_cipher():
    print("=" * 50)
    print("PART 1: MT19937 STREAM CIPHER")
    print("=" * 50)

    message = b"Cryptography Lab Assignment 10"
    seed = 12345

    ciphertext = encrypt_decrypt(message, seed)
    decrypted = encrypt_decrypt(ciphertext, seed)

    print("Test message         :", message.decode("ascii"))
    print("Seed                 :", seed)
    print("Ciphertext (hex)     :", ciphertext.hex())
    print("Decrypted message    :", decrypted.decode("ascii"))
    print("Decryption successful:", decrypted == message)


def main():
    demonstrate_stream_cipher()
    demonstrate_attack()
    demonstrate_token_attack()


if __name__ == "__main__":
    main()
