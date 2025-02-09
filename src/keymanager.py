'''
This module is responsible for handling the key events.
'''

import pygame as pg

class KeyManager:
    def __init__(self):
        self.quit = False
        self.mouse_button_down = False
        self.mouse_pos = (0, 0)
        self.backspace_pressed = False

    def handle_events(self):
        self.reset_flags()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit = True
            elif event.type == pg.MOUSEBUTTONDOWN:
                self.mouse_button_down = True
                self.mouse_pos = pg.mouse.get_pos()
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_BACKSPACE:
                    self.backspace_pressed = True

    def reset_flags(self):
        self.quit = False
        self.mouse_button_down = False
        self.backspace_pressed = False