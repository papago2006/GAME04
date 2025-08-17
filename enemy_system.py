# 統一的敵人系統
import pygame
import random
import math
from config import ENEMY_CONFIGS, BLACK, WHITE

class Enemy:
    def __init__(self, x, y, enemy_type="normal"):
        self.x = x
        self.y = y
        self.type = enemy_type
        
        # 從配置載入屬性
        config = ENEMY_CONFIGS[enemy_type]
        self.width = config["width"]
        self.height = config["height"]
        self.speed = config["speed"] * random.uniform(0.9, 1.1)
        self.health = config["health"] * random.uniform(0.9, 1.1)
        self.max_health = self.health
        self.attack_cooldown_max = config["attack_cooldown"]
        self.attack_range = config["attack_range"]
        
        # 狀態變數
        self.attack_cooldown = 0
        self.rotor_angle = 0
        self.pulse_timer = 0
        self.state = "patrol"
        self.laser_jitter = 0
        
        # 根據類型設定渲染器
        if enemy_type == "big":
            self.renderer = BigEnemyRenderer()
        else:
            self.renderer = StandardEnemyRenderer()
    
    def update(self, player, bullets, game_over=False):
        if game_over:
            return
            
        # 更新動畫計時器
        self.rotor_angle += 15
        self.pulse_timer += 0.1
        self.laser_jitter = random.uniform(-2, 2)
        
        # 更新攻擊冷卻
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
            
        # 計算與玩家的距離
        dx = player.x - self.x
        dy = player.y - self.y
        distance = math.sqrt(dx*dx + dy*dy)
        
        # AI 行為狀態機
        self._update_ai_behavior(player, bullets, distance, dx, dy)
        
        # 保持在螢幕範圍內
        from config import SCREEN_WIDTH, SCREEN_HEIGHT
        self.x = max(0, min(SCREEN_WIDTH - self.width, self.x))
        self.y = max(0, min(SCREEN_HEIGHT - self.height, self.y))
    
    def _update_ai_behavior(self, player, bullets, distance, dx, dy):
        """更新AI行為"""
        if distance < self.attack_range:
            if distance < 800:
                self.state = "attacking"
                # 攻擊行為
                if self.attack_cooldown <= 0:
                    # 發射子彈
                    bullet_speed = 11 if self.type != "big" else 16
                    bullet_dx = dx / distance * bullet_speed
                    bullet_dy = dy / distance * bullet_speed
                    
                    from bullet_system import Bullet
                    bullets.append(Bullet(self.x + self.width//2, self.y + self.height//2, bullet_dx, bullet_dy))
                    self.attack_cooldown = self.attack_cooldown_max
            else:
                self.state = "tracking"
                
            # 追蹤玩家
            if distance > 0:
                self.x += (dx / distance) * self.speed
                self.y += (dy / distance) * self.speed
        else:
            self.state = "patrol"
            # 簡單的巡邏行為
            self.x += math.sin(pygame.time.get_ticks() * 0.001) * 2
            self.y += math.cos(pygame.time.get_ticks() * 0.001) * 1
    
    def draw(self, screen, player):
        """繪製敵人"""
        self.renderer.draw(screen, self, player)
    
    def take_damage(self, damage):
        """受到傷害"""
        self.health -= damage
        if self.health < 0:
            self.health = 0
    
    def get_rect(self):
        """獲取碰撞矩形（擴大30%）"""
        expanded_width = self.width * 1.3
        expanded_height = self.height * 1.3
        offset_x = (expanded_width - self.width) / 2
        offset_y = (expanded_height - self.height) / 2
        return pygame.Rect(self.x - offset_x, self.y - offset_y, expanded_width, expanded_height)


class StandardEnemyRenderer:
    """標準敵人渲染器"""
    
    def draw(self, screen, enemy, player):
        center_x = enemy.x + enemy.width // 2
        center_y = enemy.y + enemy.height // 2
        
        # 機身多層圓形疊加
        self._draw_shadow(screen, center_x, center_y)
        self._draw_body(screen, center_x, center_y)
        self._draw_camera(screen, center_x, center_y, enemy.pulse_timer)
        self._draw_rotors(screen, center_x, center_y, enemy.rotor_angle)
        self._draw_status_lights(screen, center_x, center_y, enemy.state, enemy.type)
        
        # 瞄準雷射（攻擊狀態時）
        if enemy.state == "attacking":
            self._draw_targeting_laser(screen, center_x, center_y, enemy.laser_jitter)
    
    def _draw_shadow(self, screen, center_x, center_y):
        """繪製陰影"""
        shadow_surface = pygame.Surface((50, 50), pygame.SRCALPHA)
        pygame.draw.circle(shadow_surface, (0, 0, 0, 80), (25, 25), 22)
        screen.blit(shadow_surface, (center_x - 25, center_y - 23))
    
    def _draw_body(self, screen, center_x, center_y):
        """繪製機身"""
        # 深色金屬底盤
        pygame.draw.circle(screen, (40, 40, 40), (center_x, center_y), 20)
        
        # 頂部漸層高光圓形
        for i in range(15):
            color_val = 60 + i * 8
            pygame.draw.circle(screen, (color_val, color_val, color_val), (center_x, center_y - 2), 20 - i)
        
        # 裝甲接縫
        pygame.draw.circle(screen, BLACK, (center_x, center_y), 20, 2)
        pygame.draw.circle(screen, BLACK, (center_x, center_y), 15, 1)
    
    def _draw_camera(self, screen, center_x, center_y, pulse_timer):
        """繪製攝影機"""
        eye_radius = 8 + math.sin(pulse_timer) * 2
        pygame.draw.circle(screen, BLACK, (center_x, center_y), int(eye_radius + 2))
        pygame.draw.circle(screen, (200, 0, 0), (center_x, center_y), int(eye_radius))
        
        # 鏡頭眩光
        glare_surface = pygame.Surface((30, 6), pygame.SRCALPHA)
        pygame.draw.ellipse(glare_surface, (255, 100, 100, 100), (0, 0, 30, 6))
        screen.blit(glare_surface, (center_x - 15, center_y - 3))
    
    def _draw_rotors(self, screen, center_x, center_y, rotor_angle):
        """繪製旋翼"""
        rotor_positions = [(-25, -25), (25, -25), (-25, 25), (25, 25)]
        for rx, ry in rotor_positions:
            rotor_x = center_x + rx
            rotor_y = center_y + ry
            
            # 支架
            pygame.draw.line(screen, (100, 100, 100), (center_x, center_y), (rotor_x, rotor_y), 3)
            
            # 馬達
            pygame.draw.circle(screen, (60, 60, 60), (rotor_x, rotor_y), 5)
            
            # 旋翼動態模糊殘影
            blur_surface = pygame.Surface((20, 20), pygame.SRCALPHA)
            pygame.draw.circle(blur_surface, (150, 150, 150, 100), (10, 10), 10)
            screen.blit(blur_surface, (rotor_x - 10, rotor_y - 10))
            
            # 清晰葉片
            blade_angle1 = math.radians(rotor_angle)
            blade_angle2 = math.radians(rotor_angle + 180)
            
            blade1_end = (rotor_x + math.cos(blade_angle1) * 12, rotor_y + math.sin(blade_angle1) * 12)
            blade2_end = (rotor_x + math.cos(blade_angle2) * 12, rotor_y + math.sin(blade_angle2) * 12)
            
            pygame.draw.line(screen, (200, 200, 200), (rotor_x, rotor_y), blade1_end, 2)
            pygame.draw.line(screen, (200, 200, 200), (rotor_x, rotor_y), blade2_end, 2)
    
    def _draw_status_lights(self, screen, center_x, center_y, state, enemy_type):
        """繪製狀態燈"""
        # 狀態指示燈
        if state == "patrol":
            light_color = (0, 255, 0)
        elif state == "tracking":
            light_color = (255, 255, 0)
        else:  # attacking
            light_color = (255, 0, 0)
            
        pygame.draw.circle(screen, light_color, (center_x - 8, center_y - 15), 3)
        pygame.draw.circle(screen, light_color, (center_x + 8, center_y - 15), 3)
        
        # 原型標識燈
        type_colors = {
            "brute": (100, 0, 0),
            "rusher": (255, 255, 0),
            "normal": (0, 100, 255),
            "big": (255, 0, 255)
        }
        archetype_color = type_colors.get(enemy_type, (0, 100, 255))
        pygame.draw.circle(screen, archetype_color, (center_x, center_y - 18), 2)
    
    def _draw_targeting_laser(self, screen, center_x, center_y, laser_jitter):
        """繪製瞄準雷射"""
        laser_length = 100 + laser_jitter
        laser_end_x = center_x
        laser_end_y = center_y + laser_length
        pygame.draw.line(screen, (255, 0, 0), (center_x, center_y + 20), (laser_end_x, laser_end_y), 2)
        pygame.draw.circle(screen, (255, 100, 100), (int(laser_end_x), int(laser_end_y)), 4)


class BigEnemyRenderer:
    """大型敵人渲染器"""
    
    def draw(self, screen, enemy, player):
        center_x = enemy.x + enemy.width // 2
        center_y = enemy.y + enemy.height // 2
        
        # 使用 math 模組來實現平滑的呼吸/脈動效果
        pulse_slow = (math.sin(pygame.time.get_ticks() * 0.0015) + 1) / 2
        pulse_fast = (math.sin(pygame.time.get_ticks() * 0.008) + 1) / 2
        
        # 外星科技顏色定義
        alien_primary = (20, 180, 170)
        alien_secondary = (140, 0, 190)
        alien_glow = (0, 255, 220)
        alien_core = (255, 255, 255)
        alien_dark = (10, 40, 50)
        
        self._draw_shadow(screen, center_x, center_y)
        self._draw_main_body(screen, center_x, center_y, alien_primary)
        self._draw_dome(screen, center_x, center_y, alien_primary)
        self._draw_energy_ring(screen, center_x, center_y, alien_secondary, pulse_slow, pulse_fast)
        self._draw_energy_core(screen, center_x, center_y, alien_glow, alien_secondary, alien_core, pulse_fast)
        self._draw_hover_devices(screen, center_x, center_y, alien_dark, pulse_slow)
    
    def _draw_shadow(self, screen, center_x, center_y):
        """繪製陰影"""
        shadow_size = 120
        shadow_surface = pygame.Surface((shadow_size, shadow_size // 2), pygame.SRCALPHA)
        pygame.draw.ellipse(shadow_surface, (0, 0, 0, 60), (0, 0, shadow_size, shadow_size // 2))
        screen.blit(shadow_surface, (center_x - shadow_size // 2, center_y + 40))
    
    def _draw_main_body(self, screen, center_x, center_y, alien_primary):
        """繪製主體"""
        body_width = 140
        body_height = 50
        pygame.draw.ellipse(screen, alien_primary, (center_x - body_width // 2, center_y - body_height // 2, 
                                                  body_width, body_height))
    
    def _draw_dome(self, screen, center_x, center_y, alien_primary):
        """繪製圓頂"""
        dome_radius = 60
        dome_surface = pygame.Surface((dome_radius * 2, dome_radius), pygame.SRCALPHA)
        pygame.draw.ellipse(dome_surface, (alien_primary[0], alien_primary[1], alien_primary[2], 180), 
                           (0, 0, dome_radius * 2, dome_radius * 2))
        screen.blit(dome_surface, (center_x - dome_radius, center_y - dome_radius - 20))
    
    def _draw_energy_ring(self, screen, center_x, center_y, alien_secondary, pulse_slow, pulse_fast):
        """繪製能量環"""
        ring_radius = 80 + int(pulse_slow * 10)
        ring_width = 5 + int(pulse_fast * 3)
        pygame.draw.circle(screen, alien_secondary, (center_x, center_y), ring_radius, ring_width)
    
    def _draw_energy_core(self, screen, center_x, center_y, alien_glow, alien_secondary, alien_core, pulse_fast):
        """繪製能量核心"""
        core_radius = 25 + int(pulse_fast * 8)
        
        # 外層光暈
        glow_surface = pygame.Surface((core_radius * 2 + 20, core_radius * 2 + 20), pygame.SRCALPHA)
        for r in range(10, 0, -1):
            alpha = 150 - r * 15
            if alpha < 0:
                alpha = 0
            pygame.draw.circle(glow_surface, (alien_glow[0], alien_glow[1], alien_glow[2], alpha), 
                              (core_radius + 10, core_radius + 10), core_radius + r)
        screen.blit(glow_surface, (center_x - core_radius - 10, center_y - core_radius - 10))
        
        # 內層核心
        pygame.draw.circle(screen, alien_secondary, (center_x, center_y), core_radius // 2)
        pygame.draw.circle(screen, alien_core, (center_x, center_y), core_radius // 4)
    
    def _draw_hover_devices(self, screen, center_x, center_y, alien_dark, pulse_slow):
        """繪製懸浮裝置"""
        for i in range(3):
            angle = i * (2 * math.pi / 3)
            x = center_x + math.cos(angle) * 60
            y = center_y + math.sin(angle) * 60
            
            # 懸浮裝置基座
            pygame.draw.circle(screen, alien_dark, (int(x), int(y)), 15)
            
            # 能量光束
            beam_length = 30 + int(pulse_slow * 20)
            beam_end_y = y + beam_length
            pygame.draw.line(screen, (0, 255, 220, 150), (int(x), int(y)), (int(x), int(beam_end_y)), 8)