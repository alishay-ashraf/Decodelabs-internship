import re
import hmac
import hashlib

class SecureERC20WalletSystem:
    def __init__(self):
        # Private Ledger (BalancesMapper) - Simulated internal state [cite: 131, 152]
        # Using float/Decimal simulations for double-precision verification [cite: 21, 27]
        self.__balances = {
            "0x95222290DD7278Aa3Ddd389Cc1E1d165CC4BAfe5": 1500.50,
            "0x9965503B1a059419742974A4ff2E408AF6251CE4": 250.75,
            "0x281025AF6251CE4A4ff2E408AF625165CC4BAfe5": 0.00
        }
        # Simulated server-side secret key for validating the mockup "signature"
        self.__secret_key = b"decodelabs_secret_key"

    # --- OUTPUT PHASE: Getters & Syncing ---
    def balanceOf(self, account: str) -> float:
        """The Getter. Gasless state-reading. Returns the exact token balance[cite: 78, 79]."""
        return self.__balances.get(account, 0.0)

    # --- INPUT PHASE: Secure Data Acquisition & Sanitization ---
    def validate_target_address(self, address: str) -> bool:
        """Regex validation for 0x hex format and length (42 characters)[cite: 103, 104]."""
        if not re.match(r"^0x[a-fA-F0-9]{40}$", address):
            print("[INPUT ERROR] Invalid Address Format! Must be a 42-character '0x' hex string.")
            return False
        return True

    def validate_amount_sanity(self, amount_str: str) -> tuple[bool, float]:
        """Validates that the amount is a valid positive numeric entity[cite: 106]."""
        try:
            amount = float(amount_str)
            if amount < 0:
                print("[INPUT ERROR] Value Error: Transfer amount cannot be negative[cite: 106].")
                return False, 0.0
            return True, amount
        except ValueError:
            print("[INPUT ERROR] Value Error: Amount must be a valid number.")
            return False, 0.0

    def verify_mock_signature(self, message: str, signature: str) -> bool:
        """Cryptographic authorization simulation protecting self-custody[cite: 108, 133]."""
        expected_sig = hmac.new(self.__secret_key, message.encode(), hashlib.sha256).hexdigest()
        return hmac.compare_digest(expected_sig, signature)

    # --- PROCESS PHASE: Financial Transformation Engine ---
    def transfer(self, sender: str, to: str, amount: float) -> bool:
        """The Setter. Executes strict, sequential financial logic to alter the private state[cite: 80, 81, 128]."""
        
        # 1. Zero-Value Check (ERC-20 standard treats 0-value transfers as valid) 
        if amount == 0.0:
            print("[SYSTEM WARNING] Zero-Value Transfer initiated.")
            self.__emit_transfer_event(sender, to, amount)
            return True

        # 2. Authorization & Overdraft Check [cite: 135, 157]
        sender_balance = self.balanceOf(sender)
        if amount > sender_balance:
            print(f"[SECURITY REJECTION] Overdraft Attempted! "
                  f"Requested: {amount}, Available: {sender_balance} ")
            return False

        # 3. Deterministic State Modification (State Subtraction & Addition Logic) [cite: 46, 49, 137]
        self.__balances[sender] -= amount  # State Subtraction [cite: 49, 65]
        
        if to not in self.__balances:
            self.__balances[to] = 0.0
        self.__balances[to] += amount

        # --- OUTPUT PHASE: Permanent Logging & Synchronization ---
        self.__emit_transfer_event(sender, to, amount)
        return True

    def __emit_transfer_event(self, sender: str, to: str, amount: float):
        """Simulates on-chain event emission and ledger synchronization[cite: 40, 157]."""
        print("\n" + "="*50)
        print("         SUCCESSFUL TRANSACTION RECEIPT [cite: 41, 44]")
        print("="*50)
        print(f" EVENT   : Transfer(sender={sender},\n                    recipient={to},\n                    value={amount}) ")
        print(f" STATUS  : Finalized State Updated [cite: 42, 43]")
        print(f" SENDER  : New Balance = {self.balanceOf(sender)}")
        print(f" RECEIVER: New Balance = {self.balanceOf(to)}")
        print("="*50 + "\n")


# --- RUNNING THE APPLICATION MAIN WORKFLOW ---
if __name__ == "__main__":
    wallet_app = SecureERC20WalletSystem()
    
    # Established Sender Account
    sender_address = "0x95222290DD7278Aa3Ddd389Cc1E1d165CC4BAfe5"
    
    # Mocking generating a secure cryptographic token on the front-end/wallet system
    # Message format: "sender_address" -> used to prove caller identity
    valid_signature = hmac.new(b"decodelabs_secret_key", sender_address.encode(), hashlib.sha256).hexdigest()

    print("--- DECODELABS INDUSTRIAL TRAINING KIT: PROJECT 3 --- [cite: 1, 2, 3]")
    print(f"Logged in as Sender: {sender_address}")
    print(f"Initial Balance: {wallet_app.balanceOf(sender_address)} TOKENS\n")

    # ==========================================
    # STEP 1: INPUT PHASE (Secure Data Acquisition) [cite: 88, 91, 92]
    # ==========================================
    raw_target_address = input("Enter Target Recipient Address (0x format): ").strip()
    raw_amount = input("Enter Amount to Transfer: ").strip()

    # Perform Rigorous Sanitization Checkpoints [cite: 92, 101]
    if not wallet_app.validate_target_address(raw_target_address):
        exit()

    is_amount_sane, sanitized_amount = wallet_app.validate_amount_sanity(raw_amount)
    if not is_amount_sane:
        exit()

    # Cryptographic Authentication Checkpoint [cite: 101, 107]
    if not wallet_app.verify_mock_signature(sender_address, valid_signature):
        print("[SECURITY REJECTION] Critical Authentication Failure! Signature mismatch[cite: 108].")
        exit()

    # ==========================================
    # STEP 2 & 3: PROCESS & OUTPUT PHASES [cite: 93, 95]
    # ==========================================
    print("\n[SYSTEM] Packaging data into core transaction pipeline... [cite: 75]")
    wallet_app.transfer(sender=sender_address, to=raw_target_address, amount=sanitized_amount)