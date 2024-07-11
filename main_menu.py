import pygame

class MainMenuScreen:
    def __init__(self, screen):
        self.screen = screen
        self.active = True
        self.font = pygame.font.Font(None, 36)

        self.title_text = self.font.render("Main Menu", True, (255, 255, 255))
        self.title_rect = self.title_text.get_rect(center= [self.screen.get_width() // 2, self.screen.get_height() // 4])

        self.start_button = pygame.Rect(0, 0, 200, 50)
        self.start_button.center = (self.screen.get_width() // 2, self.screen.get_height() // 2 + 50)
        self.start_text = self.font.render("Start Game", True, (255, 255, 255))
        self.start_text_rect = self.start_text.get_rect(center=self.start_button.center)

        self.quit_button = pygame.Rect(0, 0, 200, 50)
        self.quit_button.center = (self.screen.get_width() // 2, self.start_button.center[1] + 100)
        self.quit_text = self.font.render("Quit", True, (255, 255, 255))
        self.quit_text_rect = self.quit_text.get_rect(center=self.quit_button.center)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            if self.start_button.collidepoint((mouse_x, mouse_y)):
                return "start"
            elif self.quit_button.collidepoint((mouse_x, mouse_y)):
                return "quit"
        return None

    def draw(self):
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.title_text, self.title_rect)
        pygame.draw.rect(self.screen, (0, 128, 255), self.start_button)
        pygame.draw.rect(self.screen, (0, 128, 255), self.quit_button)
        self.screen.blit(self.start_text, self.start_text_rect)
        self.screen.blit(self.quit_text, self.quit_text_rect)
