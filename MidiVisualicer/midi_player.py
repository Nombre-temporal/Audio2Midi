from midi_visualization import MidiFile

# Cargar el archivo MIDI
mid = MidiFile("../output.mid")

# Obtener la lista de todos los eventos
events = mid.get_events()

# Obtener el array de numpy de la imagen del piano roll
roll = mid.get_roll()

# Dibujar el piano roll con pyplot
mid.draw_roll()
