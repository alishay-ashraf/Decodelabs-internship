import java.util.InputMismatchException;
import java.util.Scanner;

// ==========================================
// 1. BANK ACCOUNT CLASS (The Data Vault)
// ==========================================
class BankAccount {
    private final String accountNumber;
    private double balance;

    public BankAccount(String accountNumber, double initialBalance) {
        this.accountNumber = accountNumber;
        this.balance = Math.max(initialBalance, 0.0);
    }

    public double getBalance() {
        return this.balance;
    }

    public String getAccountNumber() {
        return this.accountNumber;
    }

    public void deposit(double amount) {
        if (amount > 0) {
            this.balance += amount;
            System.out.printf("Successfully deposited: $%.2f%n", amount);
        } else {
            System.out.println("Error: Deposit amount must be positive.");
        }
    }

    public boolean withdraw(double amount) {
        if (amount <= 0) {
            System.out.println("Error: Withdrawal amount must be positive.");
            return false;
        }
        
        if (amount > this.balance) {
            System.out.println("Transaction Failed: Insufficient funds available.");
            return false;
        }

        this.balance -= amount;
        System.out.printf("Successfully withdrew: $%.2f%n", amount);
        return true;
    }
}

// ==========================================
// 2. ATM CLASS (The Interaction Hub)
// ==========================================
class ATM {
    private final BankAccount linkedAccount;
    private final Scanner scanner;

    public ATM(BankAccount account) {
        this.linkedAccount = account;
        this.scanner = new Scanner(System.in);
    }

    public void startTerminal() {
        System.out.println("===========================================");
        System.out.println("       WELCOME TO DECODELABS BANKING       ");
        System.out.println("===========================================");
        System.out.println("Account Verified: " + linkedAccount.getAccountNumber());
        
        boolean exitTerminal = false;
        while (!exitTerminal) {
            displayMenu();
            int choice = getUserChoice();

            switch (choice) {
                case 1:
                    checkBalanceTransaction();
                    break;
                case 2:
                    handleDepositTransaction();
                    break;
                case 3:
                    handleWithdrawalTransaction();
                    break;
                case 4:
                    System.out.println("\nThank you for choosing DecodeLabs. Goodbye!");
                    exitTerminal = true;
                    break;
                default:
                    System.out.println("Invalid selection. Please choose an option between 1 and 4.");
            }
        }
    }

    private void displayMenu() {
        System.out.println("\n-------------------------------------------");
        System.out.println("ATM MAIN MENU:");
        System.out.println("1. Check Balance");
        System.out.println("2. Deposit Funds");
        System.out.println("3. Withdraw Funds");
        System.out.println("4. Exit Card");
        System.out.println("-------------------------------------------");
        System.out.print("Please enter your selection (1-4): ");
    }

    private int getUserChoice() {
        try {
            int input = scanner.nextInt();
            scanner.nextLine(); 
            return input;
        } catch (InputMismatchException e) {
            scanner.nextLine(); 
            return -1; 
        }
    }

    private void checkBalanceTransaction() {
        System.out.println("\n--- BALANCE ENQUIRY ---");
        System.out.printf("Current available balance: $%.2f%n", linkedAccount.getBalance());
    }

    private void handleDepositTransaction() {
        System.out.println("\n--- DEPOSIT TRANSACTION ---");
        System.out.print("Enter deposit amount: $");
        double amount = getValidDoubleInput();
        
        if (amount >= 0) {
            linkedAccount.deposit(amount);
        }
    }

    private void handleWithdrawalTransaction() {
        System.out.println("\n--- WITHDRAWAL TRANSACTION ---");
        System.out.print("Enter withdrawal amount: $");
        double amount = getValidDoubleInput();
        
        if (amount >= 0) {
            linkedAccount.withdraw(amount);
        }
    }

    private double getValidDoubleInput() {
        try {
            double value = scanner.nextDouble();
            scanner.nextLine(); 
            if (value < 0) {
                System.out.println("Error: Negative values are completely blocked by the secure terminal.");
                return -1;
            }
            return value;
        } catch (InputMismatchException e) {
            System.out.println("Error: Invalid numeric input pattern detected. Transaction canceled.");
            scanner.nextLine(); 
            return -1;
        }
    }
}

// ==========================================
// 3. MAIN RUNTIME EXECUTION CLASS
// ==========================================
public class Main {
    public static void main(String[] args) {
        BankAccount userAccount = new BankAccount("DL-2026-9843", 1250.75);
        ATM atmTerminal = new ATM(userAccount);
        atmTerminal.startTerminal();
    }
}