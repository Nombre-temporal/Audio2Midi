class PitchDetector:
    def __init__(self, inference_model):
        """
        Inicializa el detector de tono con un modelo de inferencia dado.

        :param inference_model: Un modelo de inferencia que puede procesar audio y estimar el tono.
        """
        self.model = inference_model

    def detect_pitch(self, audio_input):
        """
        Detecta el tono en una entrada de audio.

        :param audio_input: La entrada de audio para detectar el tono.
        :return: El tono detectado.
        """
        # Aquí, utilizamos el modelo de inferencia para detectar el tono.
        # Esta es una llamada ficticia y debería ser reemplazada con la lógica real del modelo.
        return self.model.estimate_pitch(audio_input)

# Ejemplo de uso
# Supongamos que tenemos una clase de modelo de inferencia llamada MyInferenceModel
# que tiene un método estimate_pitch() para estimar el tono.

# Crear una instancia del modelo de inferencia
inference_model = MyInferenceModel()

# Crear una instancia del detector de tono
pitch_detector = PitchDetector(inference_model)

# Detectar el tono en una entrada de audio (ficticia)
audio_input = "path/to/audio/file.wav"
pitch = pitch_detector.detect_pitch(audio_input)
print("Detected pitch:", pitch)

