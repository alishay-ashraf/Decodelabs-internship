import os
import sys
from google import genai
from google.genai import types

def main():
    # 1. Frontier Connection: Establish a secure connection using the official SDK
    # The client automatically inherits the GEMINI_API_KEY environment variable.
    if not os.environ.get("GEMINI_API_KEY"):
        print("❌ Error: GEMINI_API_KEY environment variable not found.")
        print("Please set it before running the script.")
        sys.exit(1)
        
    try:
        client = genai.Client()
    except Exception as e:
        print(f"❌ Failed to initialize GenAI Client: {e}")
        sys.exit(1)

    # 2. In-Memory Array: Initialize a live local list to hold session data
    # We use a standard Python list to manage our stateful chat history.
    conversation_history = []
    
    print("====================================================")
    print("🤖 DecodeLabs Custom Chatbot with Memory Initialized")
    print("Type your message and press Enter. Type 'exit' to quit.")
    print("====================================================\n")

    while True:
        try:
            # Gather user input
            user_input = input("👤 You: ")
            
            # Check for termination command
            if user_input.strip().lower() == 'exit':
                print("\n👋 Goodbye! Session closed.")
                break
                
            # ⚠️ Structural Validation Gate (Edge Case Protection)
            # Blocks empty or whitespace-only strings locally before network transmission
            if not user_input.strip():
                print("⚠️ System Warning: Cannot send an empty message. Please try again.")
                continue

            # 3. Dynamic Appending (Step 1): Structure and append user input to history
            # Modern SDKs require a Content schema with 'role' and 'parts'
            user_message = types.Content(
                role="user",
                parts=[types.Part.from_text(text=user_input)]
            )
            conversation_history.append(user_message)

            # 3. Dynamic Appending (Step 2): Transmit complete history payload to the API
            print("🤖 Thinking...")
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=conversation_history, # Send the entire array to maintain state
            )
            
            # Extract the raw model text response
            model_text = response.text
            print(f"\n🤖 Gemini: {model_text}\n")
            
            # 3. Dynamic Appending (Step 3): Append model response back into the history array
            model_message = types.Content(
                role="model",
                parts=[types.Part.from_text(text=model_text)]
            )
            conversation_history.append(model_message)

        except Exception as e:
            # Gracefully handle API failures, rate limits, or unexpected payload issues
            print(f"\n❌ An error occurred during transmission: {e}")
            print("Your conversation history up to this point has been preserved.\n")

if __name__ == "__main__":
    main()