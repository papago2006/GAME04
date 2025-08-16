import pygame
import sys
import random
import math
import time

# 初始化 Pygame
pygame.init()

# 變身系統相關
class TransformationSystem:
    def __init__(self):
        self.word_bank = [
            {"word": "HERO", "hint": "英雄 - 拯救他人的勇敢之人"},
            {"word": "POWER", "hint": "力量 - 力量或能量"},
            {"word": "MAGIC", "hint": "魔法 - 超自然的力量"},
            {"word": "BRAVE", "hint": "勇敢 - 展現勇氣"},
            {"word": "LIGHT", "hint": "光 - 驅散黑暗的光明"},
            {"word": "PEACE", "hint": "和平 - 和諧的狀態"},
            {"word": "HOPE", "hint": "希望 - 期盼的感覺"},
            {"word": "DREAM", "hint": "夢想 - 睡眠中的景象或抱負"},
            {"word": "SMILE", "hint": "微笑 - 快樂的臉部表情"},
            {"word": "LOVE", "hint": "愛 - 深厚的情感"},
            {"word": "STAR", "hint": "星星 - 發光的天體"},
            {"word": "MOON", "hint": "月亮 - 地球的天然衛星"},
            {"word": "FIRE", "hint": "火 - 炙熱燃燒的元素"},
            {"word": "WIND", "hint": "風 - 流動的空氣"},
            {"word": "HEART", "hint": "心 - 輸送血液的器官，愛的象徵"}
        ]
        self.timer = 10.0  # 10秒計時器（測試用）
        self.confirmation_active = False  # 確認視窗狀態
        self.question_active = False
        self.current_question = None
        self.user_input = ""
        self.transformation_active = False
        self.transformation_duration = 15.0  # 變身持續15秒
        
        # 新增：問題計數器和已回答問題追蹤
        self.questions_needed = 3  # 需要回答3個問題
        self.questions_answered = 0  # 已回答的問題數
        self.used_questions = []  # 已使用的問題，避免重複
        
        # 使用支持中文的字體
        try:
            self.font = pygame.font.Font("C:\\Windows\\Fonts\\simsun.ttc", 36)
            self.big_font = pygame.font.Font("C:\\Windows\\Fonts\\simsun.ttc", 48)
        except:
            # 如果無法加載中文字體，則使用默認字體
            self.font = pygame.font.Font(None, 36)
            self.big_font = pygame.font.Font(None, 48)
        
    def update(self, dt):
        # 只有在沒有任何活動狀態時才更新計時器
        if not self.confirmation_active and not self.question_active and not self.transformation_active:
            self.timer -= dt
            if self.timer <= 0:
                self.start_confirmation()
        
        if self.transformation_active:
            self.transformation_duration -= dt
            if self.transformation_duration <= 0:
                self.end_transformation()
    
    def start_confirmation(self):
        """開始確認對話框"""
        self.confirmation_active = True
    
    def start_question(self):
        """開始問題階段"""
        self.confirmation_active = False
        self.question_active = True
        
        # 選擇一個未使用過的問題
        available_questions = [q for q in self.word_bank if q not in self.used_questions]
        if not available_questions:  # 如果所有問題都用過了，重置
            self.used_questions = []
            available_questions = self.word_bank
            
        self.current_question = random.choice(available_questions)
        self.used_questions.append(self.current_question)
        self.user_input = ""
        
    def handle_input(self, event):
        # 處理確認視窗輸入
        if self.confirmation_active and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_y:  # 按 Y 確認
                # 重置問題計數器
                self.questions_answered = 0
                self.used_questions = []
                self.start_question()
            elif event.key == pygame.K_n:  # 按 N 取消
                self.end_confirmation()
        
        # 處理問題輸入
        elif self.question_active and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                self.user_input = self.user_input[:-1]
            elif event.key == pygame.K_RETURN:
                if self.user_input.upper() == self.current_question["word"]:
                    self.questions_answered += 1
                    
                    if self.questions_answered >= self.questions_needed:
                        # 已回答完所有問題，開始變身
                        self.start_transformation()
                    else:
                        # 還需要回答更多問題，繼續下一題
                        self.start_question()
                else:
                    # 答錯了，重置問題計數
                    self.questions_answered = 0
                    self.end_question()
            elif event.unicode.isalpha():
                self.user_input += event.unicode.upper()
    
    def end_confirmation(self):
        """取消確認，重置計時器"""
        self.confirmation_active = False
        self.timer = 10.0  # 重置計時器
        
    def start_transformation(self):
        self.question_active = False
        self.transformation_active = True
        self.transformation_duration = 15.0
        self.timer = 10.0  # 重置計時器
        self.questions_answered = 0  # 重置問題計數
        
    def end_transformation(self):
        self.transformation_active = False
        self.timer = 10.0  # 重置計時器
        
    def end_question(self):
        self.question_active = False
        self.timer = 10.0  # 重置計時器
        
    def draw_ui(self, screen):
        # 繪製計時器
        if not self.confirmation_active and not self.question_active and not self.transformation_active:
            timer_text = f"Next Question: {int(self.timer)}s"
            text_surface = self.font.render(timer_text, True, WHITE)
            screen.blit(text_surface, (10, 10))
        
        # 繪製確認對話框
        if self.confirmation_active:
            # 完全不透明的黑色背景，完全暫停遊戲畫面
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.fill(BLACK)
            screen.blit(overlay, (0, 0))
            
            # 確認對話框
            dialog_width = 600
            dialog_height = 300
            dialog_rect = pygame.Rect(
                (SCREEN_WIDTH - dialog_width) // 2,
                (SCREEN_HEIGHT - dialog_height) // 2,
                dialog_width,
                dialog_height
            )
            
            # 對話框背景和邊框
            pygame.draw.rect(screen, WHITE, dialog_rect)
            pygame.draw.rect(screen, (100, 100, 255), dialog_rect, 5)
            
            # 標題
            title_text = self.big_font.render("變身系統啟動", True, BLACK)
            title_rect = title_text.get_rect(center=(dialog_rect.centerx, dialog_rect.y + 50))
            screen.blit(title_text, title_rect)
            
            # 確認訊息
            message_lines = [
                "變身系統即將啟動！",
                f"你需要回答{self.questions_needed}個英文問題來完成變身。",
                "準備好了嗎？"
            ]
            
            for i, line in enumerate(message_lines):
                text_surface = self.font.render(line, True, BLACK)
                text_rect = text_surface.get_rect(center=(dialog_rect.centerx, dialog_rect.y + 120 + i * 40))
                screen.blit(text_surface, text_rect)
            
            # 按鈕提示
            button_text = self.big_font.render("按 Y 確認 / 按 N 取消", True, (0, 100, 0))
            button_rect = button_text.get_rect(center=(dialog_rect.centerx, dialog_rect.y + 240))
            screen.blit(button_text, button_rect)
        
        # 繪製問題界面
        elif self.question_active:
            # 半透明背景
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.set_alpha(128)
            overlay.fill(BLACK)
            screen.blit(overlay, (0, 0))
            
            # 問題框
            question_rect = pygame.Rect(SCREEN_WIDTH//4, SCREEN_HEIGHT//3, SCREEN_WIDTH//2, SCREEN_HEIGHT//3)
            pygame.draw.rect(screen, WHITE, question_rect)
            pygame.draw.rect(screen, BLACK, question_rect, 3)
            
            # 問題進度
            progress_text = self.font.render(f"問題 {self.questions_answered + 1}/{self.questions_needed}", True, BLACK)
            screen.blit(progress_text, (question_rect.x + 20, question_rect.y - 40))
            
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

# 遊戲設定
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PLAYER_SPEED = 5

# 顏色定義
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 40
        self.height = 40
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
        bounce_offset = math.sin(self.bounce_timer) * 4
        
        center_x = self.x + self.width // 2
        center_y = self.y + self.height // 2 + bounce_offset
        
        # 身體 - 粉紅色圓形
        body_color = (255, 182, 193)
        pygame.draw.circle(screen, body_color, (int(center_x), int(center_y)), 20)
        
        # 眼睛
        eye_color = (0, 0, 0)
        pygame.draw.circle(screen, WHITE, (int(center_x - 8), int(center_y - 5)), 6)
        pygame.draw.circle(screen, WHITE, (int(center_x + 8), int(center_y - 5)), 6)
        pygame.draw.circle(screen, eye_color, (int(center_x - 8), int(center_y - 5)), 3)
        pygame.draw.circle(screen, eye_color, (int(center_x + 8), int(center_y - 5)), 3)
        
        # 高光
        pygame.draw.circle(screen, WHITE, (int(center_x - 10), int(center_y - 7)), 2)
        pygame.draw.circle(screen, WHITE, (int(center_x + 6), int(center_y - 7)), 2)
        
        # 嘴巴
        mouth_points = [
            (center_x - 4, center_y + 3),
            (center_x, center_y + 6),
            (center_x + 4, center_y + 3)
        ]
        pygame.draw.lines(screen, (255, 100, 100), False, mouth_points, 2)
        
        # 腮紅
        blush_color = (255, 150, 150)
        pygame.draw.circle(screen, blush_color, (int(center_x - 15), int(center_y + 2)), 4)
        pygame.draw.circle(screen, blush_color, (int(center_x + 15), int(center_y + 2)), 4)
        
        # 閃爍星星
        star_positions = [
            (center_x - 30, center_y - 20),
            (center_x + 30, center_y - 25),
            (center_x - 25, center_y + 25),
            (center_x + 25, center_y + 20)
        ]
        
        for i, (star_x, star_y) in enumerate(star_positions):
            star_phase = self.bounce_timer * (1.5 + i * 0.3)
            star_alpha = (math.sin(star_phase) + 1) / 2
            if star_alpha > 0.4:
                star_size = 2 + int(star_alpha * 2)
                star_color = (255, 215, 0)
                self.draw_star(screen, star_x, star_y, star_size, star_color)
    
    def draw_normal_form(self, screen):
        """繪製正常形態"""
        pygame.draw.rect(screen, BLUE, (self.x, self.y, self.width, self.height))
        pygame.draw.rect(screen, WHITE, (self.x + 5, self.y + 5, 10, 10))  # 眼睛
        pygame.draw.rect(screen, WHITE, (self.x + 25, self.y + 5, 10, 10))  # 眼睛
    
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
    pygame.display.set_caption("三問題變身系統")
    
    # 創建遊戲物件
    player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    transformation_system = TransformationSystem()
    
    # 遊戲時鐘
    clock = pygame.time.Clock()
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
            # 處理變身系統輸入
            transformation_system.handle_input(event)
        
        # 獲取按鍵狀態
        keys = pygame.key.get_pressed()
        
        # 檢查是否需要暫停遊戲（確認對話框或問題顯示時）
        game_paused = transformation_system.confirmation_active or transformation_system.question_active
        
        if not game_paused:
            # 更新變身系統
            transformation_system.update(dt)
            
            # 更新玩家
            player.update(keys, transformation_system)
        
        # 繪製遊戲
        screen.fill(BLACK)
        
        # 繪製玩家
        player.draw(screen)
        
        # 繪製遊戲狀態文字
        if not transformation_system.confirmation_active and not transformation_system.question_active:
            status_text = "使用方向鍵移動角色"
            if transformation_system.transformation_active:
                status_text += " - 變身中！"
            else:
                status_text += f" - 已回答 {transformation_system.questions_answered}/{transformation_system.questions_needed} 問題"
            text_surface = transformation_system.font.render(status_text, True, WHITE)
            screen.blit(text_surface, (10, SCREEN_HEIGHT - 30))
        
        # 繪製變身系統UI
        transformation_system.draw_ui(screen)
        
        # 更新顯示
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()