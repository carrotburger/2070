import pygame

from src.config.display import SCREEN_WIDTH, SCREEN_HEIGHT, TARGET_FPS
from src.core.resolution import ResolutionHandler
from src.scenes.coordinator import Coordinator, SceneTag
from src.scenes.scene import NextScene, TerminateApp

APP_TITLE = "2070"


class App:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(APP_TITLE)
        self.display_surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
        self.screen = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.coordinator = Coordinator(self.screen, ResolutionHandler((SCREEN_WIDTH, SCREEN_HEIGHT)))
        self.current_scene = self.coordinator.next_scene(SceneTag.MAIN_MENU)
        self.running = True

    def run(self):
        while self.running:
            dt = self.clock.tick(TARGET_FPS) / 1000.0
            result = self.current_scene.handle_events(pygame.event.get())
            if type(result) == TerminateApp:
                self.running = False

            if type(result) == NextScene:
                tag = result.get_tag()
                self.current_scene = self.coordinator.next_scene(tag)

            self.current_scene.update(dt)
            self.current_scene.draw(self.screen)
            self.display_surface.blit(pygame.transform.scale(self.screen, self.display_surface.get_size()), (0, 0))
            pygame.display.flip()
        pygame.quit()
