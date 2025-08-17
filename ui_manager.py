# UI管理器
import pygame
from config import WHITE, SCREEN_WIDTH, SCREEN_HEIGHT

class UIManager:
    """UI管理器"""
    
    def __init__(self):
        from config import get_fonts
        self.fonts = get_fonts()
    
    def draw_health_bar(self, screen, player):
        """繪製健康條"""
        bar_width = 200
        bar_height = 20
        bar_x = SCREEN_WIDTH - bar_width - 20
        bar_y = SCREEN_HEIGHT - bar_height - 60
        
        # 背景條
        pygame.draw.rect(screen, (100, 0, 0), (bar_x, bar_y, bar_width, bar_height))
        
        # 前景條
        health_percentage = player.health / player.max_health
        health_width = int(bar_width * health_percentage)
        
        # 根據生命值改變顏色
        if health_percentage > 0.6:
            health_color = (0, 255, 0)
        elif health_percentage > 0.3:
            health_color = (255, 255, 0)
        else:
            health_color = (255, 0, 0)
            
        pygame.draw.rect(screen, health_color, (bar_x, bar_y, health_width, bar_height))
        
        # 邊框
        pygame.draw.rect(screen, WHITE, (bar_x, bar_y, bar_width, bar_height), 2)
        
        # HP 文字
        hp_text = self.fonts['ui'].render(f"HP: {player.health}", True, WHITE)
        screen.blit(hp_text, (bar_x, bar_y - 30))
    
    def draw_level_progress(self, screen, current_level, buildings=None, prisoners=None):
        """繪製關卡進度"""
        if current_level == 1 and buildings:
            active_count = sum(1 for building in buildings if building.is_active)
            progress_text = self.fonts['ui'].render(f"巡邏進度: {active_count} / {len(buildings)}", True, WHITE)
            screen.blit(progress_text, (20, 20))
        elif current_level == 2 and prisoners is not None:
            enemies_left = len(prisoners)
            progress_text = self.fonts['ui'].render(f"剩餘囚犯: {enemies_left}", True, WHITE)
            screen.blit(progress_text, (20, 20))
    
    def draw_weapon_status(self, screen, player):
        """繪製武器狀態"""
        if player.has_gun:
            weapon_text = self.fonts['ui'].render("武器: 突擊步槍 [空白鍵射擊]", True, WHITE)
            screen.blit(weapon_text, (20, 70))
        else:
            weapon_text = self.fonts['ui'].render("尋找武器！", True, (255, 255, 0))
            screen.blit(weapon_text, (20, 70))
    
    def draw_level_transition(self, screen):
        """繪製關卡轉換畫面"""
        transition_bg = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        transition_bg.fill((0, 0, 0, 150))
        screen.blit(transition_bg, (0, 0))
        
        transition_text1 = self.fonts['transition'].render("LEVEL 1 CLEARED!", True, (0, 255, 0))
        transition_text2 = self.fonts['transition'].render("ENTERING PRISON COMPLEX...", True, WHITE)
        
        text_rect1 = transition_text1.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
        text_rect2 = transition_text2.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
        
        screen.blit(transition_text1, text_rect1)
        screen.blit(transition_text2, text_rect2)
    
    def draw_victory_screen(self, screen, current_level):
        """繪製勝利畫面"""
        if current_level == 2:
            victory_text = self.fonts['victory'].render("LEVEL 2 CLEARED!", True, (0, 255, 0))
            victory_text2 = self.fonts['ui'].render("按 ENTER 進入第三關：逆轉戰場", True, WHITE)
        else:
            victory_text = self.fonts['victory'].render("城市巡邏完成！", True, WHITE)
            victory_text2 = None
            
        text_rect = victory_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        
        # 勝利背景
        victory_bg = pygame.Surface((text_rect.width + 40, text_rect.height + 20), pygame.SRCALPHA)
        victory_bg.fill((0, 0, 0, 180))
        screen.blit(victory_bg, (text_rect.x - 20, text_rect.y - 10))
        
        screen.blit(victory_text, text_rect)
        
        if victory_text2:
            text_rect2 = victory_text2.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100))
            screen.blit(victory_text2, text_rect2)
    
    def draw_defeat_screen(self, screen):
        """繪製失敗畫面"""
        defeat_text = self.fonts['defeat'].render("任務失敗！車輛損毀！", True, (255, 0, 0))
        text_rect = defeat_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        
        # 失敗背景
        defeat_bg = pygame.Surface((text_rect.width + 40, text_rect.height + 20), pygame.SRCALPHA)
        defeat_bg.fill((0, 0, 0, 200))
        screen.blit(defeat_bg, (text_rect.x - 20, text_rect.y - 10))
        
        screen.blit(defeat_text, text_rect)