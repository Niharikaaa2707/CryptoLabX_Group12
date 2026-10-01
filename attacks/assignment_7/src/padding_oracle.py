from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad


BLOCK_SIZE = 16
query_count = 0

key = b"1234567890123456"
iv = b"abcdefghijklmnop"

plaintext = b"This is a secret message."


cipher = AES.new(key, AES.MODE_CBC, iv)

ciphertext = cipher.encrypt(
    pad(plaintext, BLOCK_SIZE)
)


def padding_oracle(ciphertext):

    global query_count
    query_count += 1

    try:
        cipher = AES.new(key, AES.MODE_CBC, iv)

        decrypted = cipher.decrypt(ciphertext)

        unpad(decrypted, BLOCK_SIZE)

        return True

    except ValueError:
        return False

print("Plaintext:")
print(plaintext)

print("\nCiphertext:")
print(ciphertext)

print("\nOracle test:")
print(padding_oracle(ciphertext))

bad_ciphertext = bytearray(ciphertext)

bad_ciphertext[-1] ^= 1

print("\nModified ciphertext oracle:")
print(padding_oracle(bytes(bad_ciphertext)))

print("\nOracle queries:", query_count)
