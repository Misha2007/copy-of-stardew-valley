import pygame, sys
from settings import *
from level import Level
from button import Button

class Game:
    def __init__(self):
        pygame.init()
        self.music_on = False
        self.sound_on = False
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.level = Level(self.music_on)

    def get_font(self, size): # Returns Press-Start-2P in the desired size
        return pygame.font.Font("graphics/font.ttf", size)
 
    def run(self):  
        paused = False
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE and self.level.esc_avaible:
                        paused = True

            dt = self.clock.tick() / 1000
            self.level.run(dt, self.music_on)
            pygame.display.update()
            while paused:
                self.main_menu()
                paused = False

    def options(self):
        BG = pygame.image.load("./graphics/Background.png")
        while True:
            self.screen.blit(BG, (0, 0))

            MENU_MOUSE_POS = pygame.mouse.get_pos()

            MENU_TEXT = self.get_font(100).render("MAIN MENU", True, "#b68f40")
            MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))

            PLAY_BUTTON = Button(image=pygame.image.load("./graphics/Play Rect.png"), pos=(640, 250), 
                                text_input="Sound", font=self.get_font(75), base_color="#d7fcd4", hovering_color="White")
            SWITCH_ON = Button(image= pygame.transform.scale(pygame.image.load("./graphics/switch-on.png"), (150,150)), pos=(800, 250), 
                                text_input="", font=self.get_font(75), base_color="#d7fcd4", hovering_color="White")
            SWITCH_Off = Button(image= pygame.transform.scale(pygame.image.load("./graphics/switch-off.png"), (150,150)), pos=(800, 250), 
                                text_input="", font=self.get_font(75), base_color="#d7fcd4", hovering_color="White")
            OPTIONS_BUTTON = Button(image=pygame.image.load("graphics/Play Rect.png"), pos=(640, 400), 
                                text_input="Music", font=self.get_font(75), base_color="#d7fcd4", hovering_color="White")
            # SWITCH_Off = Button(image= pygame.transform.scale(pygame.image.load("./graphics/switch-on.png"), (150,150)), pos=(800, 250), 
            #                     text_input="", font=self.get_font(75), base_color="#d7fcd4", hovering_color="White")
            BACK_BUTTON = Button(image=pygame.image.load("graphics/Quit Rect.png"), pos=(640, 550), 
                                text_input="Back", font=self.get_font(75), base_color="#d7fcd4", hovering_color="White")
            
            # SWITCH = SWITCH_ON

            self.screen.blit(MENU_TEXT, MENU_RECT)
            # SWITCH = SWITCH_ON

            for button in [PLAY_BUTTON, OPTIONS_BUTTON, BACK_BUTTON]:
                button.changeColor(MENU_MOUSE_POS)
                button.update(self.screen)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                        self.sound_on = not self.sound_on
                        if self.sound_on:
                            # self.level.tree_sprites.sprites()[0].axe_sound.set_volume(0)
                            self.level.player.watering.set_volume(0)
                            self.level.soil_layer.hoe_sound.set_volume(0)
                            self.level.soil_layer.plant_sound.set_volume(0)
                        else:
                            self.level.player.watering.set_volume(0.2)
                            self.level.soil_layer.hoe_sound.set_volume(0.4)
                            self.level.soil_layer.plant_sound.set_volume(0.3)
                    if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                        self.music_on = not self.music_on
                        if self.music_on:
                            self.level.music.set_volume(0)
                        else:
                            self.level.music.set_volume(0.3)
                    if BACK_BUTTON.checkForInput(MENU_MOUSE_POS):
                        self.main_menu()

            pygame.display.update()

    def main_menu(self):
        # button = Button()
        BG = pygame.image.load("./graphics/Background.png")
        while True:
            self.screen.blit(BG, (0, 0))

            MENU_MOUSE_POS = pygame.mouse.get_pos()

            MENU_TEXT = self.get_font(100).render("MAIN MENU", True, "#b68f40")
            MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))

            PLAY_BUTTON = Button(image=pygame.image.load("./graphics/Play Rect.png"), pos=(640, 250), 
                                text_input="PLAY", font=self.get_font(75), base_color="#d7fcd4", hovering_color="White")
            OPTIONS_BUTTON = Button(image=pygame.image.load("graphics/Options Rect.png"), pos=(640, 400), 
                                text_input="OPTIONS", font=self.get_font(75), base_color="#d7fcd4", hovering_color="White")
            QUIT_BUTTON = Button(image=pygame.image.load("graphics/Quit Rect.png"), pos=(640, 550), 
                                text_input="QUIT", font=self.get_font(75), base_color="#d7fcd4", hovering_color="White")

            self.screen.blit(MENU_TEXT, MENU_RECT)

            for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
                button.changeColor(MENU_MOUSE_POS)
                button.update(self.screen)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                        self.run()
                    if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                        self.options()
                    if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                        pygame.quit()
                        sys.exit()

            pygame.display.update()

if __name__ == '__main__':
    game = Game()
    game.main_menu()
    # game.run()