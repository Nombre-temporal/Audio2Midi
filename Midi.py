import librosa
import pretty_midi as pm
import numpy as np

from song import Song

FRAMELEN = librosa.frames_to_time(1)
THRESHOLD = 0

class MidiNote:
    def __init__(self, pitch, start, end, velocity):
        self.pitch = pitch
        self.start = start
        self.end = end
        self.velocity = velocity

class Midi:
    def __init__(self, tempo, actProb, onProb, offProb, volProb):
        self.tempo = tempo
        self.track = self.get_track_from_probabilities(actProb, onProb, volProb)
        self.midi = self.create_midi()
        self.actProb = actProb
        self.onProb = onProb
        self.offProb = offProb
        self.volProb = volProb

    def create_midi(self):
        midi = pm.PrettyMIDI(initial_tempo=self.tempo)
        midi.instruments.append(self.track)

        notes = midi.get_pitch_class_histogram()
        gamma = [n for _, n in sorted([(count, ['C', 'C#', 'D', 'Eb', 'E', 'F', 'F#', 'G', 'Ab', 'A', 'Bb', 'B'][i])
                                       for i, count in enumerate(notes)], reverse=True)[:7]]
        blacks = sorted(n for n in gamma if len(n) > 1)
        keySignature = Song.get_song_key(blacks, gamma)
        midi.key_signature_changes += [pm.KeySignature(pm.key_name_to_key_number(keySignature), 0)]
        return midi

    def save(self, output_path):
        self.midi.write(output_path)

    def get_track_from_probabilities(self, actProb, onProb, volProb):
        track = pm.Instrument(program=pm.instrument_name_to_program('Acoustic Grand Piano'),
                              name='Acoustic Grand Piano')
        intervals, frameLenSecs = {}, librosa.frames_to_time(1)  # Time is in absolute seconds, not relative MIDI ticks
        onsets = (onProb > THRESHOLD).astype(np.int8)
        frames = onsets | (actProb > THRESHOLD).astype(
            np.int8)  # Ensure that any frame with an onset prediction is considered active.

        def EndPitch(pitch, endFrame):

            if volProb[intervals[pitch], pitch] < 0 or volProb[intervals[pitch], pitch] > 1: return
            track.notes += [pm.Note(int(max(0, min(1, volProb[intervals[pitch], pitch])) * 80 + 10), pitch + 21,
                                    intervals[pitch] * frameLenSecs, endFrame * frameLenSecs)]
            del intervals[pitch]

        # Add silent frame at the end, so we can do a final loop and terminate any notes that are still active:
        for i, frame in enumerate(np.vstack([frames, np.zeros(frames.shape[1])])):
            for pitch, active in enumerate(frame):
                if active:
                    if pitch not in intervals:
                        if onsets is None:
                            intervals[pitch] = i
                        elif onsets[i, pitch]:
                            intervals[pitch] = i  # Start a note only if we have predicted an onset
                        # else: Even though the frame is active, there is no onset, so ignore it
                    elif onsets is not None:
                        if (onsets[i, pitch] and not onsets[i - 1, pitch]):
                            EndPitch(pitch,
                                     i)  # Pitch is already active, but because of a new onset, we should end the note
                            intervals[pitch] = i  # and start a new one
                elif pitch in intervals:
                    EndPitch(pitch, i)

        if track.notes: assert len(frames) * frameLenSecs >= track.notes[-1].end, 'Wrong MIDI sequence duration'
        return track
