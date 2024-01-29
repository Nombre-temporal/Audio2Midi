import math
import cv2
import mediapipe as mp
import pygame

# Constantes y configuraciones
CAMERA_INDEX = 0
ESC_KEY = 27
AUDIO_FILES = {
    "right_hand_up": "./wavs/right_hand_up.wav",
    "right_hand_left": "./wavs/right_hand_left.wav",
    "right_hand_down": "./wavs/right_hand_down.wav",
    "right_hand_right": "./wavs/right_hand_right.wav"
}

class HandDetector:
    """Clase para detectar las manos utilizando MediaPipe."""

    def __init__(self, detection_confidence=0.7):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(min_detection_confidence=detection_confidence)
        self.mp_draw = mp.solutions.drawing_utils

    def detect_hands(self, image):
        """Detecta las manos en la imagen y las dibuja."""
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(image_rgb)
        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                self.mp_draw.draw_landmarks(image, handLms, self.mp_hands.HAND_CONNECTIONS)
        return image

    def find_position(self, image, hand_no=0):
        """Encuentra la posición de la mano en la imagen."""
        lm_list = []
        if self.results.multi_hand_landmarks:
            my_hand = self.results.multi_hand_landmarks[hand_no]
            for id, lm in enumerate(my_hand.landmark):
                h, w, c = image.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lm_list.append((id, cx, cy))
        return lm_list

import pygame
import threading
import time

class AudioPlayer:
    """Clase para reproducir audio con Pygame, sincronizado con los BPM y con una cola de reproducción que mantiene solo el último audio por canal."""

    def __init__(self, num_channels=2, bpm=90):
        pygame.init()
        self.channels = [pygame.mixer.Channel(i) for i in range(num_channels)]
        self.bpm = bpm
        self.beat_duration = 60 / bpm  # Duración de un tiempo en segundos
        self.next_beat_time = time.time()  # Tiempo para el próximo beat
        self.play_queue = {}  # Cola de reproducción, una entrada por canal
        self.lock = threading.Lock()
        self.play_thread = threading.Thread(target=self._play_thread)
        self.play_thread.start()

    def play_audio(self, audio_file, hand_index):
        """Encola un archivo de audio para ser reproducido sincronizado con el compás."""
        with self.lock:
            # Actualizar la cola para este canal con el último archivo de audio solicitado
            self.play_queue[hand_index] = audio_file

    def _play_thread(self):
        """Hilo que maneja la reproducción de sonidos."""
        while True:
            with self.lock:
                if time.time() >= self.next_beat_time:
                    for hand_index, audio_file in self.play_queue.items():
                        channel = self.channels[hand_index]
                        if channel.get_busy():
                            channel.stop()
                        sound = pygame.mixer.Sound(audio_file)
                        channel.play(sound)
                    # Limpiar la cola y establecer el tiempo para el próximo beat
                    self.play_queue.clear()
                    self.next_beat_time = time.time() + 8 * self.beat_duration

            time.sleep(0.01)  # Pequeña espera para evitar uso excesivo de CPU

    def __del__(self):
        pygame.quit()







def calculate_angle(wrist, middle_tip):
    """Calcula el ángulo entre la muñeca y la punta del dedo medio."""
    dx = middle_tip[1] - wrist[1]
    dy = middle_tip[2] - wrist[2]
    angle_rad = math.atan2(dy, dx)
    return (math.degrees(angle_rad) + 360) % 360

def initialize_camera(index=CAMERA_INDEX):
    """Inicializa y retorna el objeto de captura de la cámara."""
    cap = cv2.VideoCapture(index)
    if not cap.isOpened():
        raise IOError("Error: No se pudo abrir la cámara.")
    return cap

def process_image(hand_detector, audio_player, image):
    """Procesa la imagen detectando manos y decidiendo qué audio reproducir."""
    image = cv2.flip(image, 1)
    image = hand_detector.detect_hands(image)

    if hand_detector.results.multi_hand_landmarks:
        for hand_no, _ in enumerate(hand_detector.results.multi_hand_landmarks):
            lm_list = hand_detector.find_position(image, hand_no)
            if lm_list:
                play_audio_based_on_hand_position(audio_player, lm_list, hand_no)

    return image


def play_audio_based_on_hand_position(audio_player, lm_list, hand_no):
    """Decide qué audio reproducir basado en la posición de la mano."""
    wrist = lm_list[0]
    middle_tip = lm_list[12]
    angle_deg = calculate_angle(wrist, middle_tip)

    #print(f"Ángulo entre la muñeca y la punta del dedo medio: {angle_deg} grados")

    if 225 <= angle_deg < 315:
    #    print("Reproduciendo audio: right_hand_up")
        audio_player.play_audio(AUDIO_FILES["right_hand_up"], hand_no)
    elif 135 <= angle_deg < 225:
    #    print("Reproduciendo audio: right_hand_left")
        audio_player.play_audio(AUDIO_FILES["right_hand_left"], hand_no)
    elif 45 <= angle_deg < 135:
    #    print("Reproduciendo audio: right_hand_down")
        audio_player.play_audio(AUDIO_FILES["right_hand_down"], hand_no)
    else:
    #    print("Reproduciendo audio: right_hand_right")
        audio_player.play_audio(AUDIO_FILES["right_hand_right"], hand_no)

def main():
    try:
        cap = initialize_camera()
        hand_detector = HandDetector()
        audio_player = AudioPlayer()

        while True:
            success, image = cap.read()
            if not success:
                continue

            image = process_image(hand_detector, audio_player, image)
            cv2.imshow("Hand Tracking", image)

            if cv2.waitKey(1) & 0xFF == ESC_KEY:
                break
    except IOError as e:
        print(e)
    finally:
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
