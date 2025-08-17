# 重構後的城市守護者遊戲
import pygame
import sys
import time
import subprocess

# 導入重構後的模組
from config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS
from game_state import GameState
from player import Player
from transformation_system import TransformationSystem
from level_manager import LevelManager
from background_renderer import BackgroundRenderer
from ui_manager import UIManager
from bullet_system import Bullet, PlayerBullet

class GameManager:
    """遊戲管理器 - 統一管理遊戲邏輯"""
    
    def __init__(self):
        # 初始化 Pygame
        pygame.init()
        
        # 創建遊戲視窗
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("城市守護者：精確巡邏 (重構版)")
        self.clock = pygame.time.Clock()
        
        # 遊戲狀態
        self.game_state = GameState()
        
        # 遊戲物件
        self.player = Player(100, SCREEN_HEIGHT // 2 - 15)
        self.transformation_system = TransformationSystem()
        
        # 管理器
        self.ui_manager = UIManager()
        
        # 遊戲物件列表
        self.buildings = []
        self.enemies = []
        self.prisoners = []
        self.weapon_pickups = []
        self.bullets = []
        self.player_bullets = []
        
        # 載入第一關
        self._load_current_level()
        
        # 時間管理
        self.last_time = time.time()
    
    def _load_current_level(self):
        """載入當前關卡"""
        self.buildings, self.enemies, self.prisoners, self.weapon_pickups = \
            LevelManager.load_level(self.game_state.current_level, self.player)
        
        # 清空子彈
        self.bullets.clear()
        self.player_bullets.clear()
    
    def handle_events(self):
        """處理事件"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            # 處理變身系統輸入
            self.transformation_system.handle_input(event)
            
            # 處理遊戲勝利後進入第三關
            if (event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN and 
                self.game_state.game_won and self.game_state.current_level == 2):
                pygame.quit()
                subprocess.run([sys.executable, "level3_battlefield_reversal.py"])
                return False
        
        return True
    
    def update_game_logic(self, dt):
        """更新遊戲邏輯"""
        # 檢查失敗條件
        if self.player.health <= 0:
            self.game_state.set_defeat()
        
        # 處理關卡轉換
        if self.game_state.update_transition():
            self._load_current_level()
        
        # 檢查是否需要暫停遊戲
        self.game_state.set_paused(self.transformation_system.is_paused())
        
        # 只有在遊戲應該更新時才執行邏輯
        if not self.game_state.should_update_game():
            return
        
        # 更新變身系統
        self.transformation_system.update(dt)
        
        # 獲取按鍵狀態
        keys = pygame.key.get_pressed()
        
        # 更新玩家
        self.player.update(keys, self.game_state.is_game_over(), 
                          self.player_bullets, self.transformation_system)
        
        # 更新遊戲物件
        self._update_enemies()
        self._update_prisoners()
        self._update_weapon_pickups()
        self._update_bullets()
        
        # 檢查碰撞
        self._check_collisions()
        
        # 檢查勝利條件
        self._check_victory_conditions()
    
    def _update_enemies(self):
        """更新敵人"""
        for enemy in self.enemies:
            enemy.update(self.player, self.bullets, self.game_state.is_game_over())
    
    def _update_prisoners(self):
        """更新囚犯"""
        for prisoner in self.prisoners[:]:
            prisoner.update(self.player, self.game_state.is_game_over())
            
            # 檢查囚犯與玩家的碰撞
            if prisoner.get_rect().colliderect(self.player.get_rect()):
                self.player.take_damage(5)
    
    def _update_weapon_pickups(self):
        """更新武器拾取點"""
        for weapon in self.weapon_pickups[:]:
            weapon.update()
            if weapon.get_rect().colliderect(self.player.get_rect()):
                self.player.has_gun = True
                self.weapon_pickups.remove(weapon)
    
    def _update_bullets(self):
        """更新子彈"""
        # 更新敵人子彈
        for bullet in self.bullets[:]:
            bullet.update()
            if bullet.is_off_screen():
                self.bullets.remove(bullet)
        
        # 更新玩家子彈
        for bullet in self.player_bullets[:]:
            bullet.update()
            if bullet.is_off_screen():
                self.player_bullets.remove(bullet)
    
    def _check_collisions(self):
        """檢查碰撞"""
        player_rect = self.player.get_rect()
        
        # 檢查敵人子彈與玩家的碰撞
        for bullet in self.bullets[:]:
            if player_rect.colliderect(bullet.get_rect()):
                self.player.take_damage(5)
                self.bullets.remove(bullet)
        
        # 檢查玩家子彈與囚犯的碰撞
        for bullet in self.player_bullets[:]:
            for prisoner in self.prisoners[:]:
                if bullet.get_rect().colliderect(prisoner.get_rect()):
                    prisoner.take_damage(30)
                    self.player_bullets.remove(bullet)
                    if prisoner.health <= 0:
                        self.prisoners.remove(prisoner)
                    break
        
        # 檢查玩家與建築物的碰撞（第一關）
        if self.game_state.current_level == 1:
            for building in self.buildings:
                if not building.is_active and player_rect.colliderect(building.rect):
                    building.is_active = True
    
    def _check_victory_conditions(self):
        """檢查勝利條件"""
        if self.game_state.current_level == 1:
            # 第一關：所有建築物都被啟動
            active_count = sum(1 for building in self.buildings if building.is_active)
            if active_count == len(self.buildings):
                self.game_state.start_level_transition()
        
        elif self.game_state.current_level == 2:
            # 第二關：所有囚犯都被消滅
            if len(self.prisoners) == 0:
                self.game_state.set_victory()
    
    def render(self):
        """渲染畫面"""
        # 繪製背景
        if self.game_state.current_level == 1:
            BackgroundRenderer.draw_level1(self.screen)
        elif self.game_state.current_level == 2:
            BackgroundRenderer.draw_level2(self.screen)
        
        # 繪製遊戲物件
        self._render_game_objects()
        
        # 繪製UI
        self._render_ui()
        
        # 更新顯示
        pygame.display.flip()
    
    def _render_game_objects(self):
        """渲染遊戲物件"""
        # 繪製建築物
        for building in self.buildings:
            building.draw(self.screen)
        
        # 繪製敵人
        for enemy in self.enemies:
            enemy.draw(self.screen, self.player)
        
        # 繪製囚犯
        for prisoner in self.prisoners:
            prisoner.draw(self.screen)
        
        # 繪製武器拾取點
        for weapon in self.weapon_pickups:
            weapon.draw(self.screen)
        
        # 繪製子彈
        for bullet in self.bullets:
            bullet.draw(self.screen)
        
        for bullet in self.player_bullets:
            bullet.draw(self.screen)
        
        # 繪製玩家
        self.player.draw(self.screen)
    
    def _render_ui(self):
        """渲染UI"""
        # 繪製關卡進度
        self.ui_manager.draw_level_progress(self.screen, self.game_state.current_level, 
                                           self.buildings, self.prisoners)
        
        # 繪製武器狀態（第二關）
        if self.game_state.current_level == 2:
            self.ui_manager.draw_weapon_status(self.screen, self.player)
        
        # 繪製健康條
        self.ui_manager.draw_health_bar(self.screen, self.player)
        
        # 繪製變身系統UI
        self.transformation_system.draw_ui(self.screen)
        
        # 繪製遊戲狀態畫面
        if self.game_state.level_transition:
            self.ui_manager.draw_level_transition(self.screen)
        elif self.game_state.game_won:
            self.ui_manager.draw_victory_screen(self.screen, self.game_state.current_level)
        elif self.game_state.game_lost:
            self.ui_manager.draw_defeat_screen(self.screen)
    
    def run(self):
        """主遊戲迴圈"""
        running = True
        
        while running:
            # 計算時間差
            current_time = time.time()
            dt = current_time - self.last_time
            self.last_time = current_time
            
            # 處理事件
            running = self.handle_events()
            if not running:
                break
            
            # 更新遊戲邏輯
            self.update_game_logic(dt)
            
            # 渲染畫面
            self.render()
            
            # 控制幀率
            self.clock.tick(FPS)
        
        # 退出遊戲
        pygame.quit()
        sys.exit()


def main():
    """主函數"""
    game = GameManager()
    game.run()


if __name__ == "__main__":
    main()