import pygame
from settings import *
from player import Player
from overlay import Overlay
from sprites import Generic, Water, WildFlower, Tree, Interaction, Particle, Boat
from pytmx.util_pygame import load_pygame
from support import *
from transition import Transition
from soil import SoilLayer
from sky import Rain, Sky
from random import randint
from menu import Menu, Inventory
from boat import Boat2, Boat


class Level:
    def __init__(self, music_on):
        # get the display surface
        self.display_surface = pygame.display.get_surface()

        # sprite groups
        self.all_sprites = CameraGroup()
        self.collision_sprites = pygame.sprite.Group()
        self.tree_sprites = pygame.sprite.Group()
        self.interaction_sprites = pygame.sprite.Group()
        self.boat2 = Boat2()
        # self.boat = Boat()

        self.soil_layer = SoilLayer(self.all_sprites)
        self.setup()
        self.overlay = Overlay(self.player)
        self.transition = Transition(self.reset, self.player)

        # sky
        self.rain = Rain(self.all_sprites)
        self.raining = randint(0,10) > 7
        self.soil_layer.raining = self.raining
        self.sky = Sky()

        # shop
        self.menu = Menu(self.player, self.toggle_shop)
        self.shop_active = False

        # inventory
        self.inventory = Inventory(self.player, self.toggle_inventory, self.boat2)
        self.inventory_active = False

        # boat
        # self.boat = Boat()
        self.music_on = True
        # music
        self.success = pygame.mixer.Sound('audio/success.wav')
        self.success.set_volume(0.3)
        self.music = pygame.mixer.Sound('audio/music.mp3')
        self.music.set_volume(0.5)
        self.music.play(loops=-1)
        self.esc_avaible = True 

    def setup(self):
        tmx_data = load_pygame('data/map.tmx')

        # house
        for layer in ['HouseFloor', 'HouseFurnitureBottom']:
            for x,y, surf in tmx_data.get_layer_by_name(layer).tiles():
                Generic((x * TILE_SIZE,y * TILE_SIZE),surf,self.all_sprites,LAYERS['house bottom'])

        for layer in ['HouseWalls', 'HouseFurnitureTop']:
            for x,y, surf in tmx_data.get_layer_by_name(layer).tiles():
                Generic((x * TILE_SIZE,y * TILE_SIZE),surf,self.all_sprites)

        # Fence
        for x,y, surf in tmx_data.get_layer_by_name('Fence').tiles():
            Generic((x * TILE_SIZE,y * TILE_SIZE), surf, [self.all_sprites, self.collision_sprites])

        # water
        water_frames = import_folder('graphics/water/')
        for x,y, surf in tmx_data.get_layer_by_name('Water').tiles():
            Water((x * TILE_SIZE,y * TILE_SIZE), water_frames, self.all_sprites)
            self.water = Water((x * TILE_SIZE,y * TILE_SIZE), water_frames, self.all_sprites)

        # trees
        for obj in tmx_data.get_layer_by_name('Trees'):
            Tree((obj.x,obj.y), obj.image, [self.all_sprites, self.collision_sprites, self.tree_sprites], obj.name, self.player_add)

        # wildflowers
        for obj in tmx_data.get_layer_by_name('Decoration'):
            WildFlower((obj.x,obj.y), obj.image, [self.all_sprites])

        # collision tiles
        for x,y, surf in tmx_data.get_layer_by_name('Collision').tiles():
            Generic((x * TILE_SIZE,y * TILE_SIZE), pygame.Surface((TILE_SIZE, TILE_SIZE)), self.collision_sprites)

        # Player
        for obj in tmx_data.get_layer_by_name('Player'):
            # print(obj)
            if obj.name == 'Start':
                self.player = Player((obj.x,obj.y), self.all_sprites, self.collision_sprites, self.tree_sprites, self.interaction_sprites, self.soil_layer, self.toggle_shop, self.boat2, self.toggle_inventory)

            if obj.name == 'Bed':
                Interaction((obj.x,obj.y), (obj.width, obj.height), self.interaction_sprites, obj.name)

            if obj.name == 'Trader':
                Interaction((obj.x,obj.y), (obj.width, obj.height), self.interaction_sprites, obj.name)

        Generic(pos = (0,0),
                surf = pygame.image.load('graphics/world/ground.png').convert_alpha(),
                groups=self.all_sprites,
                z = LAYERS['ground'])

    def player_add(self,item):
        self.player.item_inventory[item] += 1
        self.success.play()

    def toggle_shop(self):
        self.shop_active = not self.shop_active

    def toggle_inventory(self):
        self.inventory_active = not self.inventory_active
        
    def reset(self):
        # soil
        self.soil_layer.update_plants()

        # randomize the rain
        self.raining = randint(0,10) > 7
        self.soil_layer.raining = self.raining
        if self.raining:
            self.soil_layer.water_all()

        # apples on the trees
        for tree in self.tree_sprites.sprites():
            for apple in tree.apple_sprites.sprites():
                apple.kill()    
            tree.create_fruit()

        # sky
        self.sky.start_color = [255,255,255]

    def plant_collision(self):
        if self.soil_layer.plant_sprites:
            for plant in self.soil_layer.plant_sprites.sprites():
                # print(self.soil_layer.grid[plant.rect.centery // TILE_SIZE][plant.rect.centerx // TILE_SIZE])
                if plant.harvestable and plant.rect.colliderect(self.player.hitbox):
                    self.player_add(plant.plant_type)
                    plant.kill()
                    Particle(plant.rect.topleft, plant.image, self.all_sprites, LAYERS['main'])
                    if 'P' in self.soil_layer.grid[plant.rect.centery // TILE_SIZE][plant.rect.centerx // TILE_SIZE]:
                        self.soil_layer.grid[plant.rect.centery // TILE_SIZE][plant.rect.centerx // TILE_SIZE].remove('P')

    def run(self, dt, music_on):
        if music_on:
            self.music.set_volume(0)
        else:
            self.music.set_volume(0.3)
        # drawing logic
        self.display_surface.fill('black')
        self.all_sprites.customize_draw(self.player)

        # updates
        if self.shop_active:
            self.esc_avaible = False
            self.menu.update()
        elif self.inventory_active:
            self.esc_avaible = False
            self.inventory.update()
        else:
            self.esc_avaible = True
            self.all_sprites.update(dt)
            self.plant_collision()

        # weather
        self.overlay.display()

        # raining
        if self.raining and not self.shop_active and not self.inventory_active:
            self.rain.update()

        # daytime
        self.sky.display(dt)

        # transition overlay
        if self.player.sleep:
            self.transition.play()

        # display boat
        self.boat2.display(self.display_surface)
        # self.boat.display(self.display_surface)

class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = pygame.math.Vector2()

    def customize_draw(self, player):
        self.offset.x = player.rect.centerx - SCREEN_WIDTH / 2
        self.offset.y = player.rect.centery - SCREEN_HEIGHT / 2
        for layer in LAYERS.values():
            for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
                if sprite.z == layer:
                    offset_rect = sprite.rect.copy()
                    offset_rect.center -= self.offset
                    self.display_surface.blit(sprite.image, offset_rect)

