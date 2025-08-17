# 背景渲染器
import pygame
import random
import math
from config import GRASS_GREEN, ROAD_GRAY, SIDEWALK_GRAY, WHITE, BLACK, SCREEN_WIDTH, SCREEN_HEIGHT

class BackgroundRenderer:
    """背景渲染器"""
    
    @staticmethod
    def draw_level1(screen):
        """繪製第一關背景"""
        # 填充草地背景
        screen.fill(GRASS_GREEN)
        
        # 計算道路位置（Y軸中央）
        road_y = SCREEN_HEIGHT // 2 - 100
        
        # 繪製人行道
        pygame.draw.rect(screen, SIDEWALK_GRAY, (0, road_y - 30, SCREEN_WIDTH, 30))
        pygame.draw.rect(screen, SIDEWALK_GRAY, (0, road_y + 200, SCREEN_WIDTH, 30))
        
        # 繪製馬路
        pygame.draw.rect(screen, ROAD_GRAY, (0, road_y, SCREEN_WIDTH, 200))
        
        # 繪製道路中線
        for x in range(0, SCREEN_WIDTH, 40):
            pygame.draw.rect(screen, WHITE, (x, road_y + 95, 20, 10))
    
    @staticmethod
    def draw_level2(screen):
        """繪製第二關背景：監獄場景"""
        # 深灰色石磚地板
        BackgroundRenderer._draw_prison_floor(screen)
        
        # 隨機水漬
        BackgroundRenderer._draw_water_stains(screen)
        
        # 地板裂縫
        BackgroundRenderer._draw_floor_cracks(screen)
        
        # 牆壁與鐵欄杆
        BackgroundRenderer._draw_prison_walls(screen)
        
        # 探照燈光束
        BackgroundRenderer._draw_searchlights(screen)
    
    @staticmethod
    def _draw_prison_floor(screen):
        """繪製監獄地板"""
        brick_size = 40
        for y in range(0, SCREEN_HEIGHT, brick_size):
            for x in range(0, SCREEN_WIDTH, brick_size):
                gray_val = random.randint(50, 65)
                brick_color = (gray_val, gray_val, gray_val + 5)
                pygame.draw.rect(screen, brick_color, (x, y, brick_size, brick_size))
                pygame.draw.rect(screen, BLACK, (x, y, brick_size, brick_size), 1)
    
    @staticmethod
    def _draw_water_stains(screen):
        """繪製水漬"""
        for _ in range(15):
            stain_x = random.randint(0, SCREEN_WIDTH - 50)
            stain_y = random.randint(0, SCREEN_HEIGHT - 30)
            stain_surface = pygame.Surface((50, 30), pygame.SRCALPHA)
            pygame.draw.ellipse(stain_surface, (20, 20, 25, 120), (0, 0, 50, 30))
            screen.blit(stain_surface, (stain_x, stain_y))
    
    @staticmethod
    def _draw_floor_cracks(screen):
        """繪製地板裂縫"""
        for _ in range(8):
            crack_start_x = random.randint(0, SCREEN_WIDTH)
            crack_start_y = random.randint(0, SCREEN_HEIGHT)
            crack_points = [(crack_start_x, crack_start_y)]
            
            for i in range(5):
                next_x = crack_points[-1][0] + random.randint(-30, 30)
                next_y = crack_points[-1][1] + random.randint(-20, 20)
                crack_points.append((next_x, next_y))
            
            if len(crack_points) > 1:
                pygame.draw.lines(screen, (30, 30, 30), False, crack_points, 2)
    
    @staticmethod
    def _draw_prison_walls(screen):
        """繪製監獄牆壁和鐵欄杆"""
        wall_height = 80
        
        # 上下牆壁
        pygame.draw.rect(screen, (40, 40, 45), (0, 0, SCREEN_WIDTH, wall_height))
        pygame.draw.rect(screen, (40, 40, 45), (0, SCREEN_HEIGHT - wall_height, SCREEN_WIDTH, wall_height))
        
        # 鐵欄杆
        bar_spacing = 30
        for x in range(0, SCREEN_WIDTH, bar_spacing):
            # 上方鐵欄杆
            pygame.draw.rect(screen, BLACK, (x, 20, 8, wall_height - 40))
            pygame.draw.circle(screen, (139, 69, 19), (x + 4, 30 + random.randint(0, 20)), 2)
            
            # 下方鐵欄杆
            pygame.draw.rect(screen, BLACK, (x, SCREEN_HEIGHT - wall_height + 20, 8, wall_height - 40))
            pygame.draw.circle(screen, (139, 69, 19), (x + 4, SCREEN_HEIGHT - 50 + random.randint(0, 20)), 2)
        
        # 陰影入口
        shadow_positions = [(100, 10), (500, 10), (900, 10), (1300, 10), (1700, 10),
                           (100, SCREEN_HEIGHT - 70), (500, SCREEN_HEIGHT - 70), 
                           (900, SCREEN_HEIGHT - 70), (1300, SCREEN_HEIGHT - 70)]
        
        for shadow_x, shadow_y in shadow_positions:
            shadow_surface = pygame.Surface((80, 60), pygame.SRCALPHA)
            pygame.draw.ellipse(shadow_surface, (0, 0, 0, 180), (0, 0, 80, 60))
            screen.blit(shadow_surface, (shadow_x, shadow_y))
    
    @staticmethod
    def _draw_searchlights(screen):
        """繪製探照燈光束"""
        time_factor = pygame.time.get_ticks() * 0.001
        
        # 左上角探照燈
        beam_angle = math.sin(time_factor) * 30
        beam_center_x = 200 + math.sin(time_factor * 0.5) * 100
        beam_center_y = 300
        
        beam_surface = pygame.Surface((400, 600), pygame.SRCALPHA)
        beam_points = [
            (50, 50),
            (beam_center_x - 100, beam_center_y),
            (beam_center_x + 100, beam_center_y),
            (beam_center_x + 80, beam_center_y + 200),
            (beam_center_x - 80, beam_center_y + 200)
        ]
        
        if len(beam_points) >= 3:
            pygame.draw.polygon(beam_surface, (255, 255, 150, 40), beam_points)
            screen.blit(beam_surface, (0, 0))
        
        # 右下角探照燈
        beam_center_x2 = SCREEN_WIDTH - 300 + math.sin(time_factor * 0.7) * 80
        beam_center_y2 = SCREEN_HEIGHT - 400
        
        beam_surface2 = pygame.Surface((400, 600), pygame.SRCALPHA)
        beam_points2 = [
            (350, 550),
            (beam_center_x2 - SCREEN_WIDTH + 400 - 80, beam_center_y2 - SCREEN_HEIGHT + 600),
            (beam_center_x2 - SCREEN_WIDTH + 400 + 80, beam_center_y2 - SCREEN_HEIGHT + 600),
            (beam_center_x2 - SCREEN_WIDTH + 400 + 60, beam_center_y2 - SCREEN_HEIGHT + 600 - 150),
            (beam_center_x2 - SCREEN_WIDTH + 400 - 60, beam_center_y2 - SCREEN_HEIGHT + 600 - 150)
        ]
        
        if len(beam_points2) >= 3:
            pygame.draw.polygon(beam_surface2, (255, 255, 150, 30), beam_points2)
            screen.blit(beam_surface2, (SCREEN_WIDTH - 400, SCREEN_HEIGHT - 600))