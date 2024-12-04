import streamlit as st
from transformers import M2M100ForConditionalGeneration, M2M100Tokenizer
from langdetect import detect
from googletrans import Translator


# Initialize model and tokenizer
MODEL_NAME = "facebook/m2m100_418M"
model =M2M100ForConditionalGeneration.from_pretrained(MODEL_NAME)
tokenizer = M2M100Tokenizer.from_pretrained(MODEL_NAME)

# Supported languages
SUPPORTED_LANGUAGES = {
    "en": "English",
    "fr": "French",
    "es": "Spanish",
    "de": "German",
    "hi": "Hindi",
}

# google translator for sentiment analysis as an additional feature
translator = Translator()

# Detect the language of input text
def detect_language(text):
    try:
        lang_code = detect(text)
        return lang_code if lang_code in SUPPORTED_LANGUAGES else "en"
    except:
        return "en"
    
# Translate text using the M2M100 model
def translate_text(input_text, src_lang, target_lang):
    try:
        tokenizer.src_lang = src_lang
        encoded_input = tokenizer(input_text, return_tensors="pt")
        generated_tokens = model.generate(
            **encoded_input, forced_bos_token_id=tokenizer.get_lang_id(target_lang)
        )

        return tokenizer.decode(generated_tokens[0], skip_special_tokens=True)
    except Exception as e:
        return f"Error during translation: {e}"
    
     
# Generate culturally appropriate greeting based on language
def cultural_greeting(lang_code):
    greetings = {
        "en": "Hello! How can I assist you today?",
        "fr": "Bonjour! Comment puis-je vous aider aujourd'hui?",
        "es": "¡Hola! ¿Cómo puedo ayudarte hoy?",
        "de": "Hallo! Wie kann ich Ihnen heute helfen?",
        "hi": "नमस्ते! मैं आज आपकी किस प्रकार सहायता कर सकता हूँ?",
    }    
    return greetings.get(lang_code, greetings["en"])

# Streamlit
st.title("Multilingual Translate Chatbot")
st.write("This bot support the following languages: English, French, Spanish, German, Hindi")

# User input
user_input = st.text_input("Enter your message:")
if user_input:
    # Detect input language
    detected_lang = detect_language(user_input)
    st.write(f"Detected language: {SUPPORTED_LANGUAGES[detected_lang]}")

    # Instruction to the user
    st.write("Please select your desired language to translate your input:")

    # Select target language for the response
    target_lang_code = st.selectbox(
        "Select a target language for the response:",
        options=list(SUPPORTED_LANGUAGES.keys()),
        format_func=lambda x: SUPPORTED_LANGUAGES[x],
    )

    # Dynamic language translation
    if detected_lang != target_lang_code:
        # Translate the user input into the target language
        translated_text = translate_text(user_input, detected_lang, target_lang_code)

    else:
        translated_text = user_input


    # Generate cultural greeting in the target language
    greeting = cultural_greeting(target_lang_code)


    # Display the chatbot's translated response
    st.write(f"Chatbot Response in {SUPPORTED_LANGUAGES[target_lang_code]}: {translated_text}")
    st.write(f"Culturally Appropriate Greeting: {greeting}")        