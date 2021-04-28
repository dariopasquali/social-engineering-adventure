import pygame


class SoundPlayer:

    def __init__(self, sound_path):
        self.is_playing = False
        self.current_playing = None

        self.sound_path = sound_path
        self.current_background = ""

        pygame.mixer.init()

        self.modes = {
            "background" : self.play_background,
            'once': self.play_once
        }

    def play(self, track, mode):

        filename = self.sound_path + "/" + track
        self.modes[mode](filename)

    def play_background(self, filename):

        if self.current_background == filename:
            return

        if self.is_playing:
            self.stop_background()

        pygame.mixer.music.load(filename)
        pygame.mixer.music.play(-1, 0.0)
        self.is_playing = True
        self.current_background = filename

    def stop_background(self):
        pygame.mixer.music.stop()
        self.is_playing = False

    def play_once(self, filename):
        if self.current_playing is not None:
            return
        self.current_playing = pygame.mixer.Sound(filename)
        self.current_playing.play()

    def stop(self):
        if self.current_playing is None:
            return
        self.current_playing.stop()
        self.current_playing = None

