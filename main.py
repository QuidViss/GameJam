import pygame, sys

pygame.init()
w, h = 1200, 800
screen = pygame.display.set_mode((w, h))
speed = 3
FPS = 60
clock = pygame.time.Clock()
class Player():
    def __init__(self, x, y):
        self.images_right = []
        self.images_left = []
        self.index = 0
        self.counter = 0
        for num in range(1, 4):
            img_right = pygame.image.load(f"images/right{num}.png")
            img_right = pygame.transform.scale(img_right, (70, 90))
            img_left = pygame.image.load(f"images/left{num}.png")
            img_left = pygame.transform.scale(img_left, (70, 90))
            self.images_right.append(img_right)
            self.images_left.append(img_left)
        self.image = self.images_right[self.index]
        # self.image = self.images_left[self.index]


        
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vel_y = 0
        self.jumped = False
        self.direction = 0

    def update(self):
        dx = 0
        dy = 0
        walking = 20

        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_SPACE] and self.jumped == False:
            self.vel_y = -9
            self.jumped = True
       
        if self.rect.bottom == h:
            self.jumped = False
        if pressed[pygame.K_LEFT]:
            dx -= speed
            self.counter += 1
            self.direction = -1
        if pressed[pygame.K_RIGHT]:
            dx += speed
            self.counter += 1
            self.direction = 1

        if pressed[pygame.K_LEFT] == False and pressed[pygame.K_RIGHT] == False:
            self.counter = 0
            self.index = 0
            if self.direction == 1:
                self.image = self.images_right[self.index]
            if self.direction == -1:
                self.image = self.images_left[self.index]
        


        self.counter += 1
        if self.counter > walking:
            self.counter = 0
            self.index += 1
            if self.index >= len(self.images_right):
                self.index = 0
            if self.direction == 1:
                self.image = self.images_right[self.index]
            if self.direction == -1:
                self.image = self.images_left[self.index]
        


        
        self.vel_y += 1
        if self.vel_y > 10:
            self.vel_y = 10
        dy += self.vel_y

    
        self.rect.x += dx
        self.rect.y += dy


        if self.rect.bottom > h:
            self.rect.bottom = h
            dy = 0
        if self.rect.left < 0:
            self.rect.left = 0
            dx = 0
        if self.rect.right > w:
            self.rect.right = w
            dx = 0

        screen.blit(self.image, self.rect)
        

done = False

player = Player(100, h - 130)
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
            pygame.quit()
            sys.exit()
    screen.fill((0,0,0))
    player.update()
    pygame.display.update()
    clock.tick(FPS)