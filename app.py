import os
import re
import requests
from flask import Flask, render_template, request, redirect, url_for
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

### CHANGED ### Step 1: Define the new helper function here.
def build_prompt(user_text: str, length_choice: str) -> str:
    """
    Builds a prompt string guiding the model to produce a short, medium, or long summary.
    Provides explicit instructions to avoid adding facts not in the original text.
    """
    if length_choice == '1':  # short
        length_instructions = (
            "Please provide a BRIEF summary (about 2-3 sentences) of the following text. "
            "Focus on the key points. Be concise, omit minor details, and do not invent additional information."
        )
    elif length_choice == '3':  # long
        length_instructions = (
            "Please provide a DETAILED summary of the following text in multiple paragraphs. "
            "Include context and relevant details, but do NOT fabricate facts not supported by the text."
        )
    else:  # '2' => medium
        length_instructions = (
            "Please provide a MODERATE-LENGTH summary, around one short paragraph, of the following text. "
            "Cover main ideas without being overly brief or too long, and do not add new facts."
        )

    final_prompt = (
        f"{length_instructions}\n\n"
        "If anything is unclear or not mentioned, simply omit it rather than fabricating information.\n"
        "Here is the text to summarize:\n\n"
        f"{user_text}"
    )
    return final_prompt

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

    ### CHANGED ### Step 2: Instead of manually building "length_prompt", call build_prompt
    final_text_for_api = build_prompt(user_text, length_choice)

    if not GOOGLE_API_KEY:
        # If no real API key, do a dummy response
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

    return render_template(
        'index.html',
        summarized_text=summarized_text,
        summary_word_count=summary_word_count,
        input_word_count=input_word_count
    )

if __name__ == '__main__':
    app.run(debug=True, port=5000)
