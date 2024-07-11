import pygame

class GameCompletedScreen:
    def __init__(self, screen, shot_count):
        self.shot_count = shot_count

        self.font = pygame.font.Font(None, 36)

        self.title_text = self.font.render("VICTORY!", True, (255, 255, 255))
        self.title_rect = self.title_text.get_rect(center= [screen.get_width() // 2, screen.get_height() // 4])

        self.shot_count_text = self.font.render(f"Shot count: {shot_count}", True, (255, 255, 255)) # how to center it when shot count gets loaded in the moment?
        self.shot_count_rect = self.title_text.get_rect(center= [screen.get_width() // 2, screen.get_height() // 3.5])

        self.main_menu_button = pygame.Rect(0, 0, 200, 50)
        self.main_menu_button.center = (screen.get_width() // 2, screen.get_height() // 2 + 50)
        self.main_menu_text = self.font.render("Main Menu", True, (255, 255, 255))
        self.main_menu_text_rect = self.main_menu_text.get_rect(center=self.main_menu_button.center)

        self.quit_game_button = pygame.Rect(0, 0, 200, 50)
        self.quit_game_button.center = (screen.get_width() // 2, self.main_menu_button.center[1] + 100)
        self.quit_game_text = self.font.render("Quit Game", True, (255, 255, 255))
        self.quit_game_text_rect = self.quit_game_text.get_rect(center=self.quit_game_button.center)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if self.main_menu_button.collidepoint(mouse_pos):
                return "main_menu"
            elif self.quit_game_button.collidepoint(mouse_pos):
                return "quit"
        return None

    def draw(self, screen):
        screen.fill((0, 0, 0))
        screen.blit(self.title_text, self.title_rect)
        screen.blit(self.shot_count_text, self.shot_count_rect)
        pygame.draw.rect(screen, (0, 128, 255), self.main_menu_button)
        pygame.draw.rect(screen, (0, 128, 255), self.quit_game_button)
        screen.blit(self.main_menu_text, self.main_menu_text_rect)
        screen.blit(self.quit_game_text, self.quit_game_text_rect)
