import secrets
import string

from src.mt_stream_cipher import encrypt_decrypt


KNOWN_TEXT = b"A" * 14
SEED_SPACE = 2 ** 16


def create_sample():
    alphabet = string.ascii_letters + string.digits + string.punctuation + " "
    prefix_length = secrets.randbelow(16) + 5

    prefix = "".join(secrets.choice(alphabet) for i in range(prefix_length))

    plaintext = (prefix + "A" * 14).encode("ascii")
    seed = secrets.randbelow(SEED_SPACE)

    ciphertext = encrypt_decrypt(plaintext, seed)

    return plaintext, ciphertext, seed


def recover_seed(ciphertext):
    matches = []

    for candidate_seed in range(SEED_SPACE):
        plaintext = encrypt_decrypt(ciphertext, candidate_seed)

        if KNOWN_TEXT in plaintext:
            matches.append((candidate_seed, plaintext))

    return matches


def demonstrate_attack():
    plaintext, ciphertext, original_seed = create_sample()

    print("\nPART A: KNOWN-PLAINTEXT ATTACK")
    print("Original 16-bit seed:", original_seed)
    print("Plaintext            :", plaintext.decode("ascii"))
    print("Ciphertext (hex)     :", ciphertext.hex())
    print("Seeds tested         :", SEED_SPACE)

    matches = recover_seed(ciphertext)

    print("Matching seeds       :", [seed for seed, data in matches])

    if len(matches) == 1:
        recovered_seed, recovered_plaintext = matches[0]

        print("Recovered seed       :", recovered_seed)
        print("Recovered plaintext  :", recovered_plaintext.decode("ascii"))
        print("Seed is correct      :", recovered_seed == original_seed)
        print("Full plaintext match :", recovered_plaintext == plaintext)
        print("Known text present   :", KNOWN_TEXT in recovered_plaintext)

    else:
        print("Expected one matching seed, found:", len(matches))


if __name__ == "__main__":
    demonstrate_attack()
