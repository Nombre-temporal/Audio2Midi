from Midi import Midi

class Song2MidiConverter:
    def __init__(self, model):
        self.model = model

    def preprocess(self, song):
        return song.pad_song(self.model.input_len, self.model.output_step)

    def process_segment(self, preprocessed_song, segment_index):
        start = segment_index * self.model.output_step
        end = start + self.model.input_len
        return self.model.process_song_segment(preprocessed_song[start:end])

    def get_notes(self, preprocessed_song):
        results = [self.process_segment(preprocessed_song, i) for i in range((preprocessed_song.size - self.model.input_len) // self.model.output_step + 1)]
        print(results)
        return results

    def execute(self, song, output_path):
        preprocessed_song = self.preprocess(song)
        notes = self.get_notes(preprocessed_song)
        midi_data = Midi(notes)
        midi_data.save(output_path)
