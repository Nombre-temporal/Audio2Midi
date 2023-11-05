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

    @staticmethod
    def get_song_key(blacks, gamma):
        return 'Ab'
        MajorMinor = lambda mj, mn: mj if gamma.index(mj) < gamma.index(mn) else mn + 'm'

        if len(blacks) == 0:
            keySignature = MajorMinor('C', 'A')

        elif len(blacks) == 1:
            if blacks[0] == 'F#':
                assert 'F' not in gamma
                keySignature = MajorMinor('G', 'E')
            elif blacks[0] == 'Bb':
                assert 'B' not in gamma
                keySignature = MajorMinor('F', 'D')
            else:
                assert False

        elif len(blacks) == 2:
            if blacks == ['C#', 'F#']:
                assert 'C' not in gamma and 'F' not in gamma
                keySignature = MajorMinor('D', 'B')
            elif blacks == ['Bb', 'Eb']:
                assert 'B' not in gamma and 'E' not in gamma
                keySignature = MajorMinor('Bb', 'G')
            else:
                assert False

        elif len(blacks) == 3:
            if blacks == ['Ab', 'C#', 'F#']:
                assert 'C' not in gamma and 'F' not in gamma and 'G' not in gamma
                keySignature = MajorMinor('A', 'F#')
            elif blacks == ['Ab', 'Bb', 'Eb']:
                assert 'B' not in gamma and 'E' not in gamma and 'A' not in gamma
                keySignature = MajorMinor('Eb', 'C')
            else:
                assert False

        elif len(blacks) == 4:
            if blacks == ['Ab', 'C#', 'Eb', 'F#']:
                assert 'C' not in gamma and 'D' not in gamma and 'F' not in gamma and 'G' not in gamma
                keySignature = MajorMinor('E', 'C#')
            elif blacks == ['Ab', 'Bb', 'C#', 'Eb']:
                assert 'B' not in gamma and 'E' not in gamma and 'A' not in gamma and 'D' not in gamma
                keySignature = MajorMinor('Ab', 'F')
            else:
                assert False

        elif 'B' in gamma and 'E' in gamma:
            keySignature = MajorMinor('B', 'Ab')
        elif 'C' in gamma and 'F' in gamma:
            keySignature = MajorMinor('C#', 'Bb')
        else:
            assert False

        return keySignature

    def __str__(self):
        duration = self.get_duration()
        tempo = self.get_tempo()
        info = f"Song Info:\n"
        info += f"  Path: {self.path}\n"
        info += f"  Sample Rate: {self.sample_rate} Hz\n"
        info += f"  Duration: {duration} seconds\n"
        info += f"  Tempo: {tempo} BPM\n"
        return info

