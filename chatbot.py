from datetime import datetime
import pytz

def chatbot():
    name = input("Chatbot: Hi there! What's your name?\nYou: ")
    print(f"Chatbot: Hi {name}! I'm your friendly chatbot. Type 'bye' to exit.\n")

    while True:
        user_input = input(f"{name}: ").lower()

        if user_input in ['hi', 'hello', 'hey']:
            print(f"Chatbot: Hello {name}! How can I help you today?")

        elif "your name" in user_input:
            print("Chatbot: I am a simple rule-based chatbot.")

        elif "how are you" in user_input:
            print("Chatbot: I'm doing great, thank you! How about you?")

        elif "time" in user_input:
          
            ist = pytz.timezone('Asia/kolkata')
            now = datetime.now(ist)
            formatted_time = now.strftime("%I:%M:%S %p") 
            print(f"Chatbot: The current time is {formatted_time}")

        elif "date" in user_input:
            today = datetime.now().strftime("%B %d, %Y")
            print(f"Chatbot: Today's date is {today}")

        elif "bye" in user_input or "exit" in user_input:
            print(f"Chatbot: Goodbye, {name}! Have a great day!")
            break

        elif "help" in user_input:
            print("Chatbot: I can tell you the time, date, or just chat! Ask me anything.")

        else:
            print("Chatbot: I'm not sure I understand. Could you please rephrase?")


chatbot()


