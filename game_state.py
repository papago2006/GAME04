# 遊戲狀態管理
class GameState:
    def __init__(self):
        self.current_level = 1
        self.game_won = False
        self.game_lost = False
        self.level_transition = False
        self.transition_timer = 0
        self.game_paused = False
        
    def start_level_transition(self, duration=180):
        """開始關卡轉換"""
        self.level_transition = True
        self.transition_timer = duration
        
    def update_transition(self):
        """更新轉換狀態"""
        if self.level_transition:
            self.transition_timer -= 1
            if self.transition_timer <= 0:
                self.level_transition = False
                self.current_level = 2
                return True
        return False
        
    def set_victory(self):
        """設定勝利狀態"""
        self.game_won = True
        
    def set_defeat(self):
        """設定失敗狀態"""
        self.game_lost = True
        
    def is_game_over(self):
        """檢查遊戲是否結束"""
        return self.game_won or self.game_lost
        
    def set_paused(self, paused):
        """設定暫停狀態"""
        self.game_paused = paused
        
    def should_update_game(self):
        """檢查是否應該更新遊戲邏輯"""
        return not (self.is_game_over() or self.level_transition or self.game_paused)