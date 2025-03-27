from langdetect import detect  # Import a language detection library

# Predefined responses for faster access
responses = {
    'en': "This is the response in English.",  # Your actual response in English
    'hi': "यह हिंदी में उत्तर है।"  # Your actual response in Hindi
}

def generate_response(user_input):
    # Detect the language of the user input
    language = detect(user_input)

    # Use predefined responses for faster access
    response = responses.get(language, "Sorry, I cannot respond in this language.")  # General fallback response

    return response 