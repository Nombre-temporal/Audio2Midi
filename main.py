from audio2midi_model import Audio2MidiModel
from song_conversor import Song2MidiConversor
from song import Song

song = Song('./son1.wav', 16_000)
model = Audio2MidiModel("models/onsets_frames_wavinput.tflite")
song_2_midi_conversion = Song2MidiConversor(model)
song_2_midi_conversion.execute(song, "output.mid")

