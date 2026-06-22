def check_password_strength(password: str) -> str:
    # 1. Length Verification (The Zero Point Policy)
    # Less than 8 characters results in an immediate weak classification 
    # due to exponential brute-force risk.
    if len(password) < 8:
        return "Weak"
    
    # 2. Pattern Recognition (Using efficient, short-circuiting logic)
    # Evaluates character types via C-optimized built-ins.
    has_uppercase = any(char.isupper() for char in password)
    has_digit     = any(char.isdigit() for char in password)
    
    # A character is considered a symbol if it is not alphanumeric (and not whitespace)
    has_symbol    = any(not char.isalnum() and not char.isspace() for char in password)
    
    # 3. Risk Classification Logic
    # Strong: Meets the length requirement and contains ALL three criteria
    if has_uppercase and has_digit and has_symbol:
        return "Strong"
    
    # Medium: Meets the length requirement and contains at least two criteria
    # (e.g., Upper + Digit, Upper + Symbol, or Digit + Symbol)
    criteria_count = sum([has_uppercase, has_digit, has_symbol])
    if criteria_count >= 2:
        return "Medium"
    
    # Default fallback if length is met but complexity is minimal
    return "Weak"

# --- Demonstration / Testing ---
if __name__ == "__main__":
    test_passwords = [
        "sec12",          # Short length -> Immediate Fail
        "decodelabs",       # Length ok, but missing upper, digits, and symbols
        "DecodeLabs2026",   # Length ok, has Upper + Digits (2 criteria)
        "P@ssword123!"      # Length ok, has Upper + Digits + Symbols (3 criteria)
    ]
    
    print("--- PASSWORD STRENGTH CHECKER RESULTS ---")
    for pwd in test_passwords:
        strength = check_password_strength(pwd)
        print(f"Password: {pwd:<16} | Strength Result: {strength}")