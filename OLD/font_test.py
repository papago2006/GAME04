import pygame
import sys

# 初始化 Pygame
pygame.init()

# 設定
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

def main():
    # 創建遊戲視窗
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("中文字體測試")
    
    # 嘗試加載中文字體
    try:
        font = pygame.font.Font("C:\\Windows\\Fonts\\simsun.ttc", 36)
        font_status = "成功加載中文字體"
    except:
        font = pygame.font.Font(None, 36)
        font_status = "無法加載中文字體，使用默認字體"
    
    # 測試文字
    test_texts = [
        "這是中文測試文字",
        "變身系統啟動",
        "按 Y 確認 / 按 N 取消",
        "變身系統即將啟動！",
        "你需要回答一個英文問題來完成變身。",
        "準備好了嗎？"
    ]
    
    # 遊戲主迴圈
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # 繪製
        screen.fill(WHITE)
        
        # 顯示字體狀態
        status_surface = font.render(font_status, True, BLACK)
        screen.blit(status_surface, (50, 50))
        
        # 顯示測試文字
        for i, text in enumerate(test_texts):
            text_surface = font.render(text, True, BLACK)
            screen.blit(text_surface, (50, 100 + i * 50))
        
        # 顯示退出提示
        exit_text = font.render("按 ESC 鍵退出", True, BLACK)
        screen.blit(exit_text, (50, SCREEN_HEIGHT - 50))
        
        # 檢查 ESC 鍵
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            running = False
        
        pygame.display.flip()
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()