import pygame

highscore_file = "highscore.txt"

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
        with open(highscore_file, "r") as f:
            content = f.read().strip()

        if content.replace('.', '', 1).isdigit():
            saved_score = float(content)
        else:
            saved_score = None

        if saved_score is None or self.time < saved_score:
            with open(highscore_file, "w") as f:
                f.write(str(self.time))

    def load_highscore(self):
        with open(highscore_file, "r") as f:
            content = f.read().strip()

        if content.replace('.', '', 1).isdigit():
            return float(content)
        return None
