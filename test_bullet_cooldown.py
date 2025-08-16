#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
測試第三關普通子彈冷卻系統
"""

import pygame
import sys
import os

# 添加當前目錄到路徑
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from level3_battlefield_reversal import BattlefieldPlayer, PlayerBullet

def test_bullet_cooldown_system():
    """測試子彈冷卻系統"""
    pygame.init()
    
    # 創建玩家
    player = BattlefieldPlayer(100, 100)
    player_bullets = []
    
    print("=== 測試普通子彈冷卻系統 ===")
    print(f"初始狀態:")
    print(f"  已發射子彈數: {player.normal_bullets_fired}")
    print(f"  最大子彈數: {player.max_normal_bullets}")
    print(f"  重新裝彈冷卻: {player.reload_cooldown}")
    print(f"  射擊冷卻: {player.shoot_cooldown}")
    
    # 模擬按鍵狀態 - 創建一個模擬的按鍵狀態字典
    class MockKeys:
        def __init__(self):
            self.space_pressed = False
            
        def __getitem__(self, key):
            if key == pygame.K_SPACE:
                return self.space_pressed
            return False  # 其他按鍵都返回False
    
    keys = MockKeys()
    
    # 測試連續射擊6發子彈
    print("\n=== 測試連續射擊 ===")
    for i in range(8):  # 嘗試射擊8次，但只能射6發
        # 重置射擊冷卻以便連續測試
        player.shoot_cooldown = 0
        keys.space_pressed = True
        
        bullets_before = len(player_bullets)
        player.update(keys, False, player_bullets, None)
        bullets_after = len(player_bullets)
        
        if bullets_after > bullets_before:
            print(f"第{i+1}次射擊成功:")
            print(f"  已發射子彈數: {player.normal_bullets_fired}")
            print(f"  剩餘子彈數: {player.max_normal_bullets - player.normal_bullets_fired}")
            print(f"  重新裝彈冷卻: {player.reload_cooldown}")
        else:
            print(f"第{i+1}次射擊失敗 (可能正在重新裝彈)")
            print(f"  已發射子彈數: {player.normal_bullets_fired}")
            print(f"  重新裝彈冷卻: {player.reload_cooldown}")
    
    # 測試重新裝彈過程
    print("\n=== 測試重新裝彈過程 ===")
    reload_frames = 0
    keys.space_pressed = False  # 重新裝彈時不按空白鍵
    while player.reload_cooldown > 0:
        player.update(keys, False, player_bullets, None)
        reload_frames += 1
        if reload_frames % 30 == 0:  # 每30幀顯示一次進度
            progress = (player.reload_time - player.reload_cooldown) / player.reload_time * 100
            print(f"重新裝彈進度: {progress:.1f}% (剩餘: {player.reload_cooldown} 幀)")
    
    print(f"\n重新裝彈完成!")
    print(f"  已發射子彈數: {player.normal_bullets_fired}")
    print(f"  剩餘子彈數: {player.max_normal_bullets - player.normal_bullets_fired}")
    print(f"  重新裝彈冷卻: {player.reload_cooldown}")
    print(f"  總重新裝彈時間: {reload_frames} 幀 ({reload_frames/60:.1f} 秒)")
    
    # 測試重新裝彈後能否正常射擊
    print("\n=== 測試重新裝彈後射擊 ===")
    player.shoot_cooldown = 0
    keys.space_pressed = True
    bullets_before = len(player_bullets)
    player.update(keys, False, player_bullets, None)
    bullets_after = len(player_bullets)
    
    if bullets_after > bullets_before:
        print("重新裝彈後射擊成功!")
        print(f"  已發射子彈數: {player.normal_bullets_fired}")
        print(f"  剩餘子彈數: {player.max_normal_bullets - player.normal_bullets_fired}")
    else:
        print("重新裝彈後射擊失敗!")
    
    pygame.quit()
    print("\n=== 測試完成 ===")

if __name__ == "__main__":
    test_bullet_cooldown_system()