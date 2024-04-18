import pygame
import sys
import random

class Bullet(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()
        self.image = pygame.Surface((10, 30))
        self.image.fill((255, 0, 0))  # Красный цвет для пули
        self.rect = self.image.get_rect(midbottom=position)

    def update(self):
        self.rect.y -= 10  # Пуля двигается вверх
        if self.rect.bottom <= 0:
            self.kill()  # Если пуля вышла за границу экрана, удаляем ее из группы

class Zombie(pygame.sprite.Sprite):
    def __init__(self, screen_width, screen_height, player_height):
        super().__init__()
        self.image = pygame.transform.scale(zombie_image, (int(zombie_image.get_width() * (player_height / zombie_image.get_height())), player_height))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, screen_width - self.rect.width)
        self.rect.y = 0
        self.speed = 2
        self.screen_height = screen_height
        self.hp = 100

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > self.screen_height or self.hp <= 0:
            self.kill()

def main_menu(screen):
    menu_font = pygame.font.SysFont("vladimirscript", 40, True)
    menu_items = ["Play", "Settings", "Quit"]
    selected_item = 0
    title_font = pygame.font.SysFont("impact", 90)
    title_text = title_font.render("GameJam", True, (0, 0, 0))
    while True:
        screen.fill((0, 0, 0))
        screen.blit(background_menuimage, backgroundmenuimage_rect)
        screen.blit(title_text, (1200// 4 - title_text.get_width()//2, 800 // 4 - title_text.get_height()// 2))
        for i, item in enumerate(menu_items):
            color = (255,0,0) if i == selected_item else (0,0,0)
            text = menu_font.render(item, True, color)
            text_rect = text.get_rect(center=(1200//4, 800//2.5 + i * 50))
            screen.blit(text, text_rect)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_item = (selected_item-1) % len(menu_items)
                elif event.key == pygame.K_DOWN:
                    selected_item = (selected_item+1) % len(menu_items)
                elif event.key == pygame.K_RETURN:
                    return menu_items[selected_item]

pygame.init()
screen = pygame.display.set_mode((1200, 800))
pygame.display.set_caption("Gamejam")
clock = pygame.time.Clock()
background_menuimage = pygame.image.load("GaneJam/images/menupic.jpg").convert_alpha()
background_menuimage = pygame.transform.scale(background_menuimage, (1200,800))
backgroundmenuimage_rect = background_menuimage.get_rect()
zombie_image = pygame.image.load("GaneJam/images/zombie.png").convert_alpha()

#флажок для стадии игры
game_state = "Menu"

while True:
    if game_state == "Menu":
        chosen_option = main_menu(screen)
        if chosen_option == "Play":
            game_state = "Gameplay"
        elif chosen_option == "Settings":
            pass  #тут будут настройки
        elif chosen_option == "Quit":
            pygame.quit()
            sys.exit()

    elif game_state == "Gameplay":
        #флажки нажатии клавиш
        left_pressed, right_pressed, down_pressed, up_pressed = False, False, False, False

        # Создаем группу спрайтов для пуль и зомби
        bullets_group = pygame.sprite.Group()
        zombies_group = pygame.sprite.Group()

        # Функция для создания нового зомби
        def create_zombie():
            new_zombie = Zombie(1200, 800, player_height)
            zombies_group.add(new_zombie)


        player = pygame.image.load("GaneJam/images/testbg.png").convert_alpha()
        player = pygame.transform.scale(player, (100,200))
        player_rect = player.get_rect(midbottom=(600, 800))
        player_height = player_rect.height
        backgroundgame = pygame.image.load("GaneJam/images/img.png").convert_alpha()
        backgroundgame = pygame.transform.scale(backgroundgame, (1200,800))
        backgroundgame_rect = backgroundgame.get_rect()

        # мейн луп
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        left_pressed = True
                    elif event.key == pygame.K_RIGHT:
                        right_pressed = True
                    elif event.key == pygame.K_UP:
                        up_pressed = True
                    elif event.key == pygame.K_DOWN:
                        down_pressed = True
                    elif event.key == pygame.K_RETURN:  #При нажатии Enter
                        new_bullet = Bullet(player_rect.midtop)
                        bullets_group.add(new_bullet)  #добавляем новую пулю в группу
                    elif event.key == pygame.K_ESCAPE:  # При нажатии клавиши "ескейп"
                        game_state = "Menu"
                        running = False #возвращаемся в главное меню
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        left_pressed = False
                    elif event.key == pygame.K_RIGHT:
                        right_pressed = False
                    elif event.key == pygame.K_UP:
                        up_pressed = False
                    elif event.key == pygame.K_DOWN:
                        down_pressed = False

            #положение в зависимости от состояния флагов
            if left_pressed:
                player_rect.x -= 10
            if right_pressed:
                player_rect.x += 10
            if up_pressed:
                player_rect.y -= 10
            if down_pressed:
                player_rect.y += 10

            screen.fill("Black")
            screen.blit(backgroundgame, backgroundgame_rect)
            screen.blit(player, player_rect)

            #новый зомби с вероятностью
            if random.random() < 0.01:
                create_zombie()

            # отрисовываем все спрайты в группе пуль и зомби
            bullets_group.update()
            bullets_group.draw(screen)
            zombies_group.update()
            for zombie in zombies_group:
                screen.blit(zombie.image, zombie.rect)

            # столкновение пуль и зомби
            for bullet in bullets_group:
                hits = pygame.sprite.spritecollide(bullet, zombies_group, True)  # проверяем столкновение пули с зомби
                for zombie in hits:
                    zombie.hp -= 10  # уменьшаем здоровье зомби при попадании пули
                    if zombie.hp <= 0:
                        zombie.kill()  # если здоровье зомби равно нулю убиваем

            pygame.display.update()
            clock.tick(60)
