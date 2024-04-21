import pygame, sys
import random
import math
from menu import *
import pygame.colordict
pygame.init()

# SETTINGS FOR FIRST PART
w, h = 1200, 800
screen = pygame.display.set_mode((w, h))
speed = 4
speedy=2
printbot=0
cathappy=0
doghappy=0
studenthappy=0
FPS = 60
OUTX=0 # it is used for moving other objects in x except for the player
OUTY=0 # it is used for moving other objects in y except for the player
time=1 # timer
tome=0 # future limit for timer
alpha=0 # value for transparency to use it when the scenes change
color=(0,0,0)
POS=1 #player scene position
backimg = pygame.image.load("images/tolebi.png")
backimg=pygame.transform.scale(backimg, (2000, 1330))
backrect=backimg.get_rect()
backrect.x=0
backrect.y=-533
# sound for jumping
jump = pygame.mixer.Sound("sounds/jump.wav")
# game score part
game_score_font = pygame.font.Font("images/Daydream.ttf", 15)
game_score_text = game_score_font.render(f'BOTTLES: {printbot}', True, (255, 255, 255))
game_score_rect = game_score_text.get_rect(midtop=(1000,50))
# positions of stairs, floor, doors to change it when scene is changed
positions=[["images/abylaikhan.png",(0,-345),(0,-79),(0,187),(0,453),(0,719),(1200,-345),(1200,-79),(1200,187),(1200,453),(1200,719),(300,435),(1600,435),(500,169),(1800,169),(1000,-99),(300,-365),(1400,-365),(500,-433),(1700,-167),(500,630),(1700,630)],
           ["images/together.png",(0,-345),(0,-79),(0,187),(0,453),(0,719),(1200,-345),(1200,-79),(1200,187),(1200,453),(1200,719),(666,435),(1400,435),(400,169),(800,-99),(1550,-99),(500,-365),(1100,-365),(200,-167),(1700,-167),(200,630),(1700,630)],
           ["images/panfilov.png",(0,-345),(0,-79),(0,187),(0,453),(0,719),(1200,-345),(1200,-79),(1200,187),(1200,453),(1200,719),(700,435),(1700,435),(800,169),(3500,-99),(1450,-99),(600,-365),(1700,-365),(200,-167),(1400,-433),(200,630),(1400,630)],
           ["images/kazbi.png",(0,-345),(0,-79),(0,187),(0,453),(0,719),(1200,-345),(1200,-79),(1200,187),(1200,453),(1200,719),(600,435),(1400,435),(1800,169),(400,-99),(1000,-99),(700,-365),(1650,-365),(200,-433),(1700,-433),(200,630),(1700,630)]]
# position of bottles in every 4 scene
botpos=[[(200,-458),(800,-458),(1400,-458),(900,-192),(200,74),(800,74),(1400,6974),(300,340),(750,340),(1400,340),(1000,609 )],
        [(200,-458),(800,-458),(1400,-458),(900,-192),(200,74),(800,74),(1400,6974),(300,340),(750,340),(1400,340),(1000,609 )],
        [(200,-458),(800,-458),(1400,-458),(900,-192),(200,74),(800,74),(1400,6974),(300,340),(750,340),(1400,340),(1000,609 )],
        [(200,-458),(800,-458),(1400,-458),(900,-192),(200,74),(800,74),(1400,6974),(300,340),(750,340),(1400,340),(1000,609 )]]
# positions of enemy to change it when scene is changed
enem=[(800,-360),(1200,-360),(100,-94),(720,-94),(1720,-94),(300,172),(1200,172),(1680,172),(100,438),(690,438),(380,704),(800,704),(1550,704)]
clock = pygame.time.Clock()
# SETTINGS FOR SECOND PART
# ultimate settings
ultimate_sound = pygame.mixer.Sound("images/music/hd-stardust-crusaders-za-warudo_1.wav")
ultimate_image = pygame.image.load("images/photo2pixel_download.png").convert_alpha()
ultimate_image = pygame.transform.scale(ultimate_image, (1000,600))
ultimate_image_rect = ultimate_image.get_rect(center=(600,400))
#speed for zombies
speed_second=1.5
game_score = 0
pygame.display.set_caption("Gamejam")
#list to animation of zombies
zombie_image_paths = ["images/gifs/pixil-frame-0.png", "images/gifs/pixil-frame-1.png", "images/gifs/pixil-frame-2.png"]
#sprite groups for future zombies and bullets
bullets_group = pygame.sprite.Group()
zombies_group = pygame.sprite.Group()

# classes for fisrt part
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__() 
        self.images_right = []
        self.images_left = []
        self.images_climb = []
        self.index = 0
        self.counter = 0
        self.indexclimb = 0
        self.counterclimb = 0
        self.stair=False
        # making list of pictures to animation
        for num in range(1, 4):
            img_right = pygame.image.load(f"images/right{num}.png")
            img_right = pygame.transform.scale(img_right, (42, 60))
            img_left = pygame.image.load(f"images/left{num}.png")
            img_left = pygame.transform.scale(img_left, (42, 60))
            self.images_right.append(img_right)
            self.images_left.append(img_left)
        for num in range(1, 3):
            img_climb = pygame.image.load(f"images/climb{num}.png")
            img_climb = pygame.transform.scale(img_climb, (42, 60))
            self.images_climb.append(img_climb)
        self.image = self.images_right[self.index]


        # making player rectangle
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
        climbing = 20

        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_SPACE] and self.jumped == False:
            self.vel_y = -15
            self.jumped = True
            self.stair=False
            jump.play()
        # walking to the left
        if pressed[pygame.K_LEFT]:
            self.dx -= speed
            self.counter += 1
            self.direction = -1
        # walking to the right
        if pressed[pygame.K_RIGHT]:
            self.dx += speed
            self.counter += 1
            self.direction = 1
        # cheking for walking and if walking is false, counter is 0 to not change animation
        if pressed[pygame.K_LEFT] == False and pressed[pygame.K_RIGHT] == False:
            self.counter = 0
            self.index = 0
            if self.direction == 1:
                self.image = self.images_right[self.index]
            if self.direction == -1:
                self.image = self.images_left[self.index]
        # speed to go down
        if pressed[pygame.K_DOWN] and self.stair==True:
            self.dy=speedy
            self.image = self.images_climb[self.indexclimb]
        # speed to go up
        elif pressed[pygame.K_UP] and self.stair==True:
            self.dy=-speedy
            self.image = self.images_climb[self.indexclimb]
        if pressed[pygame.K_UP] == False and pressed[pygame.K_DOWN] == False and self.stair == True:
            self.counterclimb = 0
            self.indexclimb = 0
            self.image = self.images_climb[0]

        # animation part: if counter > 20 change picture to the next and counter to 0
        self.counter += 1
        self.counterclimb += 1
        if self.counter > walking:
            self.counter = 0
            self.index += 1
            if self.index >= len(self.images_right):
                self.index = 0
            if self.direction == 1:
                self.image = self.images_right[self.index]
            if self.direction == -1:
                self.image = self.images_left[self.index]
            if self.counterclimb > climbing:
                self.counterclimb = 0
                self.indexclimb += 1
            if self.indexclimb >= 2:
                self.indexclimb = 0
        


        # checking tot gravitation
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

        # checking for collide with bottom
        if self.rect.bottom > h:
            self.rect.bottom = h
            self.dy = 0
        # checking to left side 
        if self.rect.left < 0:
            self.rect.left = 0
            self.dx = 0
        # checking to right side 
        if self.rect.right > w:
            self.rect.right = w
            self.dx = 0
# classes for first part
class Floor(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__() 
        self.image=pygame.image.load("images/floorimg.png")
        self.image = pygame.transform.scale(self.image, (2000, 66))
        self.rect = self.image.get_rect()
        self.rect.center=(600+1200*x,200*(y+1)+24+66*y-532)
    def update(self):
        global OUTX
        global OUTY
        self.rect.move_ip(OUTX*speed,OUTY*speedy)
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
        self.rect.move_ip(self.speed+OUTX*speed,OUTY*speedy)
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
        self.rect.move_ip(OUTX*speed,OUTY*speedy)
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
        self.rect.move_ip(OUTX*speed,OUTY*speedy)
class Bottle(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__() 
        self.image=pygame.image.load("images/bottle.png")
        self.image = pygame.transform.scale(self.image, (34, 55))
        self.rect = self.image.get_rect() 
        self.rect.x=x
        self.rect.y=y
    def update(self):
        global OUTX
        global OUTY
        self.rect.move_ip(OUTX*speed,OUTY*speedy)
class Health():
    def __init__(self,x):
        self.image=pygame.image.load("images/health.png")
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.rect = self.image.get_rect() 
        self.rect.x=20+50*x
        self.rect.y=20
# classes for second part
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
        self.image = pygame.transform.scale(self.image,(80,80))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, screen_width - self.rect.width)
        self.rect.y = 0
        self.speed = speed_second
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
            self.image = pygame.transform.scale(self.image,(80,80))
            self.last_animation_update = current_time
        self.rect.y += self.speed
        if self.rect.top > self.screen_height:
            self.kill()
            game_score += 1
            print(game_score)
class Player_second(pygame.sprite.Sprite):
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
        self.ultimate_duration = pygame.time.get_ticks() + 600
        # Start ultimate timer

    def deactivate_ultimate(self):
        # Reset ultimate ability status
        for zombie in zombies_group:
            zombie.speed = speed_second  # Reset zombies' movement speed
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
class Button():
	def __init__(self, image, pos, text_input, font, base_color, hovering_color):
		self.image = image
		self.x_pos = pos[0]
		self.y_pos = pos[1]
		self.font = font
		self.base_color, self.hovering_color = base_color, hovering_color
		self.text_input = text_input
		self.text = self.font.render(self.text_input, True, self.base_color)
		if self.image is None:
			self.image = self.text
		self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
		self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos-10))

	def update(self, screen):
		if self.image is not None:
			screen.blit(self.image, self.rect)
		screen.blit(self.text, self.text_rect)

	def checkForInput(self, position):
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			return True
		return False

	def changeColor(self, position):
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			self.text = self.font.render(self.text_input, True, self.hovering_color)
		else:
			self.text = self.font.render(self.text_input, True, self.base_color)


player = Player(400, 300)
health=[]
#making sprites and add to groupes
for i in range(5):
    health1=Health(i)
    health.append(health1)
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
stair6=Stair(400,-365)
stair7=Stair(1100,-365)
stair=pygame.sprite.Group()
stair.add(stair1)
stair.add(stair2)
stair.add(stair3)
stair.add(stair4)
stair.add(stair5)
stair.add(stair6)
stair.add(stair7)
door1=Door(30,-168,0)
door2=Door(2000-200,-167,1)
door3=Door(30,800-168,2)
door4=Door(2000-300,800-168,3)
door5=Door(1550,98,4)
door6=Door(2000-130,366,4)
door6.image=pygame.image.load("images/deliverymachine.png")
door6.image=pygame.transform.scale(door6.image,(80,100))
door=pygame.sprite.Group()
door.add(door1)
door.add(door2)
door.add(door3)
door.add(door4)
bottle=pygame.sprite.Group()
for i in range (11):
    new_bottle=Bottle(botpos[POS][i][0],botpos[POS][i][1])
    bottle.add(new_bottle)
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

def transparency():
    done = False
    t=255#alpha level and timer
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
                pygame.quit()
                sys.exit()
        # show last elements 
        screen.blit(backimg,backrect)
        for i in all_sprites:
            screen.blit(i.image,i.rect)
        if POS==3:
            screen.blit(door5.image,door5.rect)
        if POS==2:
            screen.blit(door5.image,door5.rect)
        for i in bottle:
            screen.blit(i.image,i.rect)
        for i in health:
            screen.blit(i.image,i.rect)
        screen.blit(player.image,player.rect)
        for i in enemy:
            screen.blit(i.image,i.rect)
        #make surface to transparency
        s = pygame.Surface((1200,800))
        t-=5
        if t<0:
            t=0
            done=True
        if t==0:
            first_round() 
        s.set_alpha(t)# alpha level
        s.fill((0,0,0))# this fills the entire surface
        screen.blit(s, (0,0)) 
        pygame.display.update()
        clock.tick(FPS)
def change(colldoor):
    done = False
    t=0 #timer to transparency
    # while loop to transparency
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
    global backimg
    global backrect
    global POS
    global bottle
    index=colldoor.index
    #cheking for door index (if index%2==0 door is left)
    if index%2==0:
        POS-=1 #changing scene to left part
    else:
        POS+=1 #changing scene to right part
    if POS==-1: # -1 out of scene (so we make it last right scene)
        POS=3
    elif POS==4: # 4 out of scene (so we make it last left scene)
        POS=0
    if index==0:#index of door
        j=1
        # changing all spites position
        for i in all_sprites:  
            i.rect.x=positions[POS][j][0]-800
            i.rect.y=positions[POS][j][1]+533
            j+=1
        j=0
        # changing enemys position
        for i in enemy:  
            i.rect.x=enem[j][0]-800
            i.rect.y=enem[j][1]+533
            i.speed=-4
            j+=1
        j=0
        #remove bottle sprites to add new scene bottles
        for i in bottle:
            bottle.remove(i)
        #giving positions to all sprites
        for i in range(len(botpos[POS])):
            new_bottle=Bottle(botpos[POS][i][0]-800,botpos[POS][i][1]+533)
            bottle.add(new_bottle)
        backimg = pygame.image.load(positions[POS][0])
        backimg=pygame.transform.scale(backimg, (2000, 1333))
        backrect=backimg.get_rect()
        backrect.x=-800
        backrect.y=0
        door5.rect.x=1550-800
        door5.rect.y=98+533
        door6.rect.x=1870-800
        door6.rect.y=366+533
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
        j=0
        for i in bottle:
            bottle.remove(i)
        for i in range(len(botpos[POS])):
            new_bottle=Bottle(botpos[POS][i][0],botpos[POS][i][1]+533)
            bottle.add(new_bottle)
        backimg = pygame.image.load(positions[POS][0])
        backimg=pygame.transform.scale(backimg, (2000, 1333))
        backrect=backimg.get_rect()
        backrect.x=0
        backrect.y=0
        door5.rect.x=1550
        door5.rect.y=98+533
        door6.rect.x=1870
        door6.rect.y=366+533
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
        for i in bottle:
            bottle.remove(i)
        for i in range(len(botpos[POS])):
            new_bottle=Bottle(botpos[POS][i][0]-800,botpos[POS][i][1])
            bottle.add(new_bottle)
        backimg = pygame.image.load(positions[POS][0])
        backimg=pygame.transform.scale(backimg, (2000, 1333))
        backrect=backimg.get_rect()
        backrect.x=-800
        backrect.y=-533
        door5.rect.x=1550-800
        door5.rect.y=98
        door6.rect.x=1870-800
        door6.rect.y=366
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
        for i in bottle:
            bottle.remove(i)
        for i in range(len(botpos[POS])):
            new_bottle=Bottle(botpos[POS][i][0],botpos[POS][i][1])
            bottle.add(new_bottle)
        backimg = pygame.image.load(positions[POS][0])
        backimg=pygame.transform.scale(backimg, (2000, 1333))
        backrect=backimg.get_rect()
        backrect.x=0
        backrect.y=-533
        door5.rect.x=1550
        door5.rect.y=98
        door6.rect.x=1870
        door6.rect.y=366
        player.rect.center=(positions[POS][20][0]+50,positions[POS][20][1]+69)
    global speed
    global speedy
    speed=6
    speedy=3


    transparency()
def first_round():
    done = False
    while not done:
        global backimg
        global backrect
        global time 
        global tome
        global alpha
        global printbot
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

        collene=pygame.sprite.groupcollide(enemy,stair,False,False)
        for j in collene:
            j.speed=j.speed*(-1)
        for i in all_sprites:
            i.update()
        door5.update()
        door6.update()
        player.update()
        for i in enemy:
            i.update()
        for i in bottle:
            i.update()
        colldoor=pygame.sprite.spritecollideany(player,door)
        if colldoor and pressed[pygame.K_RETURN]:
            botpos[POS].clear()
            change(colldoor)
        time+=1
        collplay =pygame.sprite.spritecollideany(player,enemy)
        if collplay and time>tome:
            if(len(health)>1):
                health.pop()
            else:
                lose()
            alpha=128
            time=clock.get_rawtime()
            tome=clock.get_rawtime()+100

        collbot=pygame.sprite.spritecollideany(player,bottle)
        if collbot:
            printbot+=1
            print(printbot)
            bottle.remove(collbot)
        colldopl=pygame.sprite.collide_rect(player,door5)
        if colldopl and pressed[pygame.K_RETURN] and POS==3:
            second_round()
        colluppl=pygame.sprite.collide_rect(player,door6)
        if colluppl and pressed[pygame.K_RETURN] and POS==2:
            buy_menu()


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



        
        
        backrect.x+=OUTX*speed
        backrect.y+=OUTY*speedy
        screen.blit(backimg,backrect)
        for i in all_sprites:
            screen.blit(i.image,i.rect)
        if POS==3:
            screen.blit(door5.image,door5.rect)
        if POS==2:
            screen.blit(door6.image,door6.rect)
        for i in bottle:
            screen.blit(i.image,i.rect)
        for i in health:
            screen.blit(i.image,i.rect)
        screen.blit(player.image,player.rect)
        for i in enemy:
            screen.blit(i.image,i.rect)
        s = pygame.Surface((1200,800))  # the size of your rect
        if alpha>0:
            alpha-=1
            color=(255,0,0)
        else:
            color=(0,0,0)
        s.set_alpha(alpha)                # alpha level
        s.fill(color)           # this fills the entire surface
        screen.blit(s, (0,0)) 
        game_score_text = game_score_font.render(f'BOTTLES: {printbot}', True, (255, 255, 255))
        screen.blit(game_score_text, game_score_rect)
        pygame.display.update()
        clock.tick(FPS)
def second_round():
    global game_state
    global speed_second
    global game_score
    # Создаем группу спрайтов для пуль и зомби


    player_image = pygame.image.load("images/90deg.png").convert_alpha()
    player_image = pygame.transform.scale(player_image, (42, 74))
    player = Player_second(player_image, 1200, 800)

    backgroundgame = pygame.image.load("images/background3.png").convert_alpha()
    backgroundgame = pygame.transform.scale(backgroundgame, (1200, 800))
    backgroundgame_rect = backgroundgame.get_rect()

    game_score_font = pygame.font.Font("images/Daydream.ttf", 15)
    game_score_text = game_score_font.render(f'PAST ZOMBIES: {game_score}', True, (0, 0, 0))
    game_score_rect = game_score_text.get_rect(midtop=(200,50))

    # Главный цикл игры
    current_time =0
    running = True
    zombie_spawn_timer = 0  # Добавляем таймер для появления зомби
    t=0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        t+=3
        if t>255:
            t=255
            running=False
        s = pygame.Surface((1200,800))
        s.set_alpha(t)# alpha level
        s.fill((0,0,0))# this fills the entire surface
        screen.blit(s, (0,0)) 
        pygame.display.update()
        clock.tick(FPS)
    running = True
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
        current_time+=1
        if current_time < 1500:
            zombie_spawn_interval =100
            speed_second = 1.5
        elif current_time < 3000 and current_time > 1500:
            zombie_spawn_interval =70
            speed_second = 2
        elif current_time < 4500 and current_time > 3000:
            zombie_spawn_interval = 40
            speed_second = 2.5
        elif current_time>4500:
            end()



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
            lose()

        pygame.display.update()
        clock.tick(60)
def create_zombie():
    new_zombie = Zombie(1200, 800, 200, zombie_image_paths)
  # Создание нового объекта зомби
    zombies_group.add(new_zombie)  # Добавление нового зомби в группу
def load_animation_frames(image_paths):
    frames = []
    for path in image_paths:
        frame = pygame.image.load(path).convert_alpha()
        frames.append(frame)
    return frames
def main_menu():
    BG = pygame.image.load("images/bc.png")
    BG = pygame.transform.scale(BG,(1200,800))
    BG_rect = BG.get_rect()
    while True:
        screen.blit(BG, BG_rect)

        MENU_MOUSE_POS = pygame.mouse.get_pos()
        TITLE = pygame.image.load("images/title.png")
        TITLE_RECT = TITLE.get_rect(center=(500, 150))

        PLAY_BUTTON = Button(image=pygame.image.load("images/frame.png"), pos=(200, 350),
                             text_input="PLAY", font=pygame.font.Font("images/Daydream.ttf", 25), base_color=(215, 252, 212), hovering_color=(89, 4, 4))
        QUIT_BUTTON = Button(image=pygame.image.load("images/frame.png"), pos=(200, 500),
                             text_input="QUIT", font=pygame.font.Font("images/Daydream.ttf", 25), base_color=(215, 252, 212), hovering_color=(89, 4, 4))

        screen.blit(TITLE, TITLE_RECT)

        for button in [PLAY_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(screen)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    transparency()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()
def lose():
    time1=0
    done=True
    while done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
                pygame.quit()
                sys.exit()
        time1+=1
        you_lose = pygame.image.load("images/lose.png").convert_alpha()
        you_lose = pygame.transform.scale(you_lose, (1200, 800))
        you_lose_rect = you_lose.get_rect()
        screen.blit(you_lose, you_lose_rect)
        pygame.display.update()
        clock.tick(FPS)
        if time1>300:
            done= False
    pygame.quit()
    sys.exit()
def buy_menu():
    BG = pygame.image.load("images/trading.png")
    BG = pygame.transform.scale(BG,(900,600))
    BG_rect = BG.get_rect()
    BG_rect.center=(600,400)
    done=True
    image=pygame.image.load("images/cat.png")
    image=pygame.transform.scale(image,(218,90))
    cat=Button(image, pos=(326, 315),text_input="", font=pygame.font.Font("images/Daydream.ttf", 25), base_color=(215, 252, 212), hovering_color=(89, 4, 4))
    image1=pygame.image.load("images/dog.png")
    image1=pygame.transform.scale(image1,(218,90))
    dog=Button(image=image1, pos=(326, 470),text_input="", font=pygame.font.Font("images/Daydream.ttf", 25), base_color=(215, 252, 212), hovering_color=(89, 4, 4))
    image2=pygame.image.load("images/human.png")
    image2=pygame.transform.scale(image2,(218,90))
    human=Button(image=image2, pos=(326, 625),text_input="", font=pygame.font.Font("images/Daydream.ttf", 25), base_color=(215, 252, 212), hovering_color=(89, 4, 4))
    text_font1 = pygame.font.Font("images/Daydream.ttf", 15)
    text_font2 = pygame.font.Font("images/Daydream.ttf", 30)
    global cathappy
    global doghappy
    global studenthappy
    global printbot
    printbot=50
    while done:
        MENU_MOUSE_POS = pygame.mouse.get_pos()
        text_1 = text_font1.render('5 bottles:', True, (255, 255, 255))
        text1_rect = game_score_text.get_rect(midtop=(326,235))
        text_2 = text_font1.render('10 bottles', True, (255, 255, 255))
        text2_rect = game_score_text.get_rect(midtop=(326,390))
        text_3 = text_font1.render('20 bottles', True, (255, 255, 255))
        text3_rect = game_score_text.get_rect(midtop=(326,540))
        text_4 = text_font2.render(f'x{cathappy}', True, (255, 255, 255))
        text4_rect = game_score_text.get_rect(midtop=(530,305))
        text_5 = text_font2.render(f'x{doghappy}', True, (255, 255, 255))
        text5_rect = game_score_text.get_rect(midtop=(530,455))
        text_6 = text_font2.render(f'x{studenthappy}', True, (255, 255, 255))
        text6_rect = game_score_text.get_rect(midtop=(530,595))
        text_7 = text_font2.render(f'x{printbot}', True, (255, 255, 255))
        text7_rect = game_score_text.get_rect(midtop=(860,310))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if cat.checkForInput(MENU_MOUSE_POS) and printbot>=5:
                    printbot-=5
                    cathappy+=1
                if dog.checkForInput(MENU_MOUSE_POS) and printbot>=10:
                    printbot-=10
                    doghappy+=1 
                if human.checkForInput(MENU_MOUSE_POS) and printbot>=20:
                    printbot-=20
                    studenthappy+=1
        pressed=pygame.key.get_pressed()
        if pressed[pygame.K_ESCAPE]:
            first_round()  
        screen.blit(BG, BG_rect)
        screen.blit(text_1,text1_rect)
        screen.blit(text_2,text2_rect)          
        screen.blit(text_3,text3_rect) 
        screen.blit(text_4,text4_rect) 
        screen.blit(text_5,text5_rect) 
        screen.blit(text_6,text6_rect) 
        screen.blit(text_7,text7_rect)    
        cat.update(screen)
        dog.update(screen)
        human.update(screen)             
        pygame.display.update()
        clock.tick(FPS)
    pygame.quit()
    sys.exit()
def end():
    done=True
    t=0
    j=0
    # endfly=[]
    # for i in range(27):
    #     endfly.append(pygame.image.load(f"images/endfly/pixil-frame-{i}.png"))
    while done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
                pygame.quit()
                sys.exit()
        t+=1
        image=pygame.image.load("images/endtunnel/text1.png")
        image = pygame.transform.scale(image, (1200, 400))
        end_rect = image.get_rect()
        end_rect.center=(600,400)
        screen.fill((0,0,0))
        screen.blit(image, end_rect)
        pygame.display.update()
        clock.tick(FPS)
        if t==300:
            done= False
    done=True
    t=0
    j=0
    image=pygame.image.load(f"images/endtunnel/pixil-frame-{j}.png")
    while done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
                pygame.quit()
                sys.exit()
        t+=1
        if t==17:
            image=pygame.image.load(f"images/endtunnel/pixil-frame-{j}.png")
            t=0
            j+=1
        image = pygame.transform.scale(image, (1200, 400))
        end_rect = image.get_rect()
        end_rect.center=(600,400)
        screen.blit(image, end_rect)
        pygame.display.update()
        clock.tick(FPS)
        if j==18 and t==16:
            done= False
    done=True
    t=0
    j=0
    while done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
                pygame.quit()
                sys.exit()
        t+=1
        image=pygame.image.load("images/endtunnel/text2.png")
        image = pygame.transform.scale(image, (1200, 400))
        end_rect = image.get_rect()
        end_rect.center=(600,400)
        screen.fill((0,0,0))
        screen.blit(image, end_rect)
        pygame.display.update()
        clock.tick(FPS)
        if t==300:
            done= False
    done=True
    t=0
    j=0
    image=pygame.image.load(f"images/endfly/pixil-frame-{j}.png")
    while done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
                pygame.quit()
                sys.exit()
        t+=1
        if t==9:
            image=pygame.image.load(f"images/endfly/pixil-frame-{j}.png")
            t=0
            j+=1
        image = pygame.transform.scale(image, (1200, 400))
        end_rect = image.get_rect()
        end_rect.center=(600,400)
        screen.blit(image, end_rect)
        pygame.display.update()
        clock.tick(FPS)
        if j==26 and t==8:
            done= False



    
    pygame.quit()
    sys.exit()
main_menu()

    