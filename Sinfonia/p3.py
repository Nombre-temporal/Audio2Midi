import pygame
import time

def play_midi(midi_file):
    # Inicializa pygame y el mixer para reproducir sonido
    pygame.init()
    pygame.mixer.init()

    # Carga el archivo MIDI
    pygame.mixer.music.load(midi_file)

    # Reproduce el archivo MIDI
    pygame.mixer.music.play()

    # Espera hasta que la música termine
    while pygame.mixer.music.get_busy():
        time.sleep(1)

    # Finaliza pygame
    pygame.quit()

# Reemplaza 'path_to_your_midi.mid' con la ruta de tu archivo MIDI
midi_file = 'right_hand_up.mid'
play_midi(midi_file)
