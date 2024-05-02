import pygame, sys, time

def video():
    pygame.init()
    pygame.mixer.init()
    w=1200
    h=800
    FPS=56
    clock = pygame.time.Clock()
    screen=pygame.display.set_mode((w,h))
    sequence=[]
    done=True
    i=0
    ti = round(time.time() * 1000)
    print(ti)
    s="000"
    sound = pygame.mixer.Sound('video/firstcataudio/video.wav')
    sound.play()
    image = pygame.image.load(f"video/firstcat/video{s+str(i)}.jpg")
    image = pygame.transform.scale(image, (1200,800))
    image_rect=image.get_rect()
    screen.blit(image,image_rect)
    while done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pressed=pygame.key.get_pressed()
        if pressed[pygame.K_RETURN]:
            sound.stop()
            done=False
        if i/1000>=1:
            s=""
        elif i/100>=1:
            s="0"
        elif i/10>=1:
            s="00"
        else:
            s="000"
        tin = round(time.time() * 1000)
        if tin-ti>33.3*i:
            image = pygame.image.load(f"video/firstcat/video{s+str(i)}.jpg")
            image = pygame.transform.scale(image, (1200,800))
            image_rect=image.get_rect()
            screen.blit(image,image_rect)
            i+=1
            if i==1203:
                print(tin)
                done=False
        pygame.display.update()
        clock.tick(FPS)
