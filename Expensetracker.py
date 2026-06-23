# Initialize the accumulator variable
total_spent = 0.0

print("--- Welcome to the Expense Tracker ---")
print("Enter your expenses one by one.")
print("Type 'done' or 'exit' when you are finished to see the total.\n")

# Start an infinite loop to collect expenses
while True:
    user_input = input("Enter expense amount ($): ").strip().lower()
    
    # Check if the user wants to stop
    if user_input in ['done', 'exit']:
        break
        
    try:
        # Convert the input string to a float (decimal number)
        expense = float(user_input)
        
        # Check for negative amounts
        if expense < 0:
            print("Expenses cannot be negative. Please enter a valid amount.")
            continue
            
        # The Accumulator: Add the new expense to the existing total
        total_spent = total_spent + expense
        print(add_expense_msg := f"Added ${expense:.2f}. Current total: ${total_spent:.2f}\n")
        
    except ValueError:
        # Handle cases where the input isn't a valid number or the exit command
        print("Invalid input! Please enter a number or type 'done' to finish.\n")

# Final output
print("--- Summary ---")
print(f"Total Spent: ${total_spent:.2f}")
print("Thank you for using Expense Tracker!")