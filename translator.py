# translator.py
# Your language detection + translation logic here
# translator.py
from transformers import pipeline
from langdetect import detect

# Load Hugging Face Translation pipeline
translator = pipeline("translation", model="facebook/nllb-200-distilled-600M", src_lang="mya_Mymr", tgt_lang="eng_Latn")

def detect_language(text):
    try:
        return detect(text)
    except:
        return "unknown"

def translate_text(text, detected_language):
    if detected_language.lower() in ["en", "english"]:
        return text
    try:
        translation = translator(text)[0]['translation_text']
        return translation
    except Exception as e:
        print(f"Error translating: {e}")
        return text

print("Translating collected data to English...")