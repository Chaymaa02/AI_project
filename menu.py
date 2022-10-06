import pygame

def draw_text(screen, text, font, text_col, x, y):
  img = font.render(text, True, text_col)
  screen.blit(img, (x, y))

#menu class
class Menu():
    def __init__(self, screen):
        self.game_paused = True
        self.menu_state = "main"
        self.screen = screen
        #define fonts
        self.font = pygame.font.SysFont("arialblack", 40)
        #define colours
        self.TEXT_COL = (255, 255, 255)

    
    def draw(self):
        self.screen.fill((52, 78, 91))

        #check menu state
        if self.menu_state == "main":
            #draw pause screen buttons
            if resume_button.draw(self.screen):
                self.game_paused = False
            if options_button.draw(self.screen):
                self.menu_state = "options"
            if quit_button.draw(self.screen):
                run = False
        #check if the options menu is open
        if self.menu_state == "options":
            #draw the different options buttons
            if video_button.draw(self.screen):
                print("Video Settings")
            if audio_button.draw(self.screen):
                print("Audio Settings")
            if keys_button.draw(self.screen):
                print("Change Key Bindings")
            if back_button.draw(self.screen):
                self.menu_state = "main"
        else:
            draw_text("Press SPACE to pause", self.font, self.TEXT_COL, SCREEN_WIDTH/2, SCREEN_HEIGHT*0.1)