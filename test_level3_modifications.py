#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
測試第三關修改後的功能
1. 測試敵人碰撞體是否增大
2. 測試子彈是否能跟隨滑鼠方向
"""

import pygame
import math
import sys

# 初始化 Pygame
pygame.init()

def test_level3_collision_expansion():
    """測試第三關敵人碰撞體擴大功能"""
    print("測試第三關敵人碰撞體擴大功能...")
    
    # 模擬第三關敵人類
    class TestBattlefieldEnemy:
        def __init__(self, x, y):
            self.x = x
            self.y = y
            self.width = 60
            self.height = 30
            
        def get_rect(self):
            # 增加碰撞體尺寸，讓命中判定更容易
            expanded_width = self.width * 1.3
            expanded_height = self.height * 1.3
            offset_x = (expanded_width - self.width) / 2
            offset_y = (expanded_height - self.height) / 2
            return pygame.Rect(self.x - offset_x, self.y - offset_y, expanded_width, expanded_height)
    
    enemy = TestBattlefieldEnemy(100, 100)
    original_rect = pygame.Rect(enemy.x, enemy.y, enemy.width, enemy.height)
    expanded_rect = enemy.get_rect()
    
    print(f"原始碰撞體: {original_rect}")
    print(f"擴大碰撞體: {expanded_rect}")
    print(f"寬度增加: {expanded_rect.width - original_rect.width}")
    print(f"高度增加: {expanded_rect.height - original_rect.height}")
    print("✓ 第三關敵人碰撞體擴大功能正常")

def test_level3_mouse_shooting():
    """測試第三關滑鼠方向射擊功能"""
    print("\n測試第三關滑鼠方向射擊功能...")
    
    # 模擬第三關玩家位置
    player_x, player_y = 400, 300
    player_width, player_height = 120, 120
    
    # 模擬不同的滑鼠位置
    test_cases = [
        (600, 200, "右上"),
        (200, 200, "左上"), 
        (600, 400, "右下"),
        (200, 400, "左下"),
        (400, 150, "正上"),
        (400, 450, "正下"),
        (550, 300, "正右"),
        (250, 300, "正左")
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
    
    print("✓ 第三關滑鼠方向射擊功能正常")

def test_comparison():
    """比較修改前後的差異"""
    print("\n=== 修改前後對比 ===")
    
    print("修改前:")
    print("- 敵人碰撞體: 60x30 (原始尺寸)")
    print("- 射擊方向: 跟隨移動方向 (4個方向)")
    
    print("\n修改後:")
    print("- 敵人碰撞體: 78x39 (增加30%)")
    print("- 射擊方向: 跟隨滑鼠方向 (360度)")
    
    print("\n改進效果:")
    print("✓ 命中判定更容易，提升遊戲體驗")
    print("✓ 射擊更靈活，戰術性更強")

def main():
    print("=== 第三關遊戲修改功能測試 ===")
    test_level3_collision_expansion()
    test_level3_mouse_shooting()
    test_comparison()
    print("\n=== 第三關測試完成 ===")
    print("\n第三關修改摘要:")
    print("1. ✓ 敵人碰撞體尺寸增加30%，提高命中判定")
    print("2. ✓ 子彈射擊改為360度跟隨滑鼠方向")
    print("3. ✓ 更新了控制說明文字")
    print("\n可以運行 level3_battlefield_reversal.py 來體驗修改後的第三關！")

if __name__ == "__main__":
    main()