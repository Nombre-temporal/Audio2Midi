import librosa
import numpy as np


class Song:
    def __init__(self, path, sample_rate):
        self.path = path
        self.sample_rate = sample_rate

    def get_duration(self):
        y, sr = librosa.load(self.path)
        duration = librosa.get_duration(y=y, sr=sr)
        return duration

    def pad_song(self, model_input_len, model_output_step):
        song,_ = librosa.load(self.path)
        paddedSong = np.append(song, np.zeros(-(song.size - model_input_len) % model_output_step, dtype=np.float32))
        return paddedSong

    def get_tempo(self):
        y, sr = librosa.load(self.path)
        tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
        return tempo

    def __str__(self):
        duration = self.get_duration()
        tempo = self.get_tempo()
        info = f"Song Info:\n"
        info += f"  Path: {self.path}\n"
        info += f"  Sample Rate: {self.sample_rate} Hz\n"
        info += f"  Duration: {duration} seconds\n"
        info += f"  Tempo: {tempo} BPM\n"
        return info

