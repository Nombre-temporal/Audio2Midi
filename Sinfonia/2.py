import pygame

# Initialize Pygame
pygame.init()

# Set up the display (not necessary for audio, but Pygame requires it)
screen = pygame.display.set_mode((200, 200))

# Load an audio file
audio_file = "wavs/right_hand_up.wav"  # Replace with the path to your audio file
pygame.mixer.music.load(audio_file)

# Play the audio
pygame.mixer.music.play()

# Run a loop to keep the program running while the audio plays
while pygame.mixer.music.get_busy():
    pygame.time.Clock().tick(30)

# Quit Pygame
pygame.quit()

