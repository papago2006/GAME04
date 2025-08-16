import pygame
import sys
import math

# 初始化 Pygame
pygame.init()

# 遊戲設定
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
BACKGROUND_COLOR = (15, 20, 40)  # 深邃的星空藍
PLAYER_SPEED = 7

# 顏色定義
LIGHT_BLUE = (173, 216, 230)  # 淡藍色
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
PURPLE = (128, 0, 128)  # 暗紫色
MAGENTA = (255, 0, 255)  # 洋紅色
YELLOW = (255, 255, 0)
SHADOW_GRAY = (50, 50, 50, 100)  # 半透明深灰色

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 50
        self.height = 50
        self.speed = PLAYER_SPEED
        
    def update(self, keys):
        # 處理鍵盤輸入
        if keys[pygame.K_LEFT] and self.x > 0:
            self.x -= self.speed
        if keys[pygame.K_RIGHT] and self.x < SCREEN_WIDTH - self.width:
            self.x += self.speed
        if keys[pygame.K_UP] and self.y > 0:
            self.y -= self.speed
        if keys[pygame.K_DOWN] and self.y < SCREEN_HEIGHT - self.height:
            self.y += self.speed
    
    def draw(self, screen):
        # 繪製影子（漂浮效果）
        shadow_surface = pygame.Surface((self.width + 10, 15), pygame.SRCALPHA)
        pygame.draw.ellipse(shadow_surface, SHADOW_GRAY, (0, 0, self.width + 10, 15))
        screen.blit(shadow_surface, (self.x - 5, self.y + self.height + 5))
        
        # 繪製身體（圓角矩形）
        body_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(screen, LIGHT_BLUE, body_rect, border_radius=10)
        
        # 繪製眼睛
        eye_radius = 8
        left_eye_pos = (self.x + 15, self.y + 15)
        right_eye_pos = (self.x + 35, self.y + 15)
        
        # 白色眼圈
        pygame.draw.circle(screen, WHITE, left_eye_pos, eye_radius)
        pygame.draw.circle(screen, WHITE, right_eye_pos, eye_radius)
        
        # 黑色眼珠
        pygame.draw.circle(screen, BLACK, left_eye_pos, eye_radius // 2)
        pygame.draw.circle(screen, BLACK, right_eye_pos, eye_radius // 2)
    
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

class Checkpoint:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 80
        self.height = 80
        self.is_active = False
        self.particle_timer = 0
        
    def draw(self, screen):
        # 繪製底座（圓角矩形）
        base_rect = pygame.Rect(self.x, self.y + 40, self.width, 40)
        pygame.draw.rect(screen, GRAY, base_rect, border_radius=5)
        
        # 繪製水晶（多邊形）
        crystal_center_x = self.x + self.width // 2
        crystal_center_y = self.y + 30
        
        # 水晶的多邊形點
        crystal_points = [
            (crystal_center_x, self.y),  # 頂點
            (crystal_center_x - 20, crystal_center_y),  # 左中
            (crystal_center_x - 15, crystal_center_y + 20),  # 左下
            (crystal_center_x + 15, crystal_center_y + 20),  # 右下
            (crystal_center_x + 20, crystal_center_y),  # 右中
        ]
        
        if self.is_active:
            # 已啟動：明亮的洋紅色水晶
            pygame.draw.polygon(screen, MAGENTA, crystal_points)
            
            # 繪製光芒粒子效果
            self.particle_timer += 1
            for i in range(8):
                angle = (i * 45 + self.particle_timer * 2) % 360
                particle_x = crystal_center_x + math.cos(math.radians(angle)) * 35
                particle_y = crystal_center_y + math.sin(math.radians(angle)) * 25
                pygame.draw.circle(screen, YELLOW, (int(particle_x), int(particle_y)), 3)
        else:
            # 未啟動：暗淡的紫色水晶
            pygame.draw.polygon(screen, PURPLE, crystal_points)
    
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

def main():
    # 創建遊戲視窗
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("漂浮精靈的巡邏任務")
    clock = pygame.time.Clock()
    
    # 創建字體
    font_ui = pygame.font.Font(None, 50)
    font_victory = pygame.font.Font(None, 120)
    
    # 創建玩家
    player = Player(100, 100)
    
    # 創建檢查點
    checkpoint_positions = [(250, 250), (1670, 180), (350, 850), (1550, 900), (960, 540)]
    checkpoints = [Checkpoint(x, y) for x, y in checkpoint_positions]
    
    # 遊戲狀態
    game_won = False
    
    # 遊戲主迴圈
    running = True
    while running:
        # 處理事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # 獲取按鍵狀態
        keys = pygame.key.get_pressed()
        
        # 更新遊戲邏輯
        if not game_won:
            player.update(keys)
            
            # 檢查玩家與檢查點的碰撞
            player_rect = player.get_rect()
            for checkpoint in checkpoints:
                if not checkpoint.is_active and player_rect.colliderect(checkpoint.get_rect()):
                    checkpoint.is_active = True
            
            # 檢查勝利條件
            active_count = sum(1 for checkpoint in checkpoints if checkpoint.is_active)
            if active_count == len(checkpoints):
                game_won = True
        
        # 繪製畫面
        screen.fill(BACKGROUND_COLOR)
        
        # 繪製檢查點
        for checkpoint in checkpoints:
            checkpoint.draw(screen)
        
        # 繪製玩家
        player.draw(screen)
        
        # 繪製UI
        active_count = sum(1 for checkpoint in checkpoints if checkpoint.is_active)
        progress_text = font_ui.render(f"水晶能量: {active_count} / 5", True, WHITE)
        screen.blit(progress_text, (20, 20))
        
        # 繪製勝利畫面
        if game_won:
            victory_text = font_victory.render("巡邏完成！能量充滿！", True, WHITE)
            text_rect = victory_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            screen.blit(victory_text, text_rect)
        
        # 更新顯示
        pygame.display.flip()
        clock.tick(60)  # 60 FPS
    
    # 退出遊戲
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()