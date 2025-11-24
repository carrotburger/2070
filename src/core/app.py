import pygame

from src.config.display import TARGET_FPS
from src.core.resolution import ResolutionHandler
from src.scenes.coordinator import Coordinator, SceneTag
from src.scenes.scene import NextScene, TerminateApp

# ★ 追加：セーブ／ロード用
from src.core.save_manager import save_scene, load_scene

APP_TITLE = "2070"


class App:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(APP_TITLE)
        info = pygame.display.Info()
        self.width = info.current_w
        self.height = info.current_h
        self.display_surface = pygame.display.set_mode(
            (self.width, self.height), pygame.FULLSCREEN
        )
        self.clock = pygame.time.Clock()
        self.coordinator = Coordinator(
            self.display_surface, ResolutionHandler((self.width, self.height))
        )

        # ★ 追加：今どのシーンかをタグで持つ
        self.current_tag = SceneTag.MAIN_MENU
        self.current_scene = self.coordinator.next_scene(self.current_tag)
        self.running = True

    def run(self):
        while self.running:
            dt = self.clock.tick(TARGET_FPS) / 1000.0

            # すべてのイベントを一旦取得
            events = pygame.event.get()

            # --------- グローバルキー処理（F5/F9とか） ----------
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False

                if event.type == pygame.KEYDOWN:
                    # F5 でセーブ
                    if event.key == pygame.K_F5:
                        save_scene(self.current_tag)
                        print("Saved scene:", self.current_tag)

                    # F9 でロード
                    if event.key == pygame.K_F9:
                        tag = load_scene()
                        if tag is not None:
                            self.current_tag = tag
                            self.current_scene = self.coordinator.next_scene(tag)
                            print("Loaded scene:", self.current_tag)
            # ---------------------------------------------------

            # 各シーン側のイベント処理
            result = self.current_scene.handle_events(events)

            if isinstance(result, TerminateApp):
                self.running = False

            if isinstance(result, NextScene):
                tag = result.get_tag()
                # ★ シーンを切り替えるとき、タグも更新
                self.current_tag = tag
                self.current_scene = self.coordinator.next_scene(tag)

            self.current_scene.update(dt)
            self.current_scene.draw(self.display_surface)
            pygame.display.flip()

        pygame.quit()

        
