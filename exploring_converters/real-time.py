import tensorflow as tf
import os
from basic_pitch.inference import predict
from basic_pitch import ICASSP_2022_MODEL_PATH

# Cargar el modelo de pitch
basic_pitch_model = tf.saved_model.load(str(ICASSP_2022_MODEL_PATH))

# Especifica la carpeta donde se encuentran los archivos de audio
audio_folder = "./audios"

# Obtén una lista de archivos de audio en la carpeta
audio_files = [os.path.join(audio_folder, filename) for filename in os.listdir(audio_folder) if filename.endswith(".wav")]

for audio_path in audio_files:
    # Procesar un archivo de audio
    model_output, midi_data, note_events = predict(audio_path, basic_pitch_model)
    print()
    # Puedes hacer lo que necesites con los resultados aquí

# Finalmente, puedes realizar cualquier operación que requieras con los resultados.

