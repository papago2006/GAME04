# 測試重構後的遊戲
import pygame
import sys
import os

# 添加父目錄到路徑，以便導入模組
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_imports():
    """測試所有模組是否能正確導入"""
    try:
        from config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, ENEMY_CONFIGS
        from game_state import GameState
        from player import Player
        from transformation_system import TransformationSystem, WordBank, TransformationLogic, TransformationUI
        from level_manager import LevelManager
        from background_renderer import BackgroundRenderer
        from ui_manager import UIManager
        from bullet_system import Bullet, PlayerBullet
        from enemy_system import Enemy, StandardEnemyRenderer, BigEnemyRenderer
        from game_objects import Building, Prisoner, WeaponPickup
        from player_renderer import PlayerRenderer
        
        print("✅ 所有模組導入成功")
        return True
    except ImportError as e:
        print(f"❌ 模組導入失敗: {e}")
        return False

def test_game_initialization():
    """測試遊戲初始化"""
    try:
        pygame.init()
        from city_patrol_game_refactored import GameManager
        
        game = GameManager()
        print("✅ 遊戲初始化成功")
        
        # 測試基本屬性
        assert game.game_state.current_level == 1
        assert game.player.health == 100
        assert len(game.buildings) > 0
        
        pygame.quit()
        return True
    except Exception as e:
        print(f"❌ 遊戲初始化失敗: {e}")
        return False

def test_level_loading():
    """測試關卡載入"""
    try:
        from level_manager import LevelManager
        from player import Player
        
        player = Player(100, 100)
        
        # 測試第一關
        buildings, enemies, prisoners, weapons = LevelManager.load_level(1, player)
        assert len(buildings) > 0
        assert len(enemies) > 0
        print("✅ 第一關載入成功")
        
        # 測試第二關
        buildings, enemies, prisoners, weapons = LevelManager.load_level(2, player)
        assert len(prisoners) > 0
        assert len(weapons) > 0
        print("✅ 第二關載入成功")
        
        return True
    except Exception as e:
        print(f"❌ 關卡載入測試失敗: {e}")
        return False

def run_all_tests():
    """執行所有測試"""
    print("🧪 開始執行重構版本測試...")
    print("=" * 50)
    
    tests = [
        ("模組導入測試", test_imports),
        ("遊戲初始化測試", test_game_initialization),
        ("關卡載入測試", test_level_loading),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🔍 執行 {test_name}...")
        if test_func():
            passed += 1
        else:
            print(f"❌ {test_name} 失敗")
    
    print("\n" + "=" * 50)
    print(f"📊 測試結果: {passed}/{total} 通過")
    
    if passed == total:
        print("🎉 所有測試通過！重構版本運行正常。")
    else:
        print("⚠️  部分測試失敗，請檢查相關模組。")
    
    return passed == total

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)