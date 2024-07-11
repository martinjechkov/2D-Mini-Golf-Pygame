import pygame
import math
from game_objects import TeleportPad

class Ball:
    def __init__(self, position, radius=10, color=(255, 255, 255)):
        self.position = list(position)
        self.radius = radius
        self.color = color
        self.velocity = [0, 0]
        self.dragging = False
        self.visible = True

    def apply_force(self, force):
        self.velocity[0] += force[0]
        self.velocity[1] += force[1]

    def update(self):
        self.position[0] += self.velocity[0]
        self.position[1] += self.velocity[1]

        self.velocity[0] *= 0.95
        self.velocity[1] *= 0.95

        if abs(self.velocity[0]) < 0.1:
            self.velocity[0] = 0
        if abs(self.velocity[1]) < 0.1:
            self.velocity[1] = 0

    def draw(self, screen):
        if self.visible:
            pygame.draw.circle(screen, self.color, (int(self.position[0]), int(self.position[1])), self.radius)

    def check_collision(self, obj):
        if obj.shape == 'circle':
            dx = self.position[0] - obj.position[0]
            dy = self.position[1] - obj.position[1]
            distance = math.hypot(dx, dy)
            if distance < self.radius + obj.size:
                return True
        elif obj.shape == 'rectangle':
            rect = pygame.Rect(obj.position[0], obj.position[1], obj.size[0], obj.size[1])
            closest_x = max(rect.left, min(self.position[0], rect.right))
            closest_y = max(rect.top, min(self.position[1], rect.bottom))
            dx = self.position[0] - closest_x
            dy = self.position[1] - closest_y
            if (dx * dx + dy * dy) < (self.radius * self.radius):
                return True
        return False

    def handle_collision(self, obj):
        if isinstance(obj, TeleportPad):
            obj.teleport_ball(self)
        elif obj.shape == 'circle':
            dx = self.position[0] - obj.position[0]
            dy = self.position[1] - obj.position[1]
            distance = math.hypot(dx, dy)
            if distance == 0:
                return
            overlap = self.radius + obj.size - distance
            self.position[0] += (dx / distance) * overlap
            self.position[1] += (dy / distance) * overlap
            self.velocity[0] = -self.velocity[0]
            self.velocity[1] = -self.velocity[1]
        elif obj.shape == 'rectangle':
            rect = pygame.Rect(obj.position[0], obj.position[1], obj.size[0], obj.size[1])
            if self.position[0] > rect.right or self.position[0] < rect.left:
                self.velocity[0] = -self.velocity[0]
            if self.position[1] > rect.bottom or self.position[1] < rect.top:
                self.velocity[1] = -self.velocity[1]

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            if math.hypot(mouse_x - self.position[0], mouse_y - self.position[1]) < self.radius:
                self.dragging = True
                self.drag_start = (mouse_x, mouse_y)
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            mouse_x, mouse_y = event.pos
            self.drag_end = (mouse_x, mouse_y)
        elif event.type == pygame.MOUSEBUTTONUP and self.dragging:
            self.dragging = False
            mouse_x, mouse_y = event.pos
            pull_distance = math.hypot(mouse_x - self.drag_start[0], mouse_y - self.drag_start[1])
            if pull_distance > 50:
                pull_distance = 50
            force = ((self.drag_start[0] - mouse_x) / 5, (self.drag_start[1] - mouse_y) / 5)
            self.apply_force(force)
            return "ball_shot"
