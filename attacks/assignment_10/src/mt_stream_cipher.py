import random


def generate_keystream(seed, length):
    generator = random.Random(seed)
    keystream = bytearray()

    for i in range(length):
        keystream.append(generator.getrandbits(8))

    return bytes(keystream)


def encrypt_decrypt(data, seed):
    keystream = generate_keystream(seed, len(data))
    result = bytearray()

    for i in range(len(data)):
        result.append(data[i] ^ keystream[i])

    return bytes(result)


if __name__ == "__main__":
    message = b"Cryptography Lab Assignment 10"
    seed = 12345

    ciphertext = encrypt_decrypt(message, seed)
    decrypted = encrypt_decrypt(ciphertext, seed)

    print("Original message :", message.decode("ascii"))
    print("Ciphertext (hex) :", ciphertext.hex())
    print("Decrypted message:", decrypted.decode("ascii"))
    print("Decryption successful:", decrypted == message)
