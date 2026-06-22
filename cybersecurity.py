def caesar_encrypt(plaintext, shift):
    """
    Encrypts the plaintext by shifting characters by the specified shift amount.
    Handles both uppercase and lowercase letters while keeping non-alphabet characters intact.
    """
    ciphertext = ""
    for char in plaintext:
        if char.isupper():
            # Apply wrapping math for uppercase letters (ASCII 65)
            ciphertext += chr((ord(char) - 65 + shift) % 26 + 65)
        elif char.islower():
            # Apply wrapping math for lowercase letters (ASCII 97)
            ciphertext += chr((ord(char) - 97 + shift) % 26 + 97)
        else:
            # Leave spaces and punctuation unchanged
            ciphertext += char
    return ciphertext

def caesar_decrypt(ciphertext, shift):
    """
    Decrypts the ciphertext by reversing the shift (shifting backwards).
    """
    # Decryption is logically the inverse operation of encryption
    return caesar_encrypt(ciphertext, -shift)

# --- Main Demonstration Program ---
def main():
    print("=== DecodeLabs: Project 2 - Cryptographic Phase ===")
    
    # 1. Get user input
    user_text = input("Enter the text to encrypt: ")
    
    while True:
        try:
            shift_key = int(input("Enter shift key (integer, e.g., 3): "))
            break
        except ValueError:
            print("Please enter a valid integer for the shift key.")
            
    print("-" * 50)
    
    # 2. Encrypt the text
    encrypted_text = caesar_encrypt(user_text, shift_key)
    
    # 3. Decrypt the text back
    decrypted_text = caesar_decrypt(encrypted_text, shift_key)
    
    # 4. Display all outputs
    print(f"Original Plaintext : {user_text}")
    print(f"Encrypted Ciphertext: {encrypted_text}")
    print(f"Decrypted Plaintext : {decrypted_text}")
    print("-" * 50)

if __name__ == "__main__":
    main()