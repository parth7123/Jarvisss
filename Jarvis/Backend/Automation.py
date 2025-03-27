# Import required libraries
from AppOpener import close, open as appopen  # Open and close apps
from webbrowser import open as webopen  # Web browser functionality
from pywhatkit import search, playonyt,sendwhatmsg_instantly # Google search & YouTube playback
from dotenv import load_dotenv  # Load environment variables
from bs4 import BeautifulSoup  # HTML parsing
from rich import print  # Styled console output
from groq import Groq  # AI chat functionalities
import webbrowser  # Opening URLs
import subprocess  # System commands
import requests  # HTTP requests
import keyboard  # Keyboard actions
import asyncio  # Async programming
import os  # OS functionalities
from pathlib import Path  # File path handling
import winreg  # Importing winreg to access the Windows registry
import time
import pandas as pd
import pyautogui
import pygetwindow as gw
import psutil

# Load environment variables correctly
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(env_path)
# Define saved contacts
SAVED_CONTACTS = {
    "dad": "+919537749570",
    "mom": "+919879535365",
    "khushal":"+917046916812",
    # Add more contacts here
}

# Retrieve API key
GROQ_API_KEY = os.getenv("GroqAPIKey")
if not GROQ_API_KEY:
    raise ValueError("GroqAPIKey not found in .env file. Please check your .env file.")

# Initialize Groq client
client = Groq(api_key=GROQ_API_KEY)

# Define file storage path
SAVE_PATH = Path(__file__).resolve().parent.parent / "Data"
SAVE_PATH.mkdir(parents=True, exist_ok=True)  # Ensure directory exists
# Function to read and execute Excel commands
##################################################################################################################################################################################
                                                                # exceal automation
##################################################################################################################################################################################

def execute_excel_commands(file_path, text_to_speech_callback=None):
    """Read and execute commands from an Excel file, creating a default file if missing."""
    try:
        if not os.path.exists(file_path):
            print(f"Error: The file '{file_path}' was not found. Creating a default file.")
            default_commands = pd.DataFrame({"Command": ["open notepad"]})
            default_commands.to_excel(file_path, index=False)
            if text_to_speech_callback:
                text_to_speech_callback(f"Created a default Excel file at {file_path}.")
            return

        df = pd.read_excel(file_path)
        if "Command" not in df.columns:
            raise KeyError("The 'Command' column is missing in the Excel file.")

        commands = df["Command"].dropna().tolist()
        for command in commands:
            print(f"Executing command from Excel: {command}")
            asyncio.run(TranslateAndExecute([command]))
            if text_to_speech_callback:
                text_to_speech_callback(f"Executed command: {command}")

    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
        if text_to_speech_callback:
            text_to_speech_callback(f"Error: The file {file_path} was not found.")
    except KeyError as e:
        print(f"Error: {e}")
        if text_to_speech_callback:
            text_to_speech_callback(f"Error: {str(e)}")
    except Exception as e:
        print(f"Unexpected error: {e}")
        if text_to_speech_callback:
            text_to_speech_callback(f"Unexpected error: {str(e)}")
##################################################################################################################################################################################
                                                                # whatssapp automation
##################################################################################################################################################################################
def is_whatsapp_running():
    """Check if WhatsApp is running."""
    for process in psutil.process_iter(['name']):
        if process.info['name'] == "WhatsApp.exe":
            return True
    return False

def focus_whatsapp():
    """Bring WhatsApp to the foreground."""
    try:
        whatsapp_windows = [win for win in gw.getWindowsWithTitle("WhatsApp")]
        if whatsapp_windows:
            for win in whatsapp_windows:
                if "WhatsApp" in win.title:
                    win.activate()
                    print("✅ WhatsApp brought to foreground.")
                    return True
    except Exception as e:
        print(f"⚠️ Error focusing WhatsApp: {e}")
    return False

def open_whatsapp():
    """Open WhatsApp (Microsoft Store version)."""
    try:
        print("🔄 Opening WhatsApp...")
        subprocess.Popen([r"C:\Program Files\WindowsApps\5319275A.WhatsAppDesktop_2.2509.4.0_x64__cv1g1gvanyjgm\WhatsApp.exe"], shell=True)
        time.sleep(5)  # Wait for WhatsApp to open
        return True
    except Exception as e:
        print(f"❌ Error opening WhatsApp: {e}")
        return False

def open_or_focus_whatsapp():
    """Ensure WhatsApp is running and focused."""
    if is_whatsapp_running():
        return focus_whatsapp()
    return open_whatsapp()

def send_whatsapp_message(contact_name, message):
    """Send a WhatsApp message using keyboard shortcuts."""
    try:
        if not open_or_focus_whatsapp():
            return False
        
        time.sleep(1)  # Ensure WhatsApp is fully loaded
        pyautogui.hotkey("esc")
        time.sleep(0.1)
        # Open search bar using keyboard shortcut
        print("🔍 Opening search bar...")
        pyautogui.hotkey("ctrl", "alt", "/")
        time.sleep(0.5)

        # Type the contact name
        pyautogui.write(contact_name)
        time.sleep(0.5)  # Wait for search results

        # Select the first contact
        pyautogui.press("down")
        time.sleep(0.2)
        pyautogui.press("enter")
        time.sleep(0.1)

        # Type and send the message
        pyautogui.write(message)
        time.sleep(0.5)
        pyautogui.press("enter")

        print(f"✅ Message sent to {contact_name}: {message}")
        return True
    except Exception as e:
        print(f"❌ Error sending WhatsApp message: {e}")
        return False

# # Example Usage:
# send_whatsapp_message("bansil", "Hello khushal, how are you?")

##################################################################################################################################################################################
                                                                # whatssapp call automation
##################################################################################################################################################################################

# Function to handle WhatsApp calls
def handle_whatsapp_call(action):
    """Accepts or rejects an incoming WhatsApp call."""
    if action not in ["accept", "reject"]:
        print("❌ Invalid action. Use 'accept' or 'reject'.")
        return False

    # Ensure WhatsApp is in focus
    if not open_whatsapp():
        return False

    time.sleep(2)  # Ensure WhatsApp is in the foreground
    pyautogui.hotkey("esc")
    time.sleep(0.1)
    # Define the correct shortcut keys
    key = "alt+shift+y" if action == "accept" else "alt+shift+n"

    print(f"🔄 Trying to {action} WhatsApp call...")
    
    pyautogui.hotkey(*key.split("+"))  # Press shortcut keys
    time.sleep(1)

    print(f"✅ WhatsApp call {action}ed.")
    return True

# Example Usage:
# handle_whatsapp_call("accept") 
# Function to make WhatsApp calls
# def is_whatsapp_running():H
#     """Check if WhatsApp is running."""
#     try:
#         output = subprocess.check_output("tasklist", shell=True).decode()
#         return "WhatsApp.exe" in output
#     except Exception as e:ello khushal, how are you?
#         print(f"⚠️ Error checking WhatsApp process: {e}")
#         return False

# def open_whatsapp():
#     """Opens WhatsApp if not already running."""
#     try:
#         if is_whatsapp_running():
#             print("✅ WhatsApp is already running.")
#             return True
        
#         print("🔄 Opening WhatsApp...")
#         subprocess.Popen("whatsapp", shell=True)  # Open WhatsApp Desktop
#         time.sleep(5)  # Wait for WhatsApp to open
#         return True

#     except Exception as e:
#         print(f"❌ Error opening WhatsApp: {e}")
#         return False

def make_whatsapp_call(contact_name):
    """Finds a contact by name and makes a voice call in WhatsApp Desktop."""
    try:
        if not open_whatsapp():
            return False

        time.sleep(2)  # Ensure WhatsApp is fully loaded

        # Open search bar
        print("🔍 Searching for contact...")
        pyautogui.hotkey("ctrl", "alt", "/")  # Opens search bar
        time.sleep(0.1)

        # Type contact name
        pyautogui.write(contact_name)
        time.sleep(0.3)  # Wait for search results

        # Select the contact
        pyautogui.press("tab")
        time.sleep(0.3)
        pyautogui.press("enter")
        time.sleep(0.5)

        # Navigate to the call button using Tab key
        print("🔄 Navigating to call button...")
        for _ in range(11):  # Adjust the number of tabs based on UI layout
            pyautogui.press("tab")
            time.sleep(0.1)

        # Press Enter to make the call
        pyautogui.press("enter")

        print(f"📞 Calling {contact_name} on WhatsApp Desktop...")
        return True

    except Exception as e:
        print(f"❌ Error making WhatsApp call: {e}")
        return False

# Example Usage:
# make_whatsapp_call("dad")  # Replace with actual contact name
# Function to perform a Google search
##################################################################################################################################################################################
                                                                # google search automation
##################################################################################################################################################################################

def GoogleSearch(topic):
    search(topic)
    return True
##################################################################################################################################################################################
                                                                # content writing automation
##################################################################################################################################################################################


# Function to generate AI content and save it to a file
def Content(topic):
    def ContentWriterAI(prompt):
        """Generate content using Groq AI."""
        try:
            messages = [
                {"role": "system", "content": "You are a content writer. Write a detailed article on the given topic."},
                {"role": "user", "content": f"Write an article on {prompt}"}
            ]
            completion = client.chat.completions.create(
                model="llama3-70b-8192",  # Updated to a supported model
                messages=messages,
                max_tokens=2048,
                temperature=0.7,
                top_p=1,
                stream=True
            )

            answer = ""
            for chunk in completion:
                if chunk.choices[0].delta.content:
                    answer += chunk.choices[0].delta.content

            return answer.replace("</s>", "")
        except Exception as e:
            print(f"Error generating content with Groq: {e}")
            return "Failed to generate content due to an error."

    topic = topic.replace("Content", "").strip()
    content_by_ai = ContentWriterAI(topic)
    file_path = SAVE_PATH / f"{topic.lower().replace(' ', '')}.txt"

    with open(file_path, "w", encoding="utf-8") as file:
        file.write(content_by_ai)

    print(f"Content saved at: {file_path}")
    subprocess.Popen(["notepad.exe", str(file_path)])  # Open in Notepad
    return True
    
##################################################################################################################################################################################
                                                                # ypoutube  automation
##################################################################################################################################################################################

# Function to search on YouTube
def YouTubeSearch(topic):
    url = f"https://www.youtube.com/results?search_query={topic}"
    webbrowser.open(url)
    return True

# Function to play a video on YouTube
def PlayYoutube(query):
    playonyt(query)
    return True
##################################################################################################################################################################################
                                                                # app opening and closeing automation
##################################################################################################################################################################################

# Function to get the list of installed applications
def get_installed_apps():
    apps = []
    registry_paths = [
        r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall",
        r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"
    ]
    
    for path in registry_paths:
        try:
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, path) as key:
                for i in range(winreg.QueryInfoKey(key)[0]):  # Number of subkeys
                    try:
                        app_name = winreg.EnumValue(key, i)[1]  # Get the second value which is the display name
                        apps.append(app_name)
                    except OSError:
                        continue
        except FileNotFoundError:
            print(f"Registry path not found: {path}")  # Debugging output
            continue

    print(f"Installed applications: {apps}")  # Debugging output
    return apps

# Function to open an application or webpage
def OpenApp(app, sess=requests.session()):
    print(f"Attempting to open application: {app}")  # Debugging output
    installed_apps = get_installed_apps()  # Get the list of installed applications
    app = app.lower()  # Normalize the app name for comparison

    # Check if the app is in the installed applications list
    for installed_app in installed_apps:
        if installed_app.lower() == app:
            try:
                appopen(installed_app, match_closest=True, output=True, throw_error=True)
                print(f"Successfully opened application: {installed_app}")  # Debugging output
                return True
            except Exception as e:
                print(f"Error opening application '{installed_app}': {e}")  # Log the error
                return False

    # If the app is not found, check for common applications with their paths
    common_apps = {
        "notepad": r"C:\Windows\System32\notepad.exe",
        "paint": r"C:\Windows\System32\mspaint.exe",
        "calculator": r"C:\Windows\System32\calc.exe",
        "word": r"C:\Program Files\Microsoft Office\root\Office16\WINWORD.EXE",  # Adjust path as necessary
        "microsoft word": r"C:\Program Files\Microsoft Office\root\Office16\WINWORD.EXE",  # Adjust path as necessary
        "excel": r"C:\Program Files\Microsoft Office\root\Office16\EXCEL.EXE",  # Adjust path as necessary
        "powerpoint": r"C:\Program Files\Microsoft Office\root\Office16\POWERPNT.EXE",  # Adjust path as necessary
        "chrome": r"C:\Program Files\Google\Chrome\Application\chrome.exe",  # Adjust path as necessary
        "firefox": r"C:\Program Files\Mozilla Firefox\firefox.exe",  # Adjust path as necessary
        "spotify": r"C:\Program Files\WindowsApps\SpotifyAB.SpotifyMusic_1.257.463.0_x64__zpdnekdrzrea0\Spotify.exe",  # Adjust path as necessary
        "whatsapp": r"C:\Program Files\WindowsApps\5319275A.WhatsAppDesktop_2.2507.2.0_x64__cv1g1gvanyjgm\WhatsApp.exe",  # Adjust path as necessary
        # Add more applications as needed
    }

    # Check if the app is in the common apps dictionary
    if app in common_apps:
        try:
            subprocess.Popen(common_apps[app])  # Open the application using its path
            print(f"Successfully opened common application: {app}")  # Debugging output
            return True
        except Exception as e:
            print(f"Error opening common application '{app}': {e}")  # Log the error
            return False

    # If the app is still not found, construct the URL for a Google search
    url = f"https://www.google.com/search?q={app}"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = sess.get(url, headers=headers)
        if response.status_code == 200:
            webopen(url)  # Open the Google search results
            print(f"Opened Google search for: {app}")  # Debugging output
        else:
            print(f"Failed to retrieve search results for: {app}, Status Code: {response.status_code}")
        return True
    except Exception as e:
        print(f"Error during web request for '{app}': {e}")  # Log the error
        return False

# Function to close an application
def CloseApp(app):
    try:
        if "chrome" in app:
            return False
        close(app, match_closest=True, output=True, throw_error=True)
        return True
    except:
        return False
##################################################################################################################################################################################
                                                                # system automation
##################################################################################################################################################################################

# Function to control system volume
def System(command):
    actions = {
        "mute": lambda: keyboard.press_and_release("volume mute"),
        "unmute": lambda: keyboard.press_and_release("volume mute"),
        "volume up": lambda: keyboard.press_and_release("volume up"),
        "volume down": lambda: keyboard.press_and_release("volume down")
    }

    if command in actions:
        actions[command]()
        return True
    return False
##################################################################################################################################################################################
##################################################################################################################################################################################
##################################################################################################################################################################################
                                                                # function calling
##################################################################################################################################################################################
##################################################################################################################################################################################
##################################################################################################################################################################################


# Asynchronous function to translate and execute commands
async def TranslateAndExecute(commands: list[str]):
    funcs = []

    for command in commands:
        command = command.lower()

        if "send message" in command and "to" in command and "saying" in command:
            parts = command.split(" to ")
            if len(parts) == 2:
                contact, message = parts[1].split(" saying ")
                funcs.append(asyncio.to_thread(send_whatsapp_message, contact.strip(), message.strip()))

        elif "call" in command and "whatsapp" in command:
            contact = command.replace("call", "").replace("on whatsapp", "").strip()
            funcs.append(asyncio.to_thread(make_whatsapp_call, contact))

        elif command.startswith("answre the call"):
            funcs.append(asyncio.to_thread(handle_whatsapp_call, "accept"))

        elif command.startswith("reject the call"):
            funcs.append(asyncio.to_thread(handle_whatsapp_call, "reject"))

        elif command.startswith("open "):
            funcs.append(asyncio.to_thread(appopen, command.removeprefix("open ").strip()))

        elif command.startswith("close "):
            funcs.append(asyncio.to_thread(close, command.removeprefix("close ").strip()))

        elif command.startswith("search google for "):
            funcs.append(asyncio.to_thread(search, command.removeprefix("search google for ").strip()))

        elif command.startswith("play"):
            funcs.append(asyncio.to_thread(playonyt, command.removeprefix("play youtube ").strip()))

        else:
            print(f"No function found for: {command}")

    results = await asyncio.gather(*funcs)
    return results

# Asynchronous function for automation
async def Automation(commands: list[str]):
    async for result in TranslateAndExecute(commands):
        pass
    return True
