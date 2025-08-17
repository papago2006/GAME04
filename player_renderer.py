# 玩家渲染器
import pygame
import math
from config import WHITE, BLACK

class PlayerRenderer:
    def __init__(self):
        self.bounce_timer = 0
        
    def update(self, dt):
        """更新動畫計時器"""
        self.bounce_timer += 0.2
        
    def draw(self, screen, player):
        """主要繪製方法"""
        # 更新受創計時器
        flash = player.hit_timer > 0 and (player.hit_timer // 3) % 2 == 0
        
        if player.is_transformed:
            self._draw_cute_form(screen, player, flash)
        else:
            self._draw_normal_form(screen, player, flash)
    
    def _draw_cute_form(self, screen, player, flash):
        """繪製可愛變身形態"""
        # 可愛彈跳效果
        bounce_offset = math.sin(self.bounce_timer) * 4
        
        # 色彩設定
        if flash:
            body_color = (255, 255, 255)
            accent_color = (255, 200, 200)
            eye_color = (255, 255, 255)
            blush_color = (255, 180, 180)
        else:
            body_color = (255, 228, 225)
            accent_color = (255, 182, 193)
            eye_color = (45, 45, 45)
            blush_color = (255, 192, 203)
        
        center_x = player.x + player.width // 2
        center_y = player.y + player.height // 2 + bounce_offset
        
        # 繪製各部分
        self._draw_head(screen, center_x, center_y, body_color, accent_color)
        self._draw_eyes(screen, center_x, center_y, eye_color)
        self._draw_face_features(screen, center_x, center_y, accent_color, blush_color)
        self._draw_body(screen, center_x, center_y, body_color, accent_color)
        self._draw_limbs(screen, center_x, center_y, body_color, accent_color)
        self._draw_effects(screen, center_x, center_y)
    
    def _draw_head(self, screen, center_x, center_y, body_color, accent_color):
        """繪製頭部"""
        head_radius = 42
        
        # 頭部陰影
        shadow_offset = 2
        pygame.draw.circle(screen, (200, 200, 200), 
                          (int(center_x + shadow_offset), int(center_y - 8 + shadow_offset)), head_radius)
        
        # 主要頭部
        pygame.draw.circle(screen, body_color, (int(center_x), int(center_y - 8)), head_radius)
        pygame.draw.circle(screen, accent_color, (int(center_x), int(center_y - 8)), head_radius, 2)
    
    def _draw_eyes(self, screen, center_x, center_y, eye_color):
        """繪製眼睛"""
        eye_size = 16
        left_eye_x = center_x - 18
        right_eye_x = center_x + 18
        eye_y = center_y - 18
        
        # 眼白
        pygame.draw.circle(screen, WHITE, (int(left_eye_x), int(eye_y)), eye_size)
        pygame.draw.circle(screen, WHITE, (int(right_eye_x), int(eye_y)), eye_size)
        
        # 瞳孔漸層效果
        pupil_size = 10
        for i in range(pupil_size, 0, -1):
            gradient_intensity = (pupil_size - i) / pupil_size
            color_r = int(eye_color[0] + (100 - eye_color[0]) * gradient_intensity)
            color_g = int(eye_color[1] + (150 - eye_color[1]) * gradient_intensity)
            color_b = int(eye_color[2] + (200 - eye_color[2]) * gradient_intensity)
            
            pygame.draw.circle(screen, (color_r, color_g, color_b), 
                              (int(left_eye_x), int(eye_y)), i)
            pygame.draw.circle(screen, (color_r, color_g, color_b), 
                              (int(right_eye_x), int(eye_y)), i)
        
        # 高光效果
        pygame.draw.circle(screen, WHITE, (int(left_eye_x - 4), int(eye_y - 4)), 5)
        pygame.draw.circle(screen, WHITE, (int(right_eye_x - 4), int(eye_y - 4)), 5)
    
    def _draw_face_features(self, screen, center_x, center_y, accent_color, blush_color):
        """繪製臉部特徵"""
        # 嘴巴
        mouth_y = center_y - 2
        mouth_points = [
            (center_x - 6, mouth_y),
            (center_x - 3, mouth_y + 3),
            (center_x, mouth_y + 1),
            (center_x + 3, mouth_y + 3),
            (center_x + 6, mouth_y)
        ]
        pygame.draw.lines(screen, accent_color, False, mouth_points, 2)
        
        # 鼻子
        pygame.draw.circle(screen, (200, 180, 180), (int(center_x), int(center_y - 8)), 1)
        
        # 腮紅
        blush_size = 8
        left_blush_rect = pygame.Rect(center_x - 32, center_y - 8, blush_size * 2, blush_size)
        right_blush_rect = pygame.Rect(center_x + 24, center_y - 8, blush_size * 2, blush_size)
        pygame.draw.ellipse(screen, blush_color, left_blush_rect)
        pygame.draw.ellipse(screen, blush_color, right_blush_rect)
    
    def _draw_body(self, screen, center_x, center_y, body_color, accent_color):
        """繪製身體"""
        body_width = 24
        body_height = 18
        body_rect = pygame.Rect(center_x - body_width//2, center_y + 25, body_width, body_height)
        
        # 身體陰影
        shadow_body_rect = pygame.Rect(center_x - body_width//2 + 1, center_y + 26, body_width, body_height)
        pygame.draw.ellipse(screen, (200, 200, 200), shadow_body_rect)
        
        # 主要身體
        pygame.draw.ellipse(screen, body_color, body_rect)
        pygame.draw.ellipse(screen, accent_color, body_rect, 2)
    
    def _draw_limbs(self, screen, center_x, center_y, body_color, accent_color):
        """繪製四肢"""
        # 小手
        hand_size = 6
        pygame.draw.circle(screen, body_color, (int(center_x - 20), int(center_y + 28)), hand_size)
        pygame.draw.circle(screen, body_color, (int(center_x + 20), int(center_y + 28)), hand_size)
        pygame.draw.circle(screen, accent_color, (int(center_x - 20), int(center_y + 28)), hand_size, 1)
        pygame.draw.circle(screen, accent_color, (int(center_x + 20), int(center_y + 28)), hand_size, 1)
        
        # 小腳
        foot_width = 12
        foot_height = 7
        left_foot_rect = pygame.Rect(center_x - 16, center_y + 38, foot_width, foot_height)
        right_foot_rect = pygame.Rect(center_x + 4, center_y + 38, foot_width, foot_height)
        
        pygame.draw.ellipse(screen, body_color, left_foot_rect)
        pygame.draw.ellipse(screen, body_color, right_foot_rect)
        pygame.draw.ellipse(screen, accent_color, left_foot_rect, 1)
        pygame.draw.ellipse(screen, accent_color, right_foot_rect, 1)
    
    def _draw_effects(self, screen, center_x, center_y):
        """繪製特效"""
        # 星星裝飾
        star_positions = [
            (center_x - 45, center_y - 25),
            (center_x + 45, center_y - 30),
            (center_x - 35, center_y + 15),
            (center_x + 40, center_y + 20)
        ]
        
        for i, (star_x, star_y) in enumerate(star_positions):
            star_phase = self.bounce_timer * (1.5 + i * 0.3)
            star_alpha = (math.sin(star_phase) + 1) / 2
            if star_alpha > 0.4:
                star_size = 3 + int(star_alpha * 2)
                star_color = (255, 215 + int(star_alpha * 40), int(star_alpha * 100))
                self._draw_star(screen, star_x, star_y, star_size, star_color)
        
        # 光環效果
        head_radius = 42
        halo_radius = head_radius + 18 + math.sin(self.bounce_timer * 1.2) * 6
        halo_surface = pygame.Surface((halo_radius * 2, halo_radius * 2), pygame.SRCALPHA)
        
        for i in range(3):
            alpha = 80 - i * 25
            radius = halo_radius - i * 3
            pygame.draw.circle(halo_surface, (255, 215, 0, alpha), 
                              (halo_radius, halo_radius), radius, 2)
        
        screen.blit(halo_surface, (center_x - halo_radius, center_y - 8 - halo_radius))
    
    def _draw_star(self, screen, x, y, size, color):
        """繪製星星"""
        points = []
        for i in range(10):
            angle = i * math.pi / 5
            if i % 2 == 0:
                radius = size
            else:
                radius = size // 2
            px = x + math.cos(angle) * radius
            py = y + math.sin(angle) * radius
            points.append((px, py))
        pygame.draw.polygon(screen, color, points)
    
    def _draw_normal_form(self, screen, player, flash):
        """繪製正常形態"""
        if flash:
            body_color = WHITE
            front_color = (200, 200, 200)
            window_color = (255, 255, 255)
        else:
            body_color = (0, 0, 139)
            front_color = (25, 25, 112)
            window_color = (173, 216, 230)
        
        # 設定尺寸
        player.width = 180
        player.height = 80
        
        # 外星督察者設計
        shell_color_dark = (48, 10, 60)
        shell_color_light = (85, 40, 110)
        cockpit_color = (10, 0, 10)
        energy_glow_green = (50, 255, 150)
        energy_glow_magenta = (255, 0, 255)
        energy_core_white = (255, 255, 255)

        pulse_slow = (math.sin(pygame.time.get_ticks() * 0.0015) + 1) / 2
        pulse_fast = (math.sin(pygame.time.get_ticks() * 0.008) + 1) / 2

        # 主要結構
        self._draw_alien_shell(screen, player, shell_color_dark, shell_color_light)
        self._draw_alien_propulsion(screen, player, energy_glow_green, energy_core_white, pulse_slow, pulse_fast)
        self._draw_alien_weapons(screen, player, shell_color_dark, energy_glow_magenta, energy_core_white, pulse_slow, pulse_fast)
        self._draw_alien_cockpit(screen, player, cockpit_color)
    
    def _draw_alien_shell(self, screen, player, dark_color, light_color):
        """繪製外星飛船外殼"""
        lower_shell_points = [
            (player.x, player.y + 20),
            (player.x + 40, player.y + player.height),
            (player.x + player.width - 30, player.y + player.height - 10),
            (player.x + player.width, player.y + 10)
        ]
        pygame.draw.polygon(screen, dark_color, lower_shell_points)
        
        upper_shell_points = [
            (player.x + 10, player.y + 15),
            (player.x + 50, player.y),
            (player.x + player.width - 60, player.y + 5),
            (player.x + player.width - 10, player.y + 25),
            (player.x + player.width * 0.6, player.y + 35),
            (player.x + 50, player.y + 30)
        ]
        pygame.draw.polygon(screen, light_color, upper_shell_points)
    
    def _draw_alien_propulsion(self, screen, player, glow_color, core_color, pulse_slow, pulse_fast):
        """繪製推進系統"""
        crystal_y = player.y + player.height - 5
        main_crystal_points = [
            (player.x + 20, crystal_y),
            (player.x + 50, crystal_y - 15),
            (player.x + 60, crystal_y),
            (player.x + 50, crystal_y + 15 + pulse_slow * 10)
        ]
        pygame.draw.polygon(screen, glow_color, main_crystal_points)
        pygame.draw.circle(screen, core_color, (player.x + 48, crystal_y), int(3 + pulse_fast * 2))
    
    def _draw_alien_weapons(self, screen, player, base_color, glow_color, core_color, pulse_slow, pulse_fast):
        """繪製武器系統"""
        weapon_base_points = [
            (player.x + 60, player.y + 10),
            (player.x + 70, player.y - 30),
            (player.x + player.width - 20, player.y - 25),
            (player.x + player.width, player.y + 15)
        ]
        pygame.draw.polygon(screen, base_color, weapon_base_points)

        core_x = player.x + 115
        core_y = player.y - 20
        pygame.draw.circle(screen, glow_color, (core_x, core_y), int(22 + pulse_slow * 15))
        pygame.draw.circle(screen, core_color, (core_x, core_y), int(8 + pulse_fast * 6))
    
    def _draw_alien_cockpit(self, screen, player, cockpit_color):
        """繪製駕駛艙"""
        cockpit_points = [
            (player.x + 45, player.y + 8),
            (player.x + 90, player.y + 10),
            (player.x + 65, player.y + 28)
        ]
        pygame.draw.polygon(screen, cockpit_color, cockpit_points)