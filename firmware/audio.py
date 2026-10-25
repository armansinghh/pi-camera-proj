"""
audio plays through the pcm5102 dac -> tda1308 amp -> headphone jack

uses pygame.mixer (sudo apt install python3-pygame).

NOTE: the logic is tested with a dummy audio driver, but real sound can only be
tested once the dac is wired up.

put songs in ~/music
"""
import os

import pygame

MUSIC_DIR = os.path.expanduser("~/music")
EXTENSIONS = (".mp3",)
VOLUME_STEP = 0.1


class Player:
    def __init__(self):
        os.makedirs(MUSIC_DIR, exist_ok=True)
        pygame.mixer.init()
        self.tracks = sorted(f for f in os.listdir(MUSIC_DIR) if f.lower().endswith(EXTENSIONS))
        self.index = 0
        self.volume = 0.5
        self.state = "stopped"  # stopped or playing or paused
        pygame.mixer.music.set_volume(self.volume)

    def _load_and_play(self):
        path = os.path.join(MUSIC_DIR, self.tracks[self.index])
        pygame.mixer.music.load(path)
        pygame.mixer.music.play()
        self.state = "playing"

    def toggle(self):
        """play/pause button"""
        if not self.tracks:
            return
        if self.state == "stopped":
            self._load_and_play()
        elif self.state == "playing":
            pygame.mixer.music.pause()
            self.state = "paused"
        else:
            pygame.mixer.music.unpause()
            self.state = "playing"

    def next(self):
        if not self.tracks:
            return
        self.index = (self.index + 1) % len(self.tracks)
        self._load_and_play()

    def prev(self):
        if not self.tracks:
            return
        self.index = (self.index - 1) % len(self.tracks)
        self._load_and_play()

    def _set_volume(self, v):
        self.volume = round(min(1.0, max(0.0, v)), 2)
        pygame.mixer.music.set_volume(self.volume)

    def volume_up(self):
        self._set_volume(self.volume + VOLUME_STEP)

    def volume_down(self):
        self._set_volume(self.volume - VOLUME_STEP)

    def stop(self):
        pygame.mixer.music.stop()
        self.state = "stopped"

    def update(self):
        if self.state == "playing" and not pygame.mixer.music.get_busy():
            self.next()