import cv2
import mediapipe as mp
import numpy as np
import pyaudio
import math

# Inicializar MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_drawing = mp.solutions.drawing_utils

# Inicializar PyAudio
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paFloat32, channels=1, rate=44100, output=True)

# Función para generar un tono
def play_tone(frequency, length, rate=44100):
    t = np.linspace(0, length, int(length * rate), False)
    note = np.sin(frequency * 2 * np.pi * t)
    stream.write(note.astype(np.float32).tobytes())

# Iniciar la captura de la webcam
cap = cv2.VideoCapture(0)

try:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            continue

        # Procesar la imagen y detectar la mano
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(image)

        # Dibujar las anotaciones de la mano
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                # Tomar la posición del dedo índice
                x = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x
                y = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y

                # Usar la altura de la mano para cambiar la frecuencia del tono
                height, width, _ = frame.shape
                frequency = 440 + (height - y * height) * 2
                play_tone(frequency, 0.1)

        # Mostrar el frame
        cv2.imshow('Hand Tracking', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
finally:
    cap.release()
    cv2.destroyAllWindows()
    stream.stop_stream()
    stream.close()
    p.terminate()
