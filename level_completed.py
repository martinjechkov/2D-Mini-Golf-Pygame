import pygame

class LevelCompletedScreen:
    def __init__(self, screen, level_number, background_surface):
        self.level_number = level_number
        self.background_surface = background_surface

        self.font = pygame.font.Font(None, 36)
        self.title_text = self.font.render(f"LEVEL {self.level_number} COMPLETED", True, (255, 255, 255))
        self.title_rect = self.title_text.get_rect(center= [screen.get_width() // 2, screen.get_height() // 4])

        self.main_menu_button = pygame.Rect(0, 0, 200, 50)
        self.main_menu_button.center = (screen.get_width() // 2, screen.get_height() // 2 + 50)
        self.main_menu_text = self.font.render("Main Menu", True, (255, 255, 255))
        self.main_menu_text_rect = self.main_menu_text.get_rect(center=self.main_menu_button.center)

        self.next_level_button = pygame.Rect(0, 0, 200, 50)
        self.next_level_button.center = (screen.get_width() // 2, self.main_menu_button.center[1] + 100)
        self.next_level_text = self.font.render("Next Level", True, (255, 255, 255))
        self.next_level_text_rect = self.next_level_text.get_rect(center=self.next_level_button.center)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if self.main_menu_button.collidepoint(mouse_pos):
                return "main_menu"
            elif self.next_level_button.collidepoint(mouse_pos):
                return "next_level"
        return None

    def draw(self, screen):
        screen.blit(self.background_surface, (0, 0))
        screen.blit(pygame.image.load("50% dark.PNG"), (0, 0))
        screen.blit(self.title_text, self.title_rect)
        pygame.draw.rect(screen, (0, 128, 255), self.main_menu_button)
        pygame.draw.rect(screen, (0, 128, 255), self.next_level_button)
        screen.blit(self.main_menu_text, self.main_menu_text_rect)
        screen.blit(self.next_level_text, self.next_level_text_rect)
