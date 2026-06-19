import datetime

def get_response(user_input):
    text = user_input.lower().strip()

    # Rule 1 — greetings
    if any(word in text for word in ["hi", "hello", "hey", "howdy"]):
        return "Hello there! How can I help you?"

    # Rule 2 — farewells / exit
    elif any(word in text for word in ["bye", "goodbye", "exit", "quit"]):
        print("Goodbye! Have a great day!")
        return None  # signals the loop to stop

    # Rule 3 — name inquiry
    elif "your name" in text or "who are you" in text:
        return "I'm RuleBot — powered by if-else logic!"

    # Rule 4 — joke
    elif "joke" in text or "funny" in text:
        return "Why do programmers prefer dark mode? Light attracts bugs!"

    # Rule 5 — time/date
    elif "time" in text or "date" in text:
        now = datetime.datetime.now()
        return f"It's {now.strftime('%I:%M %p on %B %d, %Y')}."

    # Rule 6 — help
    elif "help" in text:
        return "I can respond to: greetings, jokes, time, name questions, and farewells."

    # Fallback — no rule matched
    else:
        return "I don't have a rule for that yet. Try: hi, joke, time, or bye!"


# Continuous loop — keeps the chatbot running
while True:
    user_input = input("You: ")
    response = get_response(user_input)
    
    if response is None:  # exit command was triggered
        break
    
    print(f"Bot: {response}")