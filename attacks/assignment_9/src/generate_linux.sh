
#!/bin/bash

set -e

mkdir -p outputs/data

SIZE=1048576

echo "Generating 1 MB using Linux /dev/urandom..."
head -c "$SIZE" /dev/urandom > outputs/data/linux_urandom.bin

echo "Generating 1 MB using OpenSSL..."
openssl rand -out outputs/data/openssl_rand.bin "$SIZE"

echo "Checking generated file sizes..."
wc -c outputs/data/linux_urandom.bin outputs/data/openssl_rand.bin

echo "Linux random data generation completed."

