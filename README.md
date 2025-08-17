# 城市守護者：精確巡邏 (重構版)

一個使用 Python 和 Pygame 開發的 2D 動作遊戲，經過完整重構，採用模組化架構設計。

## 🎮 遊戲特色

- **雙關卡設計**: 城市巡邏 + 監獄突破
- **變身系統**: 通過英文單字輸入獲得特殊能力
- **戰鬥系統**: 射擊、躲避、策略性戰鬥
- **模組化架構**: 易於維護和擴展的程式碼結構

## 🚀 快速開始

### 系統需求
- Python 3.7+
- Pygame 2.0+

### 安裝依賴
```bash
pip install pygame
```

### 執行遊戲
```bash
python city_patrol_game_refactored.py
```

### 執行測試
```bash
python tests/test_refactored_game.py
```

## 📁 專案結構

```
城市守護者遊戲/
├── city_patrol_game_refactored.py  # 主遊戲檔案
├── config.py                       # 遊戲配置
├── game_state.py                   # 狀態管理
├── player.py                       # 玩家邏輯
├── player_renderer.py              # 玩家渲染
├── enemy_system.py                 # 敵人系統
├── transformation_system.py        # 變身系統
├── game_objects.py                 # 遊戲物件
├── bullet_system.py                # 子彈系統
├── level_manager.py                # 關卡管理
├── background_renderer.py          # 背景渲染
├── ui_manager.py                   # UI管理
├── docs/                           # 文檔資料夾
│   ├── BEFORE_AFTER_COMPARISON.md  # 重構前後對比
│   └── REFACTORING_SUMMARY.md      # 重構總結
├── tests/                          # 測試資料夾
│   └── test_refactored_game.py     # 遊戲測試
├── archive/                        # 歷史版本
│   ├── city_patrol_game_0721_pm10.py  # 原始版本
│   └── ...                         # 其他歷史檔案
└── OLD/                            # 舊版本檔案
    └── ...
```

## 🎯 遊戲玩法

### 第一關：城市巡邏
- **目標**: 巡邏所有建築物（學校、公園、辦公室、社區、軍事基地）
- **操作**: 使用方向鍵移動，接觸建築物完成巡邏
- **敵人**: 避開或消滅路上的敵人

### 第二關：監獄突破
- **目標**: 消滅所有逃脫的囚犯
- **操作**: 拾取武器，使用空白鍵射擊
- **策略**: 合理利用變身系統增強戰鬥力

### 變身系統
- 按下 `T` 鍵啟動變身系統
- 根據提示輸入英文單字
- 成功變身獲得特殊能力和外觀

## 🏗️ 架構設計

### 核心原則
- **單一責任原則**: 每個模組只負責一個功能
- **開放封閉原則**: 易於擴展新功能
- **依賴倒置原則**: 高層模組不依賴低層模組
- **介面隔離原則**: 模組間介面簡潔明確

### 設計模式
- **MVC模式**: 分離模型、視圖、控制器
- **策略模式**: 敵人行為和渲染策略
- **工廠模式**: 關卡和物件創建
- **狀態模式**: 遊戲狀態管理

## 🔧 開發指南

### 添加新關卡
1. 在 `level_manager.py` 中添加新的關卡載入方法
2. 在 `background_renderer.py` 中添加對應的背景渲染
3. 更新 `game_state.py` 中的關卡轉換邏輯

### 添加新敵人類型
1. 在 `config.py` 中定義敵人配置
2. 在 `enemy_system.py` 中實現敵人邏輯和渲染
3. 在關卡管理器中使用新敵人類型

### 添加新變身形態
1. 在 `config.py` 中添加變身配置
2. 在 `transformation_system.py` 中實現變身邏輯
3. 在 `player_renderer.py` 中添加對應的渲染效果

## 📊 重構成果

- **程式碼行數**: 從 2116 行減少到平均每個模組 150 行
- **檔案數量**: 從 1 個檔案分解為 12 個模組
- **程式碼重複**: 從 30% 降低到 <5%
- **維護性**: 大幅提升，每個功能都有獨立模組

## 🤝 貢獻指南

1. Fork 專案
2. 創建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 開啟 Pull Request

## 📄 授權

此專案採用 MIT 授權 - 詳見 [LICENSE](LICENSE) 檔案

## 🙏 致謝

感謝所有為這個專案做出貢獻的開發者和測試者。

---

**享受遊戲！** 🎮✨