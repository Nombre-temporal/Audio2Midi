import numpy as np
import tensorflow as tf


class Audio2MidiModel:
    def __init__(self, model_path):
        self.interpreter = tf.lite.Interpreter(model_path=model_path)
        self.interpreter.allocate_tensors()
        self.input_details = self.interpreter.get_input_details()[0]
        self.output_details = self.interpreter.get_output_details()
        self.input_len = self.input_details['shape'][0]
        self.output_step = self.interpreter.get_output_details()[0]['shape'][1] * 512

    def process_song_segment(self, song_segment):
        self.interpreter.set_tensor(self.input_details['index'], song_segment)
        self.interpreter.invoke()

        def get_output(index):
            return self.interpreter.get_tensor(self.output_details[index]['index'])[0]

        actProb = get_output(0)
        onProb = get_output(1)
        offProb = get_output(2)
        volProb = get_output(3)

        return actProb, onProb, offProb, volProb

    def __str__(self):
        input_shape = self.input_details['shape']
        output_shapes = [detail['shape'] for detail in self.output_details]

        return f"Input shape: {input_shape} \nOutput shapes: {output_shapes}"
