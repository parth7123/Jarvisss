from groq import Groq #type:ignore # Importing the Groq library to use its API.
from json import load, dump
import datetime  # Importing the datetime module for real-time date and time information.
from dotenv import load_dotenv#type:ignore # type:# Importing dotenv_values to read environment variables from a .env file.
import os
import speech_recognition as sr
import pyttsx3  # or gTTS

load_dotenv()  # Load .env file
GroqAPIKey = os.getenv("GroqAPIKey")  # Fetch API key
Username = os.getenv("Username")
Assistantname = os.getenv("Assistantname")

# Initialize the Groq client using the provided API key.
client = Groq(api_key=GroqAPIKey)

# Define paths
data_folder = r"C:\Users\parth\Desktop\Jarvis\Data"
chatlog_path = os.path.join(data_folder, "ChatLog.json")

# Ensure the Data folder exists
if not os.path.exists(data_folder):
    os.makedirs(data_folder, exist_ok=True)  # Create the folder if it doesn't exist

# Ensure ChatLog.json exists
if not os.path.exists(chatlog_path):
    with open(chatlog_path, "w") as f:
        dump([], f)  # Create an empty JSON file

# Define system prompt
System = f"""Hello, I am {Username}, You are a very accurate and advanced AI chatbot named {Assistantname} which also has real-time up-to-date information from the internet.
*** Do not tell time until I ask, do not talk too much, just answer the question.***
*** Reply in only English, even if the question is in Hindi, reply in English.***
*** Do not provide notes in the output, just answer the question and never mention your training data. ***
"""

SystemChatBot = [{"role": "system", "content": System}]

# Load chat log
try:
    with open(chatlog_path, "r") as f:
        messages = load(f)  # Load existing messages
except (FileNotFoundError, json.JSONDecodeError):#type:ignore
    messages = []  # Reset messages if file is missing or corrupted

# Function to get real-time date and time
def RealtimeInformation():
    current_date_time = datetime.datetime.now()
    return (
        f"Please use this real-time information if needed,\n"
        f"Day: {current_date_time.strftime('%A')}\n"
        f"Date: {current_date_time.strftime('%d')}\n"
        f"Month: {current_date_time.strftime('%B')}\n"
        f"Year: {current_date_time.strftime('%Y')}\n"
        f"Time: {current_date_time.strftime('%H')} hours :{current_date_time.strftime('%M')} minutes :{current_date_time.strftime('%S')} seconds.\n"
    )

# Function to clean AI response
def AnswerModifier(Answer):
    return "\n".join(line for line in Answer.split("\n") if line.strip())

# Chatbot function
def ChatBot(Query):
    try:
        with open(chatlog_path, "r") as f:
            messages = load(f)

        messages.append({"role": "user", "content": Query})

        completion = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=SystemChatBot + [{"role": "system", "content": RealtimeInformation()}] + messages,
            max_tokens=2048,
            temperature=0.7,
            top_p=1,
            stream=True,
            stop=None,
        )

        Answer = ""
        for chunk in completion:
            if chunk.choices[0].delta.content:
                Answer += chunk.choices[0].delta.content

        Answer = Answer.replace("</s>", "")
        messages.append({"role": "assistant", "content": Answer})

        with open(chatlog_path, "w") as f:
            dump(messages, f, indent=4)

        return AnswerModifier(Answer)

    except Exception as e:
        print(f"Error: {e}")
        with open(chatlog_path, "w") as f:
            dump([], f, indent=4)
        return ChatBot(Query)  # Retry the query after resetting the log.

# Initialize recognizer and TTS engine
recognizer = sr.Recognizer()
tts_engine = pyttsx3.init()

# List available voices and select a girl's voice
voices = tts_engine.getProperty('voices')
# You can print the available voices to find the right one
for index, voice in enumerate(voices):
    print(f"Voice {index}: {voice.name} - {voice.languages}")

# Set the desired voice (you may need to adjust the index based on your system)
# For example, if the girl's voice is at index 1, use:
tts_engine.setProperty('voice', voices[1].id)  # Change the index as needed

def text_to_speech(text):
    # Set properties for faster speech
    tts_engine.setProperty('rate', 150)  # Adjust speech rate
    tts_engine.setProperty('volume', 1)   # Set volume level (0.0 to 1.0)
    tts_engine.say(text)
    tts_engine.runAndWait()

# Run chatbot loop
if __name__ == "__main__":
    while True:
        user_input = input("How can i Help you : ")
        print(ChatBot(user_input))
