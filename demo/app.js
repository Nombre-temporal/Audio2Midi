let mediaRecorder;
let audioChunks = [];
let isRecording = false;

const recordButton = document.getElementById("recordButton");

recordButton.addEventListener("click", () => {
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

function uploadAudio(mp3Blob) {
    const formData = new FormData();
    formData.append("audio", mp3Blob, "audio.mp3");

    fetch("/upload", {
        method: "POST",
        body: formData
    }).then(response => response.json())
      .then(data => {
          if (data.success) {
              console.log("Audio subido con éxito");
          }
      })
      .catch(error => console.error('Error:', error));
}
