# 遊戲物件類
import pygame
import random
from config import WHITE, BLACK, SCREEN_WIDTH, SCREEN_HEIGHT

class Building:
    def __init__(self, x, y, building_type):
        self.rect = pygame.Rect(x, y, 200, 150)
        self.type = building_type
        self.is_active = False
    
    def draw(self, screen):
        """繪製建築物"""
        if self.type == "School":
            self.draw_school(screen)
        elif self.type == "Park":
            self.draw_park(screen)
        elif self.type == "Office":
            self.draw_office(screen)
        elif self.type == "Community":
            self.draw_community(screen)
        elif self.type == "Military":
            self.draw_military(screen)
        
        # 繪製啟動指示器
        if self.is_active:
            self.draw_active_indicator(screen)
    
    def draw_school(self, surface):
        """繪製學校"""
        x, y = self.rect.topleft
        
        # 主建築
        pygame.draw.rect(surface, (255, 228, 181), (x, y, 200, 120))
        
        # 屋頂
        roof_points = [(x - 10, y), (x + 210, y), (x + 100, y - 30)]
        pygame.draw.polygon(surface, (205, 92, 92), roof_points)
        
        # 窗戶
        window_positions = [(x + 20, y + 20), (x + 60, y + 20), (x + 120, y + 20), (x + 160, y + 20),
                           (x + 20, y + 60), (x + 60, y + 60), (x + 120, y + 60), (x + 160, y + 60)]
        for wx, wy in window_positions:
            pygame.draw.rect(surface, (173, 216, 230), (wx, wy, 25, 25))
            pygame.draw.rect(surface, BLACK, (wx, wy, 25, 25), 2)
        
        # 門
        pygame.draw.rect(surface, (139, 69, 19), (x + 85, y + 90, 30, 30))
        
        # 旗桿
        pygame.draw.line(surface, (105, 105, 105), (x + 220, y - 50), (x + 220, y + 120), 5)
        pygame.draw.rect(surface, (255, 0, 0), (x + 225, y - 40, 30, 20))
    
    def draw_park(self, surface):
        """繪製公園"""
        x, y = self.rect.topleft
        
        # 草地背景
        pygame.draw.rect(surface, (34, 139, 34), (x, y, 200, 150))
        
        # 樹木
        tree_positions = [(x + 50, y + 50), (x + 150, y + 40), (x + 100, y + 100), (x + 30, y + 120)]
        for tx, ty in tree_positions:
            pygame.draw.circle(surface, (139, 69, 19), (tx, ty + 20), 8)
            pygame.draw.circle(surface, (0, 100, 0), (tx, ty), 25)
        
        # 小徑
        path_points = [(x, y + 75), (x + 50, y + 80), (x + 100, y + 70), (x + 150, y + 75), (x + 200, y + 80)]
        if len(path_points) > 1:
            pygame.draw.lines(surface, (222, 184, 135), False, path_points, 15)
        
        # 長椅
        pygame.draw.rect(surface, (160, 82, 45), (x + 80, y + 130, 40, 10))
        pygame.draw.rect(surface, (160, 82, 45), (x + 85, y + 125, 5, 15))
        pygame.draw.rect(surface, (160, 82, 45), (x + 110, y + 125, 5, 15))
        
        # 花朵
        flower_colors = [(255, 192, 203), (255, 255, 0), (255, 165, 0), (138, 43, 226)]
        for _ in range(8):
            flower_x = x + random.randint(10, 190)
            flower_y = y + 32 + random.randint(0, 16)
            color = random.choice(flower_colors)
            pygame.draw.circle(surface, color, (flower_x, flower_y), 3)
    
    def draw_office(self, surface):
        """繪製辦公大樓"""
        x, y = self.rect.topleft
        
        # 主體框架
        pygame.draw.rect(surface, (47, 79, 79), (x, y, 80, 250))
        
        # 玻璃帷幕 - 網格燈光
        for row in range(16):
            for col in range(8):
                cell_x = x + col * 10
                cell_y = y + row * 15
                if random.random() > 0.5:
                    pygame.draw.rect(surface, (255, 255, 153), (cell_x, cell_y, 10, 15))
                else:
                    pygame.draw.rect(surface, (70, 130, 180), (cell_x, cell_y, 10, 15))
        
        # 天線
        pygame.draw.line(surface, WHITE, (x + 40, y - 40), (x + 40, y), 3)
        
        # 警示燈
        if pygame.time.get_ticks() % 1000 > 500:
            pygame.draw.circle(surface, (255, 0, 0), (x + 40, y - 40), 5)
    
    def draw_community(self, surface):
        """繪製社區"""
        x, y = self.rect.topleft
        
        # 3棟小房子
        house_colors = [(245, 245, 220), (255, 250, 205)]
        house_positions = [(x + 20, y + 50), (x + 100, y + 80), (x + 160, y + 40)]
        
        for i, (house_x, house_y) in enumerate(house_positions):
            # 牆體
            wall_color = random.choice(house_colors)
            pygame.draw.rect(surface, wall_color, (house_x, house_y, 50, 40))
            
            # 屋頂
            roof_points = [(house_x - 5, house_y), (house_x + 55, house_y), (house_x + 25, house_y - 20)]
            pygame.draw.polygon(surface, (255, 69, 0), roof_points)
            
            # 門
            pygame.draw.rect(surface, (139, 69, 19), (house_x + 20, house_y + 25, 10, 15))
            
            # 窗戶
            pygame.draw.rect(surface, (173, 216, 230), (house_x + 5, house_y + 10, 10, 10))
            pygame.draw.rect(surface, (173, 216, 230), (house_x + 35, house_y + 10, 10, 10))
        
        # 灌木
        bush_positions = [(x + 80, y + 130), (x + 140, y + 120), (x + 60, y + 140), (x + 180, y + 100)]
        for bush_x, bush_y in bush_positions:
            pygame.draw.circle(surface, (34, 139, 34), (bush_x, bush_y), 15)
    
    def draw_military(self, surface):
        """繪製軍事基地"""
        x, y = self.rect.topleft
        
        # 主堡壘
        pygame.draw.rect(surface, (112, 128, 144), (x, y, 180, 100))
        
        # 迷彩圖案
        camo_colors = [(85, 107, 47), (193, 154, 107)]
        for _ in range(4):
            color = random.choice(camo_colors)
            points = []
            for _ in range(6):
                px = x + random.randint(10, 170)
                py = y + random.randint(10, 90)
                points.append((px, py))
            pygame.draw.polygon(surface, color, points)
        
        # 圍牆
        fence_positions = list(range(x - 20, x + 200, 15))
        for fence_x in fence_positions:
            pygame.draw.line(surface, (105, 105, 105), (fence_x, y - 10), (fence_x, y + 110), 4)
            spike_points = [(fence_x - 3, y - 10), (fence_x + 3, y - 10), (fence_x, y - 15)]
            pygame.draw.polygon(surface, (105, 105, 105), spike_points)
        
        # 停機坪
        pygame.draw.circle(surface, (105, 105, 105), (x + 140, y + 140), 30)
        pygame.draw.line(surface, WHITE, (x + 130, y + 130), (x + 130, y + 150), 8)
        pygame.draw.line(surface, WHITE, (x + 150, y + 130), (x + 150, y + 150), 8)
        pygame.draw.line(surface, WHITE, (x + 130, y + 140), (x + 150, y + 140), 8)
        
        # 瞭望塔
        pygame.draw.rect(surface, (105, 105, 105), (x + 200, y + 40, 15, 60))
        pygame.draw.rect(surface, (105, 105, 105), (x + 195, y + 25, 25, 15))
    
    def draw_active_indicator(self, surface):
        """繪製啟動指示器"""
        center_x = self.rect.centerx
        center_y = self.rect.centery
        radius = self.rect.width // 2
        
        indicator_surface = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(indicator_surface, (0, 255, 0, 128), (radius, radius), radius)
        pygame.draw.circle(indicator_surface, (0, 0, 0, 0), (radius, radius), radius - 20)
        
        surface.blit(indicator_surface, (center_x - radius, center_y - radius))


class Prisoner:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 40
        self.height = 40
        self.speed = 2
        self.health = 80
        self.max_health = 80
        self.move_timer = 0
        self.direction = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])
    
    def update(self, player, game_over=False):
        if game_over:
            return
            
        # 簡單的隨機移動
        self.move_timer += 1
        if self.move_timer > 120:  # 每2秒改變方向
            self.direction = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1), (0, 0)])
            self.move_timer = 0
        
        # 移動
        self.x += self.direction[0] * self.speed
        self.y += self.direction[1] * self.speed
        
        # 保持在螢幕範圍內
        self.x = max(0, min(SCREEN_WIDTH - self.width, self.x))
        self.y = max(0, min(SCREEN_HEIGHT - self.height, self.y))
    
    def draw(self, screen):
        """繪製囚犯"""
        # 橘色囚服
        pygame.draw.rect(screen, (255, 140, 0), (self.x, self.y, self.width, self.height))
        
        # 黑色條紋
        for i in range(0, self.height, 8):
            pygame.draw.rect(screen, BLACK, (self.x, self.y + i, self.width, 4))
        
        # 簡單的臉
        pygame.draw.circle(screen, (255, 220, 177), (self.x + self.width//2, self.y + 8), 6)
        pygame.draw.circle(screen, BLACK, (self.x + self.width//2 - 2, self.y + 6), 1)
        pygame.draw.circle(screen, BLACK, (self.x + self.width//2 + 2, self.y + 6), 1)
        
        # 健康條
        bar_width = self.width
        bar_height = 4
        health_percentage = self.health / self.max_health
        health_width = int(bar_width * health_percentage)
        
        pygame.draw.rect(screen, (100, 0, 0), (self.x, self.y - 8, bar_width, bar_height))
        pygame.draw.rect(screen, (255, 0, 0), (self.x, self.y - 8, health_width, bar_height))
    
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


class WeaponPickup:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 40
        self.height = 20
        self.pulse_timer = 0
    
    def update(self):
        """更新武器拾取點"""
        self.pulse_timer += 0.1
    
    def draw(self, screen):
        """繪製武器拾取點"""
        import math
        
        # 脈動效果
        pulse = math.sin(self.pulse_timer) * 0.3 + 0.7
        
        # 武器外形
        weapon_color = (int(100 * pulse), int(100 * pulse), int(100 * pulse))
        pygame.draw.rect(screen, weapon_color, (self.x, self.y, self.width, self.height))
        
        # 槍管
        pygame.draw.rect(screen, weapon_color, (self.x + self.width, self.y + 8, 20, 4))
        
        # 光暈效果
        glow_surface = pygame.Surface((80, 60), pygame.SRCALPHA)
        glow_color = (255, 255, 0, int(100 * pulse))
        pygame.draw.ellipse(glow_surface, glow_color, (0, 0, 80, 60))
        screen.blit(glow_surface, (self.x - 20, self.y - 20))
        
        # 提示文字
        from config import get_fonts
        font = get_fonts()['small']
        text = font.render("武器", True, (255, 255, 0))
        screen.blit(text, (self.x - 10, self.y - 40))
    
    def get_rect(self):
        """獲取碰撞矩形"""
        return pygame.Rect(self.x, self.y, self.width, self.height)