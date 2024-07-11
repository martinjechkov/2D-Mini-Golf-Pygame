from enum import Enum
import pygame

class ObjectType(Enum):
    OBSTACLE = 1
    HOLE = 2
    TELEPORT_PAD = 3

class Object:
    def __init__(self, shape, position, size, object_type, color):
        self.shape = shape
        self.position = position
        self.size = size
        self.object_type = object_type
        self.color = color

    def draw(self, screen):
        if self.shape == 'circle':
            self.draw_circle_alpha(screen, self.color, self.position, self.size)
        elif self.shape == 'rectangle':
            self.draw_rect_alpha(screen, self.color, (*self.position, *self.size))

    def draw_circle_alpha(self, surface, color, center, radius):                                    # We have to draw every shape on a new Surface and then draw it on the actual
        target_rect = pygame.Rect(center, (0, 0)).inflate((radius * 2, radius * 2))                 # screen. pygame.draw... doesn't draw the alpha value of the color so we
        shape_surf = pygame.Surface(target_rect.size, pygame.SRCALPHA)                              # can't have something be transparent unless we do this. 
        pygame.draw.circle(shape_surf, color, (radius, radius), radius)                             # Borrowed from: https://stackoverflow.com/a/64630102
        surface.blit(shape_surf, target_rect)                                                       #

    def draw_rect_alpha(self, surface, color, rect):
        shape_surf = pygame.Surface(pygame.Rect(rect).size, pygame.SRCALPHA)
        pygame.draw.rect(shape_surf, color, shape_surf.get_rect())
        surface.blit(shape_surf, rect)

    def draw_polygon_alpha(self, surface, color, points):
        lx, ly = zip(*points)
        min_x, min_y, max_x, max_y = min(lx), min(ly), max(lx), max(ly)
        target_rect = pygame.Rect(min_x, min_y, max_x - min_x, max_y - min_y)
        shape_surf = pygame.Surface(target_rect.size, pygame.SRCALPHA)
        pygame.draw.polygon(shape_surf, color, [(x - min_x, y - min_y) for x, y in points])
        surface.blit(shape_surf, target_rect)

class TeleportPad(Object):
    def __init__(self, shape, position, size, destination, color):
        super().__init__(shape, position, size, ObjectType.TELEPORT_PAD, color)
        self.destination = destination

    def teleport_ball(self, ball):
        ball.position = list(self.destination)
        ball.velocity = [0, 0]

class GameLevel:
    def __init__(self, background_image):
        self.objects = []
        self.background_image = background_image
        self.shot_counter = ShotCounter()

    def add_object(self, game_object):
        self.objects.append(game_object)

    def draw_objects(self, screen):
        screen.blit(self.background_image, (0, 0))
        for obj in self.objects:
            obj.draw(screen)

class ShotCounter:
    def __init__(self):
        self.shot_count = 0
        self.font = pygame.font.Font(None, 36)
        self.update_text()

    def increase_shot_count(self):
        self.shot_count += 1

    def draw(self, screen):
        self.update_text()
        self.shot_counter_rect = self.shot_counter_text.get_rect(topright= [screen.get_width(), 0])
        screen.blit(self.shot_counter_text, self.shot_counter_rect)

    def update_text(self):
        self.shot_counter_text = self.font.render(f"Shot Count: {self.shot_count}", True, (255, 255, 255))