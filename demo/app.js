let mediaRecorder;
let audioChunks = [];
let isRecording = false;

const recordButton = document.getElementById("recordButton");

recordButton.addEventListener("click", () => {
    // Verificar el estado actual de la grabación
    if (isRecording) {
        stopRecording();
    } else {
        startRecording();
    }
});

function startRecording() {
    navigator.mediaDevices.getUserMedia({ audio: true })
        .then(stream => {
            mediaRecorder = new MediaRecorder(stream);
            mediaRecorder.start();
            isRecording = true;
            recordButton.textContent = "Detener Grabación";
            audioChunks = [];

            mediaRecorder.addEventListener("dataavailable", event => {
                audioChunks.push(event.data);
            });

            mediaRecorder.addEventListener("stop", () => {
                const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
                uploadAudio(audioBlob);
            });
        });
}

function stopRecording() {
    if (mediaRecorder) {
        mediaRecorder.stop();
        isRecording = false;
        recordButton.textContent = "Grabar Audio";
    }
}

function uploadAudio(blob) {
    const formData = new FormData();
    formData.append("audio", blob, "audio.wav");

    // Convierte el archivo WAV en MP3 antes de subirlo
    convertWavToMp3(blob, mp3Blob => {
        formData.set("audio", mp3Blob, "audio.mp3");

        fetch("/upload", {
            method: "POST",
            body: formData
        }).then(response => response.json())
          .then(data => {
              if (data.success) {
                  // Aquí puedes manejar la respuesta del servidor, como mostrar el archivo MP3 generado
              }
          })
          .catch(error => console.error('Error:', error));
    });
}

function convertWavToMp3(wavBlob, callback) {
    const reader = new FileReader();
    reader.onload = function() {
        const wavData = new DataView(reader.result);

        const encoder = new lamejs.Mp3Encoder(1, 44100, 128); // Mono, 44.1 kHz, 128 kbps

        const samples = new Int16Array(wavData.byteLength / 2);
        let sampleIndex = 0;

        // Convierte los datos WAV en muestras
        for (let i = 44; i < wavData.byteLength; i += 2) {
            samples[sampleIndex++] = wavData.getInt16(i, true);
        }

        const mp3Data = encoder.encodeBuffer(samples);

        // Finaliza la codificación MP3
        const mp3Blob = new Blob([mp3Data], { type: 'audio/mp3' });
        callback(mp3Blob);
    };

    reader.readAsArrayBuffer(wavBlob);
}