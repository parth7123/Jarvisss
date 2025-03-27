from selenium import webdriver  # type: ignore
from selenium.webdriver.common.by import By  # type: ignore
from selenium.webdriver.chrome.service import Service  # type: ignore
from selenium.webdriver.chrome.options import Options  # type: ignore
from dotenv import dotenv_values  # type: ignore
import os
import time
import mtranslate as mt  # type: ignore

# Load environment variables
env_vars = dotenv_values(".env")
InputLanguage = env_vars.get("InputLanguage", "en")  # Default to English

# Define HTML code
HtmlCode = '''<!DOCTYPE html>
<html lang="en">
<head>
    <title>Speech Recognition</title>
</head>
<body>
    <button id="start" onclick="startRecognition()">Start Recognition</button>
    <button id="end" onclick="stopRecognition()">Stop Recognition</button>
    <p id="output"></p>
    <script>
        const output = document.getElementById('output');
        let recognition;

        function startRecognition() {
            recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
            recognition.lang = '';
            recognition.continuous = true;

            recognition.onresult = function(event) {
                const transcript = event.results[event.results.length - 1][0].transcript;
                output.textContent += transcript;
            };

            recognition.onend = function() {
                recognition.start();
            };
            recognition.start();
        }

        function stopRecognition() {
            recognition.stop();
            output.innerHTML = "";
        }
    </script>
</body>
</html>'''

# Ensure "Data" folder exists at the correct location
base_folder = os.path.dirname(os.getcwd())  # Move up one directory (Jarvis)
data_folder = os.path.join(base_folder, "Data")
os.makedirs(data_folder, exist_ok=True)

# Save HTML file in the correct "Data" folder
html_file_path = os.path.join(data_folder, "Voice.html")
with open(html_file_path, "w", encoding="utf-8") as f:
    f.write(HtmlCode)

# Convert file path for WebDriver
Link = "file://" + os.path.abspath(html_file_path).replace("\\", "/")

# Setup Chrome options
chrome_options = Options()
chrome_options.add_argument("--use-fake-ui-for-media-stream")
chrome_options.add_argument("--use-fake-device-for-media-stream")
chrome_options.add_argument("--headless=new")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")

# Use the specified driver path
chromedriver_path = r"C:\Users\parth\Desktop\Jarvis\Drivers\chromedriver.exe"
service = Service(chromedriver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)

# Ensure "Frontend/Files" exists
temp_folder = os.path.join(base_folder, "Frontend", "Files")
os.makedirs(temp_folder, exist_ok=True)

# Set Assistant Status
def SetAssistantStatus(Status):
    with open(os.path.join(temp_folder, "Status.data"), "w", encoding='utf-8') as file:
        file.write(Status)

# Query Modifier
def QueryModifier(Query):
    new_query = Query.lower().strip()
    query_words = new_query.split()

    if not query_words:
        return ""

    question_words = ["how", "what", "who", "where", "when", "why", "which", "whose", "whom", "can you", 
                      "what's", "where's", "how's", "can you"]

    if any(word + " " in new_query for word in question_words):
        new_query = new_query.rstrip(".?!") + "?"
    else:
        new_query = new_query.rstrip(".?!") + "."

    return new_query.capitalize()

# Universal Translator
def UniversalTranslator(Text):
    return mt.translate(Text, "en", "auto").capitalize()

# Speech Recognition with Timeout
def SpeechRecognition():
    driver.get(Link)
    driver.find_element(By.ID, "start").click()

    timeout = time.time() + 10  # 10-second timeout
    while time.time() < timeout:
        try:
            Text = driver.find_element(By.ID, "output").text
            if Text:
                driver.find_element(By.ID, "end").click()
                return QueryModifier(Text) if InputLanguage.lower() == "en" else QueryModifier(UniversalTranslator(Text))
        except:
            pass

    return ""

# Main Loop
if __name__ == "__main__":
    while True:
        Text = SpeechRecognition()
        if Text:
            print(Text)
