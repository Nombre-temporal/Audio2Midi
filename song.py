import librosa

class Song:
    def __init__(self, path, sample_rate):
        self.path = path
        self.sample_rate = sample_rate

    def get_duration(self):
        y, sr = librosa.load(self.path)
        duration = librosa.get_duration(y=y, sr=sr)
        return duration

