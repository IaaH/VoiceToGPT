let recorder;
let audioBlob;
let mediaRecorder;
let audioChunks = [];

if (typeof MediaStreamRecorder === 'undefined') {
    console.error("MediaStreamRecorder is not defined.");
} else {
    console.log("MediaStreamRecorder is defined.");
}

async function displayResult(text) {
    console.log('display')
    const response = await fetch('/api/chat-gpt', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ text: text })
    });

    if (response.ok) {
        const data = await response.json();
        const result = data.result;
        console.log('GPT Response:', result); // Add this line
        const resultElement = document.createElement('p');
        resultElement.textContent = result;
        document.body.appendChild(resultElement);
    } else {
        alert('Error: failed to get response from GPT API');
    }
}

async function sendVoiceDataToBackend(blob) {
    console.log('send voice')
    const formData = new FormData();
    formData.append("file", blob);

    try {
        const response = await fetch("/api/voice-to-text", {
            method: "POST",
            body: formData,
        });

        if (response.ok) {
            const jsonResponse = await response.json();
            const chatGPTResponse = jsonResponse.data;
            document.getElementById("response").innerText = chatGPTResponse;
        } else {
            console.error("Error during transcription:", response.status, response.statusText);
            document.getElementById("response").innerText = "An error occurred during transcription.";
        }
    } catch (error) {
        console.error("Error:", error);
        document.getElementById("response").innerText = "An error occurred during transcription.";
    }
}


function startRecording() {
    console.log('recordstart')
    audioChunks = [];
    navigator.mediaDevices.getUserMedia({ audio: true })
        .then(stream => {
            mediaRecorder = new MediaStreamRecorder(stream, { mimeType: 'audio/wav' });
            mediaRecorder.start(3000);

            mediaRecorder.ondataavailable = function (blob) {
                audioChunks.push(blob);
            };
        })
        .catch(err => {
            console.error("Error while accessing user media:", err);
            alert("Error: Unable to access microphone. Please check your microphone settings.");
        });
}



function stopRecording() {
    console.log('recordend')
    if (!mediaRecorder) {
        console.error('Error: Media recorder is not defined.');
        return;
    }

    mediaRecorder.stop();
    mediaRecorder.ondataavailable = async (event) => {
        // Convert the recorded Blob to WAV format
        const wavBlob = await convertToWav(event.data);
        sendVoiceDataToBackend(wavBlob);
    };
}



async function convertToWav(blob) {
    console.log('dupa1')
    console.log(blob);
    const arrayBuffer = await blob.arrayBuffer();
    const audioBuffer = await new AudioContext().decodeAudioData(arrayBuffer);
    const wavBuffer = toWav(audioBuffer);
    const wavBlob = new Blob([wavBuffer], { type: 'audio/wav' });
    return wavBlob;
}

