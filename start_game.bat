@echo off
echo 🎮 啟動城市守護者遊戲...
echo ================================

python city_patrol_game_refactored.py

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ❌ 遊戲啟動失敗！
    echo 請確保已安裝 Python 和 Pygame
    echo.
    echo 安裝指令：
    echo pip install pygame
    echo.
    pause
) else (
    echo.
    echo ✅ 遊戲正常結束
)

pause