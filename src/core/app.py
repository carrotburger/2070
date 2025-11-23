import pygame

from src.config.display import TARGET_FPS
from src.core.resolution import ResolutionHandler
from src.scenes.coordinator import Coordinator, SceneTag
from src.scenes.scene import NextScene, TerminateApp

APP_TITLE = "2070"


class App:
    def _init_(self):
        pygame.init()
        pygame.display.set_caption(APP_TITLE)
        info = pygame.display.Info()
        self.width = info.current_w
        self.height = info.current_h
        self.display_surface = pygame.display.set_mode((self.width, self.height), pygame.FULLSCREEN)
        self.clock = pygame.time.Clock()
        self.coordinator = Coordinator(self.display_surface, ResolutionHandler((self.width, self.height)))
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
            self.current_scene.draw(self.display_surface)
            pygame.display.flip()
        pygame.quit()
