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


def padding_oracle(iv, ciphertext):

    global query_count
    query_count += 1

    try:
        cipher = AES.new(key, AES.MODE_CBC, iv)

        decrypted = cipher.decrypt(ciphertext)

        unpad(decrypted, BLOCK_SIZE)

        return True

    except ValueError:
        return False

def attack_block(previous_block, target_block):

    intermediate = bytearray(BLOCK_SIZE)
    recovered = bytearray(BLOCK_SIZE)
    modified = bytearray(previous_block)

    for pos in range(BLOCK_SIZE - 1, -1, -1):

        padding = BLOCK_SIZE - pos

        for i in range(pos + 1, BLOCK_SIZE):
            modified[i] = intermediate[i] ^ padding

        for guess in range(256):

            modified[pos] = guess

            if padding_oracle(bytes(modified), target_block):
                intermediate[pos] = guess ^ padding
                recovered[pos] = intermediate[pos] ^ previous_block[pos]

                print(
                    "Recovered:",
                    chr(recovered[pos]) if 32 <= recovered[pos] <= 126 else recovered[pos]
                )

                break

    return bytes(recovered)

print("Plaintext:")
print(plaintext)

print("\nCiphertext:")
print(ciphertext)

print("\nOracle test:")
print(padding_oracle(iv, ciphertext))

bad_ciphertext = bytearray(ciphertext)
bad_ciphertext[-1] ^= 1

print("\nModified ciphertext oracle:")
print(padding_oracle(iv, bytes(bad_ciphertext)))

print("\nStarting attack...")

first_block = ciphertext[:BLOCK_SIZE]

recovered_block = attack_block(iv, first_block)

print("\nRecovered first block:")
print(recovered_block)

print("\nOracle queries:", query_count)
