import time
import re
import requests
import asyncio
from googletrans import Translator
from .TextToSpeech import TextToSpeech  # Ensure this exists

# ESP32's IP Address (Update as per Serial Monitor)
ESP32_IP = "http://192.168.11.165"  # Change this to match your ESP32 IP

# Initialize Translator
translator = Translator()

# Appliance Mapping (Relay Number → Appliance)
appliance_map = {
    1: "Warm Light", 2: "Cold Light", 3: "Fan 1", 4: "Fan 2",
    5: "Ceiling Light", 6: "AC", 7: "TV", 8: "Fridge"
}

# Mapping words to numbers
word_to_number = {
    "one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
    "six": 6, "seven": 7, "eight": 8, "first": 1, "second": 2,
    "third": 3, "fourth": 4, "fifth": 5, "sixth": 6,
    "seventh": 7, "eighth": 8, "last 2nd": 2, "1": 1, "2": 2,
    "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8
}

# Grouped Commands (Fixes "Turn on all lights" issue)
group_commands = {
    "everything": list(appliance_map.keys()),  # Turns on/off all appliances
    "all": list(appliance_map.keys()),  # Same as "everything"
    "all lights": [1, 2, 5],  # Only lights (Warm, Cold, Ceiling)
    "all fans": [3, 4],  # Only fans (Fan 1, Fan 2)
}

async def translate_to_english(text):
    """Translate Hindi/Gujarati commands to English asynchronously."""
    try:
        translated = await asyncio.to_thread(translator.translate, text, src='auto', dest='en')
        return translated.text.lower()
    except Exception as e:
        print(f"⚠ Translation error: {e}")
        return text  # Return original text if translation fails

def extract_appliances(command):
    """Extract appliance numbers based on various user phrasings."""
    command = command.lower()
    numbers = set()

    # Match group commands first to prevent misinterpretation
    for key, relays in group_commands.items():
        if key in command and not any(word in command for word in ["light", "fan", "ac", "tv", "fridge"]):
            return relays  # Return relevant appliances

    # Match individual appliances (e.g., "turn off second light")
    matches = re.findall(r"(light|fan|ac|tv|fridge)\s*(\d+|\w+)?", command)
    
    for appliance, num in matches:
        if num:  # If a number is mentioned
            relay = word_to_number.get(num.lower())
            if relay in appliance_map:
                numbers.add(relay)
        else:  # If no number, match appliances directly
            for relay, name in appliance_map.items():
                if appliance in name.lower():
                    numbers.add(relay)
    
    return list(numbers)  # Convert set to list

def control_appliance(command):
    """Process the voice command and send requests to ESP32."""
    command = asyncio.run(translate_to_english(command))  # Translate command
    
    appliances = extract_appliances(command)
    if not appliances:
        print("⚠ Invalid command. Only mapped appliances are supported.")
        TextToSpeech("I can only control mapped appliances.")
        return False
    
    action = None
    if any(word in command for word in ["on", "jalāo", "start", "chalu", "ચાલુ"]):
        action = 0  # ON
    elif any(word in command for word in ["off", "band", "bandh", "band karo", "stop", "બંધ", "बंद"]):
        action = 1  # OFF
    
    if action is not None:
        for relay in appliances:
            send_command(relay, action)
            response = f"Turning {'ON' if action == 0 else 'OFF'} {appliance_map[relay]}."
            print(f"💡 {response}")
            TextToSpeech(response)
        return True
    
    print("⚠ Command not clear for appliance control.")
    TextToSpeech("Command not clear. Please say turn on or turn off.")
    return False

def send_command(relay, state):
    """Send HTTP request to ESP32 to control appliances."""
    url = f"{ESP32_IP}/control?relay={relay}&state={state}"
    try:
        response = requests.get(url, timeout=5)  # Timeout for response
        response.raise_for_status()  # Check for HTTP errors
        print(f"✅ ESP32 Response: {response.text}")
    except requests.exceptions.Timeout:
        print("⚠ Timeout: ESP32 did not respond. Check the IP and WiFi connection.")
    except requests.exceptions.ConnectionError:
        print("⚠ Connection Error: ESP32 might be offline or unreachable.")
    except requests.exceptions.HTTPError as e:
        print(f"⚠ HTTP Error: {e}")
    except Exception as e:
        print(f"⚠ Unexpected Error: {e}")

if __name__ == "__main__":
    test_commands = [
        # "turn on warm light",  # ✅ Should turn on Warm Light only
        # "turn on cold light",  # ✅ Should turn off Cold Light only
        # "turn on fan 1",  # ✅ Should turn on Fan 1 only
        # "turn off all fans",  # ✅ Should turn off Fan 1 & Fan 2 only
        # "turn on all lights",  # ✅ Should turn on Warm, Cold, and Ceiling Light only
        # "turn off fridge",  # ✅ Should turn off Fridge only
        "turn on everything",  # ✅ Should turn on all appliances
        # "turn off ceiling light",  # ✅ Should turn off Ceiling Light only
        # "turn off second light",  # ✅ Should turn off Cold Light only
        # "switch on TV",  # ✅ Should turn on TV only
    ]

    for cmd in test_commands:
        print(f"📝 Testing command: {cmd}")
        control_appliance(cmd)
        time.sleep(2)  # Small delay to mimic real interactions
