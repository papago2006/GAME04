import pygame
import sys
import random
import math
import time

# 初始化 Pygame
pygame.init()

# 遊戲設定
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
PLAYER_SPEED = 8

# 顏色定義
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BRICK_COLOR = (139, 69, 19)  # 磚牆顏色
BRICK_DESTROYED = (100, 50, 25)  # 被摧毀磚牆的顏色

# 磚牆大小
BRICK_SIZE = 40

class BattlefieldPlayer:
    """第三關玩家 - 使用Enemy_big的外觀"""
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 120
        self.height = 120
        self.speed = PLAYER_SPEED
        self.health = 100
        self.max_health = 100
        self.hit_timer = 0
        self.shoot_cooldown = 0
        self.rotor_angle = 0
        self.pulse_timer = 0
        self.last_direction = (0, -1)  # 記錄最後移動方向，預設向上
        
    def update(self, keys, game_over=False, player_bullets=None, brick_walls=None):
        if game_over:
            return
            
        # 更新受創計時器
        if self.hit_timer > 0:
            self.hit_timer -= 1
            
        # 更新射擊冷卻
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1
            
        # 更新動畫計時器
        self.rotor_angle += 15
        self.pulse_timer += 0.1
        
        # 處理移動 (支援方向鍵和WASD) - 分別檢查每個方向的碰撞
        moved = False
        
        # 左移
        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and self.x > 0:
            old_x = self.x
            self.x -= self.speed
            # 檢查碰撞
            if brick_walls:
                player_rect = self.get_rect()
                for wall in brick_walls:
                    if not wall.destroyed and player_rect.colliderect(wall.get_rect()):
                        self.x = old_x  # 恢復X位置
                        break
                else:
                    self.last_direction = (-1, 0)  # 記錄向左移動
                    moved = True
            else:
                self.last_direction = (-1, 0)
                moved = True
        
        # 右移
        if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and self.x < SCREEN_WIDTH - self.width:
            old_x = self.x
            self.x += self.speed
            # 檢查碰撞
            if brick_walls:
                player_rect = self.get_rect()
                for wall in brick_walls:
                    if not wall.destroyed and player_rect.colliderect(wall.get_rect()):
                        self.x = old_x  # 恢復X位置
                        break
                else:
                    self.last_direction = (1, 0)  # 記錄向右移動
                    moved = True
            else:
                self.last_direction = (1, 0)
                moved = True
        
        # 上移
        if (keys[pygame.K_UP] or keys[pygame.K_w]) and self.y > 0:
            old_y = self.y
            self.y -= self.speed
            # 檢查碰撞
            if brick_walls:
                player_rect = self.get_rect()
                for wall in brick_walls:
                    if not wall.destroyed and player_rect.colliderect(wall.get_rect()):
                        self.y = old_y  # 恢復Y位置
                        break
                else:
                    self.last_direction = (0, -1)  # 記錄向上移動
                    moved = True
            else:
                self.last_direction = (0, -1)
                moved = True
        
        # 下移
        if (keys[pygame.K_DOWN] or keys[pygame.K_s]) and self.y < SCREEN_HEIGHT - self.height:
            old_y = self.y
            self.y += self.speed
            # 檢查碰撞
            if brick_walls:
                player_rect = self.get_rect()
                for wall in brick_walls:
                    if not wall.destroyed and player_rect.colliderect(wall.get_rect()):
                        self.y = old_y  # 恢復Y位置
                        break
                else:
                    self.last_direction = (0, 1)  # 記錄向下移動
                    moved = True
            else:
                self.last_direction = (0, 1)
                moved = True
            
        # 射擊功能 - 子彈方向跟隨移動方向
        if keys[pygame.K_SPACE] and self.shoot_cooldown <= 0 and player_bullets is not None:
            # 發射子彈，方向跟隨最後移動方向
            bullet_x = self.x + self.width // 2
            bullet_y = self.y + self.height // 2
            bullet_speed = 12
            bullet_dx = self.last_direction[0] * bullet_speed
            bullet_dy = self.last_direction[1] * bullet_speed
            player_bullets.append(PlayerBullet(bullet_x, bullet_y, bullet_dx, bullet_dy))
            self.shoot_cooldown = 15  # 射擊冷卻
    
    def take_damage(self, damage):
        self.health -= damage
        self.hit_timer = 30
        if self.health < 0:
            self.health = 0
    
    def draw(self, screen):
        """繪製Enemy_big的外觀"""
        # 受創閃爍效果
        flash = self.hit_timer > 0 and (self.hit_timer // 3) % 2 == 0
        
        center_x = self.x + self.width // 2
        center_y = self.y + self.height // 2
        
        # 使用 math 模組來實現平滑的呼吸/脈動效果
        pulse_slow = (math.sin(pygame.time.get_ticks() * 0.0015) + 1) / 2
        pulse_fast = (math.sin(pygame.time.get_ticks() * 0.008) + 1) / 2
        
        # 外星科技顏色定義
        if flash:
            alien_primary = (255, 255, 255)
            alien_secondary = (200, 200, 200)
            alien_glow = (255, 255, 255)
            alien_core = (255, 255, 255)
            alien_dark = (200, 200, 200)
        else:
            alien_primary = (20, 180, 170)
            alien_secondary = (140, 0, 190)
            alien_glow = (0, 255, 220)
            alien_core = (255, 255, 255)
            alien_dark = (10, 40, 50)
        
        # 1. 繪製大型底部陰影
        shadow_size = 120
        shadow_surface = pygame.Surface((shadow_size, shadow_size // 2), pygame.SRCALPHA)
        pygame.draw.ellipse(shadow_surface, (0, 0, 0, 60), (0, 0, shadow_size, shadow_size // 2))
        screen.blit(shadow_surface, (center_x - shadow_size // 2, center_y + 40))
        
        # 2. 繪製主體 - 橢圓形的UFO形狀
        body_width = 140
        body_height = 50
        pygame.draw.ellipse(screen, alien_primary, (center_x - body_width // 2, center_y - body_height // 2, 
                                                  body_width, body_height))
        
        # 3. 繪製上層圓頂
        dome_radius = 60
        dome_surface = pygame.Surface((dome_radius * 2, dome_radius), pygame.SRCALPHA)
        pygame.draw.ellipse(dome_surface, (alien_primary[0], alien_primary[1], alien_primary[2], 180), 
                           (0, 0, dome_radius * 2, dome_radius * 2))
        screen.blit(dome_surface, (center_x - dome_radius, center_y - dome_radius - 20))
        
        # 4. 繪製能量環
        ring_radius = 80 + int(pulse_slow * 10)
        ring_width = 5 + int(pulse_fast * 3)
        pygame.draw.circle(screen, alien_secondary, (center_x, center_y), ring_radius, ring_width)
        
        # 5. 繪製能量核心
        core_radius = 25 + int(pulse_fast * 8)
        glow_surface = pygame.Surface((core_radius * 2 + 20, core_radius * 2 + 20), pygame.SRCALPHA)
        for r in range(10, 0, -1):
            alpha = 150 - r * 15
            if alpha < 0:
                alpha = 0
            pygame.draw.circle(glow_surface, (alien_glow[0], alien_glow[1], alien_glow[2], alpha), 
                              (core_radius + 10, core_radius + 10), core_radius + r)
        screen.blit(glow_surface, (center_x - core_radius - 10, center_y - core_radius - 10))
        
        pygame.draw.circle(screen, alien_secondary, (center_x, center_y), core_radius // 2)
        pygame.draw.circle(screen, alien_core, (center_x, center_y), core_radius // 4)
    
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

class BattlefieldEnemy:
    """第三關敵人 - 使用Player的外觀"""
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 60
        self.height = 30
        self.speed = 3
        self.health = 50
        self.max_health = 50
        self.hit_timer = 0
        self.shoot_cooldown = 0
        self.attack_range = 600
        self.state = "patrol"
        self.patrol_direction = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])
        self.patrol_timer = 0
        self.bounce_timer = 0
        
    def update(self, player, bullets, game_over=False, brick_walls=None):
        if game_over:
            return
            
        # 更新受創計時器
        if self.hit_timer > 0:
            self.hit_timer -= 1
            
        # 更新射擊冷卻
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1
            
        # 更新動畫計時器
        self.bounce_timer += 0.2
        self.patrol_timer += 1
        
        # 移動前的位置
        old_x, old_y = self.x, self.y
        
        # 計算與玩家的距離
        dx = player.x - self.x
        dy = player.y - self.y
        distance = math.sqrt(dx*dx + dy*dy)
        
        # AI 行為狀態機
        if distance < self.attack_range:
            self.state = "attacking"
            # 攻擊行為
            if self.shoot_cooldown <= 0:
                # 發射子彈
                bullet_dx = dx / distance * 8
                bullet_dy = dy / distance * 8
                bullets.append(EnemyBullet(self.x + self.width//2, self.y + self.height//2, bullet_dx, bullet_dy))
                self.shoot_cooldown = 90  # 1.5秒冷卻
                
            # 追蹤玩家
            if distance > 0:
                move_x = (dx / distance) * self.speed
                move_y = (dy / distance) * self.speed
                self.x += move_x
                self.y += move_y
        else:
            self.state = "patrol"
            # 巡邏行為
            if self.patrol_timer > 120:  # 每2秒改變方向
                self.patrol_direction = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])
                self.patrol_timer = 0
                
            self.x += self.patrol_direction[0] * self.speed
            self.y += self.patrol_direction[1] * self.speed
            
        # 檢查與磚牆的碰撞
        if brick_walls:
            enemy_rect = self.get_rect()
            for wall in brick_walls:
                if not wall.destroyed and enemy_rect.colliderect(wall.get_rect()):
                    # 恢復到移動前的位置
                    self.x, self.y = old_x, old_y
                    # 改變巡邏方向
                    self.patrol_direction = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])
                    break
            
        # 保持在螢幕範圍內
        self.x = max(0, min(SCREEN_WIDTH - self.width, self.x))
        self.y = max(0, min(SCREEN_HEIGHT - self.height, self.y))
    
    def take_damage(self, damage):
        self.health -= damage
        self.hit_timer = 30
        if self.health < 0:
            self.health = 0
    
    def draw(self, screen):
        """繪製Player的外觀"""
        # 受創閃爍效果
        flash = self.hit_timer > 0 and (self.hit_timer // 3) % 2 == 0
        
        if flash:
            body_color = (255, 255, 255)
            front_color = (200, 200, 200)
            window_color = (255, 255, 255)
        else:
            body_color = (0, 0, 139)
            front_color = (25, 25, 112)
            window_color = (173, 216, 230)
        
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
        lower_shell_points = [
            (self.x, self.y + 20),
            (self.x + 40, self.y + self.height),
            (self.x + self.width - 30, self.y + self.height - 10),
            (self.x + self.width, self.y + 10)
        ]
        pygame.draw.polygon(screen, shell_color_dark, lower_shell_points)
        
        upper_shell_points = [
            (self.x + 10, self.y + 15),
            (self.x + 50, self.y),
            (self.x + self.width - 60, self.y + 5),
            (self.x + self.width - 10, self.y + 25),
            (self.x + self.width * 0.6, self.y + 35),
            (self.x + 50, self.y + 30)
        ]
        pygame.draw.polygon(screen, shell_color_light, upper_shell_points)
        
        # 能量水晶推進器
        crystal_y = self.y + self.height - 5
        main_crystal_points = [
            (self.x + 20, crystal_y),
            (self.x + 50, crystal_y - 15),
            (self.x + 60, crystal_y),
            (self.x + 50, crystal_y + 15 + pulse_slow * 10)
        ]
        pygame.draw.polygon(screen, energy_glow_green, main_crystal_points)
        pygame.draw.circle(screen, energy_core_white, (self.x + 48, crystal_y), int(3 + pulse_fast * 2))

        # 武器系統
        weapon_base_points = [
            (self.x + 60, self.y + 10),
            (self.x + 70, self.y - 30),
            (self.x + self.width - 20, self.y - 25),
            (self.x + self.width, self.y + 15)
        ]
        pygame.draw.polygon(screen, shell_color_dark, weapon_base_points)

        core_x = self.x + 115
        core_y = self.y - 20
        pygame.draw.circle(screen, energy_glow_magenta, (core_x, core_y), int(22 + pulse_slow * 15))
        pygame.draw.circle(screen, energy_core_white, (core_x, core_y), int(8 + pulse_fast * 6))
        
        # 駕駛艙
        cockpit_points = [
            (self.x + 45, self.y + 8),
            (self.x + 90, self.y + 10),
            (self.x + 65, self.y + 28)
        ]
        pygame.draw.polygon(screen, cockpit_color, cockpit_points)
    
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

class BrickWall:
    """可摧毀的磚牆"""
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = BRICK_SIZE
        self.height = BRICK_SIZE
        self.destroyed = False
        
    def draw(self, screen):
        if not self.destroyed:
            # 繪製磚牆
            pygame.draw.rect(screen, BRICK_COLOR, (self.x, self.y, self.width, self.height))
            # 磚牆紋理
            pygame.draw.rect(screen, (160, 82, 45), (self.x, self.y, self.width, self.height), 2)
            # 磚塊分割線
            pygame.draw.line(screen, (100, 50, 25), (self.x, self.y + self.height//2), 
                           (self.x + self.width, self.y + self.height//2), 1)
            pygame.draw.line(screen, (100, 50, 25), (self.x + self.width//2, self.y), 
                           (self.x + self.width//2, self.y + self.height), 1)
    
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

class PlayerBullet:
    """玩家子彈"""
    def __init__(self, x, y, dx, dy):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.width = 6
        self.height = 12
        self.trail = []
        
    def update(self):
        # 添加當前位置到尾跡
        self.trail.append((self.x, self.y))
        if len(self.trail) > 8:
            self.trail.pop(0)
            
        self.x += self.dx
        self.y += self.dy
        
    def draw(self, screen):
        # 繪製尾跡
        for i, (trail_x, trail_y) in enumerate(self.trail):
            alpha = int(255 * (i + 1) / len(self.trail))
            size = int(4 * (i + 1) / len(self.trail))
            
            trail_surface = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
            pygame.draw.circle(trail_surface, (0, 255, 220, alpha), (size, size), size)
            screen.blit(trail_surface, (trail_x - size, trail_y - size))
        
        # 子彈本體（青色能量彈）
        pygame.draw.rect(screen, (0, 255, 220), (self.x - self.width//2, self.y - self.height//2, 
                                                self.width, self.height))
        pygame.draw.rect(screen, (150, 255, 255), (self.x - self.width//2 + 1, self.y - self.height//2 + 1, 
                                                  self.width - 2, self.height - 2))
        
    def is_off_screen(self):
        return (self.x < -50 or self.x > SCREEN_WIDTH + 50 or 
                self.y < -50 or self.y > SCREEN_HEIGHT + 50)
    
    def get_rect(self):
        return pygame.Rect(self.x - self.width//2, self.y - self.height//2, self.width, self.height)

class EnemyBullet:
    """敵人子彈"""
    def __init__(self, x, y, dx, dy):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.radius = 4
        
    def update(self):
        self.x += self.dx
        self.y += self.dy
        
    def draw(self, screen):
        # 發光的紅色能量球
        glow_surface = pygame.Surface((self.radius * 6, self.radius * 6), pygame.SRCALPHA)
        pygame.draw.circle(glow_surface, (255, 0, 0, 50), (self.radius * 3, self.radius * 3), self.radius * 3)
        screen.blit(glow_surface, (self.x - self.radius * 3, self.y - self.radius * 3))
        
        pygame.draw.circle(screen, (255, 100, 100), (int(self.x), int(self.y)), self.radius)
        pygame.draw.circle(screen, (255, 200, 200), (int(self.x), int(self.y)), self.radius // 2)
        
    def is_off_screen(self):
        return (self.x < -50 or self.x > SCREEN_WIDTH + 50 or 
                self.y < -50 or self.y > SCREEN_HEIGHT + 50)
    
    def get_rect(self):
        return pygame.Rect(self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2)

def create_maze_map():
    """創建坦克大戰風格的迷宮地圖，包含隨機生成的水平牆和垂直牆"""
    brick_walls = []
    
    grid_width = SCREEN_WIDTH // BRICK_SIZE
    grid_height = SCREEN_HEIGHT // BRICK_SIZE
    
    # 創建邊界牆
    for y in range(grid_height):
        for x in range(grid_width):
            if x == 0 or x == grid_width - 1 or y == 0 or y == grid_height - 1:
                brick_walls.append(BrickWall(x * BRICK_SIZE, y * BRICK_SIZE))
    
    # 用於記錄已佔用的格子
    occupied_grid = set()
    
    # 將邊界牆加入已佔用格子
    for y in range(grid_height):
        for x in range(grid_width):
            if x == 0 or x == grid_width - 1 or y == 0 or y == grid_height - 1:
                occupied_grid.add((x, y))
    
    # 保留玩家和敵人的出生點區域
    spawn_areas = [
        (5, 5, 10, 10),  # 玩家出生區域
        (grid_width - 15, 5, 10, 10),  # 敵人出生區域1
        (grid_width - 15, grid_height - 15, 10, 10),  # 敵人出生區域2
        (5, grid_height - 15, 10, 10),  # 敵人出生區域3
        (grid_width // 2 - 5, 5, 10, 10),  # 敵人出生區域4
        (grid_width // 2 - 5, grid_height - 15, 10, 10)  # 敵人出生區域5
    ]
    
    for area_x, area_y, area_w, area_h in spawn_areas:
        for y in range(area_y, min(area_y + area_h, grid_height)):
            for x in range(area_x, min(area_x + area_w, grid_width)):
                occupied_grid.add((x, y))
    
    def is_area_free(start_x, start_y, width, height, buffer=1):
        """檢查指定區域是否空閒（包含緩衝區）"""
        for y in range(start_y - buffer, start_y + height + buffer):
            for x in range(start_x - buffer, start_x + width + buffer):
                if (x, y) in occupied_grid:
                    return False
        return True
    
    def mark_area_occupied(start_x, start_y, width, height):
        """標記區域為已佔用"""
        for y in range(start_y, start_y + height):
            for x in range(start_x, start_x + width):
                occupied_grid.add((x, y))
    
    # 創建隨機的水平牆（連續5格）
    horizontal_walls_count = random.randint(8, 12)  # 至少4組，最多7組
    horizontal_walls_created = 0
    attempts = 0
    
    while horizontal_walls_created < horizontal_walls_count and attempts < 50:
        attempts += 1
        # 隨機選擇起始位置
        start_x = random.randint(3, grid_width - 8)  # 確保有足夠空間放5格牆
        start_y = random.randint(3, grid_height - 4)
        
        # 檢查這個位置是否可以放置水平牆
        if is_area_free(start_x, start_y, 5, 1):
            # 創建連續5格的水平牆
            for i in range(5):
                brick_walls.append(BrickWall((start_x + i) * BRICK_SIZE, start_y * BRICK_SIZE))
            
            # 標記為已佔用
            mark_area_occupied(start_x, start_y, 5, 1)
            horizontal_walls_created += 1
    
    # 創建隨機的垂直牆（連續5格）
    vertical_walls_count = random.randint(4, 7)  # 至少4組，最多7組
    vertical_walls_created = 0
    attempts = 0
    
    while vertical_walls_created < vertical_walls_count and attempts < 50:
        attempts += 1
        # 隨機選擇起始位置
        start_x = random.randint(3, grid_width - 4)
        start_y = random.randint(3, grid_height - 8)  # 確保有足夠空間放5格牆
        
        # 檢查這個位置是否可以放置垂直牆
        if is_area_free(start_x, start_y, 1, 5):
            # 創建連續5格的垂直牆
            for i in range(5):
                brick_walls.append(BrickWall(start_x * BRICK_SIZE, (start_y + i) * BRICK_SIZE))
            
            # 標記為已佔用
            mark_area_occupied(start_x, start_y, 1, 5)
            vertical_walls_created += 1
    
    print(f"成功創建 {horizontal_walls_created} 組水平牆和 {vertical_walls_created} 組垂直牆")
    
    return brick_walls

def main():
    # 創建遊戲視窗
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("第三關：逆轉戰場 (Battlefield Reversal)")
    clock = pygame.time.Clock()
    
    # 創建字體
    try:
        font_ui = pygame.font.Font("C:\\Windows\\Fonts\\simsun.ttc", 36)
        font_big = pygame.font.Font("C:\\Windows\\Fonts\\simsun.ttc", 72)
    except:
        font_ui = pygame.font.Font(None, 36)
        font_big = pygame.font.Font(None, 72)
    
    # 創建玩家（使用Enemy_big外觀）- 確保在完全空曠的位置
    player = BattlefieldPlayer(200, 200)
    
    # 創建敵人（使用Player外觀）
    enemies = []
    enemy_spawn_points = [
        (SCREEN_WIDTH - 200, 100),
        (SCREEN_WIDTH - 200, SCREEN_HEIGHT - 200),
        (200, SCREEN_HEIGHT - 200),
        (SCREEN_WIDTH // 2, 200),
        (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 200)
    ]
    
    for spawn_x, spawn_y in enemy_spawn_points:
        enemies.append(BattlefieldEnemy(spawn_x, spawn_y))
    
    # 創建迷宮地圖
    brick_walls = create_maze_map()
    
    # 子彈列表
    player_bullets = []
    enemy_bullets = []
    
    # 遊戲狀態
    game_won = False
    game_lost = False
    
    # 遊戲主循環
    running = True
    
    while running:
        # 處理事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # 獲取按鍵狀態
        keys = pygame.key.get_pressed()
        
        # 檢查遊戲結束條件
        if player.health <= 0:
            game_lost = True
        elif len(enemies) == 0:
            game_won = True
        
        # 更新遊戲邏輯
        if not game_won and not game_lost:
            # 更新玩家
            player.update(keys, False, player_bullets, brick_walls)
            
            # 更新敵人
            for enemy in enemies[:]:
                enemy.update(player, enemy_bullets, False, brick_walls)
            
            # 更新玩家子彈
            for bullet in player_bullets[:]:
                bullet.update()
                if bullet.is_off_screen():
                    player_bullets.remove(bullet)
                    continue
                    
                # 檢查與敵人的碰撞
                bullet_rect = bullet.get_rect()
                for enemy in enemies[:]:
                    if bullet_rect.colliderect(enemy.get_rect()):
                        enemy.take_damage(25)
                        player_bullets.remove(bullet)
                        if enemy.health <= 0:
                            enemies.remove(enemy)
                        break
                
                # 檢查與磚牆的碰撞
                for wall in brick_walls:
                    if not wall.destroyed and bullet_rect.colliderect(wall.get_rect()):
                        wall.destroyed = True
                        player_bullets.remove(bullet)
                        break
            
            # 更新敵人子彈
            for bullet in enemy_bullets[:]:
                bullet.update()
                if bullet.is_off_screen():
                    enemy_bullets.remove(bullet)
                    continue
                    
                # 檢查與玩家的碰撞
                bullet_rect = bullet.get_rect()
                if bullet_rect.colliderect(player.get_rect()):
                    player.take_damage(10)
                    enemy_bullets.remove(bullet)
                    continue
                
                # 檢查與磚牆的碰撞
                for wall in brick_walls:
                    if not wall.destroyed and bullet_rect.colliderect(wall.get_rect()):
                        wall.destroyed = True
                        enemy_bullets.remove(bullet)
                        break
        
        # 繪製遊戲畫面
        screen.fill(BLACK)  # 純黑色背景
        
        # 繪製磚牆
        for wall in brick_walls:
            wall.draw(screen)
        
        # 繪製玩家
        player.draw(screen)
        
        # 繪製敵人
        for enemy in enemies:
            enemy.draw(screen)
        
        # 繪製子彈
        for bullet in player_bullets:
            bullet.draw(screen)
        for bullet in enemy_bullets:
            bullet.draw(screen)
        
        # 繪製UI
        # 血量條
        health_bar_width = 300
        health_bar_height = 20
        health_ratio = player.health / player.max_health
        
        pygame.draw.rect(screen, (100, 0, 0), (20, 20, health_bar_width, health_bar_height))
        pygame.draw.rect(screen, (255, 0, 0), (20, 20, health_bar_width * health_ratio, health_bar_height))
        pygame.draw.rect(screen, WHITE, (20, 20, health_bar_width, health_bar_height), 2)
        
        health_text = font_ui.render(f"血量: {int(player.health)}/{int(player.max_health)}", True, WHITE)
        screen.blit(health_text, (20, 50))
        
        # 敵人數量
        enemy_text = font_ui.render(f"剩餘敵人: {len(enemies)}", True, WHITE)
        screen.blit(enemy_text, (20, 90))
        
        # 玩家位置調試信息
        pos_text = font_ui.render(f"位置: ({int(player.x)}, {int(player.y)})", True, WHITE)
        screen.blit(pos_text, (20, 130))
        
        # 按鍵狀態調試信息
        key_status = []
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            key_status.append("左")
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            key_status.append("右")
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            key_status.append("上")
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            key_status.append("下")
        
        key_text = font_ui.render(f"按鍵: {', '.join(key_status) if key_status else '無'}", True, WHITE)
        screen.blit(key_text, (20, 170))
        
        # 碰撞檢測調試信息
        collision_count = 0
        if brick_walls:
            player_rect = player.get_rect()
            for wall in brick_walls:
                if not wall.destroyed and player_rect.colliderect(wall.get_rect()):
                    collision_count += 1
        
        collision_text = font_ui.render(f"碰撞磚塊數: {collision_count}", True, WHITE)
        screen.blit(collision_text, (20, 210))
        
        # 磚塊總數和牆體統計
        total_walls = len([w for w in brick_walls if not w.destroyed])
        wall_text = font_ui.render(f"磚塊總數: {total_walls}", True, WHITE)
        screen.blit(wall_text, (20, 250))
        
        # 顯示當前移動方向
        direction_text = f"射擊方向: "
        if player.last_direction == (-1, 0):
            direction_text += "左"
        elif player.last_direction == (1, 0):
            direction_text += "右"
        elif player.last_direction == (0, -1):
            direction_text += "上"
        elif player.last_direction == (0, 1):
            direction_text += "下"
        
        dir_text = font_ui.render(direction_text, True, WHITE)
        screen.blit(dir_text, (20, 290))
        
        # 控制說明
        control_text = font_ui.render("控制: 方向鍵或WASD移動, 空白鍵射擊(跟隨移動方向)", True, WHITE)
        screen.blit(control_text, (20, 330))
        
        # 遊戲結束畫面
        if game_won:
            win_text = font_big.render("勝利！逆轉戰場成功！", True, (0, 255, 0))
            text_rect = win_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
            screen.blit(win_text, text_rect)
        elif game_lost:
            lose_text = font_big.render("失敗！戰場逆轉失敗！", True, (255, 0, 0))
            text_rect = lose_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
            screen.blit(lose_text, text_rect)
        
        # 更新顯示
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()