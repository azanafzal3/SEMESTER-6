import numpy as np
import random
import matplotlib.pyplot as plt

def lfsr(seed, taps, length):
    """Linear Feedback Shift Register (LFSR) to generate keystream."""
    state = seed[:]
    sequence = []
    
    for _ in range(length):
        new_bit = sum(state[i] for i in taps) % 2  # XOR of selected taps
        sequence.append(state[-1])  # Output bit
        state = [new_bit] + state[:-1]  # Shift right
    
    return sequence

def generate_lfsr_sequences(n, taps):
    """Generates LFSR sequences for a given polynomial degree n."""
    seed = [random.randint(0, 1) for _ in range(n)]
    max_length = (2**n) - 1
    sequence_length = 3 * max_length
    
    return lfsr(seed, taps, sequence_length)

def check_polynomial(n, taps):
    """Check if a polynomial is primitive, irreducible, or reducible."""
    max_length = (2**n) - 1
    sequence = generate_lfsr_sequences(n, taps)
    
    if len(set(sequence)) == 2 and len(sequence) == max_length * 3:
        return "Primitive"
    elif len(set(sequence)) == 2:
        return "Irreducible (Non-Primitive)"
    else:
        return "Reducible"

def draw_lfsr(n, taps):
    """Draw ASCII representation of LFSR."""
    lfsr_diagram = ""
    for i in range(n):
        lfsr_diagram += f"[S{i}]--"
        if i in taps:
            lfsr_diagram += "XOR--"
    lfsr_diagram += "[Output]"
    print("\nLFSR Structure:")
    print(lfsr_diagram)

def analyze_lfsr_sequences():
    """Generate and analyze LFSR sequences for different polynomial types."""
    polynomials = {
        "Primitive": (5, [0, 2]),  # x^5 + x^2 + 1
        "Irreducible (Non-Primitive)": (5, [0, 1]),  # x^5 + x + 1
        "Reducible": (5, [0, 3])  # x^5 + x^3 + 1
    }
    
    for name, (n, taps) in polynomials.items():
        sequence = generate_lfsr_sequences(n, taps)
        print(f"\n{name} Polynomial (n={n}, taps={taps}):")
        print(f"Generated Sequence Length: {len(sequence)}")
        print("Output:", sequence[:50])  # Print first 50 bits

        # Plot sequence
        plt.figure(figsize=(10, 2))
        plt.plot(sequence[:200], marker='o', linestyle='None')
        plt.title(f"{name} Polynomial LFSR Output")
        plt.xlabel("Bit Position")
        plt.ylabel("Bit Value")
        plt.show()

        # Draw LFSR structure
        draw_lfsr(n, taps)
    
    # Ask user for additional polynomials
    for i in range(3):
        print(f"\nEnter details for polynomial {i + 1}:")
        n = int(input("Enter the degree of polynomial (n): "))
        taps = list(map(int, input("Enter tap positions separated by space (e.g., 0 2): ").split()))
        
        sequence = generate_lfsr_sequences(n, taps)
        poly_type = check_polynomial(n, taps)
        print(f"\nUser-Defined Polynomial {i + 1} (n={n}, taps={taps}):")
        print(f"Polynomial Type: {poly_type}")
        print(f"Generated Sequence Length: {len(sequence)}")
        print("Output:", sequence[:50])
        
        # Plot user-defined sequence
        plt.figure(figsize=(10, 2))
        plt.plot(sequence[:200], marker='o', linestyle='None')
        plt.title(f"User-Defined Polynomial {i + 1} LFSR Output")
        plt.xlabel("Bit Position")
        plt.ylabel("Bit Value")
        plt.show()

        # Draw LFSR structure
        draw_lfsr(n, taps)

# Run the analysis
analyze_lfsr_sequences()
