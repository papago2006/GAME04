#!/usr/bin/env python3
"""
城市守護者遊戲啟動器
簡化的遊戲啟動腳本
"""

import sys
import os

def main():
    """啟動遊戲"""
    try:
        print("🎮 啟動城市守護者：精確巡邏 (重構版)")
        print("=" * 50)
        
        # 導入並啟動遊戲
        from city_patrol_game_refactored import main as game_main
        game_main()
        
    except ImportError as e:
        print(f"❌ 模組導入錯誤: {e}")
        print("請確保所有必要的檔案都在同一目錄下")
        sys.exit(1)
    except Exception as e:
        print(f"❌ 遊戲啟動失敗: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()