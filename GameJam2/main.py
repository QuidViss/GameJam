import pygame
import sys
import random
import math
from menu import *

speed=1.5
game_score = 0
game_over = False
class Bullet(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()

        self.image = pygame.image.load("images/bullet.png")
        self.image = pygame.transform.scale(self.image, (11,11))
        self.rect = self.image.get_rect(midtop=(position[0], position[1]-20)) #чтобы пули вылетали с головы
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
        self.speed = speed
        self.screen_height = screen_height
        self.hp = 10
        self.last_animation_update = pygame.time.get_ticks()  # Запоминаем время последнего обновления анимации
        self.animation_interval = 300  # Интервал в миллисекундах (0.3 секунды)
        self.ultimate_image_display_time = 0
        self.score = 0
    def update(self):
        global game_score
        current_time = pygame.time.get_ticks()
        if current_time - self.last_animation_update > self.animation_interval:
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.image = self.frames[self.current_frame]
            self.last_animation_update = current_time
        self.rect.y += self.speed
        if self.rect.top > self.screen_height:
            self.kill()
            game_score += 1
            print(game_score)
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
        self.zombies_killed = 0  # Counter to track zombies killed
        self.ultimate_ready = False  # Flag to indicate if ultimate ability is ready
        self.ultimate_duration = 7000  # 7 seconds in milliseconds
        self.ultimate_timer = 0  # Timer to track ultimate duration
        self.ultimate_image_display_time = 0  # Time when ultimate image was displayed
        self.ultimate_image_display_duration = 1700  # 3 seconds in milliseconds

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

        # Check if the player has killed enough zombies to activate the ultimate ability
        if self.zombies_killed >= 13 and not self.ultimate_ready:
            self.activate_ultimate()

        # Update ultimate timer if ultimate ability is active
        if self.ultimate_ready:
            self.ultimate_timer += clock.get_rawtime()
            if self.ultimate_timer >= self.ultimate_duration:
                self.deactivate_ultimate()

        # Handle displaying ultimate image
        if self.ultimate_image_display_time > 0:
            if pygame.time.get_ticks() - self.ultimate_image_display_time >= self.ultimate_image_display_duration:
                self.ultimate_image_display_time = 0
                screen.fill((0, 0, 0))  # Clear the screen after ultimate duration
            else:
                screen.blit(ultimate_image, ultimate_image_rect)  # Display ultimate image

    def activate_ultimate(self):
        ultimate_sound.play()
        self.ultimate_image_display_time = pygame.time.get_ticks()  # Set the time when the ultimate image is displayed
        # Stop all zombies' movement
        for zombie in zombies_group:
            zombie.speed = 0
        self.ultimate_ready = True
        self.ultimate_timer = pygame.time.get_ticks()
        self.ultimate_duration = pygame.time.get_ticks() + 700
        # Start ultimate timer

    def deactivate_ultimate(self):
        # Reset ultimate ability status
        for zombie in zombies_group:
            zombie.speed = speed  # Reset zombies' movement speed
        self.ultimate_ready = False
        self.zombies_killed = 0  # Reset zombies killed counter
        self.ultimate_timer = 0  # Reset ultimate timer

    def increase_zombies_killed(self):
        self.zombies_killed += 1
            # Update ultimate timer if ultimate ability is active
        # if self.ultimate_ready:
        #     self.ultimate_timer += clock.get_rawtime()
        #     if self.ultimate_timer >= self.ultimate_duration:
        #         self.deactivate_ultimate()

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
pygame.mixer.init()
ultimate_sound = pygame.mixer.Sound("images/music/hd-stardust-crusaders-za-warudo_1.mp3")
ultimate_image = pygame.image.load("images/photo2pixel_download.png").convert_alpha()
ultimate_image = pygame.transform.scale(ultimate_image, (1000,600))
ultimate_image_rect = ultimate_image.get_rect(center=(600,400))
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

        you_lose = pygame.image.load("images/pixil-frame-0 (6).png").convert_alpha()
        you_lose = pygame.transform.scale(you_lose, (1200, 800))
        you_lose_rect = you_lose.get_rect()

        game_score_font = pygame.font.Font("images/Daydream.ttf", 15)
        game_score_text = game_score_font.render(f'PAST ZOMBIES: {game_score}', True, (0, 0, 0))
        game_score_rect = game_score_text.get_rect(midtop=(200,50))

        # Главный цикл игры
        current_time = 0
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

            game_score_text = game_score_font.render(f'PAST ZOMBIES: {game_score}', True, (255, 255, 255))

            keys = pygame.key.get_pressed()
            screen.fill((0, 0, 0))
            screen.blit(backgroundgame, backgroundgame_rect)

            player.update(pygame.mouse.get_pos())

            current_time = pygame.time.get_ticks()
            if current_time < 30000:
                zombie_spawn_interval =100
                speed = 1.5
            elif current_time < 60000 and current_time > 30000:
                zombie_spawn_interval =70
                speed = 2
            elif current_time < 90000 and current_time > 60000:
                zombie_spawn_interval = 40
                speed = 2.5
            else:
                pass#game_end() #коннц игры



            if player.ultimate_ready:
                zombie_spawn_interval = 101  # Zombies won't spawn during ultimate
            else:
                zombie_spawn_timer += clock.get_rawtime()
                if zombie_spawn_timer >= zombie_spawn_interval:
                    create_zombie()
                    zombie_spawn_timer = 0
            # Обновляем пули

            bullets_group.update(player.rect.center[0],player.rect.center[1])
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
                        zombie.kill()
                        player.increase_zombies_killed()# 3. Выводим количество убитых зомби

            screen.blit(game_score_text, game_score_rect)
            if game_score > 15:
                game_over = True
                screen.blit(you_lose, you_lose_rect)

            if game_over:
                end_time = pygame.time.get_ticks() + 5000  # 5 seconds in milliseconds
                while pygame.time.get_ticks() < end_time:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                    pygame.display.update()
                pygame.quit()
                sys.exit()

            pygame.display.update()
            clock.tick(60)
