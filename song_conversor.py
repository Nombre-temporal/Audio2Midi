from Midi import Midi


class Song2MidiConversor:
    def __init__(self, model):
        self.model = model

    def preprocess(self, song):
        return []

    def get_notes(self, preprocessed_song):
        results = []
        for segment in preprocessed_song:
            results += self.model.process_song_segment(segment)
        return results

    def execute(self, song, output_path):
        preprocessed_song = self.preprocess(song)
        notes = self.get_notes(preprocessed_song)
        Midi(notes).save(output_path)
