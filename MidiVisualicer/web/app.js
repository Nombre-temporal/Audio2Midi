let player;
const midiFileInput = document.getElementById('midiFile');
const playButton = document.getElementById('playButton');
const visualization = document.getElementById('visualization');
const audioContext = new Tone.Context();

// Function to load and play MIDI file
function playMIDI(file) {
    if (!player) {
        // Initialize the player only once
        player = new Tone.Player().toDestination();
    }

    const reader = new FileReader();
    reader.onload = (e) => {
        const dataUri = e.target.result;
        player.load(dataUri, () => {
            player.start();
        });
    };
    reader.readAsArrayBuffer(file);
}

// Event listener for the play button
playButton.addEventListener('click', () => {
    if (player && player.state === 'started') {
        player.stop();
        playButton.innerText = 'Play';
    } else {
        if (audioContext.state !== 'running') {
            audioContext.resume().then(() => {
                // Start audio after user gesture
                playMIDI(midiFileInput.files[0]);
                playButton.innerText = 'Stop';
            });
        } else {
            playMIDI(midiFileInput.files[0]);
            playButton.innerText = 'Stop';
        }
    }
});

// Event listener for MIDI file input
midiFileInput.addEventListener('change', (e) => {
    const file = e.target.files[0];
    if (file) {
        playMIDI(file);
    }
});
