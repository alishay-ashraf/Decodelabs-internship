import random
import string

def generate_password():
    # --- PHASE 1: INPUT & VALIDATION ---
    print("--- DecodeLabs Enterprise Password Generator ---")
    try:
        # Request password length from the user
        length = int(input("Enter desired password length (e.g., 8): "))
        
        # Rigorous input validation to ensure structural integrity
        if length < 4:
            print("Error: For security and stability, minimum length must be at least 4.")
            return
    except ValueError:
        print("Error: Invalid input. Please enter a valid target integer.")
        return

    # --- PHASE 2: PROCESS (CORE LOGIC ENGINE) ---
    # Pool available character sets using the standard string library
    letters = string.ascii_letters  # Contains both uppercase and lowercase letters
    digits = string.digits          # Contains numbers 0-9
    
    # Combine the character sets
    all_characters = letters + digits
    
    # Selection algorithm to transform the length integer into a complex string
    # random.choices() handles random selection with replacement efficiently
    password_list = random.choices(all_characters, k=length)
    
    # Convert list of characters back into a solid string format
    password = "".join(password_list)

    # --- PHASE 3: OUTPUT DELIVERY ---
    print("\n--- SECURE CREDENTIAL PROVISION ---")
    print(f"Generated Password: {password}")
    print("-----------------------------------")

# Execute the tool
if __name__ == "__main__":
    generate_password()