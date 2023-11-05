
const midiFileInput = document.getElementById('midiFileInput');
const staffContent = document.querySelector('.staff-content');

midiFileInput.addEventListener('change', (event) => {
  const file = event.target.files[0];
  const reader = new FileReader();

  reader.onload = (readerEvent) => {
    const midiData = readerEvent.target.result;
    const midiPlayer = document.querySelector('midi-player');
    midiPlayer.setAttribute('src', URL.createObjectURL(file));

    // No es necesario volver a agregar <midi-visualizer> al contenedor
  };

  reader.readAsArrayBuffer(file);
});

const midiPlayer = document.querySelector('midi-player');
const staffVisualizer = document.getElementById('staff-visualizer');

// Detecta cuando la reproducción del MIDI comienza
midiPlayer.addEventListener('click', () => {

  staffVisualizer.style.padding = `1rem`;
  staffVisualizer.style.animation = `1rem`;

  
});
