# 關卡管理器
from game_objects import Building, Prisoner, WeaponPickup
from enemy_system import Enemy
from config import SCREEN_HEIGHT, SCREEN_WIDTH

class LevelManager:
    """關卡管理器"""
    
    @staticmethod
    def load_level(level_number, player):
        """載入指定關卡"""
        if level_number == 1:
            return LevelManager._load_level_1(player)
        elif level_number == 2:
            return LevelManager._load_level_2(player)
        else:
            return [], [], [], []
    
    @staticmethod
    def _load_level_1(player):
        """載入第一關：城市巡邏"""
        buildings = [
            Building(200, 100, "School"),
            Building(600, 150, "Park"),
            Building(1200, 50, "Office"),
            Building(300, 700, "Community"),
            Building(1400, 650, "Military")
        ]
        
        enemies = [
            Enemy(800, 300, "big"),
            Enemy(800, 400, "normal"),
            Enemy(700, 300, "normal"),
            Enemy(900, 300, "normal"),
            Enemy(800, 1100, "normal"),
            Enemy(1500, 800, "normal")
        ]
        
        prisoners = []
        weapon_pickups = []
        
        # 重置玩家位置和狀態
        player.x = 100
        player.y = SCREEN_HEIGHT // 2 - 15
        player.health = 100
        player.has_gun = False
        
        return buildings, enemies, prisoners, weapon_pickups
    
    @staticmethod
    def _load_level_2(player):
        """載入第二關：監獄突破"""
        buildings = [
            Building(400, 100, "School"),
        ]
        
        enemies = [
            Enemy(800, 400, "normal")
        ]
        
        # 創建囚犯
        prisoners = [
            Prisoner(200, 150),
            Prisoner(400, 200),
            Prisoner(600, 180),
            Prisoner(800, 220),
            Prisoner(500, 850),
            Prisoner(700, 820),
        ]
        
        # 創建武器拾取點
        weapon_pickups = [
            WeaponPickup(SCREEN_WIDTH // 2 - 20, SCREEN_HEIGHT // 2)
        ]
        
        # 重置玩家位置和狀態
        player.x = SCREEN_WIDTH // 2 - 30
        player.y = SCREEN_HEIGHT - 100
        player.health = 100
        player.has_gun = False
        
        return buildings, enemies, prisoners, weapon_pickups