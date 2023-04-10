import os
import io
import uuid
import openai
import speech_recognition as sr
from flask import Flask, render_template, request, jsonify
from pydub import AudioSegment
import io

app = Flask(__name__)

# Configure OpenAI API key
openai.api_key = "your_openai_api_key"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start_recording', methods=['POST'])
def start_recording():
    voice_data = request.files['file']
    voice_data.save("voice.wav")

    # Convert the audio to the desired format
    audio = AudioSegment.from_file("voice.wav")
    audio = audio.set_frame_rate(16000).set_sample_width(2).set_channels(1)
    byte_io = io.BytesIO()
    audio.export(byte_io, format="wav")
    byte_io.seek(0)

    # Recognize the speech
    r = sr.Recognizer()
    with sr.AudioFile(byte_io) as source:
        audio_data = r.record(source)
    text = r.recognize_google(audio_data, language='en-US')

    # Replace this with the API call to GPT-3
    response = {
        "response": text
    }
    return jsonify(response)


@app.route('/send_to_chatgpt', methods=['POST'])
def send_to_chatgpt():
    file_id = request.form['file_id']

    with open(f"{file_id}.txt", "r") as text_file:
        text = text_file.read()

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
