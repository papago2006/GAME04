# 玩家類
import pygame
import math
from config import PLAYER_SPEED, SCREEN_WIDTH, SCREEN_HEIGHT
from player_renderer import PlayerRenderer
from bullet_system import PlayerBullet

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 60
        self.height = 30
        self.speed = PLAYER_SPEED
        self.health = 100
        self.max_health = 100
        self.hit_timer = 0
        self.has_gun = False
        self.shoot_cooldown = 0
        self.is_transformed = False
        
        # 渲染器
        self.renderer = PlayerRenderer()
        
    def update(self, keys, game_over=False, player_bullets=None, transformation_system=None):
        """更新玩家狀態"""
        # 更新受創計時器
        if self.hit_timer > 0:
            self.hit_timer -= 1
            
        # 更新射擊冷卻
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1
            
        # 更新變身狀態
        if transformation_system:
            self.is_transformed = transformation_system.transformation_active
            
        # 更新渲染器
        self.renderer.update(0.016)  # 假設60FPS
            
        # 如果遊戲結束，停止移動
        if game_over:
            return
            
        # 變身狀態下速度加快
        current_speed = self.speed * 1.5 if self.is_transformed else self.speed
        
        # 移動控制
        self._handle_movement(keys, current_speed)
        
        # 射擊控制
        if self.has_gun and keys[pygame.K_SPACE] and self.shoot_cooldown <= 0 and player_bullets is not None:
            self._handle_shooting(player_bullets)
    
    def _handle_movement(self, keys, current_speed):
        """處理移動"""
        if keys[pygame.K_LEFT] and self.x > 0:
            self.x -= current_speed
        if keys[pygame.K_RIGHT] and self.x < SCREEN_WIDTH - self.width:
            self.x += current_speed
        if keys[pygame.K_UP] and self.y > 0:
            self.y -= current_speed
        if keys[pygame.K_DOWN] and self.y < SCREEN_HEIGHT - self.height:
            self.y += current_speed
    
    def _handle_shooting(self, player_bullets):
        """處理射擊 - 360度跟隨滑鼠方向"""
        # 獲取滑鼠位置
        mouse_x, mouse_y = pygame.mouse.get_pos()
        
        # 計算玩家中心位置
        player_center_x = self.x + self.width // 2
        player_center_y = self.y + self.height // 2
        
        # 計算滑鼠與玩家的距離和方向
        dx = mouse_x - player_center_x
        dy = mouse_y - player_center_y
        distance = math.sqrt(dx*dx + dy*dy)
        
        # 避免除零錯誤
        if distance > 0:
            # 正規化方向向量並設定子彈速度
            bullet_speed = 12
            bullet_dx = (dx / distance) * bullet_speed
            bullet_dy = (dy / distance) * bullet_speed
            
            # 發射子彈
            bullet_x = player_center_x
            bullet_y = player_center_y
            player_bullets.append(PlayerBullet(bullet_x, bullet_y, bullet_dx, bullet_dy))
            self.shoot_cooldown = 15  # 射擊冷卻
    
    def take_damage(self, damage):
        """受到傷害"""
        self.health -= damage
        self.hit_timer = 30  # 0.5秒閃爍
        if self.health < 0:
            self.health = 0
    
    def draw(self, screen):
        """繪製玩家"""
        self.renderer.draw(screen, self)
    
    def get_rect(self):
        """獲取碰撞矩形"""
        return pygame.Rect(self.x, self.y, self.width, self.height)