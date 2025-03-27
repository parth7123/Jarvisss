import cohere  # type: ignore
from rich import print  # type: ignore
import os
from dotenv import load_dotenv  # type: ignore

# Load environment variables from .env file
load_dotenv()

# Get API key from environment variable
CohereAPIKey = os.getenv("CO_API_KEY")

if not CohereAPIKey:
    raise ValueError("Cohere API key not found. Please set CO_API_KEY in your .env file.")

# Initialize Cohere client
co = cohere.Client(api_key=CohereAPIKey)

# Define a list of recognized function keywords for task categorization.
# Recognized functions
funcs = [
    "exit", "general", "realtime", "open", "close", "play",
    "generate image", "system", "content", "google search",
    "youtube search", "reminder", "homeautomation",
    "call", "send message", "accept call", "reject call",
    "excel"
]


# Initialize an empty list to store user messages.
messages = []

# Define the preamble that guides the AI model on how to categorize queries.
preamble = """
You are a very accurate Decision-Making Model, which decides what kind of a query is given to you.
You will decide whether a query is a 'general' query, a 'realtime' query, or is asking to perform any task or automation like 'open facebook, instagram', 'send a WhatsApp message', 'make a call', 'work with Excel', or control home automation devices.
*** Do not answer any query, just decide what kind of query is given to you. ***

-> Respond with 'general ( query )' if a query can be answered by a conversational AI and doesn't require up-to-date information.

-> Respond with 'realtime ( query )' if a query requires up-to-date information.

-> Respond with 'open (application name or website name)' if a query asks to open an application.

-> Respond with 'close (application name)' if a query asks to close an application.

-> Respond with 'play (song name)' if a query asks to play a song.

-> Respond with 'generate image (image prompt)' if a query asks to generate an image.

-> Respond with 'reminder (datetime with message)' if a query asks to set a reminder.

-> Respond with 'system (task name)' if a query asks to adjust system settings (e.g., mute, volume up).

-> Respond with 'content (topic)' if a query asks to write content.

-> Respond with 'google search (topic)' if a query asks to search something on Google.

-> Respond with 'youtube search (topic)' if a query asks to search something on YouTube.

-> Respond with 'homeautomation (device action)' if a query asks to control home appliances.

-> **Respond with 'call (contact name)'** if a query asks to make a call , such as:
   - 'Call John ' → 'call John'
   - 'Make a call to Dad' → 'call Dad'

-> **Respond with 'accept call' or 'reject call'** if a query asks to accept or reject an incoming call.

-> **Respond with 'send message (contact name) (message)'** if a query asks to send a WhatsApp message, such as:
   - 'Send message to Alice saying Hello' → 'send message Alice Hello'
   - 'Text Mom I will be late' → 'send message Mom I will be late'

-> **Respond with 'excel (task)'** if a query asks to perform an Excel-related task, such as:
   - 'Open Excel file sales_data.xlsx' → 'excel open sales_data.xlsx'
   - 'Update cell A1 with 500' → 'excel update A1 500'
   - 'Create a new sheet named Report' → 'excel create sheet Report'

*** If a query involves multiple tasks, respond with each action separately, like 'open Facebook, call Dad, send message Alice Hello'. ***  
*** If the user says goodbye, respond with 'exit'. ***  
*** Respond with 'general (query)' if a query doesn't match any category above. ***
"""

# Chat history for context
ChatHistory = [
    {"role": "User", "message": "how are you?"},
    {"role": "Chatbot", "message": "general how are you?"},
    {"role": "User", "message": "do you like pizza?"},
    {"role": "Chatbot", "message": "general do you like pizza?"},
    {"role": "User", "message": "open chrome and tell me about mahatma gandhi."},
    {"role": "Chatbot", "message": "open chrome, general tell me about mahatma gandhi."},
    {"role": "User", "message": "open chrome and firefox"},
    {"role": "Chatbot", "message": "open chrome, open firefox"},
    {"role": "User", "message": "what is today's date and remind me i have a dance performance on 5th aug at 11pm"},
    {"role": "Chatbot", "message": "general what is today's date, reminder 11:00pm 5th aug dance performance"},
    {"role": "User", "message": "call Dad"},
    {"role": "Chatbot", "message": "call Dad"},
    {"role": "User", "message": "update A1 with 900"},
    {"role": "Chatbot", "message": "excel update A1 900"}
]


# Function to categorize queries
def FirstLayerDMM(prompt: str = "test"):
    messages.append({"role": "user", "content": f"{prompt}"})

    # Create a streaming chat session with the Cohere model.
    stream = co.chat_stream(
        model="command-r-plus",
        message=prompt,
        temperature=0.7,
        chat_history=ChatHistory,
        prompt_truncation="OFF",
        connectors=[],
        preamble=preamble
    )

    response = ""

    # Process streaming response
    for event in stream:
        if event.event_type == "text-generation":
            response += event.text

    # Clean up response
    response = response.replace("\n", "").split(",")
    response = [i.strip() for i in response]
    final_responses = []
    for task in response:
        # Fix 'call' recognition
        if task.lower().startswith("call "):
            final_responses.append(task)

        # Fix 'excel' recognition
        elif task.lower().startswith("update "):
            final_responses.append(f"excel {task}")

        # General filtering
        elif any(task.startswith(func) for func in funcs):
            final_responses.append(task)

    return final_responses if final_responses else ["general " + prompt]


# Main entry point
if __name__ == "__main__":
    while True:
        print(FirstLayerDMM(input(">>> ")))
