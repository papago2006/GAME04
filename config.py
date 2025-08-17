# 遊戲配置文件
import pygame

# 螢幕設定
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080

# 遊戲設定
PLAYER_SPEED = 7
FPS = 60

# 顏色定義
GRASS_GREEN = (50, 150, 50)
ROAD_GRAY = (100, 100, 100)
SIDEWALK_GRAY = (180, 180, 180)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# 敵人配置
ENEMY_CONFIGS = {
    "normal": {
        "width": 40,
        "height": 40,
        "speed": 3,
        "health": 50,
        "attack_cooldown": 120,
        "attack_range": 800
    },
    "big": {
        "width": 120,
        "height": 120,
        "speed": 5,
        "health": 100,
        "attack_cooldown": 120,
        "attack_range": 800
    },
    "brute": {
        "width": 56,
        "height": 56,
        "speed": 2.1,
        "health": 100,
        "attack_cooldown": 180,
        "attack_range": 600
    },
    "rusher": {
        "width": 28,
        "height": 28,
        "speed": 4.5,
        "health": 30,
        "attack_cooldown": 60,
        "attack_range": 1000
    }
}

# 字體設定
def get_fonts():
    try:
        return {
            'ui': pygame.font.Font("C:\\Windows\\Fonts\\simsun.ttc", 50),
            'victory': pygame.font.Font("C:\\Windows\\Fonts\\simsun.ttc", 120),
            'defeat': pygame.font.Font("C:\\Windows\\Fonts\\simsun.ttc", 120),
            'transition': pygame.font.Font("C:\\Windows\\Fonts\\simsun.ttc", 80),
            'small': pygame.font.Font("C:\\Windows\\Fonts\\simsun.ttc", 36),
            'big': pygame.font.Font("C:\\Windows\\Fonts\\simsun.ttc", 48)
        }
    except:
        return {
            'ui': pygame.font.Font(None, 50),
            'victory': pygame.font.Font(None, 120),
            'defeat': pygame.font.Font(None, 120),
            'transition': pygame.font.Font(None, 80),
            'small': pygame.font.Font(None, 36),
            'big': pygame.font.Font(None, 48)
        }

# 變身系統配置
TRANSFORMATION_CONFIG = {
    "timer": 10.0,
    "duration": 15.0,
    "required_answers": 2
}