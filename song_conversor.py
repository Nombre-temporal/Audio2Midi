import librosa
import numpy as np

from Midi import Midi

THRESHOLD = 0



class Song2MidiConverter:
    def __init__(self, model):
        self.model = model

    def preprocess(self, song):
        return song.pad_song(self.model.input_len, self.model.output_step)

    def get_song_segment(self, preprocessed_song, segment_index):
        start = segment_index * self.model.output_step
        end = start + self.model.input_len
        return preprocessed_song[start:end]

    def get_inference_results(self, preprocessed_song):
        actProb, onProb, offProb, volProb = np.empty((1, 88)), np.empty((1, 88)), np.empty((1, 88)), np.empty((1, 88))
        for i in range((preprocessed_song.size - self.model.input_len) // self.model.output_step + 1):
            segment = self.get_song_segment(preprocessed_song, i)
            actProb_segment, onProb_segment, offProb_segment, volProb_segment = self.model.process_song_segment(segment)
            actProb = np.vstack((actProb, actProb_segment))
            onProb = np.vstack((onProb, onProb_segment))
            offProb = np.vstack((offProb, offProb_segment))
            volProb = np.vstack((volProb, volProb_segment))
        return actProb, onProb, offProb, volProb


    def execute(self, song, output_path):
        preprocessed_song = self.preprocess(song)
        actProb, onProb, offProb, volProb = self.get_inference_results(preprocessed_song)
        Midi(song.get_tempo(), actProb, onProb, offProb, volProb).save(output_path)

