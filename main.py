import pygame, sys

pygame.init()
w, h = 1200, 800
screen = pygame.display.set_mode((w, h))
speed = 4
FPS = 60
OUTX=0
OUTY=0
clock = pygame.time.Clock()
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__() 
        self.images_right = []
        self.images_left = []
        self.index = 0
        self.counter = 0
        self.stair=False
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
            self.stair=False

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
        if pressed[pygame.K_DOWN] and self.stair==True:
            self.dy=2
        elif pressed[pygame.K_UP] and self.stair==True:
            self.dy=-2


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
        if not self.stair:
            self.dy += self.vel_y
        if OUTX==-1 or OUTX==1:
            self.dx=0
        if OUTY==-1 or OUTY==1:
            self.dy=0
        self.rect.move_ip(self.dx,self.dy)


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
    def __init__(self,x,y):
        super().__init__() 
        self.image=pygame.image.load("images/backfloor.png")
        self.image = pygame.transform.scale(self.image, (1200, 74))
        self.rect = self.image.get_rect()
        self.rect.center=(600+1200*x,200*(y+1)+24+66*y-532)
    def update(self):
        global OUTX
        global OUTY
        self.rect.move_ip(OUTX*4,OUTY*2)
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.image=pygame.image.load("images/enemy.gif")
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.rect = self.image.get_rect()
        self.rect.center=(1100,800-81)
        self.speed=-3
    def update(self):
        global OUTX
        global OUTY
        if self.rect.left<0:
            self.speed=3
        if self.rect.right>1200:
            self.speed=-3
        self.rect.move_ip(self.speed+OUTX*4,OUTY*2)
class Stair(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__() 
        self.image=pygame.image.load("images/stair.png")
        self.image = pygame.transform.scale(self.image, (66, 300))
        self.rect = self.image.get_rect()
        self.rect.x=x
        self.rect.y=y
    def update(self):
        global OUTX
        global OUTY
        self.rect.move_ip(OUTX*4,OUTY*2)

backimg = pygame.image.load("images/background.png")
backimg=pygame.transform.scale(backimg, (2000, 1333))
backrect=backimg.get_rect()
backrect.x=0
backrect.y=-533




player = Player(100, 466)
play1=pygame.sprite.Group()
play1.add(player)
floor1=Floor(0,0)
floor2=Floor(0,1)
floor3=Floor(0,2)
floor4=Floor(0,3)
floor5=Floor(0,4)
floor6=Floor(1,0)
floor7=Floor(1,1)
floor8=Floor(1,2)
floor9=Floor(1,3)
floor10=Floor(1,4)
floor=pygame.sprite.Group()
floor.add(floor1)
floor.add(floor2)
floor.add(floor3)
floor.add(floor4)
floor.add(floor5)
floor.add(floor6)
floor.add(floor7)
floor.add(floor8)
floor.add(floor9)
floor.add(floor10)
enemy1=Enemy()
enemy=pygame.sprite.Group()
enemy.add(enemy1)
all_sprites=pygame.sprite.Group()
stair1=Stair(200,169)
stair2=Stair(500,169+266)
stair3=Stair(700,169)
stair4=Stair(1200,-99)
stair5=Stair(1500,-365)
stair=pygame.sprite.Group()
stair.add(stair1)
stair.add(stair2)
stair.add(stair3)
stair.add(stair4)
stair.add(stair5)
all_sprites.add(floor1)
all_sprites.add(floor2)
all_sprites.add(floor3)
all_sprites.add(floor4)
all_sprites.add(floor5)
all_sprites.add(floor6)
all_sprites.add(floor7)
all_sprites.add(floor8)
all_sprites.add(floor9)
all_sprites.add(floor10)
all_sprites.add(stair1)
all_sprites.add(stair2)
all_sprites.add(stair3)
all_sprites.add(stair4)
all_sprites.add(stair5)
all_sprites.add(enemy1)
all_sprites.add(player)
def main():
    lastcoll=None
    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
                pygame.quit()
                sys.exit()
        collflo=pygame.sprite.spritecollideany(player,floor)
        if collflo and player.rect.bottom>collflo.rect.top and player.stair==False:
            player.rect.bottom = collflo.rect.top
            player.dy = 0
            player.jumped = False
        collsta=pygame.sprite.spritecollideany(player,stair)
        pressed=pygame.key.get_pressed()
        if collsta and pressed[pygame.K_DOWN] and player.rect.bottom+20<collsta.rect.bottom:
            player.stair=True
            lastcoll=collsta
        elif collsta and pressed[pygame.K_UP] and player.rect.bottom-26>collsta.rect.top:
            player.stair=True
        elif collsta and player.rect.bottom-18<collsta.rect.top  and player.jumped==False:
            player.stair=False
            player.rect.bottom=collsta.rect.top+18
        elif collsta and player.rect.bottom+7>collsta.rect.bottom and player.jumped==False:
            player.stair=False
            player.rect.bottom=collsta.rect.bottom-7
        elif not collsta:
            player.stair=False
        global OUTX
        global OUTY
        if player.rect.right>799 and backrect.x>-800 and pressed[pygame.K_RIGHT]:
            OUTX=-1
            player.rect.right=800
        elif player.rect.right>799 and backrect.x<-800:
            OUTX=0
            backrect.x=-800
        elif player.rect.left<401 and backrect.x<0 and pressed[pygame.K_LEFT]:
            OUTX=1
            player.rect.left=400
        elif player.rect.left<401 and backrect.x>0:
            OUTX=0
            backrect.x=0
        else:
            OUTX=0
        if player.rect.top<400 and backrect.y<0 and player.stair==True and pressed[pygame.K_UP]:
            OUTY=1
        elif backrect.y>0:
            OUTY=0
            backrect.y=0
        elif  backrect.y>-533 and player.stair==True and pressed[pygame.K_DOWN]:
            OUTY=-1
        elif backrect.y<-533:
            OUTY=0
            backrect.y=-533
        else:
            OUTY=0
                
        for i in all_sprites:
            i.update()
        backrect.x+=OUTX*4
        backrect.y+=OUTY*2
        screen.fill((0,0,0))
        screen.blit(backimg,backrect)
        for i in all_sprites:
            screen.blit(i.image,i.rect)
        pygame.display.update()
        clock.tick(FPS)
main()