import pygame  # Import pygame for audio playback
import random  # Import random for generating random values
import asyncio  # Import asyncio for asynchronous execution
import edge_tts  # Import edge_tts for text-to-speech conversion
import os  # Import os for file path handling
from dotenv import dotenv_values  # Import dotenv to manage environment variables

# Set the event loop policy to avoid asyncio issues on Windows
if os.name == 'nt':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# Load environment variables from a .env file
env_vars = dotenv_values(".env")
AssistantVoice = env_vars.get("AssistantVoice", "en-US-AriaNeural")  # Default voice if not set

if not isinstance(AssistantVoice, str):
    print("Error: AssistantVoice must be a string")
    exit(1)

# Asynchronous function to convert text to an audio file
async def TextToAudioFile(text) -> None:
    file_path = r"C:\Users\parth\Desktop\Jarvis\Data\speech.mp3"  # Define the path where the speech file will be saved

    if os.path.exists(file_path):  # Check if the file already exists
        os.remove(file_path)  # If it exists, remove it to avoid overwriting errors

    communicate = edge_tts.Communicate(text, AssistantVoice, pitch='+2Hz', rate='-5%')

    await communicate.save(file_path)  # Save the generated speech as an MP3 file

# Function to run an async task within a synchronous function
def run_async_task(task):
    try:
        loop = asyncio.get_running_loop()
        return loop.run_until_complete(task)
    except RuntimeError:
        return asyncio.run(task)

# Function to manage Text-to-Speech (TTS) functionality
def TTS(Text, func=lambda r=None: True):
    try:
        # Convert text to an audio file asynchronously
        run_async_task(TextToAudioFile(Text))

        # Initialize pygame mixer for audio playback
        try:
            pygame.mixer.init()
        except pygame.error as e:
            print(f"Error initializing pygame mixer: {e}")
            return

        # Load and play the generated speech file
        pygame.mixer.music.load(r"C:\Users\parth\Desktop\Jarvis\Data\speech.mp3")
        pygame.mixer.music.play()

        # Wait for the audio to finish or stop if func() returns False
        while pygame.mixer.music.get_busy():
            if func() == False:
                break
            pygame.time.Clock().tick(10)
    
    except Exception as e:
        print(f"Error in TTS: {e}")
    finally:
        try:
            func(False)
            pygame.mixer.music.stop()
            pygame.mixer.quit()
        except Exception as e:
            print(f"Error in finally block: {e}")

# Function to manage Text-to-Speech with additional responses for long text
def TextToSpeech(Text, func=lambda r=None: True):
    Data = str(Text).split(".")  # Split the text into sentences

    responses = [
        "The rest of the result has been printed to the chat screen, kindly check it out sir.",
        "The rest of the text is now on the chat screen, sir, please check it.",
        "You can see the rest of the text on the chat screen, sir.",
        "The remaining part of the text is now on the chat screen, sir.",
        "Sir, you'll find more text on the chat screen for you to see.",
        "The rest of the answer is now on the chat screen, sir.",
        "Sir, please look at the chat screen, the rest of the answer is there.",
        "You'll find the complete answer on the chat screen, sir.",
        "The next part of the text is on the chat screen, sir.",
        "Sir, please check the chat screen for more information."
    ]

    # If the text is very long, summarize and add a response message
    if len(Data) > 20 and len(Text) > 250:
        TTS(".".join(Text.split(".")[:2]) + ". " + random.choice(responses), func)
    else:
        TTS(Text, func)

# Main execution loop
if __name__ == "__main__":
    while True:
        try:
            # Prompt user for input and pass it to TextToSpeech function
            TTS(input("Enter the text: "))
        except KeyboardInterrupt:
            print("\nExiting program...")
            break