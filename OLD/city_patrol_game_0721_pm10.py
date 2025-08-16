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
            {"word": "ENOS", "hint": "右邊沒有酒窩"},
            {"word": "ADVENTURE", "hint": "冒險 - An unusual and exciting experience"},
            {"word": "MYSTERY", "hint": "神秘 - Something that is difficult or impossible to understand or explain"},
            {"word": "PLANET", "hint": "行星 - A large object in space that moves around a star"},
            {"word": "INVENTION", "hint": "發明 - Something that has been created for the first time"},
            {"word": "COURAGE", "hint": "勇氣 - The ability to do something that frightens one"},
            {"word": "LEADER", "hint": "領導者 - A person who guides or directs a group"},
            {"word": "CHALLENGE", "hint": "挑戰 - A new or difficult task that tests somebody's ability and skill"},
            {"word": "GROW", "hint": "成長 - To increase in size or develop"},
            {"word": "SHARE", "hint": "分享 - To have or use something at the same time as someone else"},
            {"word": "DISCOVER", "hint": "發現 - To find something unexpectedly or during a search"},
            {"word": "PROTECT", "hint": "保護 - To keep safe from harm or injury"},
            {"word": "IMPORTANT", "hint": "重要的 - Having great significance or value"},
            {"word": "BEAUTIFUL", "hint": "美麗的 - Pleasing the senses or mind aesthetically"},
            {"word": "SUCCESS", "hint": "成功 - The accomplishment of an aim or purpose"},
            {"word": "PENCIL", "hint": "鉛筆 - You use it to write or draw"},
            {"word": "ERASER", "hint": "橡皮擦 - You use it to fix mistakes"},
            {"word": "RULER", "hint": "尺 - A tool to measure things or draw straight lines"},
            {"word": "TEACHER", "hint": "老師 - A person who teaches students in a school"},
            {"word": "STUDENT", "hint": "學生 - A person who is studying at a school"},
            {"word": "PARK", "hint": "公園 - A place with grass and trees where you can play"},
            {"word": "ZOO", "hint": "動物園 - A place to see many kinds of animals"},
            {"word": "RABBIT", "hint": "兔子 - An animal with long ears that likes carrots"},
            {"word": "TURTLE", "hint": "烏龜 - A slow animal with a hard shell"},
            {"word": "ELEPHANT", "hint": "大象 - A very large animal with a long trunk"},
            {"word": "RICE", "hint": "米飯 - Small grains that are a common food"},
            {"word": "NOODLES", "hint": "麵條 - Long strips of food made from flour"},
            {"word": "JUICE", "hint": "果汁 - A drink made from fruit"},
            {"word": "RUN", "hint": "跑步 - To move with your legs faster than walking"},
            {"word": "JUMP", "hint": "跳 - To push yourself up into the air"},
            {"word": "SWIM", "hint": "游泳 - To move through water using your body"},
            {"word": "READ", "hint": "閱讀 - To look at and understand words"},
            {"word": "WRITE", "hint": "寫字 - To make letters or words on paper"},
            {"word": "TALL", "hint": "高的 - Having a large height"},
            {"word": "SHORT", "hint": "矮的、短的 - Having a small height or length"},
            {"word": "ACTIVITY", "hint": "活動 - Something that you do for enjoyment, especially an organized one"},
            {"word": "FESTIVAL", "hint": "節日 - A day or period of celebration, for religious or cultural reasons"},
            {"word": "SUBJECT", "hint": "科目 - An area of knowledge that is studied in school, such as math or English"},
            {"word": "VACATION", "hint": "假期 - A period of time spent away from home or work for rest or travel"},
            {"word": "NATURE", "hint": "自然 - All the plants, animals, and things that exist in the universe that are not made by people"},
            {"word": "PRACTICE", "hint": "練習 - To do something regularly in order to become skilled at it"},
            {"word": "GOAL", "hint": "目標 - Something that you aim for or hope to achieve"},
            {"word": "KINDNESS", "hint": "善良 - The quality of being friendly, generous, and considerate"},
            {"word": "UNIFORM", "hint": "制服 - The special set of clothes worn by all members of a group or organization"},
            {"word": "PROJECT", "hint": "專案/報告 - A piece of schoolwork that involves detailed study of a subject"},
            {"word": "SMALL", "hint": "小的 - Not large in size"}
        ]
        self.timer = 05.0  # 30秒計時器
        self.confirmation_active = False  # 確認視窗狀態
        self.question_active = False
        self.current_question = None
        self.user_input = ""
        self.transformation_active = False
        self.transformation_duration = 15.0  # 變身持續15秒
        self.correct_answers = 0  # 連續答對的題目數
        self.required_answers = 2  # 需要連續答對的題目數
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
        """開始問題階段 - 需要連續答對2題才可以變身"""
        self.confirmation_active = False
        self.question_active = True
        self.current_question = random.choice(self.word_bank)
        self.user_input = ""
        
    def handle_input(self, event):
        # 處理確認視窗輸入
        if self.confirmation_active and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_y:  # 按 Y 確認
                self.start_question()
            elif event.key == pygame.K_n:  # 按 N 取消
                self.end_confirmation()
        
        # 處理問題輸入
        elif self.question_active and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                self.user_input = self.user_input[:-1]
            elif event.key == pygame.K_RETURN:
                if self.user_input.upper() == self.current_question["word"]:
                    self.correct_answers += 1
                    if self.correct_answers >= self.required_answers:
                        # 連續答對足夠題目，開始變身
                        self.start_transformation()
                    else:
                        # 答對了但還需要更多題目，繼續下一題
                        self.start_question()
                else:
                    # 答錯了，重置計數器
                    self.correct_answers = 0
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
        self.correct_answers = 0  # 重置答對計數器
        
    def end_transformation(self):
        self.transformation_active = False
        self.timer = 10.0  # 重置計時器
        
    def end_question(self):
        self.question_active = False
        self.timer = 10.0  # 重置計時器
        self.correct_answers = 0  # 重置答對計數器
        
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
            
            # 進度顯示
            progress_text = f"進度: {self.correct_answers}/{self.required_answers} 題正確"
            progress_surface = self.font.render(progress_text, True, (0, 100, 0))
            screen.blit(progress_surface, (question_rect.x + 20, question_rect.y + 10))
            
            # 問題文字
            hint_text = self.big_font.render("Hint:", True, BLACK)
            screen.blit(hint_text, (question_rect.x + 20, question_rect.y + 40))
            
            hint_content = self.font.render(self.current_question["hint"], True, BLACK)
            screen.blit(hint_content, (question_rect.x + 20, question_rect.y + 80))
            
            # 輸入框
            input_text = self.big_font.render(f"Answer: {self.user_input}", True, BLACK)
            screen.blit(input_text, (question_rect.x + 20, question_rect.y + 140))
            
            # 指示文字
            instruction = self.font.render("Type your answer and press ENTER", True, BLACK)
            screen.blit(instruction, (question_rect.x + 20, question_rect.y + 200))
        
        # 變身狀態指示
        if self.transformation_active:
            transform_text = f"TRANSFORMED! {int(self.transformation_duration)}s left"
            text_surface = self.big_font.render(transform_text, True, (255, 215, 0))
            screen.blit(text_surface, (SCREEN_WIDTH//2 - 200, 50))

# 遊戲設定
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
PLAYER_SPEED = 7

# 顏色定義
GRASS_GREEN = (50, 150, 50)
ROAD_GRAY = (100, 100, 100)
SIDEWALK_GRAY = (180, 180, 180)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 60
        self.height = 30
        self.speed = PLAYER_SPEED
        self.health = 100
        self.max_health = 100
        self.hit_timer = 0  # 受創閃爍計時器
        self.has_gun = False  # 是否擁有武器
        self.shoot_cooldown = 0  # 射擊冷卻
        self.is_transformed = False  # 變身狀態
        self.bounce_timer = 0  # 可愛彈跳動畫計時器
        
    def update(self, keys, game_over=False, player_bullets=None, transformation_system=None):
        # 更新受創計時器
        if self.hit_timer > 0:
            self.hit_timer -= 1
            
        # 更新射擊冷卻
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1
            
        # 更新變身狀態
        if transformation_system:
            self.is_transformed = transformation_system.transformation_active
            
        # 更新可愛動畫計時器
        self.bounce_timer += 0.2
            
        # 如果遊戲結束，停止移動
        if game_over:
            return
            
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
            
        # 射擊功能
        if self.has_gun and keys[pygame.K_SPACE] and self.shoot_cooldown <= 0 and player_bullets is not None:
            # 發射子彈
            bullet_x = self.x + self.width // 2
            bullet_y = self.y
            player_bullets.append(PlayerBullet(bullet_x, bullet_y, 0, -12))  # 向上發射
            self.shoot_cooldown = 15  # 射擊冷卻
    
    def take_damage(self, damage):
        self.health -= damage
        self.hit_timer = 30  # 0.5秒閃爍 (30 frames at 60 FPS)
        if self.health < 0:
            self.health = 0
    
    def draw(self, screen):
        # 受創閃爍效果
        flash = self.hit_timer > 0 and (self.hit_timer // 3) % 2 == 0
        
        if self.is_transformed:
            self.draw_cute_form(screen, flash)
        else:
            self.draw_normal_form(screen, flash)
    
    def draw_cute_form(self, screen, flash):
        """繪製可愛變身形態 - 現代日本ゆるキャラ風格"""
        # 可愛彈跳效果
        bounce_offset = math.sin(self.bounce_timer) * 4
        
        # 柔和的賽璐璐風格色彩調色盤
        if flash:
            # 閃爍時的顏色
            body_color = (255, 255, 255)
            accent_color = (255, 200, 200)
            eye_color = (255, 255, 255)
            blush_color = (255, 180, 180)
        else:
            # 正常可愛顏色 - 柔和粉彩色系
            body_color = (255, 228, 225)    # 溫暖的淺粉色 (大福麻糬色)
            accent_color = (255, 182, 193)  # 淡粉紅輪廓
            eye_color = (45, 45, 45)        # 深灰色眼睛 (不是純黑)
            blush_color = (255, 192, 203)   # 淡粉色腮紅
        
        center_x = self.x + self.width // 2
        center_y = self.y + self.height // 2 + bounce_offset
        
        # 1. 繪製完美圓形的巨大頭部 (二頭身比例)
        head_radius = 42  # 更大的頭部
        
        # 頭部陰影 (增加立體感)
        shadow_offset = 2
        pygame.draw.circle(screen, (200, 200, 200, 100), 
                          (int(center_x + shadow_offset), int(center_y - 8 + shadow_offset)), head_radius)
        
        # 主要頭部 - 完美圓形
        pygame.draw.circle(screen, body_color, (int(center_x), int(center_y - 8)), head_radius)
        
        # 柔和的輪廓線 (賽璐璐風格)
        pygame.draw.circle(screen, accent_color, (int(center_x), int(center_y - 8)), head_radius, 2)
        
        # 2. 繪製巨大且富有表現力的「萌え」風格眼睛
        eye_size = 16  # 更大的眼睛
        left_eye_x = center_x - 18
        right_eye_x = center_x + 18
        eye_y = center_y - 18
        
        # 眼白 - 完美的圓形
        pygame.draw.circle(screen, WHITE, (int(left_eye_x), int(eye_y)), eye_size)
        pygame.draw.circle(screen, WHITE, (int(right_eye_x), int(eye_y)), eye_size)
        
        # 眼睛輪廓
        pygame.draw.circle(screen, (220, 220, 220), (int(left_eye_x), int(eye_y)), eye_size, 1)
        pygame.draw.circle(screen, (220, 220, 220), (int(right_eye_x), int(eye_y)), eye_size, 1)
        
        # 瞳孔 - 像宇宙星雲一樣的漸層效果
        pupil_size = 10
        
        # 創建漸層瞳孔效果
        for i in range(pupil_size, 0, -1):
            # 從外到內的漸層色彩
            gradient_intensity = (pupil_size - i) / pupil_size
            color_r = int(eye_color[0] + (100 - eye_color[0]) * gradient_intensity)
            color_g = int(eye_color[1] + (150 - eye_color[1]) * gradient_intensity)
            color_b = int(eye_color[2] + (200 - eye_color[2]) * gradient_intensity)
            
            pygame.draw.circle(screen, (color_r, color_g, color_b), 
                              (int(left_eye_x), int(eye_y)), i)
            pygame.draw.circle(screen, (color_r, color_g, color_b), 
                              (int(right_eye_x), int(eye_y)), i)
        
        # 多層次高光效果
        # 主要高光
        main_highlight_size = 5
        pygame.draw.circle(screen, WHITE, (int(left_eye_x - 4), int(eye_y - 4)), main_highlight_size)
        pygame.draw.circle(screen, WHITE, (int(right_eye_x - 4), int(eye_y - 4)), main_highlight_size)
        
        # 次要高光
        secondary_highlight_size = 2
        pygame.draw.circle(screen, (255, 255, 255, 180), (int(left_eye_x + 3), int(eye_y + 2)), secondary_highlight_size)
        pygame.draw.circle(screen, (255, 255, 255, 180), (int(right_eye_x + 3), int(eye_y + 2)), secondary_highlight_size)
        
        # 3. 繪製精緻的「w」形小嘴巴
        mouth_y = center_y - 2
        mouth_points = [
            (center_x - 6, mouth_y),
            (center_x - 3, mouth_y + 3),
            (center_x, mouth_y + 1),
            (center_x + 3, mouth_y + 3),
            (center_x + 6, mouth_y)
        ]
        pygame.draw.lines(screen, accent_color, False, mouth_points, 2)
        
        # 4. 繪製幾乎看不見的點點鼻
        nose_size = 1
        pygame.draw.circle(screen, (200, 180, 180), (int(center_x), int(center_y - 8)), nose_size)
        
        # 5. 繪製胖嘟嘟的「大福麻糬」腮紅
        blush_size = 8
        # 左腮紅 - 橢圓形更自然
        left_blush_rect = pygame.Rect(center_x - 32, center_y - 8, blush_size * 2, blush_size)
        pygame.draw.ellipse(screen, blush_color, left_blush_rect)
        
        # 右腮紅
        right_blush_rect = pygame.Rect(center_x + 24, center_y - 8, blush_size * 2, blush_size)
        pygame.draw.ellipse(screen, blush_color, right_blush_rect)
        
        # 6. 繪製像豆子一樣的小身體
        body_width = 24
        body_height = 18
        body_rect = pygame.Rect(center_x - body_width//2, center_y + 25, body_width, body_height)
        
        # 身體陰影
        shadow_body_rect = pygame.Rect(center_x - body_width//2 + 1, center_y + 26, body_width, body_height)
        pygame.draw.ellipse(screen, (200, 200, 200), shadow_body_rect)
        
        # 主要身體
        pygame.draw.ellipse(screen, body_color, body_rect)
        pygame.draw.ellipse(screen, accent_color, body_rect, 2)
        
        # 7. 繪製又短又胖的可愛四肢
        limb_color = body_color
        
        # 小手 - 更圓潤
        hand_size = 6
        pygame.draw.circle(screen, limb_color, (int(center_x - 20), int(center_y + 28)), hand_size)
        pygame.draw.circle(screen, limb_color, (int(center_x + 20), int(center_y + 28)), hand_size)
        pygame.draw.circle(screen, accent_color, (int(center_x - 20), int(center_y + 28)), hand_size, 1)
        pygame.draw.circle(screen, accent_color, (int(center_x + 20), int(center_y + 28)), hand_size, 1)
        
        # 小腳 - 橢圓形更可愛
        foot_width = 12
        foot_height = 7
        left_foot_rect = pygame.Rect(center_x - 16, center_y + 38, foot_width, foot_height)
        right_foot_rect = pygame.Rect(center_x + 4, center_y + 38, foot_width, foot_height)
        
        pygame.draw.ellipse(screen, limb_color, left_foot_rect)
        pygame.draw.ellipse(screen, limb_color, right_foot_rect)
        pygame.draw.ellipse(screen, accent_color, left_foot_rect, 1)
        pygame.draw.ellipse(screen, accent_color, right_foot_rect, 1)
        
        # 8. 繪製閃閃發光的星星裝飾
        star_positions = [
            (center_x - 45, center_y - 25),
            (center_x + 45, center_y - 30),
            (center_x - 35, center_y + 15),
            (center_x + 40, center_y + 20)
        ]
        
        for i, (star_x, star_y) in enumerate(star_positions):
            # 每顆星星不同的閃爍節奏
            star_phase = self.bounce_timer * (1.5 + i * 0.3)
            star_alpha = (math.sin(star_phase) + 1) / 2
            if star_alpha > 0.4:
                star_size = 3 + int(star_alpha * 2)
                star_color = (255, 215 + int(star_alpha * 40), int(star_alpha * 100))
                self.draw_star(screen, star_x, star_y, star_size, star_color)
        
        # 9. 繪製變身光環效果 (更柔和)
        halo_radius = head_radius + 18 + math.sin(self.bounce_timer * 1.2) * 6
        halo_surface = pygame.Surface((halo_radius * 2, halo_radius * 2), pygame.SRCALPHA)
        
        # 多層光環效果
        for i in range(3):
            alpha = 80 - i * 25
            radius = halo_radius - i * 3
            pygame.draw.circle(halo_surface, (255, 215, 0, alpha), 
                              (halo_radius, halo_radius), radius, 2)
        
        screen.blit(halo_surface, (center_x - halo_radius, center_y - 8 - halo_radius))
        
        # 10. 繪製柔軟舒適的質感高光
        # 頭部頂部的柔和高光
        highlight_surface = pygame.Surface((head_radius, head_radius // 2), pygame.SRCALPHA)
        pygame.draw.ellipse(highlight_surface, (255, 255, 255, 60), 
                           (0, 0, head_radius, head_radius // 2))
        screen.blit(highlight_surface, (center_x - head_radius // 2, center_y - 25))
    
    def draw_normal_form(self, screen, flash):
        """繪製正常形態 - 原來的外星督察者設計"""
        if flash:
            # 閃爍時使用白色
            body_color = WHITE
            front_color = (200, 200, 200)
            window_color = (255, 255, 255)
        else:
            # 正常顏色
            body_color = (0, 0, 139)
            front_color = (25, 25, 112)
            window_color = (173, 216, 230)
        
        # 原來的外星督察者設計
        self.width = 180
        self.height = 80
        
        shell_color_dark = (48, 10, 60)
        shell_color_light = (85, 40, 110)
        cockpit_color = (10, 0, 10)
        energy_glow_green = (50, 255, 150)
        energy_glow_magenta = (255, 0, 255)
        energy_core_white = (255, 255, 255)

        pulse_slow = (math.sin(pygame.time.get_ticks() * 0.0015) + 1) / 2
        pulse_fast = (math.sin(pygame.time.get_ticks() * 0.008) + 1) / 2

        # 主要結構
        lower_shell_points = [
            (self.x, self.y + 20),
            (self.x + 40, self.y + self.height),
            (self.x + self.width - 30, self.y + self.height - 10),
            (self.x + self.width, self.y + 10)
        ]
        pygame.draw.polygon(screen, shell_color_dark, lower_shell_points)
        
        upper_shell_points = [
            (self.x + 10, self.y + 15),
            (self.x + 50, self.y),
            (self.x + self.width - 60, self.y + 5),
            (self.x + self.width - 10, self.y + 25),
            (self.x + self.width * 0.6, self.y + 35),
            (self.x + 50, self.y + 30)
        ]
        pygame.draw.polygon(screen, shell_color_light, upper_shell_points)
        
        # 能量水晶推進器
        crystal_y = self.y + self.height - 5
        main_crystal_points = [
            (self.x + 20, crystal_y),
            (self.x + 50, crystal_y - 15),
            (self.x + 60, crystal_y),
            (self.x + 50, crystal_y + 15 + pulse_slow * 10)
        ]
        pygame.draw.polygon(screen, energy_glow_green, main_crystal_points)
        pygame.draw.circle(screen, energy_core_white, (self.x + 48, crystal_y), int(3 + pulse_fast * 2))

        # 武器系統
        weapon_base_points = [
            (self.x + 60, self.y + 10),
            (self.x + 70, self.y - 30),
            (self.x + self.width - 20, self.y - 25),
            (self.x + self.width, self.y + 15)
        ]
        pygame.draw.polygon(screen, shell_color_dark, weapon_base_points)

        core_x = self.x + 115
        core_y = self.y - 20
        pygame.draw.circle(screen, energy_glow_magenta, (core_x, core_y), int(22 + pulse_slow * 15))
        pygame.draw.circle(screen, energy_core_white, (core_x, core_y), int(8 + pulse_fast * 6))
        
        # 駕駛艙
        cockpit_points = [
            (self.x + 45, self.y + 8),
            (self.x + 90, self.y + 10),
            (self.x + 65, self.y + 28)
        ]
        pygame.draw.polygon(screen, cockpit_color, cockpit_points)
    
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
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
        # 隨機分配敵人原型
        self.archetype = random.choice(['Normal', 'Brute', 'Rusher'])
        
        # 基礎屬性
        base_width = 40
        base_height = 40
        base_speed = 3
        base_health = 50
        
        # 根據原型調整屬性
        if self.archetype == 'Brute':
            # 蠻力型：更大、更慢、更強
            self.width = int(base_width * 1.4)
            self.height = int(base_height * 1.4)
            self.speed = base_speed * 0.7
            self.health = base_health * 2.0
            self.max_health = self.health
        elif self.archetype == 'Rusher':
            # 突襲型：更小、更快、更脆
            self.width = int(base_width * 0.7)
            self.height = int(base_height * 0.7)
            self.speed = base_speed * 1.5
            self.health = base_health * 0.6
            self.max_health = self.health
        else:  # Normal
            # 普通型：基準屬性
            self.width = base_width
            self.height = base_height
            self.speed = base_speed
            self.health = base_health
            self.max_health = self.health
        
        # 個體差異微調
        self.speed *= random.uniform(0.9, 1.1)
        self.health *= random.uniform(0.9, 1.1)
        self.max_health = self.health
        
        self.attack_cooldown = 0
        self.attack_range = 800
        self.rotor_angle = 0
        self.pulse_timer = 0
        self.state = "patrol"  # patrol, tracking, attacking
        self.laser_jitter = 0
        
    def update(self, player, bullets, game_over=False):
        if game_over:
            return
            
        # 更新動畫計時器
        self.rotor_angle += 15  # 旋翼旋轉
        self.pulse_timer += 0.1
        self.laser_jitter = random.uniform(-2, 2)
        
        # 更新攻擊冷卻
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
            
        # 計算與玩家的距離
        dx = player.x - self.x
        dy = player.y - self.y
        distance = math.sqrt(dx*dx + dy*dy)
        
        # AI 行為狀態機
        if distance < self.attack_range:
            if distance < 800:
                self.state = "attacking"
                # 攻擊行為
                if self.attack_cooldown <= 0:
                    # 發射子彈
                    bullet_dx = dx / distance * 11  # 子彈速度
                    bullet_dy = dy / distance * 11
                    bullets.append(Bullet(self.x + self.width//2, self.y + self.height//2, bullet_dx, bullet_dy))
                    self.attack_cooldown = 120  #           2秒冷卻 (120 frames at 60 FPS)
            else:
                self.state = "tracking"
                
            # 追蹤玩家
            if distance > 0:
                self.x += (dx / distance) * self.speed
                self.y += (dy / distance) * self.speed
        else:
            self.state = "patrol"
            # 簡單的巡邏行為
            self.x += math.sin(pygame.time.get_ticks() * 0.001) * 2
            self.y += math.cos(pygame.time.get_ticks() * 0.001) * 1
            
        # 保持在螢幕範圍內
        self.x = max(0, min(SCREEN_WIDTH - self.width, self.x))
        self.y = max(0, min(SCREEN_HEIGHT - self.height, self.y))
    
    def draw(self, screen, player):
        center_x = self.x + self.width // 2
        center_y = self.y + self.height // 2
        
        # 機身多層圓形疊加
        # 底部陰影
        shadow_surface = pygame.Surface((50, 50), pygame.SRCALPHA)
        pygame.draw.circle(shadow_surface, (0, 0, 0, 80), (25, 25), 22)
        screen.blit(shadow_surface, (center_x - 25, center_y - 23))
        
        # 深色金屬底盤
        pygame.draw.circle(screen, (40, 40, 40), (center_x, center_y), 20)
        
        # 頂部漸層高光圓形
        for i in range(15):
            color_val = 60 + i * 8
            pygame.draw.circle(screen, (color_val, color_val, color_val), (center_x, center_y - 2), 20 - i)
        
        # 裝甲接縫
        pygame.draw.circle(screen, BLACK, (center_x, center_y), 20, 2)
        pygame.draw.circle(screen, BLACK, (center_x, center_y), 15, 1)
        
        # 核心攝影機 - 脈動效果
        eye_radius = 8 + math.sin(self.pulse_timer) * 2
        pygame.draw.circle(screen, BLACK, (center_x, center_y), int(eye_radius + 2))  # 眼窩
        pygame.draw.circle(screen, (200, 0, 0), (center_x, center_y), int(eye_radius))  # 惡魔紅鏡頭
        
        # 鏡頭眩光
        glare_surface = pygame.Surface((30, 6), pygame.SRCALPHA)
        pygame.draw.ellipse(glare_surface, (255, 100, 100, 100), (0, 0, 30, 6))
        screen.blit(glare_surface, (center_x - 15, center_y - 3))
        
        # 四旋翼推進器
        rotor_positions = [(-25, -25), (25, -25), (-25, 25), (25, 25)]
        for rx, ry in rotor_positions:
            rotor_x = center_x + rx
            rotor_y = center_y + ry
            
            # 支架
            pygame.draw.line(screen, (100, 100, 100), (center_x, center_y), (rotor_x, rotor_y), 3)
            
            # 馬達
            pygame.draw.circle(screen, (60, 60, 60), (rotor_x, rotor_y), 5)
            
            # 旋翼動態模糊殘影
            blur_surface = pygame.Surface((20, 20), pygame.SRCALPHA)
            pygame.draw.circle(blur_surface, (150, 150, 150, 100), (10, 10), 10)
            screen.blit(blur_surface, (rotor_x - 10, rotor_y - 10))
            
            # 清晰葉片
            blade_angle1 = math.radians(self.rotor_angle)
            blade_angle2 = math.radians(self.rotor_angle + 180)
            
            blade1_end = (rotor_x + math.cos(blade_angle1) * 12, rotor_y + math.sin(blade_angle1) * 12)
            blade2_end = (rotor_x + math.cos(blade_angle2) * 12, rotor_y + math.sin(blade_angle2) * 12)
            
            pygame.draw.line(screen, (200, 200, 200), (rotor_x, rotor_y), blade1_end, 2)
            pygame.draw.line(screen, (200, 200, 200), (rotor_x, rotor_y), blade2_end, 2)
        
        # 狀態指示燈
        if self.state == "patrol":
            light_color = (0, 255, 0)  # 綠色
        elif self.state == "tracking":
            light_color = (255, 255, 0)  # 黃色
        else:  # attacking
            light_color = (255, 0, 0)  # 紅色
            
        pygame.draw.circle(screen, light_color, (center_x - 8, center_y - 15), 3)
        pygame.draw.circle(screen, light_color, (center_x + 8, center_y - 15), 3)
        
        # 原型標識燈
        if self.archetype == 'Brute':
            archetype_color = (100, 0, 0)  # 深紅色
        elif self.archetype == 'Rusher':
            archetype_color = (255, 255, 0)  # 亮黃色
        else:  # Normal
            archetype_color = (0, 100, 255)  # 藍色
            
        pygame.draw.circle(screen, archetype_color, (center_x, center_y - 18), 2)
        
        # 瞄準雷射（攻擊狀態時）
        if self.state == "attacking":
            laser_length = 100 + self.laser_jitter
            laser_end_x = center_x
            laser_end_y = center_y + laser_length
            pygame.draw.line(screen, (255, 0, 0), (center_x, center_y + 20), (laser_end_x, laser_end_y), 2)
            
            # 雷射光點
            pygame.draw.circle(screen, (255, 100, 100), (int(laser_end_x), int(laser_end_y)), 4)
    
    def take_damage(self, damage):
        self.health -= damage
        if self.health < 0:
            self.health = 0
    
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

class Enemy_big:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
        # 隨機分配敵人原型
        self.archetype = random.choice(['Normal', 'Brute', 'Rusher'])
        
        # 基礎屬性
        base_width = 120
        base_height = 120
        base_speed = 5
        base_health = 100
        
        # 根據原型調整屬性
        if self.archetype == 'Brute':
            # 蠻力型：更大、更慢、更強
            self.width = int(base_width * 1.4)
            self.height = int(base_height * 1.4)
            self.speed = base_speed * 0.7
            self.health = base_health * 2.0
            self.max_health = self.health
        elif self.archetype == 'Rusher':
            # 突襲型：更小、更快、更脆
            self.width = int(base_width * 0.7)
            self.height = int(base_height * 0.7)
            self.speed = base_speed * 1.5
            self.health = base_health * 0.6
            self.max_health = self.health
        else:  # Normal
            # 普通型：基準屬性
            self.width = base_width
            self.height = base_height
            self.speed = base_speed
            self.health = base_health
            self.max_health = self.health
        
        # 個體差異微調
        self.speed *= random.uniform(0.9, 1.1)
        self.health *= random.uniform(0.9, 1.1)
        self.max_health = self.health
        
        self.attack_cooldown = 0
        self.attack_range = 800
        self.rotor_angle = 0
        self.pulse_timer = 0
        self.state = "patrol"  # patrol, tracking, attacking
        self.laser_jitter = 0
        
    def update(self, player, bullets, game_over=False):
        if game_over:
            return
            
        # 更新動畫計時器
        self.rotor_angle += 15  # 旋翼旋轉
        self.pulse_timer += 0.1
        self.laser_jitter = random.uniform(-2, 2)
        
        # 更新攻擊冷卻
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
            
        # 計算與玩家的距離
        dx = player.x - self.x
        dy = player.y - self.y
        distance = math.sqrt(dx*dx + dy*dy)
        
        # AI 行為狀態機
        if distance < self.attack_range:
            if distance < 800:
                self.state = "attacking"
                # 攻擊行為
                if self.attack_cooldown <= 0:
                    # 發射子彈
                    bullet_dx = dx / distance * 16  # 子彈速度
                    bullet_dy = dy / distance * 16
                    bullets.append(Bullet(self.x + self.width//2, self.y + self.height//2, bullet_dx, bullet_dy))
                    self.attack_cooldown = 120  #           2秒冷卻 (120 frames at 60 FPS)
            else:
                self.state = "tracking"
                
            # 追蹤玩家
            if distance > 0:
                self.x += (dx / distance) * self.speed
                self.y += (dy / distance) * self.speed
        else:
            self.state = "patrol"
            # 簡單的巡邏行為
            self.x += math.sin(pygame.time.get_ticks() * 0.001) * 2
            self.y += math.cos(pygame.time.get_ticks() * 0.001) * 1
            
        # 保持在螢幕範圍內
        self.x = max(0, min(SCREEN_WIDTH - self.width, self.x))
        self.y = max(0, min(SCREEN_HEIGHT - self.height, self.y))
        
    def draw(self, screen, player):
        center_x = self.x + self.width // 2
        center_y = self.y + self.height // 2
        
        # 使用 math 模組來實現平滑的呼吸/脈動效果
        pulse_slow = (math.sin(pygame.time.get_ticks() * 0.0015) + 1) / 2  # 慢速呼吸
        pulse_fast = (math.sin(pygame.time.get_ticks() * 0.008) + 1) / 2   # 快速脈動
        
        # 外星科技顏色定義
        alien_primary = (20, 180, 170)       # 青藍色主體
        alien_secondary = (140, 0, 190)      # 紫色能量
        alien_glow = (0, 255, 220)           # 能量光芒
        alien_core = (255, 255, 255)         # 核心白光
        alien_dark = (10, 40, 50)            # 暗部
        
        # 1. 繪製大型底部陰影 (增加體積感)
        shadow_size = 120  # 更大的陰影
        shadow_surface = pygame.Surface((shadow_size, shadow_size // 2), pygame.SRCALPHA)
        pygame.draw.ellipse(shadow_surface, (0, 0, 0, 60), (0, 0, shadow_size, shadow_size // 2))
        screen.blit(shadow_surface, (center_x - shadow_size // 2, center_y + 40))
        
        # 2. 繪製主體 - 不規則的外星飛行器形狀
        # 主體是一個橢圓形的UFO形狀
        body_width = 140
        body_height = 50
        pygame.draw.ellipse(screen, alien_primary, (center_x - body_width // 2, center_y - body_height // 2, 
                                                  body_width, body_height))
        
        # 3. 繪製上層圓頂 - 類似飛碟的透明罩
        dome_radius = 60
        dome_surface = pygame.Surface((dome_radius * 2, dome_radius), pygame.SRCALPHA)
        pygame.draw.ellipse(dome_surface, (alien_primary[0], alien_primary[1], alien_primary[2], 180), 
                           (0, 0, dome_radius * 2, dome_radius * 2))
        screen.blit(dome_surface, (center_x - dome_radius, center_y - dome_radius - 20))
        
        # 4. 繪製能量環 - 圍繞主體的脈動光環
        ring_radius = 80 + int(pulse_slow * 10)
        ring_width = 5 + int(pulse_fast * 3)
        pygame.draw.circle(screen, alien_secondary, (center_x, center_y), ring_radius, ring_width)
        
        # 5. 繪製能量核心 - 中央的強大能量源
        core_radius = 25 + int(pulse_fast * 8)
        # 外層光暈
        glow_surface = pygame.Surface((core_radius * 2 + 20, core_radius * 2 + 20), pygame.SRCALPHA)
        for r in range(10, 0, -1):
            alpha = 150 - r * 15
            if alpha < 0:
                alpha = 0
            pygame.draw.circle(glow_surface, (alien_glow[0], alien_glow[1], alien_glow[2], alpha), 
                              (core_radius + 10, core_radius + 10), core_radius + r)
        screen.blit(glow_surface, (center_x - core_radius - 10, center_y - core_radius - 10))
        
        # 內層核心
        pygame.draw.circle(screen, alien_secondary, (center_x, center_y), core_radius // 2)
        pygame.draw.circle(screen, alien_core, (center_x, center_y), core_radius // 4)
        
        # 6. 繪製懸浮裝置 - 底部的反重力裝置
        for i in range(3):
            angle = i * (2 * math.pi / 3)
            x = center_x + math.cos(angle) * 60
            y = center_y + math.sin(angle) * 60
            
            # 懸浮裝置基座
            pygame.draw.circle(screen, alien_dark, (int(x), int(y)), 15)
            
            # 能量光束 - 向下發射的反重力光束
            beam_length = 30 + int(pulse_slow * 20)
            beam_surface = pygame.Surface((20, beam_length), pygame.SRCALPHA)
            for j in range(beam_length):
                alpha = 150 - j * 5
                if alpha < 0:
                    alpha = 0
                pygame.draw.line(beam_surface, (alien_glow[0], alien_glow[1], alien_glow[2], alpha), 
                                (10, j), (10, j), 3)
            screen.blit(beam_surface, (int(x) - 10, int(y) + 10))
            
            # 能量核心
            pygame.draw.circle(screen, alien_glow, (int(x), int(y)), 8)
            pygame.draw.circle(screen, alien_core, (int(x), int(y)), 3)
        
        # 7. 繪製觀察窗 - 外星生物觀察窗
        window_y = center_y - 15
        window_width = 70
        window_height = 20
        pygame.draw.ellipse(screen, alien_dark, (center_x - window_width // 2, window_y - window_height // 2, 
                                               window_width, window_height))
        
        # 8. 繪製外星眼睛 - 多個詭異的觀察眼睛
        eye_positions = [(-20, 0), (0, -5), (20, 0)]
        for ex, ey in eye_positions:
            eye_x = center_x + ex
            eye_y = window_y + ey
            eye_size = 6 + int(pulse_fast * 3)
            
            # 眼球
            pygame.draw.circle(screen, (0, 0, 0), (eye_x, eye_y), eye_size)
            
            # 瞳孔 - 垂直橢圓形的外星瞳孔
            pupil_color = (alien_glow[0], alien_glow[1], alien_glow[2])
            pupil_x = eye_x + int(math.sin(self.pulse_timer * 0.5) * 2)  # 瞳孔移動
            pygame.draw.ellipse(screen, pupil_color, (pupil_x - 1, eye_y - 4, 2, 8))
        
        # 9. 繪製科技紋路 - 船體上的神秘紋路
        for i in range(4):
            start_x = center_x - 60 + i * 40
            start_y = center_y + 10
            end_x = start_x + random.randint(-10, 10)
            end_y = start_y + 15
            pygame.draw.line(screen, alien_glow, (start_x, start_y), (end_x, end_y), 2)
        
        # 10. 繪製狀態指示燈
        if self.state == "patrol":
            light_color = (0, 255, 100)  # 綠色
        elif self.state == "tracking":
            light_color = (255, 255, 0)  # 黃色
        else:  # attacking
            light_color = (255, 50, 50)  # 紅色
            
        # 更大的狀態指示燈
        pygame.draw.circle(screen, light_color, (center_x - 30, center_y - 30), 8)
        pygame.draw.circle(screen, light_color, (center_x + 30, center_y - 30), 8)
        
        # 11. 繪製武器系統 - 攻擊狀態時
        if self.state == "attacking":
            # 主武器 - 強大的能量炮
            weapon_length = 80
            weapon_width = 15
            weapon_x = center_x
            weapon_y = center_y - 40
            
            # 武器基座
            pygame.draw.rect(screen, alien_dark, (weapon_x - weapon_width // 2, 
                                                weapon_y - 10, 
                                                weapon_width, 20))
            
            # 能量聚集效果
            charge_radius = 15 + int(pulse_fast * 10)
            charge_surface = pygame.Surface((charge_radius * 2, charge_radius * 2), pygame.SRCALPHA)
            for r in range(charge_radius, 0, -2):
                alpha = 200 - r * 10
                if alpha < 0:
                    alpha = 0
                pygame.draw.circle(charge_surface, (255, 50, 50, alpha), 
                                  (charge_radius, charge_radius), r)
            screen.blit(charge_surface, (weapon_x - charge_radius, weapon_y - charge_radius - 40))
            
            # 雷射光束
            laser_length = 200 + self.laser_jitter
            laser_end_y = weapon_y - laser_length
            
            # 主光束
            pygame.draw.line(screen, (255, 50, 50), (weapon_x, weapon_y - 40), 
                            (weapon_x, laser_end_y), 5)
            
            # 光束光暈
            for i in range(3):
                alpha = 100 - i * 30
                width = 5 + i * 3
                pygame.draw.line(screen, (255, 100, 100, alpha), (weapon_x, weapon_y - 40), 
                                (weapon_x, laser_end_y), width)
                
            # 雷射光點
            impact_surface = pygame.Surface((30, 30), pygame.SRCALPHA)
            pygame.draw.circle(impact_surface, (255, 100, 100, 150), (15, 15), 15)
            screen.blit(impact_surface, (weapon_x - 15, laser_end_y - 15))


    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

class Bullet:
    def __init__(self, x, y, dx, dy):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.radius = 4
        
    def update(self):
        self.x += self.dx
        self.y += self.dy
        
    def draw(self, screen):
        # 發光的紅色能量球
        # 外層光暈
        glow_surface = pygame.Surface((self.radius * 6, self.radius * 6), pygame.SRCALPHA)
        pygame.draw.circle(glow_surface, (255, 0, 0, 50), (self.radius * 3, self.radius * 3), self.radius * 3)
        screen.blit(glow_surface, (self.x - self.radius * 3, self.y - self.radius * 3))
        
        # 核心能量球
        pygame.draw.circle(screen, (255, 100, 100), (int(self.x), int(self.y)), self.radius)
        pygame.draw.circle(screen, (255, 200, 200), (int(self.x), int(self.y)), self.radius // 2)
        
    def is_off_screen(self):
        return (self.x < -50 or self.x > SCREEN_WIDTH + 50 or 
                self.y < -50 or self.y > SCREEN_HEIGHT + 50)
    
    def get_rect(self):
        return pygame.Rect(self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2)

class Prisoner:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
        # 隨機分配敵人原型
        self.archetype = random.choice(['Dimensional Shard', 'Void Goliath', 'Plasma Swarm'])
        
        # 基礎屬性
        base_width = 40
        base_height = 40
        base_speed = 4
        base_health = 30
        
        # 根據原型調整屬性
        if self.archetype == 'Void Goliath': # 原 Brute
            # 虛空巨噬者：巨大、緩慢、極其強韌
            self.width = int(base_width * 1.8)
            self.height = int(base_height * 1.8)
            self.speed = base_speed * 0.65
            self.health = base_health * 2.5
            self.max_health = self.health
        elif self.archetype == 'Plasma Swarm': # 原 Rusher
            # 電漿蜂群：敏捷、高速、脆弱
            self.width = int(base_width * 0.9)
            self.height = int(base_height * 0.9)
            self.speed = base_speed * 1.7
            self.health = base_health * 0.6
            self.max_health = self.health
        else:  # 'Dimensional Shard' (原 Normal)
            # 次元裂隙者：基準屬性
            self.width = base_width
            self.height = base_height
            self.speed = base_speed
            self.health = base_health
            self.max_health = self.health
        
        # 個體差異微調
        self.speed *= random.uniform(0.9, 1.1)
        self.health *= random.uniform(0.9, 1.1)
        self.max_health = self.health
        
        # 用於動畫的計時器
        self.animation_timer = random.uniform(0, 2 * math.pi) # 隨機起始動畫相位
        
    def update(self, player, game_over=False):
        if game_over:
            return
            
        # 更新動畫計時器
        self.animation_timer += 0.1
        
        # 追蹤玩家
        dx = player.x - self.x
        dy = player.y - self.y
        distance = math.sqrt(dx*dx + dy*dy)
        
        if distance > 0:
            self.x += (dx / distance) * self.speed
            self.y += (dy / distance) * self.speed
            
        # 保持在螢幕範圍內
        self.x = max(0, min(SCREEN_WIDTH - self.width, self.x))
        self.y = max(0, min(SCREEN_HEIGHT - self.height, self.y))
    
    def draw(self, screen):
        center_x = self.x + self.width / 2
        center_y = self.y + self.height / 2
        
        # 陰影效果
        shadow_radius = self.width * 0.7
        shadow_surface = pygame.Surface((shadow_radius * 2, shadow_radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(shadow_surface, (0, 0, 0, 70), (shadow_radius, shadow_radius), shadow_radius)
        screen.blit(shadow_surface, (center_x - shadow_radius, center_y + self.height * 0.4 - shadow_radius))


        # --- 根據原型繪製極度誇張的外星生物 ---
        
        if self.archetype == 'Void Goliath':
            # --- 虛空巨噬者 (Brute) ---
            # 蠕動的觸手
            num_tentacles = 6
            for i in range(num_tentacles):
                angle = (i / num_tentacles) * 2 * math.pi + self.animation_timer * 0.5
                # 每條觸手有自己的蠕動頻率
                base_len = self.width * 0.6
                anim_len = math.sin(self.animation_timer * 2 + i) * 15
                tentacle_len = base_len + anim_len
                
                start_pos = (center_x, center_y)
                end_pos = (
                    center_x + math.cos(angle) * tentacle_len,
                    center_y + math.sin(angle) * tentacle_len
                )
                
                mid_offset_angle = angle + math.pi / 2
                mid_offset_mag = math.sin(self.animation_timer * 3 + i * 2) * 20
                mid_pos = (
                    (start_pos[0] + end_pos[0]) / 2 + math.cos(mid_offset_angle) * mid_offset_mag,
                    (start_pos[1] + end_pos[1]) / 2 + math.sin(mid_offset_angle) * mid_offset_mag
                )
                
                # 繪製平滑的曲線觸手
                pygame.draw.line(screen, (50, 20, 80), start_pos, mid_pos, 10)
                pygame.draw.line(screen, (80, 40, 120), mid_pos, end_pos, 8)

            # 黑暗核心
            core_radius = self.width * 0.3 * (1 + 0.05 * math.sin(self.animation_timer))
            pygame.draw.circle(screen, BLACK, (center_x, center_y), core_radius)
            # 核心的紅色威脅光芒
            pygame.draw.circle(screen, (150, 0, 0), (center_x, center_y), core_radius * 0.7, 3)

        elif self.archetype == 'Plasma Swarm':
            # --- 電漿蜂群 (Rusher) ---
            # 主要核心
            core_color = (255, 255, 150)
            core_radius = self.width * 0.4
            # 核心的抖動效果
            core_x = center_x + random.uniform(-2, 2)
            core_y = center_y + random.uniform(-2, 2)
            
            # 核心光暈
            glow_surface = pygame.Surface((core_radius * 4, core_radius * 4), pygame.SRCALPHA)
            pygame.draw.circle(glow_surface, (255, 200, 0, 80), (core_radius * 2, core_radius * 2), core_radius * 2)
            screen.blit(glow_surface, (core_x - core_radius * 2, core_y - core_radius * 2))
            
            pygame.draw.circle(screen, core_color, (core_x, core_y), core_radius)
            
            # 環繞的粒子蜂群
            num_particles = 8
            for i in range(num_particles):
                # 每顆粒子有自己的軌道和速度
                angle = self.animation_timer * (3 + i*0.2) + random.uniform(0, math.pi)
                orbit_radius = self.width * (0.6 + math.sin(angle) * 0.4) + random.uniform(-5, 5)
                
                p_x = core_x + math.cos(angle) * orbit_radius
                p_y = core_y + math.sin(angle) * orbit_radius
                
                # 繪製閃爍的粒子
                particle_size = random.randint(3, 6)
                particle_color = random.choice([(255, 255, 0), (255, 150, 0), (255, 255, 255)])
                pygame.draw.circle(screen, particle_color, (p_x, p_y), particle_size)


        else: # 'Dimensional Shard' (Normal)
            # --- 次元裂隙者 (Normal) ---
            # 繪製不安定的主體多邊形
            num_points = 7
            points = []
            for i in range(num_points):
                angle = (i / num_points) * 2 * math.pi
                # 每個頂點都在不斷變化
                flicker = random.uniform(0.8, 1.2)
                radius = (self.width / 2) * (1 + 0.15 * math.sin(self.animation_timer * 2 + i * 1.5)) * flicker
                px = center_x + math.cos(angle) * radius
                py = center_y + math.sin(angle) * radius
                points.append((px, py))
            
            # 裂隙的顏色和光暈
            main_color = (180, 50, 255)
            line_color = (220, 150, 255)
            pygame.draw.polygon(screen, main_color, points)
            pygame.draw.polygon(screen, line_color, points, 2)

            # 內部星空效果 (隨機點)
            for _ in range(10):
                p = random.choice(points)
                rp_x = center_x + (p[0] - center_x) * random.uniform(0.1, 0.9)
                rp_y = center_y + (p[1] - center_y) * random.uniform(0.1, 0.9)
                pygame.draw.circle(screen, (255, 255, 255), (rp_x, rp_y), 1)

            # 環繞的懸浮水晶碎片
            num_crystals = 3
            for i in range(num_crystals):
                orbit_radius = self.width * 0.8
                angle = self.animation_timer + (i / num_crystals) * 2 * math.pi
                
                cx = center_x + math.cos(angle) * orbit_radius
                cy = center_y + math.sin(angle) * orbit_radius
                
                # 繪製小水晶
                crystal_points = [
                    (cx, cy - 8), (cx - 4, cy), (cx + 4, cy)
                ]
                pygame.draw.polygon(screen, (200, 200, 255), crystal_points)
                
    def take_damage(self, damage):
        self.health -= damage
        if self.health < 0:
            self.health = 0
    
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

class WeaponPickup:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 40
        self.height = 15
        self.pulse_timer = 0
        
    def update(self):
        self.pulse_timer += 0.1
        
    def draw(self, screen):
        # 脈動光暈
        pulse_alpha = int(100 + 50 * math.sin(self.pulse_timer))
        glow_surface = pygame.Surface((60, 35), pygame.SRCALPHA)
        pygame.draw.ellipse(glow_surface, (255, 255, 255, pulse_alpha), (0, 0, 60, 35))
        screen.blit(glow_surface, (self.x - 10, self.y - 10))
        
        # 槍身（深灰色）
        pygame.draw.rect(screen, (60, 60, 60), (self.x, self.y + 5, 35, 8))
        
        # 槍托（黑色）
        pygame.draw.rect(screen, BLACK, (self.x - 5, self.y + 3, 8, 12))
        
        # 握把（黑色）
        pygame.draw.rect(screen, BLACK, (self.x + 15, self.y + 13, 6, 10))
        
        # 彈匣（彎曲）
        pygame.draw.rect(screen, (40, 40, 40), (self.x + 18, self.y + 13, 4, 15))
        
        # 金屬高光
        pygame.draw.line(screen, WHITE, (self.x + 2, self.y + 6), (self.x + 32, self.y + 6), 1)
        
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

class PlayerBullet:
    def __init__(self, x, y, dx, dy):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.width = 6
        self.height = 12
        self.trail = []  # 尾跡粒子
        
    def update(self):
        # 添加當前位置到尾跡
        self.trail.append((self.x, self.y))
        if len(self.trail) > 8:  # 限制尾跡長度
            self.trail.pop(0)
            
        self.x += self.dx
        self.y += self.dy
        
    def draw(self, screen):
        # 繪製尾跡
        for i, (trail_x, trail_y) in enumerate(self.trail):
            alpha = int(255 * (i + 1) / len(self.trail))
            size = int(4 * (i + 1) / len(self.trail))
            
            trail_surface = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
            pygame.draw.circle(trail_surface, (255, 255, 0, alpha), (size, size), size)
            screen.blit(trail_surface, (trail_x - size, trail_y - size))
        
        # 子彈本體（明亮黃色矩形）
        pygame.draw.rect(screen, (255, 255, 0), (self.x - self.width//2, self.y - self.height//2, 
                                                self.width, self.height))
        pygame.draw.rect(screen, (255, 255, 200), (self.x - self.width//2 + 1, self.y - self.height//2 + 1, 
                                                  self.width - 2, self.height - 2))
        
    def is_off_screen(self):
        return (self.x < -50 or self.x > SCREEN_WIDTH + 50 or 
                self.y < -50 or self.y > SCREEN_HEIGHT + 50)
    
    def get_rect(self):
        return pygame.Rect(self.x - self.width//2, self.y - self.height//2, self.width, self.height)

class Building:
    def __init__(self, x, y, building_type):
        self.rect = pygame.Rect(x, y, 200, 200)  # 基礎尺寸
        self.building_type = building_type
        self.is_active = False
        
    def draw(self, surface):
        if self.building_type == "School":
            self.draw_school(surface)
        elif self.building_type == "Park":
            self.draw_park(surface)
        elif self.building_type == "Office":
            self.draw_office(surface)
        elif self.building_type == "Community":
            self.draw_community(surface)
        elif self.building_type == "Military":
            self.draw_military(surface)
            
        # 繪製「已檢查」狀態
        if self.is_active:
            self.draw_active_indicator(surface)
    
    def draw_school(self, surface):
        x, y = self.rect.topleft
        
        # 陰影面 (後層)
        pygame.draw.rect(surface, (139, 0, 0), (x + 5, y + 5, 150, 100))
        
        # 受光面 (前層)
        pygame.draw.rect(surface, (205, 92, 92), (x, y, 145, 100))
        
        # 屋頂
        pygame.draw.rect(surface, (105, 105, 105), (x - 5, y - 20, 165, 25))
        
        # 窗戶 - 2排4個
        for row in range(2):
            for col in range(4):
                window_x = x + 15 + col * 30
                window_y = y + 15 + row * 35
                # 窗戶框架
                pygame.draw.rect(surface, (173, 216, 230), (window_x, window_y, 15, 25))
                # 十字窗框
                pygame.draw.line(surface, WHITE, (window_x + 7, window_y), (window_x + 7, window_y + 25), 2)
                pygame.draw.line(surface, WHITE, (window_x, window_y + 12), (window_x + 15, window_y + 12), 2)
        
        # 大門
        pygame.draw.rect(surface, (139, 69, 19), (x + 60, y + 70, 25, 30))
        
        # 旗桿
        pygame.draw.line(surface, (192, 192, 192), (x + 160, y - 50), (x + 160, y + 10), 2)
        # 旗幟
        pygame.draw.rect(surface, (255, 0, 0), (x + 160, y - 50, 15, 10))
    
    def draw_park(self, surface):
        x, y = self.rect.topleft
        
        # 草地 - 不規則多邊形
        grass_points = [
            (x, y + 20), (x + 50, y), (x + 120, y + 10), (x + 200, y + 30),
            (x + 190, y + 100), (x + 150, y + 150), (x + 80, y + 140), (x + 20, y + 120)
        ]
        pygame.draw.polygon(surface, (144, 238, 144), grass_points)
        
        # 小徑
        path_points = [(x + 20, y + 140), (x + 60, y + 100), (x + 120, y + 80), (x + 160, y + 50), (x + 180, y + 20)]
        pygame.draw.lines(surface, (245, 222, 179), False, path_points, 8)
        
        # 樹木
        tree_positions = [(x + 40, y + 60), (x + 100, y + 40), (x + 140, y + 100), (x + 60, y + 120)]
        for tree_x, tree_y in tree_positions:
            # 樹幹
            pygame.draw.rect(surface, (139, 69, 19), (tree_x, tree_y, 10, 30))
            # 樹冠
            pygame.draw.circle(surface, (0, 100, 0), (tree_x + 5, tree_y), 15)
        
        # 池塘
        pygame.draw.ellipse(surface, (0, 191, 255), (x + 120, y + 110, 50, 30))
        
        # 花圃
        pygame.draw.rect(surface, (160, 82, 45), (x + 30, y + 30, 40, 20), border_radius=5)
        # 花朵
        flower_colors = [(255, 0, 0), (255, 255, 0), (255, 192, 203)]
        for _ in range(12):
            flower_x = x + 32 + random.randint(0, 36)
            flower_y = y + 32 + random.randint(0, 16)
            color = random.choice(flower_colors)
            pygame.draw.circle(surface, color, (flower_x, flower_y), 3)
    
    def draw_office(self, surface):
        x, y = self.rect.topleft
        
        # 主體框架
        pygame.draw.rect(surface, (47, 79, 79), (x, y, 80, 250))
        
        # 玻璃帷幕 - 網格燈光
        for row in range(16):  # 250/15 ≈ 16
            for col in range(8):  # 80/10 = 8
                cell_x = x + col * 10
                cell_y = y + row * 15
                if random.random() > 0.5:
                    # 亮燈
                    pygame.draw.rect(surface, (255, 255, 153), (cell_x, cell_y, 10, 15))
                else:
                    # 關燈
                    pygame.draw.rect(surface, (70, 130, 180), (cell_x, cell_y, 10, 15))
        
        # 天線
        pygame.draw.line(surface, WHITE, (x + 40, y - 40), (x + 40, y), 3)
        
        # 警示燈 - 閃爍效果
        if pygame.time.get_ticks() % 1000 > 500:
            pygame.draw.circle(surface, (255, 0, 0), (x + 40, y - 40), 5)
    
    def draw_community(self, surface):
        x, y = self.rect.topleft
        
        # 3棟小房子
        house_colors = [(245, 245, 220), (255, 250, 205)]
        house_positions = [(x + 20, y + 50), (x + 100, y + 80), (x + 160, y + 40)]
        
        for i, (house_x, house_y) in enumerate(house_positions):
            # 牆體
            wall_color = random.choice(house_colors)
            pygame.draw.rect(surface, wall_color, (house_x, house_y, 50, 40))
            
            # 屋頂 - 三角形
            roof_points = [(house_x - 5, house_y), (house_x + 55, house_y), (house_x + 25, house_y - 20)]
            pygame.draw.polygon(surface, (255, 69, 0), roof_points)
            
            # 門
            pygame.draw.rect(surface, (139, 69, 19), (house_x + 20, house_y + 25, 10, 15))
            
            # 窗戶
            pygame.draw.rect(surface, (173, 216, 230), (house_x + 5, house_y + 10, 10, 10))
            pygame.draw.rect(surface, (173, 216, 230), (house_x + 35, house_y + 10, 10, 10))
        
        # 灌木
        bush_positions = [(x + 80, y + 130), (x + 140, y + 120), (x + 60, y + 140), (x + 180, y + 100)]
        for bush_x, bush_y in bush_positions:
            pygame.draw.circle(surface, (34, 139, 34), (bush_x, bush_y), 15)
    
    def draw_military(self, surface):
        x, y = self.rect.topleft
        
        # 主堡壘
        pygame.draw.rect(surface, (112, 128, 144), (x, y, 180, 100))
        
        # 迷彩圖案
        camo_colors = [(85, 107, 47), (193, 154, 107)]
        for _ in range(4):
            color = random.choice(camo_colors)
            # 隨機多邊形
            points = []
            for _ in range(6):
                px = x + random.randint(10, 170)
                py = y + random.randint(10, 90)
                points.append((px, py))
            pygame.draw.polygon(surface, color, points)
        
        # 圍牆 - 柵欄
        fence_positions = list(range(x - 20, x + 200, 15))
        for fence_x in fence_positions:
            # 垂直線
            pygame.draw.line(surface, (105, 105, 105), (fence_x, y - 10), (fence_x, y + 110), 4)
            # 尖刺三角形
            spike_points = [(fence_x - 3, y - 10), (fence_x + 3, y - 10), (fence_x, y - 15)]
            pygame.draw.polygon(surface, (105, 105, 105), spike_points)
        
        # 停機坪
        pygame.draw.circle(surface, (105, 105, 105), (x + 140, y + 140), 30)
        # H標記
        pygame.draw.line(surface, WHITE, (x + 130, y + 130), (x + 130, y + 150), 8)
        pygame.draw.line(surface, WHITE, (x + 150, y + 130), (x + 150, y + 150), 8)
        pygame.draw.line(surface, WHITE, (x + 130, y + 140), (x + 150, y + 140), 8)
        
        # 瞭望塔
        pygame.draw.rect(surface, (105, 105, 105), (x + 200, y + 40, 15, 60))
        pygame.draw.rect(surface, (105, 105, 105), (x + 195, y + 25, 25, 15))
    
    def draw_active_indicator(self, surface):
        # 半透明綠色光環
        center_x = self.rect.centerx
        center_y = self.rect.centery
        radius = self.rect.width // 2
        
        # 創建透明表面
        indicator_surface = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
        
        # 畫外圓
        pygame.draw.circle(indicator_surface, (0, 255, 0, 128), (radius, radius), radius)
        # 畫內圓（創造圓環效果）
        pygame.draw.circle(indicator_surface, (0, 0, 0, 0), (radius, radius), radius - 20)
        
        # 將指示器繪製到主表面
        surface.blit(indicator_surface, (center_x - radius, center_y - radius))

def draw_background_level1(screen):
    # 填充草地背景
    screen.fill(GRASS_GREEN)
    
    # 計算道路位置（Y軸中央）
    road_y = SCREEN_HEIGHT // 2 - 100  # 200像素寬度的一半
    
    # 繪製人行道（上下兩條）
    pygame.draw.rect(screen, SIDEWALK_GRAY, (0, road_y - 30, SCREEN_WIDTH, 30))  # 上人行道
    pygame.draw.rect(screen, SIDEWALK_GRAY, (0, road_y + 200, SCREEN_WIDTH, 30))  # 下人行道
    
    # 繪製馬路
    pygame.draw.rect(screen, ROAD_GRAY, (0, road_y, SCREEN_WIDTH, 200))
    
    # 繪製道路中線
    for x in range(0, SCREEN_WIDTH, 40):
        pygame.draw.rect(screen, WHITE, (x, road_y + 95, 20, 10))

def draw_background_level2(screen):
    # 監獄場景背景
    
    # 深灰色石磚地板
    brick_size = 40
    for y in range(0, SCREEN_HEIGHT, brick_size):
        for x in range(0, SCREEN_WIDTH, brick_size):
            # 隨機變化的深灰色
            gray_val = random.randint(50, 65)
            brick_color = (gray_val, gray_val, gray_val + 5)
            pygame.draw.rect(screen, brick_color, (x, y, brick_size, brick_size))
            
            # 黑色縫隙
            pygame.draw.rect(screen, BLACK, (x, y, brick_size, brick_size), 1)
    
    # 隨機水漬
    for _ in range(15):
        stain_x = random.randint(0, SCREEN_WIDTH - 50)
        stain_y = random.randint(0, SCREEN_HEIGHT - 30)
        stain_surface = pygame.Surface((50, 30), pygame.SRCALPHA)
        pygame.draw.ellipse(stain_surface, (20, 20, 25, 120), (0, 0, 50, 30))
        screen.blit(stain_surface, (stain_x, stain_y))
    
    # 地板裂縫
    for _ in range(8):
        crack_start_x = random.randint(0, SCREEN_WIDTH)
        crack_start_y = random.randint(0, SCREEN_HEIGHT)
        crack_points = [(crack_start_x, crack_start_y)]
        
        for i in range(5):
            next_x = crack_points[-1][0] + random.randint(-30, 30)
            next_y = crack_points[-1][1] + random.randint(-20, 20)
            crack_points.append((next_x, next_y))
        
        if len(crack_points) > 1:
            pygame.draw.lines(screen, (30, 30, 30), False, crack_points, 2)
    
    # 上下牆壁與鐵欄杆
    wall_height = 80
    
    # 上牆壁
    pygame.draw.rect(screen, (40, 40, 45), (0, 0, SCREEN_WIDTH, wall_height))
    # 下牆壁
    pygame.draw.rect(screen, (40, 40, 45), (0, SCREEN_HEIGHT - wall_height, SCREEN_WIDTH, wall_height))
    
    # 鐵欄杆
    bar_spacing = 30
    for x in range(0, SCREEN_WIDTH, bar_spacing):
        # 上方鐵欄杆
        pygame.draw.rect(screen, BLACK, (x, 20, 8, wall_height - 40))
        # 鏽跡
        pygame.draw.circle(screen, (139, 69, 19), (x + 4, 30 + random.randint(0, 20)), 2)
        
        # 下方鐵欄杆
        pygame.draw.rect(screen, BLACK, (x, SCREEN_HEIGHT - wall_height + 20, 8, wall_height - 40))
        # 鏽跡
        pygame.draw.circle(screen, (139, 69, 19), (x + 4, SCREEN_HEIGHT - 50 + random.randint(0, 20)), 2)
    
    # 陰影入口（敵人生成點）
    shadow_positions = [(100, 10), (500, 10), (900, 10), (1300, 10), (1700, 10),
                       (100, SCREEN_HEIGHT - 70), (500, SCREEN_HEIGHT - 70), 
                       (900, SCREEN_HEIGHT - 70), (1300, SCREEN_HEIGHT - 70)]
    
    for shadow_x, shadow_y in shadow_positions:
        shadow_surface = pygame.Surface((80, 60), pygame.SRCALPHA)
        pygame.draw.ellipse(shadow_surface, (0, 0, 0, 180), (0, 0, 80, 60))
        screen.blit(shadow_surface, (shadow_x, shadow_y))
    
    # 探照燈光束
    time_factor = pygame.time.get_ticks() * 0.001
    
    # 左上角探照燈
    beam_angle = math.sin(time_factor) * 30
    beam_center_x = 200 + math.sin(time_factor * 0.5) * 100
    beam_center_y = 300
    
    beam_surface = pygame.Surface((400, 600), pygame.SRCALPHA)
    beam_points = [
        (50, 50),
        (beam_center_x - 100, beam_center_y),
        (beam_center_x + 100, beam_center_y),
        (beam_center_x + 80, beam_center_y + 200),
        (beam_center_x - 80, beam_center_y + 200)
    ]
    
    if len(beam_points) >= 3:
        pygame.draw.polygon(beam_surface, (255, 255, 150, 40), beam_points)
        screen.blit(beam_surface, (0, 0))
    
    # 右下角探照燈
    beam_angle2 = math.sin(time_factor + math.pi) * 25
    beam_center_x2 = SCREEN_WIDTH - 300 + math.sin(time_factor * 0.7) * 80
    beam_center_y2 = SCREEN_HEIGHT - 400
    
    beam_surface2 = pygame.Surface((400, 600), pygame.SRCALPHA)
    beam_points2 = [
        (350, 550),
        (beam_center_x2 - SCREEN_WIDTH + 400 - 80, beam_center_y2 - SCREEN_HEIGHT + 600),
        (beam_center_x2 - SCREEN_WIDTH + 400 + 80, beam_center_y2 - SCREEN_HEIGHT + 600),
        (beam_center_x2 - SCREEN_WIDTH + 400 + 60, beam_center_y2 - SCREEN_HEIGHT + 600 - 150),
        (beam_center_x2 - SCREEN_WIDTH + 400 - 60, beam_center_y2 - SCREEN_HEIGHT + 600 - 150)
    ]
    
    if len(beam_points2) >= 3:
        pygame.draw.polygon(beam_surface2, (255, 255, 150, 30), beam_points2)
        screen.blit(beam_surface2, (SCREEN_WIDTH - 400, SCREEN_HEIGHT - 600))

def draw_health_bar(screen, player, font):
    # 健康條位置（右下角）
    bar_width = 200
    bar_height = 20
    bar_x = SCREEN_WIDTH - bar_width - 20
    bar_y = SCREEN_HEIGHT - bar_height - 60
    
    # 背景條（深紅色）
    pygame.draw.rect(screen, (100, 0, 0), (bar_x, bar_y, bar_width, bar_height))
    
    # 前景條（綠色，寬度與生命值聯動）
    health_percentage = player.health / player.max_health
    health_width = int(bar_width * health_percentage)
    
    # 根據生命值改變顏色
    if health_percentage > 0.6:
        health_color = (0, 255, 0)  # 綠色
    elif health_percentage > 0.3:
        health_color = (255, 255, 0)  # 黃色
    else:
        health_color = (255, 0, 0)  # 紅色
        
    pygame.draw.rect(screen, health_color, (bar_x, bar_y, health_width, bar_height))
    
    # 邊框
    pygame.draw.rect(screen, WHITE, (bar_x, bar_y, bar_width, bar_height), 2)
    
    # HP 文字
    hp_text = font.render(f"HP: {player.health}", True, WHITE)
    screen.blit(hp_text, (bar_x, bar_y - 30))

def load_level(level_number, player):
    """加載指定關卡"""
    if level_number == 1:
        # 第一關：城市巡邏
        buildings = [
            Building(200, 100, "School"),
            Building(600, 150, "Park"),
            Building(1200, 50, "Office"),
            Building(300, 700, "Community"),
            Building(1400, 650, "Military")
        ]
        
        enemies = [
            Enemy_big(800, 300),
            Enemy(800, 400),
            Enemy(700, 300),
            Enemy(900, 300),
            Enemy(800, 1100),
            Enemy(1500, 800)
        ]
        
        prisoners = []
        weapon_pickups = []
        
        # 重置玩家位置和狀態
        player.x = 100
        player.y = SCREEN_HEIGHT // 2 - 15
        player.health = 100
        player.has_gun = False
        
        return buildings, enemies, prisoners, weapon_pickups
        
    elif level_number == 2:
        # 第二關：監獄突破
        buildings = []  # 第二關沒有建築物
        enemies = [Enemy(800, 400),]    # 第二關沒有無人機
        
        # 創建囚犯
        prisoners = [
            Prisoner(200, 150),
            Prisoner(400, 200),
            Prisoner(600, 180),
            Prisoner(800, 220),
            #Prisoner(1000, 160),
            #Prisoner(1200, 190),
            #Prisoner(1400, 170),
            #Prisoner(1600, 200),
            #Prisoner(300, 800),
            #Prisoner(500, 850),
            #Prisoner(700, 820),
            #Prisoner(900, 880),
            #Prisoner(1100, 840),
            #Prisoner(1300, 860)
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
    
    return [], [], [], []

def main():
    # 創建遊戲視窗
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("城市守護者：精確巡邏")
    clock = pygame.time.Clock()
    
    # 創建字體 - 使用支持中文的字體
    try:
        font_ui = pygame.font.Font("C:\\Windows\\Fonts\\simsun.ttc", 50)
        font_victory = pygame.font.Font("C:\\Windows\\Fonts\\simsun.ttc", 120)
        font_defeat = pygame.font.Font("C:\\Windows\\Fonts\\simsun.ttc", 120)
        font_transition = pygame.font.Font("C:\\Windows\\Fonts\\simsun.ttc", 80)
    except:
        # 如果無法加載中文字體，則使用默認字體
        font_ui = pygame.font.Font(None, 50)
        font_victory = pygame.font.Font(None, 120)
        font_defeat = pygame.font.Font(None, 120)
        font_transition = pygame.font.Font(None, 80)
    
    # 創建玩家
    player = Player(100, SCREEN_HEIGHT // 2 - 15)
    
    # 創建變身系統
    transformation_system = TransformationSystem()
    
    # 關卡管理
    current_level = 1
    buildings, enemies, prisoners, weapon_pickups = load_level(current_level, player)
    
    # 子彈列表
    bullets = []
    player_bullets = []
    
    # 遊戲狀態
    game_won = False
    game_lost = False
    level_transition = False
    transition_timer = 0
    
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
            # 處理變身系統輸入
            transformation_system.handle_input(event)
            
            # 處理遊戲勝利後進入第三關
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN and game_won and current_level == 2:
                # 啟動第三關
                import subprocess
                pygame.quit()
                subprocess.run([sys.executable, "level3_battlefield_reversal.py"])
                running = False
        
        # 獲取按鍵狀態
        keys = pygame.key.get_pressed()
        
        # 檢查失敗條件
        if player.health <= 0:
            game_lost = True
        
        # 處理關卡轉換
        if level_transition:
            transition_timer -= 1
            if transition_timer <= 0:
                level_transition = False
                current_level = 2
                buildings, enemies, prisoners, weapon_pickups = load_level(current_level, player)
                bullets.clear()
                player_bullets.clear()
        
        # 更新遊戲邏輯
        game_over = game_won or game_lost
        
        # 檢查是否需要暫停遊戲（確認對話框或問題顯示時）
        game_paused = transformation_system.confirmation_active or transformation_system.question_active
        
        if not game_over and not level_transition and not game_paused:
            # 更新變身系統
            transformation_system.update(dt)
            
            # 更新玩家
            player.update(keys, game_over, player_bullets, transformation_system)
            
            # 更新敵人（第一關）
            for enemy in enemies:
                enemy.update(player, bullets, game_over)
            
            # 更新囚犯（第二關）
            for prisoner in prisoners[:]:
                prisoner.update(player, game_over)
                
                # 檢查囚犯與玩家的碰撞（近戰傷害）
                if prisoner.get_rect().colliderect(player.get_rect()):
                    player.take_damage(5)
            
            # 更新武器拾取點
            for weapon in weapon_pickups[:]:
                weapon.update()
                if weapon.get_rect().colliderect(player.get_rect()):
                    player.has_gun = True
                    weapon_pickups.remove(weapon)
            
            # 更新敵人子彈
            for bullet in bullets[:]:
                bullet.update()
                if bullet.is_off_screen():
                    bullets.remove(bullet)
            
            # 更新玩家子彈
            for bullet in player_bullets[:]:
                bullet.update()
                if bullet.is_off_screen():
                    player_bullets.remove(bullet)
            
            # 檢查敵人子彈與玩家的碰撞
            player_rect = player.get_rect()
            for bullet in bullets[:]:
                if player_rect.colliderect(bullet.get_rect()):
                    player.take_damage(5)
                    bullets.remove(bullet)
            
            # 檢查玩家子彈與囚犯的碰撞
            for bullet in player_bullets[:]:
                for prisoner in prisoners[:]:
                    if bullet.get_rect().colliderect(prisoner.get_rect()):
                        prisoner.take_damage(30)
                        player_bullets.remove(bullet)
                        if prisoner.health <= 0:
                            prisoners.remove(prisoner)
                        break
            
            # 第一關邏輯
            if current_level == 1:
                # 檢查玩家與建築物的碰撞
                for building in buildings:
                    if not building.is_active and player_rect.colliderect(building.rect):
                        building.is_active = True
                
                # 檢查第一關勝利條件
                active_count = sum(1 for building in buildings if building.is_active)
                if active_count == len(buildings):
                    level_transition = True
                    transition_timer = 180  # 3秒轉換時間
            
            # 第二關邏輯
            elif current_level == 2:
                # 檢查第二關勝利條件
                if len(prisoners) == 0:
                    game_won = True
        
        # 繪製畫面
        if current_level == 1:
            draw_background_level1(screen)
        elif current_level == 2:
            draw_background_level2(screen)
        
        # 繪製建築物（第一關）
        for building in buildings:
            building.draw(screen)
        
        # 繪製敵人（第一關）
        for enemy in enemies:
            enemy.draw(screen, player)
        
        # 繪製囚犯（第二關）
        for prisoner in prisoners:
            prisoner.draw(screen)
        
        # 繪製武器拾取點
        for weapon in weapon_pickups:
            weapon.draw(screen)
        
        # 繪製子彈
        for bullet in bullets:
            bullet.draw(screen)
        
        # 繪製玩家子彈
        for bullet in player_bullets:
            bullet.draw(screen)
        
        # 繪製玩家
        player.draw(screen)
        
        # 繪製UI
        if current_level == 1:
            active_count = sum(1 for building in buildings if building.is_active)
            progress_text = font_ui.render(f"巡邏進度: {active_count} / {len(buildings)}", True, WHITE)
            screen.blit(progress_text, (20, 20))
        elif current_level == 2:
            enemies_left = len(prisoners)
            progress_text = font_ui.render(f"剩餘囚犯: {enemies_left}", True, WHITE)
            screen.blit(progress_text, (20, 20))
            
            # 武器狀態
            if player.has_gun:
                weapon_text = font_ui.render("武器: 突擊步槍 [空白鍵射擊]", True, WHITE)
                screen.blit(weapon_text, (20, 70))
            else:
                weapon_text = font_ui.render("尋找武器！", True, (255, 255, 0))
                screen.blit(weapon_text, (20, 70))
        
        # 繪製健康條
        draw_health_bar(screen, player, font_ui)
        
        # 繪製變身系統UI
        transformation_system.draw_ui(screen)
        
        # 繪製關卡轉換畫面
        if level_transition:
            transition_bg = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            transition_bg.fill((0, 0, 0, 150))
            screen.blit(transition_bg, (0, 0))
            
            transition_text1 = font_transition.render("LEVEL 1 CLEARED!", True, (0, 255, 0))
            transition_text2 = font_transition.render("ENTERING PRISON COMPLEX...", True, WHITE)
            
            text_rect1 = transition_text1.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
            text_rect2 = transition_text2.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
            
            screen.blit(transition_text1, text_rect1)
            screen.blit(transition_text2, text_rect2)
        
        # 繪製勝利畫面
        if game_won:
            if current_level == 2:
                victory_text = font_victory.render("LEVEL 2 CLEARED!", True, (0, 255, 0))
                victory_text2 = font_ui.render("按 ENTER 進入第三關：逆轉戰場", True, WHITE)
            else:
                victory_text = font_victory.render("城市巡邏完成！", True, WHITE)
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
        
        # 繪製失敗畫面
        if game_lost:
            defeat_text = font_defeat.render("任務失敗！車輛損毀！", True, (255, 0, 0))
            text_rect = defeat_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            
            # 失敗背景
            defeat_bg = pygame.Surface((text_rect.width + 40, text_rect.height + 20), pygame.SRCALPHA)
            defeat_bg.fill((0, 0, 0, 200))
            screen.blit(defeat_bg, (text_rect.x - 20, text_rect.y - 10))
            
            screen.blit(defeat_text, text_rect)
        
        # 更新顯示
        pygame.display.flip()
        clock.tick(60)  # 60 FPS
    
    # 退出遊戲
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()