# 子彈系統
import pygame
import math
from config import SCREEN_WIDTH, SCREEN_HEIGHT

class Bullet:
    """敵人子彈"""
    def __init__(self, x, y, dx, dy):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.width = 8
        self.height = 8
    
    def update(self):
        """更新子彈位置"""
        self.x += self.dx
        self.y += self.dy
    
    def draw(self, screen):
        """繪製子彈"""
        pygame.draw.circle(screen, (255, 100, 100), (int(self.x), int(self.y)), 4)
        pygame.draw.circle(screen, (255, 255, 255), (int(self.x), int(self.y)), 2)
    
    def is_off_screen(self):
        """檢查是否離開螢幕"""
        return (self.x < -50 or self.x > SCREEN_WIDTH + 50 or 
                self.y < -50 or self.y > SCREEN_HEIGHT + 50)
    
    def get_rect(self):
        """獲取碰撞矩形"""
        return pygame.Rect(self.x - self.width//2, self.y - self.height//2, self.width, self.height)


class PlayerBullet:
    """玩家子彈"""
    def __init__(self, x, y, dx, dy):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.width = 6
        self.height = 6
    
    def update(self):
        """更新子彈位置"""
        self.x += self.dx
        self.y += self.dy
    
    def draw(self, screen):
        """繪製子彈"""
        pygame.draw.circle(screen, (100, 255, 100), (int(self.x), int(self.y)), 3)
        pygame.draw.circle(screen, (255, 255, 255), (int(self.x), int(self.y)), 1)
    
    def is_off_screen(self):
        """檢查是否離開螢幕"""
        return (self.x < -50 or self.x > SCREEN_WIDTH + 50 or 
                self.y < -50 or self.y > SCREEN_HEIGHT + 50)
    
    def get_rect(self):
        """獲取碰撞矩形"""
        return pygame.Rect(self.x - self.width//2, self.y - self.height//2, self.width, self.height)