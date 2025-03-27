import sys
import os
import threading
import time
import asyncio
from PyQt5.QtWidgets import QApplication
from dotenv import dotenv_values
from Frontend.GUI import start_gui, SetAssistantStatus, ShowTextToScreen, GetMicrophoneStatus, GetAssistantStatus
from Backend.Model import FirstLayerDMM
from Backend.RealtimeSearchEngine import RealtimeSearchEngine
from Backend.SpeechToText import SpeechRecognition
from Backend.Chatbot import ChatBot
from Backend.TextToSpeech import TextToSpeech
from Backend.HomeAutomation import control_appliance
from Backend.Automation import (
    OpenApp, CloseApp, GoogleSearch, YouTubeSearch, PlayYoutube, Content, System,
    send_whatsapp_message, execute_excel_commands, handle_whatsapp_call, make_whatsapp_call,
    is_whatsapp_running, focus_whatsapp, open_whatsapp
)
from Backend.ImageGeneration import generate_and_open_images

# Add paths for imports
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "Backend")))

# Load environment variables
env_vars = dotenv_values(".env")
Username = env_vars.get("Username", "User")
Assistantname = env_vars.get("Assistantname", "Assistant")

# Global reference to the QApplication instance for graceful exit
app_instance = None

# Wake word detection
def WakeWordDetection():
    print("Listening for wake word: 'Hey Jarvis'...")
    while True:
        try:
            wake_query = SpeechRecognition().strip().lower()
            if "hey jarvis" in wake_query:
                print("Wake word detected!")
                TextToSpeech("Yes, I am listening.")
                return  # Exit loop and continue execution
        except Exception as e:
            print(f"Error in WakeWordDetection: {e}")
            time.sleep(1)  # Prevent tight loop on error

# Main execution logic for processing queries
def MainExecution(query, input_type="speech"):
    try:
        SetAssistantStatus("Thinking...")
        ShowTextToScreen(f"{Username} ({input_type}): {query}")

        Decision = FirstLayerDMM(query)

        for Queries in Decision:
            if "homeautomation" in Queries:
                try:
                    control_appliance(query)
                    SetAssistantStatus("Listening...")
                except Exception as e:
                    print(f"Error in homeautomation: {e}")
                    TextToSpeech("Sorry, I couldn't control the appliance.")
                    SetAssistantStatus("Listening...")
                return

            elif "general" in Queries:
                try:
                    Answer = ChatBot(Queries.replace("general ", ""))
                    ShowTextToScreen(f"{Assistantname}: {Answer}")
                    TextToSpeech(Answer)
                    SetAssistantStatus("Listening...")
                except Exception as e:
                    print(f"Error in general query: {e}")
                    TextToSpeech("Sorry, I couldn't process your query.")
                    SetAssistantStatus("Listening...")
                return

            elif "realtime" in Queries:
                try:
                    Answer = RealtimeSearchEngine(Queries.replace("realtime ", ""))
                    SetAssistantStatus("Listening...")
                except Exception as e:
                    print(f"Error in realtime search: {e}")
                    Answer = "I couldn't find the answer right now."
                    ShowTextToScreen(f"{Assistantname}: {Answer}")
                    TextToSpeech(Answer)
                    SetAssistantStatus("Listening...")
                return

            elif "open" in Queries:
                try:
                    program_name = Queries.replace("open ", "").strip()
                    if OpenApp(program_name):
                        TextToSpeech(f"Opening {program_name}")
                    else:
                        TextToSpeech(f"I couldn't open {program_name}")
                    SetAssistantStatus("Listening...")
                except Exception as e:
                    print(f"Error opening app: {e}")
                    TextToSpeech("Sorry, I couldn't open the application.")
                    SetAssistantStatus("Listening...")
                return

            elif "close" in Queries:
                try:
                    program_name = Queries.replace("close ", "").strip()
                    if CloseApp(program_name):
                        TextToSpeech(f"Closing {program_name}")
                        
                    else:
                        TextToSpeech(f"I couldn't close {program_name}")
                    SetAssistantStatus("Listening...")
                except Exception as e:
                    print(f"Error closing app: {e}")
                    TextToSpeech("Sorry, I couldn't close the application.")
                    SetAssistantStatus("Listening...")
                return

            elif "google search" in Queries:
                try:
                    topic = Queries.replace("google search ", "").strip()
                    GoogleSearch(topic)
                    TextToSpeech(f"Searching Google for {topic}")
                    SetAssistantStatus("Listening...")
                except Exception as e:
                    print(f"Error in Google search: {e}")
                    TextToSpeech("Sorry, I couldn't perform the Google search.")
                    SetAssistantStatus("Listening...")
                return

            elif "youtube search" in Queries:
                try:
                    topic = Queries.replace("youtube search ", "").strip()
                    YouTubeSearch(topic)
                    TextToSpeech(f"Searching YouTube for {topic}")
                    SetAssistantStatus("Listening...")
                except Exception as e:
                    print(f"Error in YouTube search: {e}")
                    TextToSpeech("Sorry, I couldn't perform the YouTube search.")
                    SetAssistantStatus("Listening...")
                return

            elif "play" in Queries:
                try:
                    song = Queries.replace("play ", "").strip()
                    PlayYoutube(song)
                    TextToSpeech(f"Playing {song} on YouTube")
                    SetAssistantStatus("Listening...")
                except Exception as e:
                    print(f"Error playing YouTube: {e}")
                    TextToSpeech("Sorry, I couldn't play the video on YouTube.")
                    SetAssistantStatus("Listening...")
                return

            elif "content" in Queries:
                try:
                    topic = Queries.replace("content ", "").strip()
                    Content(topic)
                    TextToSpeech(f"Content generated for {topic}")
                    SetAssistantStatus("Listening...")
                except Exception as e:
                    print(f"Error generating content: {e}")
                    TextToSpeech("Sorry, I couldn't generate the content.")
                    SetAssistantStatus("Listening...")
                return

            elif "system" in Queries:
                try:
                    command = Queries.replace("system ", "").strip()
                    System(command)
                    TextToSpeech(f"Performed system action: {command}")
                    SetAssistantStatus("Listening...")
                    SetAssistantStatus("Listening...")
                except Exception as e:
                    print(f"Error in system command: {e}")
                    TextToSpeech("Sorry, I couldn't perform the system action.")
                    SetAssistantStatus("Listening...")
                    SetAssistantStatus("Listening...")
                return

            elif "generate image" in Queries:
                try:
                    prompt = Queries.replace("generate image ", "").strip()
                    SetAssistantStatus("Generating image...")
                    asyncio.run(generate_and_open_images(prompt))
                    TextToSpeech("Your image is ready.")
                    SetAssistantStatus("Idle")
                except Exception as e:
                    print(f"Error generating image: {e}")
                    TextToSpeech("I couldn't generate the image.")
                    SetAssistantStatus("Idle")
                return

            elif "call" in Queries:
                try:
                    contact_name = Queries.replace("call ", "").strip()
                    SetAssistantStatus(f"Calling {contact_name}...")
                    make_whatsapp_call(contact_name)
                    TextToSpeech(f"Calling {contact_name}")
                    SetAssistantStatus("Listening...")
                except Exception as e:
                    print(f"Error making WhatsApp call: {e}")
                    TextToSpeech("Sorry, I couldn't make the call.")
                    SetAssistantStatus("Idle")
                return

            elif "accept call" in Queries:
                try:
                    handle_whatsapp_call("accept")
                    TextToSpeech("Accepting the call")
                    SetAssistantStatus("Listening...")
                except Exception as e:
                    print(f"Error accepting WhatsApp call: {e}")
                    TextToSpeech("Sorry, I couldn't accept the call.")
                    SetAssistantStatus("Listening...")
                return

            elif "reject call" in Queries:
                try:
                    handle_whatsapp_call("reject")
                    TextToSpeech("Rejecting the call")
                    SetAssistantStatus("Listening...")
                except Exception as e:
                    print(f"Error rejecting WhatsApp call: {e}")
                    TextToSpeech("Sorry, I couldn't reject the call.")
                    SetAssistantStatus("Listening...")
                return

            elif "send message" in Queries:
                try:
                    details = Queries.replace("send message ", "").strip()
                    parts = details.split(" ", 1)
                    if len(parts) < 2:
                        TextToSpeech("Please specify both the contact name and the message.")
                    else:
                        contact_name, message = parts
                        TextToSpeech(f"Sending message: {message} to {contact_name}.")
                        success = send_whatsapp_message(contact_name, message)
                        if success:
                            TextToSpeech("Message sent successfully.")
                        else:
                            TextToSpeech("❌ Failed to send message.")
                    SetAssistantStatus("Listening...")
                except Exception as e:
                    print(f"Error sending WhatsApp message: {e}")
                    TextToSpeech("Sorry, I couldn't send the message.")
                    SetAssistantStatus("Listening...")
                return

            elif "excel" in Queries:
                try:
                    excel_file = Queries.replace("excel ", "").strip()
                    execute_excel_commands(excel_file, TextToSpeech)
                    TextToSpeech(f"Executed commands from {excel_file}")
                    SetAssistantStatus("Listening...")
                except Exception as e:
                    print(f"Error executing Excel commands: {e}")
                    TextToSpeech("Sorry, I couldn't execute the Excel commands.")
                    SetAssistantStatus("Listening...")
                return

            elif "exit" in Queries:
                try:
                    TextToSpeech("Okay, Bye!")
                    app_instance.quit()  # Gracefully close the GUI
                except Exception as e:
                    print(f"Error during exit: {e}")
                    os._exit(1)  # Fallback to os._exit if quit fails
                return

    except Exception as e:
        print(f"Error in MainExecution: {e}")
        TextToSpeech("An unexpected error occurred while processing your command.")
        SetAssistantStatus("Listening...")

# Thread for wake word detection and speech input
def FirstThread():
    while True:
        try:
            print("Starting WakeWordDetection...")
            WakeWordDetection()
            print("Wake word detected, setting status to Listening...")
            SetAssistantStatus("Listening...")

            last_activity = time.time()
            print("Entering speech input loop...")
            while time.time() - last_activity < 30:
                try:
                    print("Listening for command...")
                    query = SpeechRecognition().strip()
                    if query:
                        print(f"Speech input received: {query}")
                        MainExecution(query, input_type="speech")
                        last_activity = time.time()
                        print("Command executed, resetting last activity time.")
                except Exception as e:
                    print(f"Error processing speech input: {e}")
                    TextToSpeech("Sorry, I couldn’t hear you clearly. Please try again.")
                time.sleep(0.1)

            print("Speech input loop timed out, going back to sleep...")
            TextToSpeech("Going back to sleep. Say 'Hey Jarvis' to wake me up.")
            SetAssistantStatus("slleeping....")
            print("Waiting for wake word again...")

        except Exception as e:
            print(f"Error in FirstThread: {e}")
            TextToSpeech("An error occurred. Going back to wake word detection.")
            time.sleep(1)  # Prevent tight loop on error

# Main function to start the GUI and threads
def main():
    global app_instance
    app = QApplication(sys.argv)
    app_instance = app

    # Define the callback for GUI inputs
    def on_input(input_type, query):
        MainExecution(query, input_type)

    # Start the GUI in the main thread
    app, window = start_gui(app, on_input_callback=on_input)

    # Start the wake word detection in a separate thread
    thread1 = threading.Thread(target=FirstThread, daemon=True)
    thread1.start()

    # Start the application event loop
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()