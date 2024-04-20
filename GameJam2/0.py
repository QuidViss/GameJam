import pygame
import sys
import random
import math
from menu import *

class Bullet(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()

        self.image = pygame.image.load("images/bullet.png")
        self.image = pygame.transform.scale(self.image, (11,11))
        self.rect = self.image.get_rect(midtop=position)
        self.direction = None

    def set_direction(self, target):
        dx = target[0] - self.rect.centerx
        dy = target[1] - self.rect.centery
        self.angle = math.atan2(-dy, dx)
        self.direction = [math.cos(self.angle), -math.sin(self.angle)]

    def update(self, x, y):
        if self.direction:
            self.rect.x += self.direction[0] * 10
            self.rect.y += self.direction[1] * 10


        # Удаляем пулю, если она ушла за пределы экрана
        if self.rect.bottom <= 0 or self.rect.top >= 800 or self.rect.right <= 0 or self.rect.left >= 1200:
            self.kill()


class Zombie(pygame.sprite.Sprite):
    def __init__(self, screen_width, screen_height, player_height, image_paths):
        super().__init__()
        self.frames = load_animation_frames(image_paths)
        self.current_frame = 0
        self.image = self.frames[self.current_frame]
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, screen_width - self.rect.width)
        self.rect.y = 0
        self.speed = 2
        self.screen_height = screen_height
        self.hp = 10
        self.last_animation_update = pygame.time.get_ticks()  # Запоминаем время последнего обновления анимации
        self.animation_interval = 300  # Интервал в миллисекундах (0.3 секунды)

    def update(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_animation_update > self.animation_interval:
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.image = self.frames[self.current_frame]
            self.last_animation_update = current_time
        self.rect.y += self.speed
        if self.rect.top > self.screen_height or self.hp <= 0:
            self.kill()

def load_animation_frames(image_paths):
    frames = []
    for path in image_paths:
        frame = pygame.image.load(path).convert_alpha()
        frames.append(frame)
    return frames







class Player(pygame.sprite.Sprite):
    def __init__(self, image, screen_width, screen_height):
        super().__init__()
        self.original_image = image
        self.image = self.original_image
        self.rect = self.image.get_rect(midbottom=(screen_width // 2, screen_height))
        self.speed = 10
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.gun = MachineGun()  # Start with the machine gun

    def switch_gun(self, gun_type):
        if gun_type == "MachineGun":
            self.gun = MachineGun()
        elif gun_type == "Pistol":
            self.gun = Pistol()
        elif gun_type == "Shotgun":
            self.gun = Shotgun()

    def shootgun(self, position, direction):
        if self.can_shoot():
            # Shoot three bullets in different directions
            for angle in [-0.1, 0, 0.1]:
                new_bullet = Bullet(position)
                new_bullet.set_direction((direction[0] + angle, direction[1]))
                bullets_group.add(new_bullet)
            self.last_shot_time = pygame.time.get_ticks()

    def shootpistol(self, position, direction):
        if self.can_shoot():
            new_bullet = Bullet(position)
            new_bullet.set_direction(direction)
            bullets_group.add(new_bullet)
            self.last_shot_time = pygame.time.get_ticks()

    def shootmk(self, position, direction):
        if self.can_shoot():
            new_bullet = Bullet(position)
            new_bullet.set_direction(direction)
            bullets_group.add(new_bullet)
            self.last_shot_time = pygame.time.get_ticks()
    def update(self, mouse_pos):
        dx = mouse_pos[0] - self.rect.centerx
        dy = mouse_pos[1] - self.rect.centery
        angle = math.atan2(-dy, dx)
        self.image = pygame.transform.rotate(self.original_image, math.degrees(angle) + 270)
        self.rect = self.image.get_rect(center=self.rect.center)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < self.screen_width:
            self.rect.x += self.speed
        if keys[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] and self.rect.bottom < self.screen_height:
            self.rect.y += self.speed

        if pygame.mouse.get_pressed()[0]:  # Left mouse button
            mouse_pos = pygame.mouse.get_pos()
            self.gun.shoot(self.rect.midbottom, (mouse_pos[0] - self.rect.centerx, mouse_pos[1] - self.rect.centery))

# def main_menu(screen):
#     menu_font = pygame.font.SysFont("vladimirscript", 40, True)
#     menu_items = ["Play", "Settings", "Quit"]
#     selected_item = 0
#     title_font = pygame.font.SysFont("impact", 90)
#     title_text = title_font.render("GameJam", True, (0, 0, 0))
#     while True:
#         screen.fill((0, 0, 0))
#         screen.blit(background_menuimage, backgroundmenuimage_rect)
#         screen.blit(title_text, (1200// 4 - title_text.get_width()//2, 800 // 4 - title_text.get_height()// 2))
#         for i, item in enumerate(menu_items):
#             color = (255,0,0) if i == selected_item else (0,0,0)
#             text = menu_font.render(item, True, color)
#             text_rect = text.get_rect(center=(1200//4, 800//2.5 + i * 50))
#             screen.blit(text, text_rect)
#         pygame.display.flip()
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 pygame.quit()
#                 sys.exit()
#             elif event.type == pygame.KEYDOWN:
#                 if event.key == pygame.K_UP:
#                     selected_item = (selected_item-1) % len(menu_items)
#                 elif event.key == pygame.K_DOWN:
#                     selected_item = (selected_item+1) % len(menu_items)
#                 elif event.key == pygame.K_RETURN:
#                     return menu_items[selected_item]

def create_zombie():
    new_zombie = Zombie(1200, 800, 200, zombie_image_paths)
  # Создание нового объекта зомби
    zombies_group.add(new_zombie)  # Добавление нового зомби в группу

pygame.init()
screen = pygame.display.set_mode((1200, 800))
pygame.display.set_caption("Gamejam")
clock = pygame.time.Clock()
# background_menuimage = pygame.image.load("images/menupic.jpg").convert_alpha()
# background_menuimage = pygame.transform.scale(background_menuimage, (1200,800))
# backgroundmenuimage_rect = background_menuimage.get_rect()
zombie_image_paths = ["images/gifs/pixil-frame-0.png", "images/gifs/pixil-frame-1.png", "images/gifs/pixil-frame-2.png"]



# Флаг для стадии игры
game_state = "Menu"
while True:
    if game_state == "Menu":
        main_menu()
        game_state = "Gameplay"

    elif game_state == "Gameplay":

        # Создаем группу спрайтов для пуль и зомби

        bullets_group = pygame.sprite.Group()
        zombies_group = pygame.sprite.Group()

        player_image = pygame.image.load("images/90deg.png").convert_alpha()
        player_image = pygame.transform.scale(player_image, (42, 74))
        player = Player(player_image, 1200, 800)
        backgroundgame = pygame.image.load("images/img.png").convert_alpha()
        backgroundgame = pygame.transform.scale(backgroundgame, (1200, 800))
        backgroundgame_rect = backgroundgame.get_rect()
        killed_zombie = 0
        # Главный цикл игры

        running = True
        zombie_spawn_timer = 0  # Добавляем таймер для появления зомби

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:  # При нажатии клавиши "Escape"
                        game_state = "Menu"
                        running = False  # Возвращаемся в главное меню
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Правая кнопка мыши
                        mouse_pos = pygame.mouse.get_pos()
                        new_bullet = Bullet(player.rect.midbottom)
                        new_bullet.set_direction(mouse_pos)
                        bullets_group.add(new_bullet)

            keys = pygame.key.get_pressed()
            screen.fill((0, 0, 0))
            screen.blit(backgroundgame, backgroundgame_rect)

            player.update(pygame.mouse.get_pos())


            # Создаем нового зомби периодически

            zombie_spawn_timer += clock.get_rawtime()
            if zombie_spawn_timer >= 100:  # Настройте интервал времени по необходимости
                create_zombie()
                zombie_spawn_timer = 0

            # Обновляем пули

            bullets_group.update(player.rect.center[0],player.rect.center[1],)
            for i in bullets_group:
                screen.blit(i.image,i.rect)
            screen.blit(player.image, player.rect)
            # Обновляем зомби

            zombies_group.update()

            for zombie in zombies_group:
                screen.blit(zombie.image, zombie.rect)

            # Обрабатываем столкновения пуль и зомби
            # coll=pygame.sprite.groupcollide(bullets_group,zombies_group,True,False)
            for bullet in bullets_group:
                hits = pygame.sprite.spritecollide(bullet, zombies_group, False)
                for zombie in hits:
                    zombie.hp -= 10
                    bullet.kill()
                    if zombie.hp <= 0:
                        killed_zombie += 1
                        zombie.kill()  # 3. Выводим количество убитых зомби

            pygame.display.update()
            clock.tick(60)
