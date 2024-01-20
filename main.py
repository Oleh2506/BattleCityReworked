import pygame
import game_config as gc
import ctypes
from game_assets import GameAssets
from game import Game
from start_screen import StartScreen
from stage_editor import StageEditor
from stage_data import StageData


class Main:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()

        self._screen = pygame.display.set_mode((gc.SCREEN_WIDTH, gc.SCREEN_HEIGHT))
        pygame.display.set_caption("Battle City Reworked")
        self._clock = pygame.time.Clock()

        self._game_assets = GameAssets()

        self._game = None
        self._stage_editor = None
        self._start_screen = StartScreen(self._game_assets)

        self._is_default_game_active = False
        self._is_custom_game_active = False
        self._is_stage_editor_active = False
        self._is_start_screen_active = True

        self._is_game_on = True

    def run(self):
        while self._is_game_on:
            event_list = pygame.event.get()
            for event in event_list:
                if event.type == pygame.QUIT:
                    self._is_game_on = False

            if (self._is_default_game_active or self._is_custom_game_active) and self._game:
                self._game.draw(self._screen)
                self._game.input(event_list)
                self._game.update()

                if self._is_default_game_active:
                    self._is_default_game_active = self._game.is_active
                    if not self._is_default_game_active:
                        self._get_back_to_start_screen()
                else:
                    self._is_custom_game_active = self._game.is_active
                    if not self._is_custom_game_active:
                        self._get_back_to_start_screen()

            if self._is_stage_editor_active and self._stage_editor:
                self._stage_editor.draw(self._screen)
                self._stage_editor.input(event_list)
                self._stage_editor.update()
                self._is_custom_game_active = self._stage_editor.is_active
                if not self._is_custom_game_active:
                    self._get_back_to_start_screen()

            if self._is_start_screen_active and self._start_screen:
                self._start_screen.draw(self._screen)
                self._start_screen.input(event_list)
                self._start_screen.update()

                self._is_start_screen_active = self._start_screen.is_active
                if not self._is_start_screen_active:
                    if self._start_screen.is_default_game_active:
                        self._start_default_game()
                    elif self._start_screen.is_custom_game_active:
                        self._start_custom_game()
                    elif self._start_screen.is_stage_editor_active:
                        self._start_stage_editor()
                    else:
                        self._start_default_game()

            pygame.display.update()
            self._clock.tick(gc.FPS)

    def _start_stage_editor(self):
        self._stage_editor = StageEditor(self._game_assets)
        self._is_stage_editor_active = True
        self._start_screen = None

    def _start_default_game(self):
        self._game = Game(self._game_assets, StageData(gc.DEFAULT_STAGES_DIR,
                                                       gc.NUM_OF_DEFAULT_STAGES).load_stage_data())
        self._is_default_game_active = True
        self._start_screen = None

    def _start_custom_game(self):
        self._game = Game(self._game_assets, StageData(gc.CUSTOM_STAGES_DIR, gc.NUM_OF_CUSTOM_STAGES).load_stage_data())
        self._is_custom_game_active = True
        self._start_screen = None

    def _get_back_to_start_screen(self):
        self._start_screen = StartScreen(self._game_assets)
        self._is_start_screen_active = True
        self._game = None
        self._stage_editor = None


if __name__ == '__main__':
    ctypes.windll.user32.SetProcessDPIAware()
    battleCity = Main()
    battleCity.run()
    pygame.quit()
