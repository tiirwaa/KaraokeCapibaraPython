import pygame
import os

class AudioManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AudioManager, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.initialized = True
            pygame.mixer.init()

    def play_audio(self, filename=None):
        print("Iniciando reproducción de audio")
        if filename is None:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            filename = os.path.join(script_dir, '..', 'res', 'wav', 'capibara.wav')
        pygame.mixer.music.load(filename)
        pygame.mixer.music.play(-1)  # loop

    def stop_audio(self):
        print("Deteniendo audio")
        pygame.mixer.music.stop()