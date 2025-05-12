def lfsr(seed, polynomial, sequence_length):
    """
    Generates a sequence using a Linear Feedback Shift Register (LFSR).
    """
    state = seed
    sequence = []
    for _ in range(sequence_length):
        sequence.append(state & 1)
        feedback = 0
        for i in polynomial:
            feedback ^= (state >> (i - 1)) & 1
        state = (state >> 1) | (feedback << (max(polynomial) - 1))
    return sequence

def find_period(sequence):
    """Finds the actual period of the sequence."""
    for period in range(1, len(sequence)//2 + 1):
        if all(sequence[i] == sequence[i % period] for i in range(period, len(sequence))):
            return period
    return len(sequence)

def analyze_polynomial(poly_name, poly_positions, initial_value, sequence_length):
    """Analyzes a single polynomial."""
    sequence = lfsr(initial_value, poly_positions, sequence_length)
    period = find_period(sequence)
    max_possible = (2**max(poly_positions)) - 1
    
    print(f"\nAnalysis for {poly_name} (taps at {poly_positions}):")
    print(f"First 20 bits: {sequence[:20]}")
    print(f"Actual period: {period}")
    print(f"Maximum possible period: {max_possible}")
    
    # Determine polynomial type
    if period == max_possible:
        poly_type = "Primitive (maximum-length sequence)"
    elif period == 1:
        poly_type = "Reducible (degenerate sequence)"
    else:
        poly_type = "Irreducible but not primitive"
    
    print(f"Polynomial type: {poly_type}")
    return poly_type

def get_user_polynomials():
    """Gets 3 additional polynomials from the user."""
    user_polys = {}
    print("\n" + "="*50)
    print("Now please enter 3 additional polynomials to analyze")
    print("Format: For x^4 + x + 1, enter '4,1'")
    print("="*50)
    
    for i in range(3):
        while True:
            try:
                input_str = input(f"Enter polynomial {i+1} (degree,tap1,tap2,...): ")
                parts = [int(x) for x in input_str.split(',')]
                degree = parts[0]
                taps = parts[1:]
                if all(1 <= tap <= degree for tap in taps):
                    poly_name = f"x^{degree} + " + " + ".join(f"x^{tap}" for tap in taps)
                    user_polys[poly_name] = taps
                    break
                print("Error: Tap positions must be between 1 and the degree")
            except:
                print("Invalid input. Please try again.")
    return user_polys

def main():
    # Built-in polynomials
    polynomials = {
        "x^4 + x + 1": [4, 1],
        "x^4 + x^2 + 1": [4, 2],
        "x^4 + x^3 + x^2 + x + 1": [4, 3, 2, 1]
    }
    
    initial_value = 0b1001
    sequence_length = 45  # 3*(2^4-1) for n=4
    
    # Analyze built-in polynomials
    print("=== Built-in Polynomial Analysis ===")
    for poly_name, poly_pos in polynomials.items():
        analyze_polynomial(poly_name, poly_pos, initial_value, sequence_length)
    
    # Get and analyze user polynomials
    user_polynomials = get_user_polynomials()
    print("\n=== User Polynomial Analysis ===")
    for poly_name, poly_pos in user_polynomials.items():
        degree = max(poly_pos)
        analyze_polynomial(poly_name, poly_pos, initial_value, 3*(2**degree - 1))

if __name__ == "__main__":
    main()