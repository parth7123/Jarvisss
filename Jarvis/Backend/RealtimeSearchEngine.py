from googlesearch import search  # type:ignore
from groq import Groq  # Importing the Groq library to use its API. #type:ignore
import groq  # type:ignore
from json import load, dump  # Importing functions to read and write JSON files.
import json
import datetime  # Importing the datetime module for real-time date and time information.
from dotenv import dotenv_values  # Importing dotenv_values to read environment variables from a .env file. #type:ignore
import os
from dotenv import load_dotenv  # type:ignore

# Define the correct absolute path to ChatLog.json
BASE_DIR = r"C:\Users\parth\Desktop\Jarvis"  # Update this if needed
CHATLOG_PATH = os.path.join(BASE_DIR, "Data", "ChatLog.json")

# Load environment variables from the .env file.
load_dotenv()
GroqAPIKey = os.getenv("GroqAPIKey")

# Retrieve environment variables for the chatbot configuration.
Username = os.getenv("Username")
Assistantname = os.getenv("Assistantname")

# Initialize the Groq client with the provided API key.
client = Groq(api_key=GroqAPIKey)

# Define the system interaction to the chatbot.
System = f"""Hello, I am {Username}, You are a very accurate and advanced AI chatbot named {Assistantname} which has real-time up-to-date information from the internet.
*** Provide Answers In a Professional Way, make sure to add full stops, commas, question marks, and use proper grammar.***
*** Just answer the question from the provided data in a professional way. ***"""

# Try to load the chat log from a JSON file, or create an empty one if it doesn't exist.
try:
    with open(CHATLOG_PATH, "r") as f:
        messages = load(f)
except FileNotFoundError:
    messages = []
    with open(CHATLOG_PATH, "w") as f:
        dump(messages, f)

# Function to perform a Google search and format the results.
def GoogleSearch(query):
    results = list(search(query, advanced=True, num_results=5))
    Answer = f"The search results for '{query}' are:\n[start]\n"

    for i in results:
        Answer += f"Title: {i.title}\nDescription: {i.description}\n\n"

    Answer += "[end]"
    return Answer

# Function to clean up the answer by removing empty lines.
def AnswerModifier(Answer):
    lines = Answer.split('\n')
    non_empty_lines = [line for line in lines if line.strip()]
    modified_answer = '\n'.join(non_empty_lines)
    return modified_answer

# Predefined chatbot conversation system message and an initial user message.
SystemChatBot = [
    {"role": "system", "content": System},
    {"role": "user", "content": "Hi"},
    {"role": "assistant", "content": "Hello, how can I help you?"}
]

# Function to get real-time information like the current date and time.
def Information():
    current_date_time = datetime.datetime.now()
    day = current_date_time.strftime("%A")
    date = current_date_time.strftime("%d")
    month = current_date_time.strftime("%B")
    year = current_date_time.strftime("%Y")
    hour = current_date_time.strftime("%H")
    minute = current_date_time.strftime("%M")
    second = current_date_time.strftime("%S")

    data = f"""Use This Real-time Information if needed:
Day: {day}
Date: {date}
Month: {month}
Year: {year}
Time: {hour} hours, {minute} minutes, {second} seconds.
"""
    
    return data

# Function to handle real-time search and response generation.
def RealtimeSearchEngine(prompt):
    global SystemChatBot, messages

    # Load the chat log from the JSON file.
    with open(CHATLOG_PATH, "r") as f:
        messages = load(f)
    messages.append({"role": "user", "content": f"{prompt}"})

    # Add Google search results to the system chatbot messages.
    SystemChatBot.append({"role": "system", "content": GoogleSearch(prompt)})

    # Generate a response using the Groq client.
    completion = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=SystemChatBot + [{"role": "system", "content": Information()}] + messages,
        temperature=0.7,
        max_tokens=4096,
        top_p=1,
        stream=True,
        stop=None
    )

    Answer = ""
    # Concatenate response chunks from the streaming output.
    for chunk in completion:
        if chunk.choices[0].delta.content:
            Answer += chunk.choices[0].delta.content

    # Clean up the response.
    Answer = Answer.strip().replace("</s>", "")
    messages.append({"role": "assistant", "content": Answer})

    # Save the updated chat log back to the JSON file.
    with open(CHATLOG_PATH, "w") as f:
        dump(messages, f, indent=4)

    # Remove the most recent system message from the chatbot conversation.
    SystemChatBot.pop()
    return AnswerModifier(Answer=Answer)

# Main entry point of the program for interactive querying.
if __name__ == "__main__":
    while True:
        prompt = input("how can i help you sir : ")
        print(RealtimeSearchEngine(prompt))
