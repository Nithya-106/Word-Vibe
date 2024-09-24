from flask import Flask, render_template, request
import speech_recognition as sr
from googletrans import Translator
from gtts import gTTS
import os
import platform

app = Flask(__name__, template_folder='template')

# Initialize the recognizer and translator
r = sr.Recognizer()
translator = Translator()

# Path to the file where translations will be stored
HISTORY_FILE = 'translation_history.txt'

def save_translation(input_text, translated_text, input_lang, output_lang):
    translation = f"{input_text} ({input_lang}) -> {translated_text} ({output_lang})\n"
    with open(HISTORY_FILE, 'a', encoding='utf-8') as file:
        file.write(translation)

def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, 'r', encoding='utf-8') as file:
            history = file.readlines()
    else:
        history = []
    return history

@app.route('/')
def index():
    translations = load_history()
    return render_template('h.html', translations=translations)

@app.route('/translate', methods=['POST'])
def translate_audio():
    input_lang = request.form['input_lang']
    output_lang = request.form['output_lang']

    with sr.Microphone() as source:
        print("Speak now...")
        audio = r.listen(source)

    try:
        text = r.recognize_google(audio, language=input_lang)
        print("You said:", text)

        translation = translator.translate(text, src=input_lang, dest=output_lang)
        print("Translation:", translation.text)

        tts = gTTS(translation.text, lang=output_lang)
        tts_filename = "captured_voice.mp3"
        tts.save(tts_filename)

        if os.name == "nt":  # Windows
            os.system(f"start {tts_filename}")
        elif os.name == "posix":
            if platform.system() == "Darwin":  # macOS
                os.system(f"open {tts_filename}")
            else:  # Linux
                os.system(f"xdg-open {tts_filename}")

        # Save translation to history
        save_translation(text, translation.text, input_lang, output_lang)

        return translation.text
    except sr.UnknownValueError:
        return "Sorry, I could not understand the audio."
    except sr.RequestError as e:
        return f"Error: {e}"

if __name__ == '__main__':
    app.run(debug=True)
