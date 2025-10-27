import random
import pygame

class LyricsManager:
    def __init__(self, lyrics_file='res/txt/letra.txt', word_time=0.3):
        self.word_time = word_time
        self.events = []
        self.current_event_index = 0
        self.last_event_change = 0
        self.current_word_index = 0
        self.last_word_change = 0
        self.current_word_data = []
        self.is_instrumental = False
        self.current_y = 300
        self.load_lyrics(lyrics_file)

    def load_lyrics(self, filename):
        lyrics = []
        with open(filename, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    lyrics.append(line)

        # Procesar eventos: lyrics o instrumentales
        for line in lyrics:
            if line.startswith('[') and line.endswith('s]'):
                try:
                    duration = float(line[1:-2])
                    self.events.append(('instrumental', duration))
                except ValueError:
                    pass
            else:
                self.events.append(('lyric', line))

        # Inicializar el primer evento
        if self.events:
            self._initialize_event()

    def _initialize_event(self):
        event_type, *content = self.events[self.current_event_index]
        if event_type == 'instrumental':
            self.is_instrumental = True
        else:
            self.is_instrumental = False
            self._setup_lyrics(content[0])

    def _setup_lyrics(self, line):
        words = line.split()
        self.current_word_data = []
        if words:
            # Calcular anchos para centrar la línea
            font_normal = pygame.font.Font(None, 40)
            widths = []
            for word in words:
                if word.strip():
                    temp_surf = font_normal.render(word, True, (255,255,255))
                    widths.append(temp_surf.get_width())
            total_width = sum(widths) + (len(widths) - 1) * 20
            start_x = 50
            current_x = start_x
            y = self.current_y
            for word, width in zip(words, widths):
                if not word.strip():
                    continue
                color = (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255))
                angle = 0
                # normal
                surf_normal = font_normal.render(word, True, color)
                surf_normal_rot = pygame.transform.rotate(surf_normal, angle)
                # big
                font_big = pygame.font.Font(None, 80)
                surf_big = font_big.render(word, True, color)
                surf_big_rot = pygame.transform.rotate(surf_big, angle)
                self.current_word_data.append((surf_normal_rot, surf_big_rot, current_x, y))
                current_x += width + 20
        self.current_word_index = 0
        self.last_word_change = 0

    def update(self, time_elapsed):
        current_event = self.events[self.current_event_index]

        # Check for end
        if current_event[0] == 'lyric' and current_event[1] == '[END]':
            return True  # End signal

        # Cambiar evento
        if current_event[0] == 'instrumental':
            duration = current_event[1]
        else:
            line = current_event[1]
            words = line.split()
            duration = self.word_time * len(words) + 1
        if time_elapsed - self.last_event_change >= duration:
            print(f"At time {time_elapsed:.2f}, switching from event {self.current_event_index}: {current_event}, duration {duration}")
            self.current_event_index = (self.current_event_index + 1) % len(self.events)
            self.last_event_change = time_elapsed
            event_type, *content = self.events[self.current_event_index]
            print(f"To event {self.current_event_index}: {event_type}")
            if event_type == 'instrumental':
                self.is_instrumental = True
                print("Setting to instrumental")
            else:
                self.is_instrumental = False
                print("Setting to lyric")
                current_line = content[0]
                if current_line == '[END]':
                    return True
                self._setup_lyrics(current_line)

        # Avanzar palabra
        if not self.is_instrumental and self.current_word_data:
            if time_elapsed - self.last_word_change >= self.word_time:
                self.current_word_index += 1
                self.last_word_change = time_elapsed
                if self.current_word_index >= len(self.current_word_data):
                    self.current_word_index = len(self.current_word_data) - 1

        return False

    def render(self, screen, width, height):
        if self.is_instrumental:
            font = pygame.font.Font(None, 100)
            text_surf = font.render("Instrumental", True, (255, 255, 0))
            screen.blit(text_surf, (width//2 - text_surf.get_width()//2, 100))
        else:
            # Dibujar letras con efecto karaoke por palabras
            for i, (surf_normal, surf_big, x, y) in enumerate(self.current_word_data):
                if i == self.current_word_index:
                    w, h = surf_big.get_size()
                    factor = 2
                    new_w = int(w * factor)
                    new_h = int(h * factor)
                    scaled_surf = pygame.transform.scale(surf_big, (new_w, new_h))
                    screen.blit(scaled_surf, (x, y - 150))
                else:
                    screen.blit(surf_normal, (x, y))