import pygame
import sys
import random
import math

# 初始化 Pygame
pygame.init()

# 遊戲設定
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
PLAYER_SPEED = 7

# 顏色定義
GRASS_GREEN = (50, 150, 50)
ROAD_GRAY = (100, 100, 100)
SIDEWALK_GRAY = (180, 180, 180)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 60
        self.height = 30
        self.speed = PLAYER_SPEED
        self.health = 100
        self.max_health = 100
        self.hit_timer = 0  # 受創閃爍計時器
        self.has_gun = False  # 是否擁有武器
        self.shoot_cooldown = 0  # 射擊冷卻
        
    def update(self, keys, game_over=False, player_bullets=None):
        # 更新受創計時器
        if self.hit_timer > 0:
            self.hit_timer -= 1
            
        # 更新射擊冷卻
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1
            
        # 如果遊戲結束，停止移動
        if game_over:
            return
            
        if keys[pygame.K_LEFT] and self.x > 0:
            self.x -= self.speed
        if keys[pygame.K_RIGHT] and self.x < SCREEN_WIDTH - self.width:
            self.x += self.speed
        if keys[pygame.K_UP] and self.y > 0:
            self.y -= self.speed
        if keys[pygame.K_DOWN] and self.y < SCREEN_HEIGHT - self.height:
            self.y += self.speed
            
        # 射擊功能
        if self.has_gun and keys[pygame.K_SPACE] and self.shoot_cooldown <= 0 and player_bullets is not None:
            # 發射子彈
            bullet_x = self.x + self.width // 2
            bullet_y = self.y
            player_bullets.append(PlayerBullet(bullet_x, bullet_y, 0, -12))  # 向上發射
            self.shoot_cooldown = 15  # 射擊冷卻
    
    def take_damage(self, damage):
        self.health -= damage
        self.hit_timer = 30  # 0.5秒閃爍 (30 frames at 60 FPS)
        if self.health < 0:
            self.health = 0
    
    def draw(self, screen):
        # 受創閃爍效果
        flash = self.hit_timer > 0 and (self.hit_timer // 3) % 2 == 0
        
        if flash:
            # 閃爍時使用白色
            body_color = WHITE
            front_color = (200, 200, 200)
            window_color = (255, 255, 255)
        else:
            # 正常顏色
            body_color = (0, 0, 139)
            front_color = (25, 25, 112)
            window_color = (173, 216, 230)
        
        # 警車車身 - 主體
        pygame.draw.rect(screen, body_color, (self.x, self.y, self.width, self.height))
        
        # 警車前部
        pygame.draw.rect(screen, front_color, (self.x + 45, self.y + 5, 15, 20))
        
        # 警車窗戶
        pygame.draw.rect(screen, window_color, (self.x + 10, self.y + 5, 35, 20))
        
        # 警燈
        pygame.draw.circle(screen, (255, 0, 0), (self.x + 15, self.y + 2), 3)
        pygame.draw.circle(screen, (0, 0, 255), (self.x + 45, self.y + 2), 3)
        
        # 車輪
        pygame.draw.circle(screen, BLACK, (self.x + 10, self.y + 25), 5)
        pygame.draw.circle(screen, BLACK, (self.x + 50, self.y + 25), 5)
    
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
        # 隨機分配敵人原型
        self.archetype = random.choice(['Normal', 'Brute', 'Rusher'])
        
        # 基礎屬性
        base_width = 40
        base_height = 40
        base_speed = 3
        base_health = 50
        
        # 根據原型調整屬性
        if self.archetype == 'Brute':
            # 蠻力型：更大、更慢、更強
            self.width = int(base_width * 1.4)
            self.height = int(base_height * 1.4)
            self.speed = base_speed * 0.7
            self.health = base_health * 2.0
            self.max_health = self.health
        elif self.archetype == 'Rusher':
            # 突襲型：更小、更快、更脆
            self.width = int(base_width * 0.7)
            self.height = int(base_height * 0.7)
            self.speed = base_speed * 1.5
            self.health = base_health * 0.6
            self.max_health = self.health
        else:  # Normal
            # 普通型：基準屬性
            self.width = base_width
            self.height = base_height
            self.speed = base_speed
            self.health = base_health
            self.max_health = self.health
        
        # 個體差異微調
        self.speed *= random.uniform(0.9, 1.1)
        self.health *= random.uniform(0.9, 1.1)
        self.max_health = self.health
        
        self.attack_cooldown = 0
        self.attack_range = 800
        self.rotor_angle = 0
        self.pulse_timer = 0
        self.state = "patrol"  # patrol, tracking, attacking
        self.laser_jitter = 0
        
    def update(self, player, bullets, game_over=False):
        if game_over:
            return
            
        # 更新動畫計時器
        self.rotor_angle += 15  # 旋翼旋轉
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
        if distance < self.attack_range:
            if distance < 800:
                self.state = "attacking"
                # 攻擊行為
                if self.attack_cooldown <= 0:
                    # 發射子彈
                    bullet_dx = dx / distance * 11  # 子彈速度
                    bullet_dy = dy / distance * 11
                    bullets.append(Bullet(self.x + self.width//2, self.y + self.height//2, bullet_dx, bullet_dy))
                    self.attack_cooldown = 120  #           2秒冷卻 (120 frames at 60 FPS)
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
            
        # 保持在螢幕範圍內
        self.x = max(0, min(SCREEN_WIDTH - self.width, self.x))
        self.y = max(0, min(SCREEN_HEIGHT - self.height, self.y))
    
    def draw(self, screen, player):
        center_x = self.x + self.width // 2
        center_y = self.y + self.height // 2
        
        # 機身多層圓形疊加
        # 底部陰影
        shadow_surface = pygame.Surface((50, 50), pygame.SRCALPHA)
        pygame.draw.circle(shadow_surface, (0, 0, 0, 80), (25, 25), 22)
        screen.blit(shadow_surface, (center_x - 25, center_y - 23))
        
        # 深色金屬底盤
        pygame.draw.circle(screen, (40, 40, 40), (center_x, center_y), 20)
        
        # 頂部漸層高光圓形
        for i in range(15):
            color_val = 60 + i * 8
            pygame.draw.circle(screen, (color_val, color_val, color_val), (center_x, center_y - 2), 20 - i)
        
        # 裝甲接縫
        pygame.draw.circle(screen, BLACK, (center_x, center_y), 20, 2)
        pygame.draw.circle(screen, BLACK, (center_x, center_y), 15, 1)
        
        # 核心攝影機 - 脈動效果
        eye_radius = 8 + math.sin(self.pulse_timer) * 2
        pygame.draw.circle(screen, BLACK, (center_x, center_y), int(eye_radius + 2))  # 眼窩
        pygame.draw.circle(screen, (200, 0, 0), (center_x, center_y), int(eye_radius))  # 惡魔紅鏡頭
        
        # 鏡頭眩光
        glare_surface = pygame.Surface((30, 6), pygame.SRCALPHA)
        pygame.draw.ellipse(glare_surface, (255, 100, 100, 100), (0, 0, 30, 6))
        screen.blit(glare_surface, (center_x - 15, center_y - 3))
        
        # 四旋翼推進器
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
            blade_angle1 = math.radians(self.rotor_angle)
            blade_angle2 = math.radians(self.rotor_angle + 180)
            
            blade1_end = (rotor_x + math.cos(blade_angle1) * 12, rotor_y + math.sin(blade_angle1) * 12)
            blade2_end = (rotor_x + math.cos(blade_angle2) * 12, rotor_y + math.sin(blade_angle2) * 12)
            
            pygame.draw.line(screen, (200, 200, 200), (rotor_x, rotor_y), blade1_end, 2)
            pygame.draw.line(screen, (200, 200, 200), (rotor_x, rotor_y), blade2_end, 2)
        
        # 狀態指示燈
        if self.state == "patrol":
            light_color = (0, 255, 0)  # 綠色
        elif self.state == "tracking":
            light_color = (255, 255, 0)  # 黃色
        else:  # attacking
            light_color = (255, 0, 0)  # 紅色
            
        pygame.draw.circle(screen, light_color, (center_x - 8, center_y - 15), 3)
        pygame.draw.circle(screen, light_color, (center_x + 8, center_y - 15), 3)
        
        # 原型標識燈
        if self.archetype == 'Brute':
            archetype_color = (100, 0, 0)  # 深紅色
        elif self.archetype == 'Rusher':
            archetype_color = (255, 255, 0)  # 亮黃色
        else:  # Normal
            archetype_color = (0, 100, 255)  # 藍色
            
        pygame.draw.circle(screen, archetype_color, (center_x, center_y - 18), 2)
        
        # 瞄準雷射（攻擊狀態時）
        if self.state == "attacking":
            laser_length = 100 + self.laser_jitter
            laser_end_x = center_x
            laser_end_y = center_y + laser_length
            pygame.draw.line(screen, (255, 0, 0), (center_x, center_y + 20), (laser_end_x, laser_end_y), 2)
            
            # 雷射光點
            pygame.draw.circle(screen, (255, 100, 100), (int(laser_end_x), int(laser_end_y)), 4)
    
    def take_damage(self, damage):
        self.health -= damage
        if self.health < 0:
            self.health = 0
    
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

class Enemy_big:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
        # 隨機分配敵人原型
        self.archetype = random.choice(['Normal', 'Brute', 'Rusher'])
        
        # 基礎屬性
        base_width = 120
        base_height = 120
        base_speed = 5
        base_health = 100
        
        # 根據原型調整屬性
        if self.archetype == 'Brute':
            # 蠻力型：更大、更慢、更強
            self.width = int(base_width * 1.4)
            self.height = int(base_height * 1.4)
            self.speed = base_speed * 0.7
            self.health = base_health * 2.0
            self.max_health = self.health
        elif self.archetype == 'Rusher':
            # 突襲型：更小、更快、更脆
            self.width = int(base_width * 0.7)
            self.height = int(base_height * 0.7)
            self.speed = base_speed * 1.5
            self.health = base_health * 0.6
            self.max_health = self.health
        else:  # Normal
            # 普通型：基準屬性
            self.width = base_width
            self.height = base_height
            self.speed = base_speed
            self.health = base_health
            self.max_health = self.health
        
        # 個體差異微調
        self.speed *= random.uniform(0.9, 1.1)
        self.health *= random.uniform(0.9, 1.1)
        self.max_health = self.health
        
        self.attack_cooldown = 0
        self.attack_range = 800
        self.rotor_angle = 0
        self.pulse_timer = 0
        self.state = "patrol"  # patrol, tracking, attacking
        self.laser_jitter = 0
        
    def update(self, player, bullets, game_over=False):
        if game_over:
            return
            
        # 更新動畫計時器
        self.rotor_angle += 15  # 旋翼旋轉
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
        if distance < self.attack_range:
            if distance < 800:
                self.state = "attacking"
                # 攻擊行為
                if self.attack_cooldown <= 0:
                    # 發射子彈
                    bullet_dx = dx / distance * 16  # 子彈速度
                    bullet_dy = dy / distance * 16
                    bullets.append(Bullet(self.x + self.width//2, self.y + self.height//2, bullet_dx, bullet_dy))
                    self.attack_cooldown = 120  #           2秒冷卻 (120 frames at 60 FPS)
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
            
        # 保持在螢幕範圍內
        self.x = max(0, min(SCREEN_WIDTH - self.width, self.x))
        self.y = max(0, min(SCREEN_HEIGHT - self.height, self.y))
    
    def draw(self, screen, player):
        center_x = self.x + self.width // 2
        center_y = self.y + self.height // 2
        
        # 機身多層圓形疊加
        # 底部陰影
        shadow_surface = pygame.Surface((50, 50), pygame.SRCALPHA)
        pygame.draw.circle(shadow_surface, (0, 0, 0, 80), (25, 25), 22)
        screen.blit(shadow_surface, (center_x - 25, center_y - 23))
        
        # 深色金屬底盤
        pygame.draw.circle(screen, (40, 40, 40), (center_x, center_y), 20)
        
        # 頂部漸層高光圓形
        for i in range(15):
            color_val = 60 + i * 8
            pygame.draw.circle(screen, (color_val, color_val, color_val), (center_x, center_y - 2), 20 - i)
        
        # 裝甲接縫
        pygame.draw.circle(screen, BLACK, (center_x, center_y), 20, 2)
        pygame.draw.circle(screen, BLACK, (center_x, center_y), 15, 1)
        
        # 核心攝影機 - 脈動效果
        eye_radius = 8 + math.sin(self.pulse_timer) * 2
        pygame.draw.circle(screen, BLACK, (center_x, center_y), int(eye_radius + 2))  # 眼窩
        pygame.draw.circle(screen, (200, 0, 0), (center_x, center_y), int(eye_radius))  # 惡魔紅鏡頭
        
        # 鏡頭眩光
        glare_surface = pygame.Surface((30, 6), pygame.SRCALPHA)
        pygame.draw.ellipse(glare_surface, (255, 100, 100, 100), (0, 0, 30, 6))
        screen.blit(glare_surface, (center_x - 15, center_y - 3))
        
        # 四旋翼推進器
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
            blade_angle1 = math.radians(self.rotor_angle)
            blade_angle2 = math.radians(self.rotor_angle + 180)
            
            blade1_end = (rotor_x + math.cos(blade_angle1) * 12, rotor_y + math.sin(blade_angle1) * 12)
            blade2_end = (rotor_x + math.cos(blade_angle2) * 12, rotor_y + math.sin(blade_angle2) * 12)
            
            pygame.draw.line(screen, (200, 200, 200), (rotor_x, rotor_y), blade1_end, 2)
            pygame.draw.line(screen, (200, 200, 200), (rotor_x, rotor_y), blade2_end, 2)
        
        # 狀態指示燈
        if self.state == "patrol":
            light_color = (0, 255, 128)  # 綠色
        elif self.state == "tracking":
            light_color = (255, 255, 128)  # 黃色
        else:  # attacking
            light_color = (255, 0, 0)  # 紅色
            
        pygame.draw.circle(screen, light_color, (center_x - 8, center_y - 15), 3)
        pygame.draw.circle(screen, light_color, (center_x + 8, center_y - 15), 3)
        
        # 原型標識燈
        if self.archetype == 'Brute':
            archetype_color = (100, 0, 0)  # 深紅色
        elif self.archetype == 'Rusher':
            archetype_color = (255, 255, 0)  # 亮黃色
        else:  # Normal
            archetype_color = (0, 100, 255)  # 藍色
            
        pygame.draw.circle(screen, archetype_color, (center_x, center_y - 18), 2)
        
        # 瞄準雷射（攻擊狀態時）
        if self.state == "attacking":
            laser_length = 100 + self.laser_jitter
            laser_end_x = center_x
            laser_end_y = center_y + laser_length
            pygame.draw.line(screen, (255, 0, 0), (center_x, center_y + 20), (laser_end_x, laser_end_y), 2)
            
            # 雷射光點
            pygame.draw.circle(screen, (255, 100, 100), (int(laser_end_x), int(laser_end_y)), 4)

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

class Bullet:
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
        # 外層光暈
        glow_surface = pygame.Surface((self.radius * 6, self.radius * 6), pygame.SRCALPHA)
        pygame.draw.circle(glow_surface, (255, 0, 0, 50), (self.radius * 3, self.radius * 3), self.radius * 3)
        screen.blit(glow_surface, (self.x - self.radius * 3, self.y - self.radius * 3))
        
        # 核心能量球
        pygame.draw.circle(screen, (255, 100, 100), (int(self.x), int(self.y)), self.radius)
        pygame.draw.circle(screen, (255, 200, 200), (int(self.x), int(self.y)), self.radius // 2)
        
    def is_off_screen(self):
        return (self.x < -50 or self.x > SCREEN_WIDTH + 50 or 
                self.y < -50 or self.y > SCREEN_HEIGHT + 50)
    
    def get_rect(self):
        return pygame.Rect(self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2)

class Prisoner:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
        # 隨機分配敵人原型
        self.archetype = random.choice(['Normal', 'Brute', 'Rusher'])
        
        # 基礎屬性
        base_width = 30
        base_height = 40
        base_speed = 4
        base_health = 30
        
        # 根據原型調整屬性
        if self.archetype == 'Brute':
            # 蠻力型：更大、更慢、更強
            self.width = int(base_width * 1.4)
            self.height = int(base_height * 1.2)
            self.speed = base_speed * 0.7
            self.health = base_health * 2.0
            self.max_health = self.health
        elif self.archetype == 'Rusher':
            # 突襲型：更小、更快、更脆
            self.width = int(base_width * 0.8)
            self.height = int(base_height * 0.9)
            self.speed = base_speed * 1.5
            self.health = base_health * 0.6
            self.max_health = self.health
        else:  # Normal
            # 普通型：基準屬性
            self.width = base_width
            self.height = base_height
            self.speed = base_speed
            self.health = base_health
            self.max_health = self.health
        
        # 個體差異微調
        self.speed *= random.uniform(0.9, 1.1)
        self.health *= random.uniform(0.9, 1.1)
        self.max_health = self.health
        
        self.arm_swing = 0
        self.move_direction = 1
        
    def update(self, player, game_over=False):
        if game_over:
            return
            
        # 更新手臂擺動動畫
        self.arm_swing += 0.3
        
        # 追蹤玩家
        dx = player.x - self.x
        dy = player.y - self.y
        distance = math.sqrt(dx*dx + dy*dy)
        
        if distance > 0:
            self.x += (dx / distance) * self.speed
            self.y += (dy / distance) * self.speed
            
        # 保持在螢幕範圍內
        self.x = max(0, min(SCREEN_WIDTH - self.width, self.x))
        self.y = max(0, min(SCREEN_HEIGHT - self.height, self.y))
    
    def draw(self, screen):
        center_x = self.x + self.width // 2
        center_y = self.y + self.height // 2
        
        # 根據原型調整視覺特徵
        if self.archetype == 'Brute':
            # 蠻力型：更大、更深沉的顏色
            body_color = (200, 100, 0)  # 更深的橘色
            fold_color = (150, 80, 0)
            head_radius = 10
            body_width = int(self.width * 0.8)
            body_height = int(self.height * 0.6)
            eye_size = 3
        elif self.archetype == 'Rusher':
            # 突襲型：更小、更亮的顏色
            body_color = (255, 180, 50)  # 更亮的橘色
            fold_color = (255, 150, 30)
            head_radius = 6
            body_width = int(self.width * 0.6)
            body_height = int(self.height * 0.6)
            eye_size = 1
        else:  # Normal
            # 普通型：標準顏色
            body_color = (255, 140, 0)
            fold_color = (200, 110, 0)
            head_radius = 8
            body_width = 20
            body_height = 25
            eye_size = 2
        
        # 陰影
        shadow_surface = pygame.Surface((self.width + 10, 8), pygame.SRCALPHA)
        pygame.draw.ellipse(shadow_surface, (0, 0, 0, 100), (0, 0, self.width + 10, 8))
        screen.blit(shadow_surface, (self.x - 5, self.y + self.height))
        
        # 身體（橘色囚服）
        body_x = center_x - body_width // 2
        pygame.draw.rect(screen, body_color, (body_x, self.y + 15, body_width, body_height))
        
        # 囚服褶皺紋理
        fold_count = 4 if self.archetype == 'Brute' else 3
        for i in range(fold_count):
            fold_y = self.y + 18 + i * (body_height // fold_count)
            pygame.draw.line(screen, fold_color, (body_x + 1, fold_y), (body_x + body_width - 1, fold_y), 1)
        
        # 頭部（膚色）
        pygame.draw.circle(screen, (222, 184, 135), (center_x, self.y + 10), head_radius)
        
        # 眼睛
        eye_offset = 3 if self.archetype != 'Rusher' else 2
        pygame.draw.circle(screen, BLACK, (center_x - eye_offset, self.y + 8), eye_size)
        pygame.draw.circle(screen, BLACK, (center_x + eye_offset, self.y + 8), eye_size)
        
        # 手臂擺動（根據原型調整動態特徵）
        if self.archetype == 'Rusher':
            # 突襲型：更大的手臂擺動
            arm_offset = math.sin(self.arm_swing) * 8
            arm_thickness = 2
        elif self.archetype == 'Brute':
            # 蠻力型：較小但更粗的手臂
            arm_offset = math.sin(self.arm_swing) * 3
            arm_thickness = 4
        else:  # Normal
            # 普通型：標準擺動
            arm_offset = math.sin(self.arm_swing) * 5
            arm_thickness = 3
        
        # 左臂
        left_arm_start = (body_x, self.y + 20)
        left_arm_end = (body_x - 3, self.y + 25 + arm_offset)
        pygame.draw.line(screen, (222, 184, 135), left_arm_start, left_arm_end, arm_thickness)
        
        # 右臂
        right_arm_start = (body_x + body_width, self.y + 20)
        right_arm_end = (body_x + body_width + 3, self.y + 25 - arm_offset)
        pygame.draw.line(screen, (222, 184, 135), right_arm_start, right_arm_end, arm_thickness)
        
        # 腿部（根據原型調整）
        leg_thickness = 5 if self.archetype == 'Brute' else 4
        leg_color = body_color
        
        pygame.draw.line(screen, leg_color, (center_x - 5, self.y + self.height - 10), 
                        (center_x - 7, self.y + self.height + 5), leg_thickness)
        pygame.draw.line(screen, leg_color, (center_x + 5, self.y + self.height - 10), 
                        (center_x + 7, self.y + self.height + 5), leg_thickness)
    
    def take_damage(self, damage):
        self.health -= damage
        if self.health < 0:
            self.health = 0
    
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

class WeaponPickup:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 40
        self.height = 15
        self.pulse_timer = 0
        
    def update(self):
        self.pulse_timer += 0.1
        
    def draw(self, screen):
        # 脈動光暈
        pulse_alpha = int(100 + 50 * math.sin(self.pulse_timer))
        glow_surface = pygame.Surface((60, 35), pygame.SRCALPHA)
        pygame.draw.ellipse(glow_surface, (255, 255, 255, pulse_alpha), (0, 0, 60, 35))
        screen.blit(glow_surface, (self.x - 10, self.y - 10))
        
        # 槍身（深灰色）
        pygame.draw.rect(screen, (60, 60, 60), (self.x, self.y + 5, 35, 8))
        
        # 槍托（黑色）
        pygame.draw.rect(screen, BLACK, (self.x - 5, self.y + 3, 8, 12))
        
        # 握把（黑色）
        pygame.draw.rect(screen, BLACK, (self.x + 15, self.y + 13, 6, 10))
        
        # 彈匣（彎曲）
        pygame.draw.rect(screen, (40, 40, 40), (self.x + 18, self.y + 13, 4, 15))
        
        # 金屬高光
        pygame.draw.line(screen, WHITE, (self.x + 2, self.y + 6), (self.x + 32, self.y + 6), 1)
        
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

class PlayerBullet:
    def __init__(self, x, y, dx, dy):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.width = 6
        self.height = 12
        self.trail = []  # 尾跡粒子
        
    def update(self):
        # 添加當前位置到尾跡
        self.trail.append((self.x, self.y))
        if len(self.trail) > 8:  # 限制尾跡長度
            self.trail.pop(0)
            
        self.x += self.dx
        self.y += self.dy
        
    def draw(self, screen):
        # 繪製尾跡
        for i, (trail_x, trail_y) in enumerate(self.trail):
            alpha = int(255 * (i + 1) / len(self.trail))
            size = int(4 * (i + 1) / len(self.trail))
            
            trail_surface = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
            pygame.draw.circle(trail_surface, (255, 255, 0, alpha), (size, size), size)
            screen.blit(trail_surface, (trail_x - size, trail_y - size))
        
        # 子彈本體（明亮黃色矩形）
        pygame.draw.rect(screen, (255, 255, 0), (self.x - self.width//2, self.y - self.height//2, 
                                                self.width, self.height))
        pygame.draw.rect(screen, (255, 255, 200), (self.x - self.width//2 + 1, self.y - self.height//2 + 1, 
                                                  self.width - 2, self.height - 2))
        
    def is_off_screen(self):
        return (self.x < -50 or self.x > SCREEN_WIDTH + 50 or 
                self.y < -50 or self.y > SCREEN_HEIGHT + 50)
    
    def get_rect(self):
        return pygame.Rect(self.x - self.width//2, self.y - self.height//2, self.width, self.height)

class Building:
    def __init__(self, x, y, building_type):
        self.rect = pygame.Rect(x, y, 200, 200)  # 基礎尺寸
        self.building_type = building_type
        self.is_active = False
        
    def draw(self, surface):
        if self.building_type == "School":
            self.draw_school(surface)
        elif self.building_type == "Park":
            self.draw_park(surface)
        elif self.building_type == "Office":
            self.draw_office(surface)
        elif self.building_type == "Community":
            self.draw_community(surface)
        elif self.building_type == "Military":
            self.draw_military(surface)
            
        # 繪製「已檢查」狀態
        if self.is_active:
            self.draw_active_indicator(surface)
    
    def draw_school(self, surface):
        x, y = self.rect.topleft
        
        # 陰影面 (後層)
        pygame.draw.rect(surface, (139, 0, 0), (x + 5, y + 5, 150, 100))
        
        # 受光面 (前層)
        pygame.draw.rect(surface, (205, 92, 92), (x, y, 145, 100))
        
        # 屋頂
        pygame.draw.rect(surface, (105, 105, 105), (x - 5, y - 20, 165, 25))
        
        # 窗戶 - 2排4個
        for row in range(2):
            for col in range(4):
                window_x = x + 15 + col * 30
                window_y = y + 15 + row * 35
                # 窗戶框架
                pygame.draw.rect(surface, (173, 216, 230), (window_x, window_y, 15, 25))
                # 十字窗框
                pygame.draw.line(surface, WHITE, (window_x + 7, window_y), (window_x + 7, window_y + 25), 2)
                pygame.draw.line(surface, WHITE, (window_x, window_y + 12), (window_x + 15, window_y + 12), 2)
        
        # 大門
        pygame.draw.rect(surface, (139, 69, 19), (x + 60, y + 70, 25, 30))
        
        # 旗桿
        pygame.draw.line(surface, (192, 192, 192), (x + 160, y - 50), (x + 160, y + 10), 2)
        # 旗幟
        pygame.draw.rect(surface, (255, 0, 0), (x + 160, y - 50, 15, 10))
    
    def draw_park(self, surface):
        x, y = self.rect.topleft
        
        # 草地 - 不規則多邊形
        grass_points = [
            (x, y + 20), (x + 50, y), (x + 120, y + 10), (x + 200, y + 30),
            (x + 190, y + 100), (x + 150, y + 150), (x + 80, y + 140), (x + 20, y + 120)
        ]
        pygame.draw.polygon(surface, (144, 238, 144), grass_points)
        
        # 小徑
        path_points = [(x + 20, y + 140), (x + 60, y + 100), (x + 120, y + 80), (x + 160, y + 50), (x + 180, y + 20)]
        pygame.draw.lines(surface, (245, 222, 179), False, path_points, 8)
        
        # 樹木
        tree_positions = [(x + 40, y + 60), (x + 100, y + 40), (x + 140, y + 100), (x + 60, y + 120)]
        for tree_x, tree_y in tree_positions:
            # 樹幹
            pygame.draw.rect(surface, (139, 69, 19), (tree_x, tree_y, 10, 30))
            # 樹冠
            pygame.draw.circle(surface, (0, 100, 0), (tree_x + 5, tree_y), 15)
        
        # 池塘
        pygame.draw.ellipse(surface, (0, 191, 255), (x + 120, y + 110, 50, 30))
        
        # 花圃
        pygame.draw.rect(surface, (160, 82, 45), (x + 30, y + 30, 40, 20), border_radius=5)
        # 花朵
        flower_colors = [(255, 0, 0), (255, 255, 0), (255, 192, 203)]
        for _ in range(12):
            flower_x = x + 32 + random.randint(0, 36)
            flower_y = y + 32 + random.randint(0, 16)
            color = random.choice(flower_colors)
            pygame.draw.circle(surface, color, (flower_x, flower_y), 3)
    
    def draw_office(self, surface):
        x, y = self.rect.topleft
        
        # 主體框架
        pygame.draw.rect(surface, (47, 79, 79), (x, y, 80, 250))
        
        # 玻璃帷幕 - 網格燈光
        for row in range(16):  # 250/15 ≈ 16
            for col in range(8):  # 80/10 = 8
                cell_x = x + col * 10
                cell_y = y + row * 15
                if random.random() > 0.5:
                    # 亮燈
                    pygame.draw.rect(surface, (255, 255, 153), (cell_x, cell_y, 10, 15))
                else:
                    # 關燈
                    pygame.draw.rect(surface, (70, 130, 180), (cell_x, cell_y, 10, 15))
        
        # 天線
        pygame.draw.line(surface, WHITE, (x + 40, y - 40), (x + 40, y), 3)
        
        # 警示燈 - 閃爍效果
        if pygame.time.get_ticks() % 1000 > 500:
            pygame.draw.circle(surface, (255, 0, 0), (x + 40, y - 40), 5)
    
    def draw_community(self, surface):
        x, y = self.rect.topleft
        
        # 3棟小房子
        house_colors = [(245, 245, 220), (255, 250, 205)]
        house_positions = [(x + 20, y + 50), (x + 100, y + 80), (x + 160, y + 40)]
        
        for i, (house_x, house_y) in enumerate(house_positions):
            # 牆體
            wall_color = random.choice(house_colors)
            pygame.draw.rect(surface, wall_color, (house_x, house_y, 50, 40))
            
            # 屋頂 - 三角形
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
        x, y = self.rect.topleft
        
        # 主堡壘
        pygame.draw.rect(surface, (112, 128, 144), (x, y, 180, 100))
        
        # 迷彩圖案
        camo_colors = [(85, 107, 47), (193, 154, 107)]
        for _ in range(4):
            color = random.choice(camo_colors)
            # 隨機多邊形
            points = []
            for _ in range(6):
                px = x + random.randint(10, 170)
                py = y + random.randint(10, 90)
                points.append((px, py))
            pygame.draw.polygon(surface, color, points)
        
        # 圍牆 - 柵欄
        fence_positions = list(range(x - 20, x + 200, 15))
        for fence_x in fence_positions:
            # 垂直線
            pygame.draw.line(surface, (105, 105, 105), (fence_x, y - 10), (fence_x, y + 110), 4)
            # 尖刺三角形
            spike_points = [(fence_x - 3, y - 10), (fence_x + 3, y - 10), (fence_x, y - 15)]
            pygame.draw.polygon(surface, (105, 105, 105), spike_points)
        
        # 停機坪
        pygame.draw.circle(surface, (105, 105, 105), (x + 140, y + 140), 30)
        # H標記
        pygame.draw.line(surface, WHITE, (x + 130, y + 130), (x + 130, y + 150), 8)
        pygame.draw.line(surface, WHITE, (x + 150, y + 130), (x + 150, y + 150), 8)
        pygame.draw.line(surface, WHITE, (x + 130, y + 140), (x + 150, y + 140), 8)
        
        # 瞭望塔
        pygame.draw.rect(surface, (105, 105, 105), (x + 200, y + 40, 15, 60))
        pygame.draw.rect(surface, (105, 105, 105), (x + 195, y + 25, 25, 15))
    
    def draw_active_indicator(self, surface):
        # 半透明綠色光環
        center_x = self.rect.centerx
        center_y = self.rect.centery
        radius = self.rect.width // 2
        
        # 創建透明表面
        indicator_surface = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
        
        # 畫外圓
        pygame.draw.circle(indicator_surface, (0, 255, 0, 128), (radius, radius), radius)
        # 畫內圓（創造圓環效果）
        pygame.draw.circle(indicator_surface, (0, 0, 0, 0), (radius, radius), radius - 20)
        
        # 將指示器繪製到主表面
        surface.blit(indicator_surface, (center_x - radius, center_y - radius))

def draw_background_level1(screen):
    # 填充草地背景
    screen.fill(GRASS_GREEN)
    
    # 計算道路位置（Y軸中央）
    road_y = SCREEN_HEIGHT // 2 - 100  # 200像素寬度的一半
    
    # 繪製人行道（上下兩條）
    pygame.draw.rect(screen, SIDEWALK_GRAY, (0, road_y - 30, SCREEN_WIDTH, 30))  # 上人行道
    pygame.draw.rect(screen, SIDEWALK_GRAY, (0, road_y + 200, SCREEN_WIDTH, 30))  # 下人行道
    
    # 繪製馬路
    pygame.draw.rect(screen, ROAD_GRAY, (0, road_y, SCREEN_WIDTH, 200))
    
    # 繪製道路中線
    for x in range(0, SCREEN_WIDTH, 40):
        pygame.draw.rect(screen, WHITE, (x, road_y + 95, 20, 10))

def draw_background_level2(screen):
    # 監獄場景背景
    
    # 深灰色石磚地板
    brick_size = 40
    for y in range(0, SCREEN_HEIGHT, brick_size):
        for x in range(0, SCREEN_WIDTH, brick_size):
            # 隨機變化的深灰色
            gray_val = random.randint(50, 65)
            brick_color = (gray_val, gray_val, gray_val + 5)
            pygame.draw.rect(screen, brick_color, (x, y, brick_size, brick_size))
            
            # 黑色縫隙
            pygame.draw.rect(screen, BLACK, (x, y, brick_size, brick_size), 1)
    
    # 隨機水漬
    for _ in range(15):
        stain_x = random.randint(0, SCREEN_WIDTH - 50)
        stain_y = random.randint(0, SCREEN_HEIGHT - 30)
        stain_surface = pygame.Surface((50, 30), pygame.SRCALPHA)
        pygame.draw.ellipse(stain_surface, (20, 20, 25, 120), (0, 0, 50, 30))
        screen.blit(stain_surface, (stain_x, stain_y))
    
    # 地板裂縫
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
    
    # 上下牆壁與鐵欄杆
    wall_height = 80
    
    # 上牆壁
    pygame.draw.rect(screen, (40, 40, 45), (0, 0, SCREEN_WIDTH, wall_height))
    # 下牆壁
    pygame.draw.rect(screen, (40, 40, 45), (0, SCREEN_HEIGHT - wall_height, SCREEN_WIDTH, wall_height))
    
    # 鐵欄杆
    bar_spacing = 30
    for x in range(0, SCREEN_WIDTH, bar_spacing):
        # 上方鐵欄杆
        pygame.draw.rect(screen, BLACK, (x, 20, 8, wall_height - 40))
        # 鏽跡
        pygame.draw.circle(screen, (139, 69, 19), (x + 4, 30 + random.randint(0, 20)), 2)
        
        # 下方鐵欄杆
        pygame.draw.rect(screen, BLACK, (x, SCREEN_HEIGHT - wall_height + 20, 8, wall_height - 40))
        # 鏽跡
        pygame.draw.circle(screen, (139, 69, 19), (x + 4, SCREEN_HEIGHT - 50 + random.randint(0, 20)), 2)
    
    # 陰影入口（敵人生成點）
    shadow_positions = [(100, 10), (500, 10), (900, 10), (1300, 10), (1700, 10),
                       (100, SCREEN_HEIGHT - 70), (500, SCREEN_HEIGHT - 70), 
                       (900, SCREEN_HEIGHT - 70), (1300, SCREEN_HEIGHT - 70)]
    
    for shadow_x, shadow_y in shadow_positions:
        shadow_surface = pygame.Surface((80, 60), pygame.SRCALPHA)
        pygame.draw.ellipse(shadow_surface, (0, 0, 0, 180), (0, 0, 80, 60))
        screen.blit(shadow_surface, (shadow_x, shadow_y))
    
    # 探照燈光束
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
    beam_angle2 = math.sin(time_factor + math.pi) * 25
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

def draw_health_bar(screen, player, font):
    # 健康條位置（右下角）
    bar_width = 200
    bar_height = 20
    bar_x = SCREEN_WIDTH - bar_width - 20
    bar_y = SCREEN_HEIGHT - bar_height - 60
    
    # 背景條（深紅色）
    pygame.draw.rect(screen, (100, 0, 0), (bar_x, bar_y, bar_width, bar_height))
    
    # 前景條（綠色，寬度與生命值聯動）
    health_percentage = player.health / player.max_health
    health_width = int(bar_width * health_percentage)
    
    # 根據生命值改變顏色
    if health_percentage > 0.6:
        health_color = (0, 255, 0)  # 綠色
    elif health_percentage > 0.3:
        health_color = (255, 255, 0)  # 黃色
    else:
        health_color = (255, 0, 0)  # 紅色
        
    pygame.draw.rect(screen, health_color, (bar_x, bar_y, health_width, bar_height))
    
    # 邊框
    pygame.draw.rect(screen, WHITE, (bar_x, bar_y, bar_width, bar_height), 2)
    
    # HP 文字
    hp_text = font.render(f"HP: {player.health}", True, WHITE)
    screen.blit(hp_text, (bar_x, bar_y - 30))

def load_level(level_number, player):
    """加載指定關卡"""
    if level_number == 1:
        # 第一關：城市巡邏
        buildings = [
            Building(200, 100, "School"),
            Building(600, 150, "Park"),
            Building(1200, 50, "Office"),
            Building(300, 700, "Community"),
            Building(1400, 650, "Military")
        ]
        
        enemies = [
            Enemy_big(800, 300),
            Enemy(800, 400),
            Enemy(700, 300),
            Enemy(900, 300),
            Enemy(800, 1100),
            Enemy(1500, 800)
        ]
        
        prisoners = []
        weapon_pickups = []
        
        # 重置玩家位置和狀態
        player.x = 100
        player.y = SCREEN_HEIGHT // 2 - 15
        player.health = 100
        player.has_gun = False
        
        return buildings, enemies, prisoners, weapon_pickups
        
    elif level_number == 2:
        # 第二關：監獄突破
        buildings = []  # 第二關沒有建築物
        enemies = []    # 第二關沒有無人機
        
        # 創建囚犯
        prisoners = [
            Prisoner(200, 150),
            Prisoner(400, 200),
            Prisoner(600, 180),
            Prisoner(800, 220),
            Prisoner(1000, 160),
            Prisoner(1200, 190),
            Prisoner(1400, 170),
            Prisoner(1600, 200),
            Prisoner(300, 800),
            #Prisoner(500, 850),
            #Prisoner(700, 820),
            #Prisoner(900, 880),
            #Prisoner(1100, 840),
            #Prisoner(1300, 860)
        ]
        
        # 創建武器拾取點
        weapon_pickups = [
            WeaponPickup(SCREEN_WIDTH // 2 - 20, SCREEN_HEIGHT // 2)
        ]
        
        # 重置玩家位置和狀態
        player.x = SCREEN_WIDTH // 2 - 30
        player.y = SCREEN_HEIGHT - 100
        player.health = 100
        player.has_gun = False
        
        return buildings, enemies, prisoners, weapon_pickups
    
    return [], [], [], []

def main():
    # 創建遊戲視窗
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("城市守護者：精確巡邏")
    clock = pygame.time.Clock()
    
    # 創建字體
    font_ui = pygame.font.Font(None, 50)
    font_victory = pygame.font.Font(None, 120)
    font_defeat = pygame.font.Font(None, 120)
    font_transition = pygame.font.Font(None, 80)
    
    # 創建玩家
    player = Player(100, SCREEN_HEIGHT // 2 - 15)
    
    # 關卡管理
    current_level = 1
    buildings, enemies, prisoners, weapon_pickups = load_level(current_level, player)
    
    # 子彈列表
    bullets = []
    player_bullets = []
    
    # 遊戲狀態
    game_won = False
    game_lost = False
    level_transition = False
    transition_timer = 0
    
    # 遊戲主迴圈
    running = True
    while running:
        # 處理事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # 獲取按鍵狀態
        keys = pygame.key.get_pressed()
        
        # 檢查失敗條件
        if player.health <= 0:
            game_lost = True
        
        # 處理關卡轉換
        if level_transition:
            transition_timer -= 1
            if transition_timer <= 0:
                level_transition = False
                current_level = 2
                buildings, enemies, prisoners, weapon_pickups = load_level(current_level, player)
                bullets.clear()
                player_bullets.clear()
        
        # 更新遊戲邏輯
        game_over = game_won or game_lost
        
        if not game_over and not level_transition:
            # 更新玩家
            player.update(keys, game_over, player_bullets)
            
            # 更新敵人（第一關）
            for enemy in enemies:
                enemy.update(player, bullets, game_over)
            
            # 更新囚犯（第二關）
            for prisoner in prisoners[:]:
                prisoner.update(player, game_over)
                
                # 檢查囚犯與玩家的碰撞（近戰傷害）
                if prisoner.get_rect().colliderect(player.get_rect()):
                    player.take_damage(5)
            
            # 更新武器拾取點
            for weapon in weapon_pickups[:]:
                weapon.update()
                if weapon.get_rect().colliderect(player.get_rect()):
                    player.has_gun = True
                    weapon_pickups.remove(weapon)
            
            # 更新敵人子彈
            for bullet in bullets[:]:
                bullet.update()
                if bullet.is_off_screen():
                    bullets.remove(bullet)
            
            # 更新玩家子彈
            for bullet in player_bullets[:]:
                bullet.update()
                if bullet.is_off_screen():
                    player_bullets.remove(bullet)
            
            # 檢查敵人子彈與玩家的碰撞
            player_rect = player.get_rect()
            for bullet in bullets[:]:
                if player_rect.colliderect(bullet.get_rect()):
                    player.take_damage(10)
                    bullets.remove(bullet)
            
            # 檢查玩家子彈與囚犯的碰撞
            for bullet in player_bullets[:]:
                for prisoner in prisoners[:]:
                    if bullet.get_rect().colliderect(prisoner.get_rect()):
                        prisoner.take_damage(30)
                        player_bullets.remove(bullet)
                        if prisoner.health <= 0:
                            prisoners.remove(prisoner)
                        break
            
            # 第一關邏輯
            if current_level == 1:
                # 檢查玩家與建築物的碰撞
                for building in buildings:
                    if not building.is_active and player_rect.colliderect(building.rect):
                        building.is_active = True
                
                # 檢查第一關勝利條件
                active_count = sum(1 for building in buildings if building.is_active)
                if active_count == len(buildings):
                    level_transition = True
                    transition_timer = 180  # 3秒轉換時間
            
            # 第二關邏輯
            elif current_level == 2:
                # 檢查第二關勝利條件
                if len(prisoners) == 0:
                    game_won = True
        
        # 繪製畫面
        if current_level == 1:
            draw_background_level1(screen)
        elif current_level == 2:
            draw_background_level2(screen)
        
        # 繪製建築物（第一關）
        for building in buildings:
            building.draw(screen)
        
        # 繪製敵人（第一關）
        for enemy in enemies:
            enemy.draw(screen, player)
        
        # 繪製囚犯（第二關）
        for prisoner in prisoners:
            prisoner.draw(screen)
        
        # 繪製武器拾取點
        for weapon in weapon_pickups:
            weapon.draw(screen)
        
        # 繪製子彈
        for bullet in bullets:
            bullet.draw(screen)
        
        # 繪製玩家子彈
        for bullet in player_bullets:
            bullet.draw(screen)
        
        # 繪製玩家
        player.draw(screen)
        
        # 繪製UI
        if current_level == 1:
            active_count = sum(1 for building in buildings if building.is_active)
            progress_text = font_ui.render(f"巡邏進度: {active_count} / {len(buildings)}", True, WHITE)
            screen.blit(progress_text, (20, 20))
        elif current_level == 2:
            enemies_left = len(prisoners)
            progress_text = font_ui.render(f"剩餘囚犯: {enemies_left}", True, WHITE)
            screen.blit(progress_text, (20, 20))
            
            # 武器狀態
            if player.has_gun:
                weapon_text = font_ui.render("武器: 突擊步槍 [空白鍵射擊]", True, WHITE)
                screen.blit(weapon_text, (20, 70))
            else:
                weapon_text = font_ui.render("尋找武器！", True, (255, 255, 0))
                screen.blit(weapon_text, (20, 70))
        
        # 繪製健康條
        draw_health_bar(screen, player, font_ui)
        
        # 繪製關卡轉換畫面
        if level_transition:
            transition_bg = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            transition_bg.fill((0, 0, 0, 150))
            screen.blit(transition_bg, (0, 0))
            
            transition_text1 = font_transition.render("LEVEL 1 CLEARED!", True, (0, 255, 0))
            transition_text2 = font_transition.render("ENTERING PRISON COMPLEX...", True, WHITE)
            
            text_rect1 = transition_text1.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
            text_rect2 = transition_text2.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
            
            screen.blit(transition_text1, text_rect1)
            screen.blit(transition_text2, text_rect2)
        
        # 繪製勝利畫面
        if game_won:
            if current_level == 2:
                victory_text = font_victory.render("LEVEL 2 CLEARED!", True, (0, 255, 0))
                victory_text2 = font_ui.render("PREPARE FOR THE NEXT CHALLENGE...", True, WHITE)
            else:
                victory_text = font_victory.render("城市巡邏完成！", True, WHITE)
                victory_text2 = None
                
            text_rect = victory_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            
            # 勝利背景
            victory_bg = pygame.Surface((text_rect.width + 40, text_rect.height + 20), pygame.SRCALPHA)
            victory_bg.fill((0, 0, 0, 180))
            screen.blit(victory_bg, (text_rect.x - 20, text_rect.y - 10))
            
            screen.blit(victory_text, text_rect)
            
            if victory_text2:
                text_rect2 = victory_text2.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100))
                screen.blit(victory_text2, text_rect2)
        
        # 繪製失敗畫面
        if game_lost:
            defeat_text = font_defeat.render("任務失敗！車輛損毀！", True, (255, 0, 0))
            text_rect = defeat_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            
            # 失敗背景
            defeat_bg = pygame.Surface((text_rect.width + 40, text_rect.height + 20), pygame.SRCALPHA)
            defeat_bg.fill((0, 0, 0, 200))
            screen.blit(defeat_bg, (text_rect.x - 20, text_rect.y - 10))
            
            screen.blit(defeat_text, text_rect)
        
        # 更新顯示
        pygame.display.flip()
        clock.tick(60)  # 60 FPS
    
    # 退出遊戲
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()