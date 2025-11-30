from typing import List

import pygame

from src.core.resolution import ResolutionHandler
from src.core.sources import load_image, load_theme, Resources
from src.dialogs.dialog import BaseDialog
from src.repositories.consequences import ConsequencesRepository
from src.scenes.demo_class_room_teacher_dialogs import TeacherMainDialog, TeacherPostMainDialog
from src.scenes.scene import Scene, Handled, NextScene, TerminateApp
from src.ui.clickable import ClickableArea
from src.ui.dialog import DialogPanel
from src.ui.geometry import relative_rect


class ClassRoom(Scene):
    def __init__(
            self,
            screen: pygame.Surface,
            resolution_handler: ResolutionHandler,
            resources: Resources,
            consequences: ConsequencesRepository,
    ):
        super().__init__()
        self.screen = screen
        self.resolution_handler = resolution_handler
        self.resources = resources
        self.consequences = consequences
        self.background = load_image("background/class_room.png")
        self.background = pygame.transform.scale(self.background, self.resolution_handler.get_scaled_resolution())
        self.teacher_dialog: None | BaseDialog = None
        teacher_rect = relative_rect(screen, 0.475, 0.175, 0.115, 0.75)
        self.teacher = ClickableArea(teacher_rect.x, teacher_rect.y, teacher_rect.width, teacher_rect.height)
        self.teacher_img_path = "character/old_teacher.png"

        self.theme = load_theme("fucking_school.mp3")
        pygame.mixer.music.load(self.theme)
        pygame.mixer.music.play(-1)

        dialog_rec = relative_rect(screen, 0.70, 0.0, 0.28, 1.0)
        self.dialog_panel = DialogPanel(dialog_rec.x, dialog_rec.y, dialog_rec.width, dialog_rec.height,
                                        padding=12, line_spacing=4, option_hover_sfx="option_hover.mp3")
        self.focused_object = None
        self.overlay = None

    def on_teacher_area_click(self):
        if self.consequences.is_Kento_off:
            self.teacher_dialog = TeacherPostMainDialog(self.resources, self.consequences)
        elif self.teacher_dialog is None:
            self.teacher_dialog = TeacherMainDialog(self.resources, self.consequences)

        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        self.focused_object = load_image(self.teacher_img_path)
        self.focused_object = pygame.transform.scale(self.focused_object,
                                                     self.resolution_handler.get_scaled_resolution())
        overlay_surface = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        overlay_surface.fill((0, 0, 0, 128))
        self.overlay = overlay_surface
        self.dialog_panel.set_dialog(self.teacher_dialog)

    def handle_events(self, events: List[pygame.event.Event]) -> Handled | NextScene | TerminateApp:
        # 1) ダイアログが出ているときは、ダイアログだけイベント処理
        if self.dialog_panel.text_height:
            if self.dialog_panel.handle_event(events):
                self.dialog_panel.set_is_active(False)
                self.focused_object = None
                self.overlay = None
                if self.consequences.is_teacher_knocked:
                    self.teacher_img_path = "character/old_teacher_knocked.png"
                    # This is not efficient to reload entire background, and it would be better to replace
                    # the teacher path only, but this screen is just a demo, so it's ok here.
                    self.background = load_image("background/class_room_teacher_knocked.png")
                    self.background = pygame.transform.scale(self.background,
                                                             self.resolution_handler.get_scaled_resolution())
                    teacher_rect = relative_rect(self.screen, 0.475, 0.7, 0.115, 0.30)
                    self.teacher = ClickableArea(teacher_rect.x, teacher_rect.y, teacher_rect.width,
                                                 teacher_rect.height)
            return Handled()

        # 2) ダイアログが出ていないときは、先生クリックなどを処理
        for event in events:
            if event.type == pygame.QUIT:
                return TerminateApp()
            if event.type == pygame.MOUSEMOTION:
                self.teacher.check_hover(event.pos)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.teacher.check_click(event.pos):
                    self.on_teacher_area_click()
            if event.type == pygame.VIDEORESIZE:
                self.resolution_handler.update_resolution((event.w, event.h))
                self.background = pygame.transform.scale(
                    self.background,
                    self.resolution_handler.get_scaled_resolution()
                )

        return Handled()

    def draw(self, screen: pygame.Surface):
        screen.blit(self.background, (0, 0))
        if self.overlay:
            screen.blit(self.overlay, (0, 0))
        if self.focused_object:
            screen.blit(self.focused_object, (0, 0))
        if self.dialog_panel.is_active:
            self.dialog_panel.draw(screen)
