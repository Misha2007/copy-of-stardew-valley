import pygame
from settings import *
from timer import Timer

class Menu:
    def __init__(self, player, toggle_menu):
        # setup
        self.player = player
        self.toggle_menu = toggle_menu
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font('font/LycheeSoda.ttf', 30)

        # options
        self.width = 400
        self.space = 10
        self.padding = 8

        # entries
        self.options = list(self.player.item_inventory.keys()) + list(self.player.seed_inventory.keys())
        self.sell_border = len(self.player.item_inventory) -1
        self.setup()

        # movement
        self.index = 0
        self.timer = Timer(200)

        # buy / sell text surface
        self.buy_text = self.font.render('buy', False, 'Black')
        self.sell_text = self.font.render('sell', False, 'Black')

    def display_money(self):
        text_surface = self.font.render(f'${self.player.money}', False, 'Black')
        text_rect = text_surface.get_rect(midbottom = (SCREEN_WIDTH / 2, SCREEN_HEIGHT - 20))

        pygame.draw.rect(self.display_surface, 'White', text_rect.inflate(10,10),0,6)
        self.display_surface.blit(text_surface, text_rect)

    def setup(self):
        # create the text surfaces
        self.text_surfs = []
        self.total_height = 0
        for item in self.options:
            text_surf = self.font.render(str(item) + ' seeds' if item in list(self.player.seed_inventory.keys()) and len(self.text_surfs) >= len(list(self.player.item_inventory.keys())) else item, False, 'Black')
            self.text_surfs.append(text_surf)
            self.total_height += text_surf.get_height() + (self.padding * 2)

        self.total_height += (len(self.text_surfs) - 1) * self.space
        self.menu_top = SCREEN_HEIGHT / 2 - self.total_height / 2
        self.main_rect = pygame.Rect(SCREEN_WIDTH / 2 - self.width / 2,self.menu_top, self.width,self.total_height)

    def input(self):
        keys = pygame.key.get_pressed()
        self.timer.update()

        if keys[pygame.K_ESCAPE]:
            self.toggle_menu()

        if not self.timer.active:
            if keys[pygame.K_UP]:
                self.index -= 1
                self.timer.activate()
            if keys[pygame.K_DOWN]:
                self.index += 1
                self.timer.activate()

            if keys[pygame.K_SPACE]:
                self.timer.activate()

                # get item
                current_item = self.options[self.index]
                file1 = open("mon.txt", "w")
                file = open("wood.txt", "w")
                file2 = open("fish.txt", "w")

                # sell
                if self.index <= self.sell_border:
                    if self.player.item_inventory[current_item] > 0:
                        self.player.item_inventory[current_item] -= 1
                        self.player.money += SALE_PRICES[current_item]

                        file1.write(str(self.player.money))
                        file2.write(str(self.player.item_inventory['fish']))

                # buy
                else:
                    seed_prices = PURCHES_PRICES[current_item]
                    if self.player.money >= seed_prices:
                        self.player.seed_inventory[current_item] += 1
                        self.player.money -= PURCHES_PRICES[current_item]
                        text = [
                            str(self.player.seed_inventory['corn']) + '\n',
                            str(self.player.seed_inventory['tomato']) + '\n',
                            str(self.player.seed_inventory['wheat']) + '\n'
                        ]

                        file.writelines(text)

                        file1.write(str(self.player.money))

        # clamo the values
        if self.index < 0:
            self.index = len(self.options) - 1
        if self.index > len(self.options) - 1:
            self.index = 0

    def show_entry(self, text_surf, amount, top, selected):
        # background
        bg_rect = pygame.Rect(self.main_rect.left, top, self.width, text_surf.get_height() + (self.padding * 2))
        pygame.draw.rect(self.display_surface, 'White', bg_rect,0,6)

        # text
        text_rect = text_surf.get_rect(midleft = (self.main_rect.left + 20, bg_rect.centery))
        self.display_surface.blit(text_surf, text_rect)

        # amount
        amount_surf = self.font.render(str(amount), False, 'Black')
        amount_rect = amount_surf.get_rect(midright = (self.main_rect.right - 20, bg_rect.centery))
        self.display_surface.blit(amount_surf,amount_rect)

        # selected
        if selected:
            pygame.draw.rect(self.display_surface, 'Black', bg_rect,5,5)
            if self.index <= self.sell_border: #sell
                pos_rect = self.sell_text.get_rect(midleft = (self.main_rect.left + 150, bg_rect.centery))
                self.display_surface.blit(self.sell_text, pos_rect)
            
            else: # buy
                pos_rect = self.buy_text.get_rect(midleft = (self.main_rect.left + 210, bg_rect.centery))
                self.display_surface.blit(self.buy_text, pos_rect)

    def update(self):
        self.input()
        self.display_money()

        for text_index, text_surf in enumerate(self.text_surfs):
            top = self.main_rect.top + text_index * (text_surf.get_height() + (self.padding * 2) + self.space)
            amount_list = list(self.player.item_inventory.values()) + list(self.player.seed_inventory.values())
            amount = amount_list[text_index]
            self.show_entry(text_surf,amount,top, self.index == text_index)


class Inventory:
    def __init__(self, player, toggle_inventory, boat):
        # setup
        self.player = player
        self.toggle_inventory = toggle_inventory
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font('font/LycheeSoda.ttf', 30)

        # options
        self.width = 400
        self.space = 10
        self.padding = 15

        # entries
        self.options = list(self.player.item_inventory.keys()) + list(self.player.seed_inventory.keys())
        self.sell_border = len(self.player.item_inventory) -1
        self.setup()

        self.boat = boat
        self.timer = Timer(200)

    def display_money(self):
        text_surface = self.font.render(f'${self.player.money}', False, 'Black')
        text_rect = text_surface.get_rect(midbottom = (SCREEN_WIDTH / 2, SCREEN_HEIGHT - 20))

        pygame.draw.rect(self.display_surface, 'White', text_rect.inflate(10,10),0,6)
        self.display_surface.blit(text_surface, text_rect)

    def setup(self):
        # create the text surfaces
        self.text_surfs = []
        self.total_height = 0
        for item in self.options:
            text_surf = self.font.render(str(item) + ' seeds' if item in list(self.player.seed_inventory.keys()) and len(self.text_surfs) >= len(list(self.player.item_inventory.keys())) else item, False, 'Black')
            self.text_surfs.append(text_surf)
            self.total_height += text_surf.get_height() + (self.padding * 2)

        self.total_height += (len(self.text_surfs) - 1) * self.space
        self.menu_top = SCREEN_HEIGHT / 2 - self.total_height / 2
        self.main_rect = pygame.Rect(SCREEN_WIDTH / 2 - self.width / 2,self.menu_top, self.width,self.total_height)

    def input(self):
        keys = pygame.key.get_pressed()
        self.timer.update()

        if keys[pygame.K_ESCAPE]:
            self.toggle_inventory()

    def show_entry(self):
        rows = 7
        SQSIZE = (SCREEN_WIDTH - 700) // rows
        for row in range(rows):
                rect = (row * SQSIZE + 400, SQSIZE - 70, SQSIZE, SQSIZE)
                # blit
                pygame.draw.rect(self.display_surface, 'White', rect, 0,6)
                pygame.draw.rect(self.display_surface, 'Black', rect,5,5)

    def show_items(self):
        h_item = []
        rows = 7
        SQSIZE = (SCREEN_WIDTH - 700) // rows
        n_row = -1
        new_seed_inv = {}
        new_seed_inv["corn_seed"] = self.player.seed_inventory["corn"]
        new_seed_inv["tomato_seed"] = self.player.seed_inventory["tomato"]
        new_seed_inv["wheat_seed"] = self.player.seed_inventory["wheat"]
        all_items = self.player.item_inventory | new_seed_inv
        # print(all_items)
        for key in all_items:
            if all_items[key] > 0:
                n_row = n_row + 1

                black = (255, 255, 255)
                white = (0, 0, 0)
                font = pygame.font.Font('freesansbold.ttf', 20)
                h_item.append(key)
                img_item = pygame.image.load(f".\\graphics\\fruit\\{key}.png").convert_alpha()
                text = font.render(str(all_items[key]), True, black, white)
                img_center_quant = (h_item.index(key) * SQSIZE + 465, SQSIZE - 15, SQSIZE, SQSIZE)
                if key == "apple":
                    img_center_apple = (h_item.index(key) * SQSIZE + 425, SQSIZE - 40, SQSIZE, SQSIZE)
                    self.display_surface.blit(img_item, img_center_apple)
                    self.display_surface.blit(text, img_center_quant)
                if key == "corn":
                    img_center_apple = (h_item.index(key) * SQSIZE + 415, SQSIZE - 55, SQSIZE, SQSIZE)
                    self.display_surface.blit(img_item, img_center_apple)
                    self.display_surface.blit(text, img_center_quant)
                if key == "tomato":
                    img_center_apple = (h_item.index(key) * SQSIZE + 415, SQSIZE - 55, SQSIZE, SQSIZE)
                    self.display_surface.blit(img_item, img_center_apple)
                    self.display_surface.blit(text, img_center_quant)
                if key == "corn_seed":
                    img_item = pygame.transform.scale(img_item, (70, 70)) 
                    img_center_corn = (h_item.index(key) * SQSIZE + 405, SQSIZE - 70, SQSIZE, SQSIZE)
                    self.display_surface.blit(img_item, img_center_corn)
                    self.display_surface.blit(text, img_center_quant)
                if key == "fish":
                    img_item = pygame.transform.scale(img_item, (90, 40)) 
                    img_item = pygame.transform.rotate(img_item, 45)
                    img_center_fish = (h_item.index(key) * SQSIZE + 400, SQSIZE - 75, SQSIZE, SQSIZE)
                    self.display_surface.blit(img_item, img_center_fish)
                    self.display_surface.blit(text, img_center_quant)
                if key == "wood":
                    img_item = pygame.transform.scale(img_item, (70, 50))
                    img_center_wood = (h_item.index(key) * SQSIZE + 405, SQSIZE - 55, SQSIZE, SQSIZE)
                    self.display_surface.blit(img_item, img_center_wood)
                    self.display_surface.blit(text, img_center_quant)
                if key == "tomato_seed":
                    img_item = pygame.transform.scale(img_item, (50, 50))
                    img_center_wood = (h_item.index(key) * SQSIZE + 415, SQSIZE - 55, SQSIZE, SQSIZE)
                    self.display_surface.blit(img_item, img_center_wood)
                    self.display_surface.blit(text, img_center_quant)
                if key == "wheat":
                    img_item = pygame.transform.scale(img_item, (50, 50))
                    img_center_wood = (h_item.index(key) * SQSIZE + 415, SQSIZE - 55, SQSIZE, SQSIZE)
                    self.display_surface.blit(img_item, img_center_wood)
                    self.display_surface.blit(text, img_center_quant)
                if key == "wheat_seed":
                    img_item = pygame.transform.scale(img_item, (50, 50))
                    img_center_wood = (h_item.index(key) * SQSIZE + 415, SQSIZE - 55, SQSIZE, SQSIZE)
                    self.display_surface.blit(img_item, img_center_wood)
                    self.display_surface.blit(text, img_center_quant)



    def update(self):
        self.input()
        self.display_money()
        self.show_entry()
        self.show_items()