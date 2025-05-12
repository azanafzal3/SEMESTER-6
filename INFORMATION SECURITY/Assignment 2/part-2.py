import numpy as np
import random
import matplotlib.pyplot as plt

def lfsr(seed, taps, length):
    """
    Linear Feedback Shift Register (LFSR) to generate a keystream.
    
    :param seed: Initial state of the LFSR (list of 0s and 1s).
    :param taps: Positions of the feedback taps (list of indices).
    :param length: Length of the sequence to generate.
    :return: Generated sequence of bits (list of 0s and 1s).
    """
    state = seed[:]  # Copy the initial state
    sequence = []  # Store the generated sequence

    for _ in range(length):
        # Calculate the new bit as the XOR of the tapped bits
        new_bit = sum(state[i] for i in taps) % 2
        sequence.append(state[-1])  # Output the last bit of the current state
        state = [new_bit] + state[:-1]  # Shift right and prepend the new bit

    return sequence

def generate_lfsr_sequences(n, taps):
    """
    Generates LFSR sequences for a given polynomial degree n and feedback taps.
    
    :param n: Degree of the polynomial (length of the LFSR).
    :param taps: Positions of the feedback taps (list of indices).
    :return: Generated sequence of bits (list of 0s and 1s).
    """
    seed = [random.randint(0, 1) for _ in range(n)]  # Random initial state
    max_length = (2**n) - 1  # Maximum length of the sequence
    sequence_length = 3 * max_length  # Generate 3 times the maximum length

    return lfsr(seed, taps, sequence_length)

def analyze_lfsr_sequences():
    """
    Generates and analyzes LFSR sequences for different polynomial types.
    """
    # Define polynomials and their feedback taps
    polynomials = {
        "Primitive": (4, [0, 1]),  # x^4 + x + 1 (taps at positions 0 and 1)
        "Irreducible (Non-Primitive)": (4, [0, 2]),  # x^4 + x^2 + 1 (taps at positions 0 and 2)
        "Reducible": (4, [0, 1, 2, 3])  # x^4 + x^3 + x^2 + x + 1 (taps at all positions)
    }

    for name, (n, taps) in polynomials.items():
        sequence = generate_lfsr_sequences(n, taps)
        print(f"\n{name} Polynomial (n={n}, taps={taps}):")
        print(f"Generated Sequence Length: {len(sequence)}")
        print("Sample Output (First 50 Bits):", sequence[:50])  # Print first 50 bits

        # Plot the first 200 bits of the sequence
        plt.figure(figsize=(10, 2))
        plt.plot(sequence[:200], marker='o', linestyle='None')
        plt.title(f"{name} Polynomial LFSR Output")
        plt.xlabel("Bit Position")
        plt.ylabel("Bit Value")
        plt.show()

# Run the analysis
analyze_lfsr_sequences()