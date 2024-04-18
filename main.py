import pygame, sys

pygame.init()
w, h = 1200, 800
screen = pygame.display.set_mode((w, h))
speed = 4
FPS = 60
clock = pygame.time.Clock()
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__() 
        self.images_right = []
        self.images_left = []
        self.index = 0
        self.counter = 0
        for num in range(1, 4):
            img_right = pygame.image.load(f"images/right{num}.png")
            img_right = pygame.transform.scale(img_right, (42, 60))
            img_left = pygame.image.load(f"images/left{num}.png")
            img_left = pygame.transform.scale(img_left, (42, 60))
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
        self.dx = 0
        self.dy = 0
        walking = 20

        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_SPACE] and self.jumped == False:
            self.vel_y = -15
            self.jumped = True

        if pressed[pygame.K_LEFT]:
            self.dx -= speed
            self.counter += 1
            self.direction = -1
        if pressed[pygame.K_RIGHT]:
            self.dx += speed
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
        self.dy += self.vel_y

    
        self.rect.x += self.dx
        self.rect.y += self.dy


        if self.rect.bottom > h:
            self.rect.bottom = h
            self.dy = 0
        if self.rect.left < 0:
            self.rect.left = 0
            self.dx = 0
        if self.rect.right > w:
            self.rect.right = w
            self.dx = 0
class Floor(pygame.sprite.Sprite):
    def __init__(self,index):
        super().__init__() 
        self.image=pygame.image.load("images/backfloor.png")
        self.image = pygame.transform.scale(self.image, (1200, 74))
        self.rect = self.image.get_rect()
        self.rect.center=(600,200*(index+1)+24+66*index)
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.image=pygame.image.load("images/enemy.gif")
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.rect = self.image.get_rect()
        self.rect.center=(1100,800-81)
        self.speed=-3
    def move(self):
        if self.rect.left<0:
            self.speed=3
        if self.rect.right>1200:
            self.speed=-3
        self.rect.move_ip(self.speed,0)
class Stair(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.image=pygame.image.load("images/stair.png")
        self.image = pygame.transform.scale(self.image, (66, 278))
        self.rect = self.image.get_rect()
        self.rect.x=200
        self.rect.y=191
        
        



player = Player(100, 0)
play1=pygame.sprite.Group()
play1.add(player)
floor1=Floor(0)
floor2=Floor(1)
floor3=Floor(2)
floor=pygame.sprite.Group()
floor.add(floor1)
floor.add(floor2)
floor.add(floor3)
enemy1=Enemy()
enemy=pygame.sprite.Group()
enemy.add(enemy1)
all_sprites=pygame.sprite.Group()
all_sprites.add(player)
all_sprites.add(floor1)
all_sprites.add(floor2)
all_sprites.add(floor3)
all_sprites.add(enemy1)
image1=pygame.image.load("images/back1.png")
image1 = pygame.transform.scale(image1, (333, 205))
rect1 =image1.get_rect()
stair=Stair()
all_sprites.add(stair)
rect1.x=0
rect1.y=0
def main():
    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
                pygame.quit()
                sys.exit()

        coll=pygame.sprite.spritecollideany(player,floor)
        if coll and player.rect.bottom>coll.rect.top:
            player.rect.bottom = coll.rect.top
            player.dy = 0
            player.jumped = False
        # for i in floor:      
        #     if player.rect.bottom == i.rect.top:
                
        
        enemy1.move()

        
        screen.fill((0,0,0))
        screen.blit(image1,rect1)
        player.update()
        for i in all_sprites:
            screen.blit(i.image,i.rect)
        pygame.display.update()
        clock.tick(FPS)
main()