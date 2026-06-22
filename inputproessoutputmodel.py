def main():
    # STORAGE: Initialize the volatile container (The list lives in Heap memory)
    my_tasks = []
    
    print("=" * 40)
    print("   DECODELABS TASK ENGINE v1.0   ")
    print("=" * 40)
    
    while True:
        # DISPLAY: Show Menu Options
        print("\n[1] Add Task")
        print("[2] View Tasks")
        print("[3] Exit Engine")
        
        # INPUT: Gather User Choice
        choice = input("\nSelect an option (1-3): ").strip()
        
        # PROCESS & MODIFY: Logic handling
        if choice == "1":
            new_task = input("Enter the task description: ").strip()
            if new_task:
                # Amortized O(1) Time Complexity operation
                my_tasks.append(new_task)
                print(f"✔️ Task successfully added to memory.")
            else:
                print("❌ Task description cannot be empty.")
                
        elif choice == "2":
            # DISPLAY: The Read Operation using an Iterator Loop
            print("\n--- CURRENT TASKS ---")
            if not my_tasks:
                print("Your list is empty. No tasks found in heap storage.")
            else:
                for index, task in enumerate(my_tasks, start=1):
                    print(f"{index}. {task}")
            print("---------------------")
            
        elif choice == "3":
            print("\nShutting down engine. Goodbye, Developer!")
            break
            
        else:
            print("❌ Invalid selection. Please choose 1, 2, or 3.")

if __name__ == "__main__":
    main()