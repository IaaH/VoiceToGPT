import io
import openai
import speech_recognition as sr
from flask import Flask, render_template, request, jsonify
from flask import Flask, request, jsonify
import uuid
import os
import speech_recognition as sr
from pydub import AudioSegment

app = Flask(__name__)

# Configure OpenAI API key
openai.api_key = ""


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/start_recording', methods=['POST'])
def start_recording():
    file = request.files['file']
    file_id = str(uuid.uuid4())
    file.save(file_id)

    # Convert the audio to a supported format
    audio = AudioSegment.from_file(file_id, format="webm")
    audio.export(file_id + ".wav", format="wav")

    with sr.AudioFile(file_id + ".wav") as source:
        recognizer = sr.Recognizer()
        audio_data = recognizer.record(source)
        text = recognizer.recognize_google(audio_data)

    os.remove(file_id)
    os.remove(file_id + ".wav")

    return jsonify({"text": text, "file_id": file_id})


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
