import pygame, sys

pygame.init()
w, h = 1200, 800
screen = pygame.display.set_mode((w, h))
speed = 4
FPS = 60
OUTX=0
OUTY=0
POS=1
positions=[["images/together.png",(0,-345),(0,-79),(0,187),(0,453),(0,719),(1200,-345),(1200,-79),(1200,187),(1200,453),(1200,719),(300,435),(1600,435),(500,169),(1800,169),(1000,-99),(300,-365),(1400,-365),(500,-433),(1700,-167),(500,630),(1700,630)],
           ["images/together.png",(0,-345),(0,-79),(0,187),(0,453),(0,719),(1200,-345),(1200,-79),(1200,187),(1200,453),(1200,719),(666,435),(1400,435),(400,169),(800,-99),(1550,-99),(500,-365),(1100,-365),(200,-167),(1700,-167),(200,630),(1700,630)],
           ["images/together.png",(0,-345),(0,-79),(0,187),(0,453),(0,719),(1200,-345),(1200,-79),(1200,187),(1200,453),(1200,719),(700,435),(1700,435),(800,169),(3500,-99),(1450,-99),(600,-365),(1700,-365),(200,-167),(1400,-433),(200,630),(1400,630)],
           ["images/together.png",(0,-345),(0,-79),(0,187),(0,453),(0,719),(1200,-345),(1200,-79),(1200,187),(1200,453),(1200,719),(600,435),(1400,435),(1800,169),(400,-99),(1000,-99),(700,-365),(1650,-365),(200,-433),(1700,-433),(200,630),(1700,630)]]
botpos=[[(200,-463),(800,-463),(1400,-463),(900,-197),(200,69),(800,69),(1400,69),(300,335),(750,335),(1400,335),(1000,604)],[],[],[]]
enem=[(800,-360),(1200,-360),(100,-94),(720,-94),(1720,-94),(300,172),(1200,172),(1680,172),(100,438),(690,438),(380,704),(800,704),(1550,704)]
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
    def __init__(self,x,y):
        super().__init__() 
        self.image=pygame.image.load("images/enemy.gif")
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.rect = self.image.get_rect()
        self.rect.x=x
        self.rect.y=y
        self.speed=-3
    def update(self):
        global OUTX
        global OUTY
        if self.rect.left<backrect.x:
            self.speed=3
        if self.rect.right>backrect.x+2000:
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
class Door(pygame.sprite.Sprite):
    def __init__(self,x,y,index):
        super().__init__() 
        self.image=pygame.image.load("images/door.png")
        self.image = pygame.transform.scale(self.image, (80, 100))
        self.rect = self.image.get_rect()
        self.rect.x=x
        self.rect.y=y
        self.index=index
    def update(self):
        global OUTX
        global OUTY
        self.rect.move_ip(OUTX*4,OUTY*2)
class Bottle(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__() 
        self.image=pygame.image.load("images/bottle.png")
        self.image = pygame.transform.scale(self.image, (30, 60))
        self.rect = self.image.get_rect() 
        self.rect.x=x
        self.rect.y=y
    def update(self):
        global OUTX
        global OUTY
        self.rect.move_ip(OUTX*4,OUTY*2)
backimg = pygame.image.load("images/together.png")
backimg=pygame.transform.scale(backimg, (2000, 1333))
backrect=backimg.get_rect()
backrect.x=0
backrect.y=-533




player = Player(400, 300)
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
enemy=pygame.sprite.Group()
enemy1=Enemy(400,-360)
enemy2=Enemy(1200,-360)
enemy3=Enemy(100,-94)
enemy4=Enemy(600,-94)
enemy5=Enemy(1680,-94)
enemy6=Enemy(300,172)
enemy7=Enemy(1200,172)
enemy8=Enemy(1680,172)
enemy9=Enemy(100,438)
enemy10=Enemy(600,438)
enemy11=Enemy(380,704)
enemy12=Enemy(800,704)
enemy13=Enemy(1550,704)
enemy.add(enemy1)
enemy.add(enemy2)
enemy.add(enemy3)
enemy.add(enemy4)
enemy.add(enemy5)
enemy.add(enemy6)
enemy.add(enemy7)
enemy.add(enemy8)
enemy.add(enemy9)
enemy.add(enemy10)
enemy.add(enemy11)
enemy.add(enemy12)
enemy.add(enemy13)
all_sprites=pygame.sprite.Group()
stair1=Stair(666,169+266)
stair2=Stair(1400,169+266)
stair3=Stair(400,169)
stair4=Stair(800,-99)
stair5=Stair(1600,-99)
stair6=Stair(500,-365)
stair7=Stair(1100,-365)
stair=pygame.sprite.Group()
stair.add(stair1)
stair.add(stair2)
stair.add(stair3)
stair.add(stair4)
stair.add(stair5)
stair.add(stair6)
stair.add(stair7)
door1=Door(300,-167,0)
door2=Door(2000-300,-167,1)
door3=Door(300,800-170,2)
door4=Door(2000-300,800-170,3)
door=pygame.sprite.Group()
door.add(door1)
door.add(door2)
door.add(door3)
door.add(door4)
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
all_sprites.add(stair6)
all_sprites.add(stair7)
all_sprites.add(door1)
all_sprites.add(door2)
all_sprites.add(door3)
all_sprites.add(door4)
def start(colldoor):
    done = False
    t=0
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
                pygame.quit()
                sys.exit()
        s = pygame.Surface((1200,800))
        t+=3
        if t>255:
            t=255
            done=True
        s.set_alpha(t)# alpha level
        s.fill((0,0,0))# this fills the entire surface
        screen.blit(s, (0,0)) 
        pygame.display.update()
        clock.tick(FPS)
    change(colldoor)
def end():
    done = False
    t=255
    while not done:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
                pygame.quit()
                sys.exit()
        
        screen.blit(backimg,backrect)
        for i in all_sprites:
            screen.blit(i.image,i.rect)
        screen.blit(player.image,player.rect)
        for i in enemy:
            screen.blit(i.image,i.rect)
        s = pygame.Surface((1200,800))
        t-=5
        if t<0:
            t=0
            done=True
        if t==0:
            main()
        s.set_alpha(t)# alpha level
        s.fill((0,0,0))# this fills the entire surface
        screen.blit(s, (0,0)) 
        pygame.display.update()
        clock.tick(FPS)
def change(colldoor):
    global backimg
    global backrect
    global POS
    index=colldoor.index
    if index%2==0:
        POS-=1
    else:
        POS+=1
    if POS==-1:
        POS=3
    elif POS==4:
        POS=0
    if index==0:
        j=1
        for i in all_sprites:  
            i.rect.x=positions[POS][j][0]-800
            i.rect.y=positions[POS][j][1]+533
            j+=1
        j=0
        for i in enemy:  
            i.rect.x=enem[j][0]-800
            i.rect.y=enem[j][1]+533
            i.speed=-4
            j+=1
        backimg = pygame.image.load("images/back1.png")
        backimg=pygame.transform.scale(backimg, (2000, 1333))
        backrect=backimg.get_rect()
        backrect.x=-800
        backrect.y=0
        player.rect.center=(positions[POS][19][0]-800+50,positions[POS][19][1]+533+69)
    elif index==1:
        j=1
        for i in all_sprites:  
            i.rect.x=positions[POS][j][0]
            i.rect.y=positions[POS][j][1]+533
            j+=1
        j=0
        for i in enemy:  
            i.rect.x=enem[j][0]
            i.rect.y=enem[j][1]+533
            i.speed=-4
            j+=1
        backimg = pygame.image.load("images/back1.png")
        backimg=pygame.transform.scale(backimg, (2000, 1333))
        backrect=backimg.get_rect()
        backrect.x=0
        backrect.y=0
        player.rect.center=(positions[POS][18][0]+50,positions[POS][18][1]+533+69)
    elif index==2:
        j=1
        for i in all_sprites:  
            i.rect.x=positions[POS][j][0]-800
            i.rect.y=positions[POS][j][1]
            j+=1
        j=0
        for i in enemy:  
            i.rect.x=enem[j][0]-800
            i.rect.y=enem[j][1]
            i.speed=-4
            j+=1
        backimg = pygame.image.load("images/back1.png")
        backimg=pygame.transform.scale(backimg, (2000, 1333))
        backrect=backimg.get_rect()
        backrect.x=-800
        backrect.y=-533
        player.rect.center=(positions[POS][21][0]-800+50,positions[POS][21][1]+69)
    else:
        j=1
        for i in all_sprites:  
            i.rect.x=positions[POS][j][0]
            i.rect.y=positions[POS][j][1]
            j+=1
        j=0
        for i in enemy:  
            i.rect.x=enem[j][0]
            i.rect.y=enem[j][1]
            i.speed=-4
            j+=1
        backimg = pygame.image.load("images/back1.png")
        backimg=pygame.transform.scale(backimg, (2000, 1333))
        backrect=backimg.get_rect()
        backrect.x=0
        backrect.y=-533
        player.rect.center=(positions[POS][20][0]+50,positions[POS][20][1]+69)
    global speed
    speed=6

    end()
def main():
    done = False
    while not done:
        global backimg
        global backrect
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
                pygame.quit()
                sys.exit()



        collflo=pygame.sprite.spritecollideany(player,floor)
        if collflo and player.rect.bottom>collflo.rect.top and player.rect.bottom<collflo.rect.bottom-28 and player.stair==False:
            player.rect.bottom = collflo.rect.top
            player.dy = 0
            player.jumped = False



        collsta=pygame.sprite.spritecollideany(player,stair)
        pressed=pygame.key.get_pressed()
        if collsta and pressed[pygame.K_DOWN] and player.rect.bottom+20<collsta.rect.bottom:
            player.stair=True
        elif collsta and pressed[pygame.K_UP] and player.rect.bottom-26>collsta.rect.top:
            player.stair=True
        elif collsta and player.rect.bottom-18<collsta.rect.top  and player.jumped==False:
            player.stair=False
            player.rect.bottom=collsta.rect.top+18
        elif collsta and player.rect.bottom+7>collsta.rect.bottom and player.jumped==True:
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



        collene=pygame.sprite.groupcollide(enemy,stair,False,False)
        for j in collene:
            j.speed=j.speed*(-1)
        for i in all_sprites:
            i.update()
        player.update()
        for i in enemy:
            i.update()
        colldoor=pygame.sprite.spritecollideany(player,door)
        if colldoor and pressed[pygame.K_RETURN]:
            start(colldoor)

        backrect.x+=OUTX*4
        backrect.y+=OUTY*2
        screen.blit(backimg,backrect)
        for i in all_sprites:
            screen.blit(i.image,i.rect)
        screen.blit(player.image,player.rect)
        for i in enemy:
            screen.blit(i.image,i.rect)
        s = pygame.Surface((1200,800))  # the size of your rect
        s.set_alpha(1)                # alpha level
        s.fill((0,0,0))           # this fills the entire surface
        screen.blit(s, (0,0)) 
        pygame.display.update()
        clock.tick(FPS)
main()


    