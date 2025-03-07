import os
import re
import requests
from flask import Flask, render_template, request, redirect, url_for
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    user_text = request.form.get('user_text', '').strip()
    length_choice = request.form.get('length', '2')
    if not user_text:
        return redirect(url_for('home'))

    # Count words in the input
    input_word_list = re.findall(r'\w+', user_text)
    input_word_count = len(input_word_list)

    # Prompt trick
    if length_choice == '1':
        length_prompt = "Please provide a brief summary of the following text:\n\n"
    elif length_choice == '3':
        length_prompt = "Please provide a detailed summary of the following text:\n\n"
    else:
        length_prompt = "Please provide a summary of the following text:\n\n"

    final_text_for_api = length_prompt + user_text

    # Summarize
    if not GOOGLE_API_KEY:
        summarized_text = "(No real API call)\n\n" + final_text_for_api
    else:
        endpoint = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GOOGLE_API_KEY}"
        payload = {
            "contents": [
                {
                    "parts": [
                        {"text": final_text_for_api}
                    ]
                }
            ]
        }
        try:
            response = requests.post(endpoint, json=payload, timeout=15)
            data = response.json()
            if response.status_code == 200:
                try:
                    summarized_text = data["candidates"][0]["content"]["parts"][0]["text"]
                except (KeyError, IndexError):
                    summarized_text = "No text found in the API response."
            else:
                summarized_text = f"API Error: HTTP {response.status_code}\nDetails: {response.text}"
        except Exception as e:
            summarized_text = f"Exception calling Google API: {e}"

    # Summarized word count
    summarized_word_list = re.findall(r'\w+', summarized_text)
    summary_word_count = len(summarized_word_list)

    return render_template('index.html',
                           summarized_text=summarized_text,
                           summary_word_count=summary_word_count,
                           input_word_count=input_word_count)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
