# 變身系統 - 分離邏輯和UI
import pygame
import random
from config import TRANSFORMATION_CONFIG, WHITE, BLACK

class WordBank:
    """題庫管理"""
    def __init__(self):
        self.words = [
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
            {"word": "HEART", "hint": "心 - 輸送血液的器官，愛的象徵"},
            {"word": "APPLE", "hint": "蘋果 - A round fruit, often red or green"},
            {"word": "WATER", "hint": "水 - A clear liquid you drink"},
            {"word": "SUN", "hint": "太陽 - The star that gives us daylight"},
            {"word": "DOG", "hint": "狗 - A common pet that barks"},
            {"word": "CAT", "hint": "貓 - A pet that says 'meow'"},
            {"word": "BOOK", "hint": "書 - Something you read with many pages"},
            {"word": "SCHOOL", "hint": "學校 - A place where children learn"},
            {"word": "HOME", "hint": "家 - The place where you live with your family"},
            {"word": "FRIEND", "hint": "朋友 - A person you like and have fun with"},
            {"word": "HAPPY", "hint": "開心 - Feeling good and cheerful"},
            {"word": "PLAY", "hint": "玩 - To have fun or do an activity"},
            {"word": "EAT", "hint": "吃 - To put food in your mouth"},
            {"word": "SLEEP", "hint": "睡覺 - To rest your body and mind at night"},
            {"word": "BIG", "hint": "大的 - Large in size"},
            {"word": "FATHER", "hint": "家裡最帥的"},
            {"word": "ENZO", "hint": "不是右邊的男生"},
            {"word": "ENOCH", "hint": "不是用右手寫法"},
            {"word": "ENOS", "hint": "右邊沒有酒窩"}
        ]
    
    def get_random_word(self):
        """獲取隨機單字"""
        return random.choice(self.words)


class TransformationLogic:
    """變身邏輯管理"""
    def __init__(self):
        self.timer = TRANSFORMATION_CONFIG["timer"]
        self.transformation_duration = TRANSFORMATION_CONFIG["duration"]
        self.required_answers = TRANSFORMATION_CONFIG["required_answers"]
        
        self.confirmation_active = False
        self.question_active = False
        self.transformation_active = False
        self.current_question = None
        self.user_input = ""
        self.correct_answers = 0
        
        self.word_bank = WordBank()
    
    def update(self, dt):
        """更新邏輯狀態"""
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
        self.current_question = self.word_bank.get_random_word()
        self.user_input = ""
    
    def handle_input(self, event):
        """處理輸入事件"""
        # 處理確認視窗輸入
        if self.confirmation_active and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_y:
                self.start_question()
            elif event.key == pygame.K_n:
                self.end_confirmation()
        
        # 處理問題輸入
        elif self.question_active and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                self.user_input = self.user_input[:-1]
            elif event.key == pygame.K_RETURN:
                if self.user_input.upper() == self.current_question["word"]:
                    self.correct_answers += 1
                    if self.correct_answers >= self.required_answers:
                        self.start_transformation()
                    else:
                        self.start_question()
                else:
                    self.correct_answers = 0
                    self.end_question()
            elif event.unicode.isalpha():
                self.user_input += event.unicode.upper()
    
    def end_confirmation(self):
        """取消確認"""
        self.confirmation_active = False
        self.timer = TRANSFORMATION_CONFIG["timer"]
    
    def start_transformation(self):
        """開始變身"""
        self.question_active = False
        self.transformation_active = True
        self.transformation_duration = TRANSFORMATION_CONFIG["duration"]
        self.timer = TRANSFORMATION_CONFIG["timer"]
        self.correct_answers = 0
    
    def end_transformation(self):
        """結束變身"""
        self.transformation_active = False
        self.timer = TRANSFORMATION_CONFIG["timer"]
    
    def end_question(self):
        """結束問題"""
        self.question_active = False
        self.timer = TRANSFORMATION_CONFIG["timer"]
        self.correct_answers = 0
    
    def is_paused(self):
        """檢查是否暫停遊戲"""
        return self.confirmation_active or self.question_active


class TransformationUI:
    """變身系統UI"""
    def __init__(self):
        from config import get_fonts
        fonts = get_fonts()
        self.font = fonts['small']
        self.big_font = fonts['big']
    
    def draw(self, screen, logic):
        """繪製UI"""
        from config import SCREEN_WIDTH, SCREEN_HEIGHT
        
        # 繪製計時器
        if not logic.confirmation_active and not logic.question_active and not logic.transformation_active:
            timer_text = f"Next Question: {int(logic.timer)}s"
            text_surface = self.font.render(timer_text, True, WHITE)
            screen.blit(text_surface, (10, 10))
        
        # 繪製確認對話框
        if logic.confirmation_active:
            self._draw_confirmation_dialog(screen, SCREEN_WIDTH, SCREEN_HEIGHT)
        
        # 繪製問題界面
        elif logic.question_active:
            self._draw_question_interface(screen, logic, SCREEN_WIDTH, SCREEN_HEIGHT)
        
        # 變身狀態指示
        if logic.transformation_active:
            transform_text = f"TRANSFORMED! {int(logic.transformation_duration)}s left"
            text_surface = self.big_font.render(transform_text, True, (255, 215, 0))
            screen.blit(text_surface, (SCREEN_WIDTH//2 - 200, 50))
    
    def _draw_confirmation_dialog(self, screen, screen_width, screen_height):
        """繪製確認對話框"""
        # 完全不透明的黑色背景
        overlay = pygame.Surface((screen_width, screen_height))
        overlay.fill(BLACK)
        screen.blit(overlay, (0, 0))
        
        # 確認對話框
        dialog_width = 600
        dialog_height = 300
        dialog_rect = pygame.Rect(
            (screen_width - dialog_width) // 2,
            (screen_height - dialog_height) // 2,
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
            "你需要連續答對2個英文問題來完成變身。",
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
    
    def _draw_question_interface(self, screen, logic, screen_width, screen_height):
        """繪製問題界面"""
        # 半透明背景
        overlay = pygame.Surface((screen_width, screen_height))
        overlay.set_alpha(128)
        overlay.fill(BLACK)
        screen.blit(overlay, (0, 0))
        
        # 問題框
        question_rect = pygame.Rect(screen_width//4, screen_height//3, screen_width//2, screen_height//3)
        pygame.draw.rect(screen, WHITE, question_rect)
        pygame.draw.rect(screen, BLACK, question_rect, 3)
        
        # 進度顯示
        progress_text = f"進度: {logic.correct_answers}/{logic.required_answers} 題正確"
        progress_surface = self.font.render(progress_text, True, (0, 100, 0))
        screen.blit(progress_surface, (question_rect.x + 20, question_rect.y + 10))
        
        # 問題文字
        hint_text = self.big_font.render("Hint:", True, BLACK)
        screen.blit(hint_text, (question_rect.x + 20, question_rect.y + 40))
        
        hint_content = self.font.render(logic.current_question["hint"], True, BLACK)
        screen.blit(hint_content, (question_rect.x + 20, question_rect.y + 80))
        
        # 輸入框
        input_text = self.big_font.render(f"Answer: {logic.user_input}", True, BLACK)
        screen.blit(input_text, (question_rect.x + 20, question_rect.y + 140))
        
        # 指示文字
        instruction = self.font.render("Type your answer and press ENTER", True, BLACK)
        screen.blit(instruction, (question_rect.x + 20, question_rect.y + 200))


class TransformationSystem:
    """變身系統主類"""
    def __init__(self):
        self.logic = TransformationLogic()
        self.ui = TransformationUI()
    
    def update(self, dt):
        """更新系統"""
        self.logic.update(dt)
    
    def handle_input(self, event):
        """處理輸入"""
        self.logic.handle_input(event)
    
    def draw_ui(self, screen):
        """繪製UI"""
        self.ui.draw(screen, self.logic)
    
    @property
    def transformation_active(self):
        """是否正在變身"""
        return self.logic.transformation_active
    
    @property
    def confirmation_active(self):
        """是否顯示確認對話框"""
        return self.logic.confirmation_active
    
    @property
    def question_active(self):
        """是否顯示問題"""
        return self.logic.question_active
    
    def is_paused(self):
        """檢查是否暫停遊戲"""
        return self.logic.is_paused()