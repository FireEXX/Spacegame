import pygame
from pathlib import Path

highscore_file = Path("highscore.txt")

class highscore:
    def __init__(self):
        self.start_ticks = pygame.time.get_ticks()
        self.end_ticks = None
        self.time = 0

    def stop(self):
        self.end_ticks = pygame.time.get_ticks()
        self.time = round((self.end_ticks - self.start_ticks) / 1000, 2)
        return self.time

    def get_time(self):
        return round((pygame.time.get_ticks() - self.start_ticks) / 1000, 2)

    def save_highscore(self):
        new_highscore = highscore_file.read_text().strip()
        if new_highscore.replace('.', '', 1).isdigit():
            highscore = float(new_highscore)
        else:
            highscore = None

        if highscore is None or self.time < highscore:
            highscore_file.write_text(str(self.time))

    def load_highscore(self):
        new_highscore = highscore_file.read_text().strip()
        if new_highscore.replace('.', '', 1).isdigit():
            return float(new_highscore)
        return None
