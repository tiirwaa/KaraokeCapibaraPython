import winsound
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
            # Deshabilitar audio en SDL para que winsound funcione
            os.environ['SDL_AUDIODRIVER'] = 'dummy'
            os.environ['SDL_INIT_AUDIO'] = '0'

    def play_audio(self, filename='capibara.wav'):
        print("Iniciando reproducción de audio")
        winsound.PlaySound(filename, winsound.SND_FILENAME | winsound.SND_ASYNC | winsound.SND_LOOP)

    def stop_audio(self):
        print("Deteniendo audio")
        winsound.PlaySound(None, winsound.SND_PURGE)