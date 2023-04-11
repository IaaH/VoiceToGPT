import io
import openai
import speech_recognition as sr
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Configure OpenAI API key
openai.api_key = ""


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/start_recording', methods=['POST'])
def start_recording():
    r = sr.Recognizer()
    audio_file = request.files['file']

    # Save the audio file to disk
    file_id = "audio.wav"
    audio_file.save(file_id)

    with sr.AudioFile(file_id) as source:
        audio_data = r.record(source)

    try:
        text = r.recognize_google(audio_data, language='en-US')
        return jsonify({'text': text, 'file_id': file_id})
    except sr.UnknownValueError:
        return "Speech recognition failed. Please try again.", 400
    except Exception as e:
        return str(e), 500


@app.route('/send_to_chatgpt', methods=['POST'])
def send_to_chatgpt():
    file_id = request.form['file_id']

    with sr.AudioFile(file_id) as source:
        audio_data = r.record(source)
    text = r.recognize_google(audio_data, language='en-US')

    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=text,
        max_tokens=150,
        n=1,
        stop=None,
        temperature=0.5,
    )

    answer = response.choices[0].text.strip()
    return jsonify({"answer": answer})


if __name__ == '__main__':
    app.run(debug=True)
