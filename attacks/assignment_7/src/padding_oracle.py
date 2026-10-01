from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad


BLOCK_SIZE = 16
query_count = 0

key = b"1234567890123456"
iv = b"abcdefghijklmnop"

plaintext = b"This is a secret message."

# Encrypt plaintext
cipher = AES.new(key, AES.MODE_CBC, iv)
ciphertext = cipher.encrypt(pad(plaintext, BLOCK_SIZE))


# Padding oracle
def padding_oracle(test_iv, test_ciphertext):
    global query_count
    query_count += 1

    try:
        cipher = AES.new(key, AES.MODE_CBC, test_iv)
        decrypted = cipher.decrypt(test_ciphertext)
        unpad(decrypted, BLOCK_SIZE)
        return True
    except ValueError:
        return False


# Recover one plaintext block
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

                # Check for false positive padding
                if pos > 0:
                    check = bytearray(modified)
                    check[pos - 1] ^= 1

                    if not padding_oracle(bytes(check), target_block):
                        continue

                intermediate[pos] = guess ^ padding
                recovered[pos] = intermediate[pos] ^ previous_block[pos]

                break

    return bytes(recovered)


# Split ciphertext into blocks
blocks = [
    ciphertext[i:i + BLOCK_SIZE]
    for i in range(0, len(ciphertext), BLOCK_SIZE)
]


# Recover all plaintext blocks
recovered_plaintext = b""
previous_block = iv

for block in blocks:

    recovered_block = attack_block(previous_block, block)

    recovered_plaintext += recovered_block

    previous_block = block


# Remove PKCS#7 padding
recovered_plaintext = unpad(recovered_plaintext, BLOCK_SIZE)


print("Original plaintext:")
print(plaintext)

print("\nCiphertext:")
print(ciphertext)

print("\nRecovered plaintext:")
print(recovered_plaintext)

print("\nOracle queries:")
print(query_count)
