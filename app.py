from flask import Flask, render_template, request, jsonify
import speech_recognition as sr
import requests

app = Flask(__name__)
app.static_folder = 'static'
API_KEY = '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'

@app.route('/')
def index():
    print('start?')
    return render_template('index.html')

@app.route('/api/voice-to-text', methods=['POST'])
def voice_to_text():
    print('voice to text')
    recognizer = sr.Recognizer()
    file = request.files['file']
    with sr.AudioFile(file) as source:
        audio = recognizer.record(source)
    try:
        text = recognizer.recognize_google(audio)
        print('Recognized text:', text)
        return jsonify({'text': text})
    except sr.UnknownValueError:
        return jsonify({'error': 'Speech recognition failed'}), 400



def chat_gpt(prompt):
    print('chat gpt')
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {API_KEY}'
    }

    response = requests.post(
        'https://api.openai.com/v1/engines/davinci-codex/completions',
        headers=headers,
        json={
            'prompt': prompt,
            'max_tokens': 100
        }
    )

    if response.status_code == 200:
        result = response.json()['choices'][0]['text']
        print("GPT-4 Response:", result)
        return jsonify({'text': prompt, 'result': result})
    else:
        return jsonify({'error': 'GPT API call failed'}), 400

if __name__ == '__main__':
    print('main')
    app.run(debug=True)