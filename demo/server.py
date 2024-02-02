from flask import Flask, request, jsonify, send_from_directory
from basic_pitch.inference import predict_and_save

app = Flask(__name__, static_folder='.', static_url_path='')

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'audio' in request.files:
        audio = request.files['audio']
        audio_filename = "audio.mp3"
        audio.save(audio_filename)

        # Procesa el archivo de audio con tu función
        predict_and_save(
            [audio_filename],
            ".",  # Asegúrate de que el directorio de salida sea correcto
            True,
            False,
            False,
            False,
        )

        # Aquí puedes manejar la respuesta, como enviar la ubicación del archivo MIDI generado
        return jsonify(success=True)

    return jsonify(success=False)



if __name__ == '__main__':
    app.run(debug=True)