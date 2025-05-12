import numpy as np
import random

def lfsr(seed, taps, length):
    """Linear Feedback Shift Register (LFSR) to generate keystream."""
    state = seed[:]
    keystream = []
    
    for _ in range(length):
        new_bit = sum(state[i] for i in taps) % 2  # XOR of selected taps
        keystream.append(state[-1])  # Output bit
        state = [new_bit] + state[:-1]  # Shift right
    
    return keystream

def text_to_binary(text):
    """Convert ASCII text to binary."""
    return [format(ord(c), '08b') for c in text]

def binary_to_text(binary):
    """Convert binary back to ASCII text."""
    chars = [binary[i:i+8] for i in range(0, len(binary), 8)]
    return ''.join(chr(int(c, 2)) for c in chars)

def xor_binary(bin_text, keystream):
    """XOR binary text with keystream."""
    return ''.join(str(int(bin_text[i]) ^ keystream[i]) for i in range(len(bin_text)))

# User input
plaintext = input("Enter plaintext: ")
while True:
    n = int(input("Enter degree of polynomial (n >= 4): "))
    if n >= 4:
        break
    print("Degree must be at least 4.")

while True:
    primitive_poly_taps = list(map(int, input(f"Enter space-separated tap positions (between 0 and {n-1}): ").split()))
    if all(0 <= t < n for t in primitive_poly_taps):
        break
    print(f"Invalid tap positions. Ensure values are between 0 and {n-1}.")

seed = [random.randint(0, 1) for _ in range(n)]  # Random seed

plaintext_binary_list = text_to_binary(plaintext)
plaintext_binary = ''.join(plaintext_binary_list)
keystream = lfsr(seed, primitive_poly_taps, len(plaintext_binary))

# Display ASCII and binary values
print("\nCharacter-wise ASCII and Binary Representation:")
for char, binary in zip(plaintext, plaintext_binary_list):
    print(f"Character: {char} | ASCII: {ord(char)} | Binary: {binary}")

print("\nKeystream is generated using an LFSR with the given polynomial taps.")
print("Initial seed:", ''.join(map(str, seed)))
print("Keystream Generation: Feedback XOR of specified tap positions.")

# Encryption
ciphertext_binary = xor_binary(plaintext_binary, keystream)
ciphertext = binary_to_text(ciphertext_binary)

# Decryption (Same process since XOR is reversible)
decrypted_binary = xor_binary(ciphertext_binary, keystream)
decrypted_text = binary_to_text(decrypted_binary)

# Output
print("\nPlaintext:", plaintext)
print("Binary Plaintext:", plaintext_binary)
print("Keystream:", ''.join(map(str, keystream)))
print("Ciphertext (Binary):", ciphertext_binary)
print("Decrypted Text:", decrypted_text)

# Plaintext Attack: Recovering the Feedback Polynomial
# Step 1: Capture plaintext-ciphertext pairs
# Step 2: Derive keystream by XORing plaintext & ciphertext
# Step 3: Use keystream bits to reconstruct LFSR feedback equation
