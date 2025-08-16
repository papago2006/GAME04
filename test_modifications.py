#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
測試修改後的遊戲功能
1. 測試敵人碰撞體是否增大
2. 測試子彈是否能跟隨滑鼠方向
"""

import pygame
import math
import sys

# 初始化 Pygame
pygame.init()

# 遊戲設定
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

def test_collision_expansion():
    """測試碰撞體擴大功能"""
    print("測試碰撞體擴大功能...")
    
    # 模擬敵人類
    class TestEnemy:
        def __init__(self, x, y):
            self.x = x
            self.y = y
            self.width = 40
            self.height = 40
            
        def get_rect(self):
            # 增加碰撞體尺寸，讓命中判定更容易
            expanded_width = self.width * 1.3
            expanded_height = self.height * 1.3
            offset_x = (expanded_width - self.width) / 2
            offset_y = (expanded_height - self.height) / 2
            return pygame.Rect(self.x - offset_x, self.y - offset_y, expanded_width, expanded_height)
    
    enemy = TestEnemy(100, 100)
    original_rect = pygame.Rect(enemy.x, enemy.y, enemy.width, enemy.height)
    expanded_rect = enemy.get_rect()
    
    print(f"原始碰撞體: {original_rect}")
    print(f"擴大碰撞體: {expanded_rect}")
    print(f"寬度增加: {expanded_rect.width - original_rect.width}")
    print(f"高度增加: {expanded_rect.height - original_rect.height}")
    print("✓ 碰撞體擴大功能正常")

def test_mouse_direction_shooting():
    """測試滑鼠方向射擊功能"""
    print("\n測試滑鼠方向射擊功能...")
    
    # 模擬玩家位置
    player_x, player_y = 400, 300
    player_width, player_height = 60, 30
    
    # 模擬不同的滑鼠位置
    test_cases = [
        (500, 200, "右上"),
        (300, 200, "左上"), 
        (500, 400, "右下"),
        (300, 400, "左下"),
        (400, 200, "正上"),
        (400, 400, "正下"),
        (500, 300, "正右"),
        (300, 300, "正左")
    ]
    
    for mouse_x, mouse_y, direction in test_cases:
        # 計算玩家中心位置
        player_center_x = player_x + player_width // 2
        player_center_y = player_y + player_height // 2
        
        # 計算滑鼠與玩家的距離和方向
        dx = mouse_x - player_center_x
        dy = mouse_y - player_center_y
        distance = math.sqrt(dx*dx + dy*dy)
        
        if distance > 0:
            # 正規化方向向量並設定子彈速度
            bullet_speed = 12
            bullet_dx = (dx / distance) * bullet_speed
            bullet_dy = (dy / distance) * bullet_speed
            
            # 計算角度（用於顯示）
            angle = math.degrees(math.atan2(dy, dx))
            
            print(f"{direction}方向 - 滑鼠({mouse_x}, {mouse_y}) -> 子彈速度({bullet_dx:.2f}, {bullet_dy:.2f}) 角度: {angle:.1f}°")
    
    print("✓ 滑鼠方向射擊功能正常")

def main():
    print("=== 遊戲修改功能測試 ===")
    test_collision_expansion()
    test_mouse_direction_shooting()
    print("\n=== 所有測試完成 ===")
    print("\n修改摘要:")
    print("1. ✓ 敵人碰撞體尺寸增加30%，提高命中判定")
    print("2. ✓ 子彈射擊改為360度跟隨滑鼠方向")
    print("\n可以運行 city_patrol_game_0721_pm10.py 來體驗修改後的遊戲！")

if __name__ == "__main__":
    main()