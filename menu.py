import pygame, sys
pygame.init()

pygame.display.set_caption("THE WALKING STUDENTS")
SCREEN = pygame.display.set_mode((1200,800))
BG = pygame.image.load("images/bc.png")
BG = pygame.transform.scale(BG,(1200,800))
BG_rect = BG.get_rect()
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

def main_menu():
    # running =True
    # while running:
    #     for event in pygame.event.get():
    #         if event.type == pygame.QUIT:
    #             pygame.quit()
    #             sys.exit()
    #     t+=5
    #     if t>255:
    #         t=255
    #         running=False
    #     s = pygame.Surface((1200,800))
    #     s.set_alpha(t)# alpha level
    #     s.fill((0,0,0))# this fills the entire surface
    #     SCREEN.blit(s, (0,0)) 
    #     pygame.display.update()
    # t=255 #alpha level and timerrunning =True
    # running=True
    # while running:
    #     for event in pygame.event.get():
    #         if event.type == pygame.QUIT:
    #             running=False
    #             pygame.quit()
    #                 sys.exit()
    #         # show last elements 
    #         SCREEN.blit(BG, BG_rect)
    #         #make surface to transparency
    #         s = pygame.Surface((1200,800))
    #         t-=5
    #         if t<=0:
    #             t=0
    #             running=False
    #         s.set_alpha(t)# alpha level
    #         s.fill((0,255,0))# this fills the entire surface
    #         SCREEN.blit(s, (0,0)) 
    #         pygame.display.update()
    while True:
        SCREEN.blit(BG, BG_rect)

        MENU_MOUSE_POS = pygame.mouse.get_pos()
        TITLE = pygame.image.load("images/title.png")
        TITLE_RECT = TITLE.get_rect(center=(500, 150))

        PLAY_BUTTON = Button(image=pygame.image.load("images/frame.png"), pos=(200, 350),
                             text_input="PLAY", font=pygame.font.Font("images/Daydream.ttf", 25), base_color=(215, 252, 212), hovering_color=(89, 4, 4))
        OPTIONS_BUTTON = Button(image=pygame.image.load("images/frame.png"), pos=(200, 500),
                                text_input="OPTIONS", font=pygame.font.Font("images/Daydream.ttf", 21), base_color=(215, 252, 212), hovering_color=(89, 4, 4))
        QUIT_BUTTON = Button(image=pygame.image.load("images/frame.png"), pos=(200, 650),
                             text_input="QUIT", font=pygame.font.Font("images/Daydream.ttf", 25), base_color=(215, 252, 212), hovering_color=(89, 4, 4))

        SCREEN.blit(TITLE, TITLE_RECT)

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    return False
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()
