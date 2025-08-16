#!/usr/bin/env python3
"""
測試等離子子彈功能
"""

import pygame
import sys
import math
import random

# 導入等離子子彈類
from level3_battlefield_reversal import UnstablePlasmaBolt

# 初始化 Pygame
pygame.init()

# 遊戲設定
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

def main():
    # 創建遊戲視窗
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("等離子子彈測試")
    clock = pygame.time.Clock()
    
    # 創建字體
    font = pygame.font.Font(None, 36)
    
    # 創建等離子子彈列表
    plasma_bullets = []
    
    # 遊戲主循環
    running = True
    
    while running:
        # 處理事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # 滑鼠點擊時創建等離子子彈
                mouse_x, mouse_y = pygame.mouse.get_pos()
                center_x, center_y = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
                
                # 計算方向
                dx = mouse_x - center_x
                dy = mouse_y - center_y
                distance = math.sqrt(dx*dx + dy*dy)
                
                if distance > 0:
                    bullet_speed = 8
                    bullet_dx = (dx / distance) * bullet_speed
                    bullet_dy = (dy / distance) * bullet_speed
                    
                    # 創建等離子子彈
                    plasma_bullets.append(UnstablePlasmaBolt(center_x, center_y, bullet_dx, bullet_dy))
        
        # 更新等離子子彈
        for bullet in plasma_bullets[:]:
            bullet.update()
            if bullet.is_off_screen():
                plasma_bullets.remove(bullet)
        
        # 繪製遊戲畫面
        screen.fill(BLACK)
        
        # 繪製中心點
        pygame.draw.circle(screen, WHITE, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), 10)
        
        # 繪製等離子子彈
        for bullet in plasma_bullets:
            bullet.draw(screen)
        
        # 繪製說明文字
        info_text = font.render("點擊滑鼠發射等離子子彈", True, WHITE)
        screen.blit(info_text, (10, 10))
        
        count_text = font.render(f"等離子子彈數量: {len(plasma_bullets)}", True, WHITE)
        screen.blit(count_text, (10, 50))
        
        # 更新顯示
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()