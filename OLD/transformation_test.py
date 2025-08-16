import pygame
import sys
import random
import math
import time

# 初始化 Pygame
pygame.init()

# 遊戲設定
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
PLAYER_SPEED = 7

# 顏色定義
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# 變身系統
class TransformationSystem:
    def __init__(self):
        self.word_bank = [
            {"word": "HERO", "hint": "A brave person who saves others"},
            {"word": "POWER", "hint": "Strength or energy"},
            {"word": "MAGIC", "hint": "Supernatural force"},
            {"word": "BRAVE", "hint": "Showing courage"},
            {"word": "LIGHT", "hint": "Brightness that defeats darkness"},
        ]
        self.timer = 10.0  # 縮短到10秒方便測試
        self.question_active = False
        self.current_question = None
        self.user_input = ""
        self.transformation_active = False
        self.transformation_duration = 8.0  # 變身持續8秒
        # 使用支持中文的字體
        try:
            self.font = pygame.font.Font("C:\\Windows\\Fonts\\simsun.ttc", 36)
            self.big_font = pygame.font.Font("C:\\Windows\\Fonts\\simsun.ttc", 48)
        except:
            # 如果無法加載中文字體，則使用默認字體
            self.font = pygame.font.Font(None, 36)
            self.big_font = pygame.font.Font(None, 48)
        
    def update(self, dt):
        if not self.question_active and not self.transformation_active:
            self.timer -= dt
            if self.timer <= 0:
                self.start_question()
        
        if self.transformation_active:
            self.transformation_duration -= dt
            if self.transformation_duration <= 0:
                self.end_transformation()
    
    def start_question(self):
        self.question_active = True
        self.current_question = random.choice(self.word_bank)
        self.user_input = ""
        
    def handle_input(self, event):
        if self.question_active and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                self.user_input = self.user_input[:-1]
            elif event.key == pygame.K_RETURN:
                if self.user_input.upper() == self.current_question["word"]:
                    self.start_transformation()
                else:
                    self.end_question()
            elif event.unicode.isalpha():
                self.user_input += event.unicode.upper()
    
    def start_transformation(self):
        self.question_active = False
        self.transformation_active = True
        self.transformation_duration = 8.0
        self.timer = 10.0
        
    def end_transformation(self):
        self.transformation_active = False
        self.timer = 10.0
        
    def end_question(self):
        self.question_active = False
        self.timer = 10.0
        
    def draw_ui(self, screen):
        # 繪製計時器
        if not self.question_active and not self.transformation_active:
            timer_text = f"Next Question: {int(self.timer)}s"
            text_surface = self.font.render(timer_text, True, BLACK)
            screen.blit(text_surface, (10, 10))
        
        # 繪製問題界面
        if self.question_active:
            # 半透明背景
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.set_alpha(128)
            overlay.fill(BLACK)
            screen.blit(overlay, (0, 0))
            
            # 問題框
            question_rect = pygame.Rect(SCREEN_WIDTH//4, SCREEN_HEIGHT//3, SCREEN_WIDTH//2, SCREEN_HEIGHT//3)
            pygame.draw.rect(screen, WHITE, question_rect)
            pygame.draw.rect(screen, BLACK, question_rect, 3)
            
            # 問題文字
            hint_text = self.big_font.render("Hint:", True, BLACK)
            screen.blit(hint_text, (question_rect.x + 20, question_rect.y + 20))
            
            hint_content = self.font.render(self.current_question["hint"], True, BLACK)
            screen.blit(hint_content, (question_rect.x + 20, question_rect.y + 60))
            
            # 輸入框
            input_text = self.big_font.render(f"Answer: {self.user_input}", True, BLACK)
            screen.blit(input_text, (question_rect.x + 20, question_rect.y + 120))
            
            # 指示文字
            instruction = self.font.render("Type your answer and press ENTER", True, BLACK)
            screen.blit(instruction, (question_rect.x + 20, question_rect.y + 180))
        
        # 變身狀態指示
        if self.transformation_active:
            transform_text = f"TRANSFORMED! {int(self.transformation_duration)}s left"
            text_surface = self.big_font.render(transform_text, True, (255, 215, 0))
            screen.blit(text_surface, (SCREEN_WIDTH//2 - 200, 50))

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 60
        self.height = 60
        self.speed = PLAYER_SPEED
        self.is_transformed = False
        self.bounce_timer = 0
        
    def update(self, keys, transformation_system=None):
        # 更新變身狀態
        if transformation_system:
            self.is_transformed = transformation_system.transformation_active
            
        # 更新可愛動畫計時器
        self.bounce_timer += 0.2
            
        # 變身狀態下速度加快
        current_speed = self.speed * 1.5 if self.is_transformed else self.speed
            
        if keys[pygame.K_LEFT] and self.x > 0:
            self.x -= current_speed
        if keys[pygame.K_RIGHT] and self.x < SCREEN_WIDTH - self.width:
            self.x += current_speed
        if keys[pygame.K_UP] and self.y > 0:
            self.y -= current_speed
        if keys[pygame.K_DOWN] and self.y < SCREEN_HEIGHT - self.height:
            self.y += current_speed
    
    def draw(self, screen):
        if self.is_transformed:
            self.draw_cute_form(screen)
        else:
            self.draw_normal_form(screen)
    
    def draw_cute_form(self, screen):
        """繪製可愛變身形態"""
        # 可愛彈跳效果
        bounce_offset = math.sin(self.bounce_timer) * 3
        
        # 可愛的顏色調色盤
        body_color = (255, 182, 193)  # 淺粉紅
        accent_color = (255, 105, 180)  # 熱粉紅
        eye_color = (0, 0, 0)  # 黑色眼睛
        
        center_x = self.x + self.width // 2
        center_y = self.y + self.height // 2 + bounce_offset
        
        # 1. 繪製可愛的大頭身比例
        head_radius = 35
        pygame.draw.circle(screen, body_color, (int(center_x), int(center_y - 10)), head_radius)
        pygame.draw.circle(screen, accent_color, (int(center_x), int(center_y - 10)), head_radius, 3)
        
        # 2. 繪製超大的卡通眼睛
        eye_size = 12
        left_eye_x = center_x - 15
        right_eye_x = center_x + 15
        eye_y = center_y - 15
        
        # 眼白
        pygame.draw.circle(screen, WHITE, (int(left_eye_x), int(eye_y)), eye_size)
        pygame.draw.circle(screen, WHITE, (int(right_eye_x), int(eye_y)), eye_size)
        
        # 瞳孔
        pupil_size = 8
        pygame.draw.circle(screen, eye_color, (int(left_eye_x), int(eye_y)), pupil_size)
        pygame.draw.circle(screen, eye_color, (int(right_eye_x), int(eye_y)), pupil_size)
        
        # 眼睛高光
        highlight_size = 3
        pygame.draw.circle(screen, WHITE, (int(left_eye_x - 3), int(eye_y - 3)), highlight_size)
        pygame.draw.circle(screen, WHITE, (int(right_eye_x - 3), int(eye_y - 3)), highlight_size)
        
        # 3. 繪製可愛的小嘴巴
        mouth_y = center_y - 5
        pygame.draw.arc(screen, accent_color, 
                       (center_x - 8, mouth_y - 4, 16, 8), 
                       0, math.pi, 2)
        
        # 4. 繪製腮紅
        blush_color = (255, 150, 150)
        pygame.draw.circle(screen, blush_color, (int(center_x - 25), int(center_y - 5)), 6)
        pygame.draw.circle(screen, blush_color, (int(center_x + 25), int(center_y - 5)), 6)
        
        # 5. 繪製小小的身體
        body_width = 20
        body_height = 15
        body_rect = pygame.Rect(center_x - body_width//2, center_y + 15, body_width, body_height)
        pygame.draw.ellipse(screen, body_color, body_rect)
        pygame.draw.ellipse(screen, accent_color, body_rect, 2)
        
        # 6. 繪製可愛的小手小腳
        hand_size = 5
        pygame.draw.circle(screen, body_color, (int(center_x - 18), int(center_y + 20)), hand_size)
        pygame.draw.circle(screen, body_color, (int(center_x + 18), int(center_y + 20)), hand_size)
        
        foot_size = 6
        pygame.draw.ellipse(screen, body_color, (center_x - 15, center_y + 28, 10, foot_size))
        pygame.draw.ellipse(screen, body_color, (center_x + 5, center_y + 28, 10, foot_size))
        
        # 7. 繪製可愛的裝飾 - 小星星特效
        star_positions = [
            (center_x - 40, center_y - 20),
            (center_x + 40, center_y - 25),
            (center_x - 30, center_y + 10),
            (center_x + 35, center_y + 15)
        ]
        
        for star_x, star_y in star_positions:
            star_alpha = (math.sin(self.bounce_timer * 2) + 1) / 2
            if star_alpha > 0.5:
                self.draw_star(screen, star_x, star_y, 4, (255, 215, 0))
        
        # 8. 變身光環效果
        halo_radius = head_radius + 15 + math.sin(self.bounce_timer * 1.5) * 5
        halo_surface = pygame.Surface((halo_radius * 2, halo_radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(halo_surface, (255, 215, 0, 100), (halo_radius, halo_radius), halo_radius, 3)
        screen.blit(halo_surface, (center_x - halo_radius, center_y - 10 - halo_radius))
    
    def draw_normal_form(self, screen):
        """繪製正常形態 - 簡單的藍色方塊"""
        pygame.draw.rect(screen, (0, 0, 255), (self.x, self.y, self.width, self.height))
        pygame.draw.rect(screen, BLACK, (self.x, self.y, self.width, self.height), 2)
    
    def draw_star(self, screen, x, y, size, color):
        """繪製小星星"""
        points = []
        for i in range(10):
            angle = i * math.pi / 5
            if i % 2 == 0:
                radius = size
            else:
                radius = size // 2
            px = x + math.cos(angle) * radius
            py = y + math.sin(angle) * radius
            points.append((px, py))
        pygame.draw.polygon(screen, color, points)

def main():
    # 創建遊戲視窗
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("變身系統測試")
    clock = pygame.time.Clock()
    
    # 創建玩家和變身系統
    player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    transformation_system = TransformationSystem()
    
    # 遊戲主迴圈
    running = True
    last_time = time.time()
    
    while running:
        # 計算時間差
        current_time = time.time()
        dt = current_time - last_time
        last_time = current_time
        
        # 處理事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            transformation_system.handle_input(event)
        
        # 獲取按鍵狀態
        keys = pygame.key.get_pressed()
        
        # 更新
        transformation_system.update(dt)
        player.update(keys, transformation_system)
        
        # 繪製
        screen.fill(WHITE)
        player.draw(screen)
        transformation_system.draw_ui(screen)
        
        # 繪製說明
        # 使用支持中文的字體
        try:
            font = pygame.font.Font("C:\\Windows\\Fonts\\simsun.ttc", 24)
        except:
            font = pygame.font.Font(None, 24)
        instructions = [
            "Use arrow keys to move",
            "Answer English word questions to transform!",
            "Transformation lasts 8 seconds",
            "Questions appear every 10 seconds"
        ]
        
        for i, instruction in enumerate(instructions):
            text = font.render(instruction, True, BLACK)
            screen.blit(text, (10, SCREEN_HEIGHT - 100 + i * 25))
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()