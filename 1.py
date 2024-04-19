import pygame, sys
pygame.init()
WIDTH = 1000
HEIGHT = 750
BG = pygame.image.load("bc.png")
pygame.display.set_caption("THE WALKING STUDENTS")
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.font.get_fonts()
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

def play():
    while True:
        # ТУТ ДОЛЖНА ИГРА ЗАПУСКАТЬСЯ
        pygame.quit()
    
def options():
    while True:
        pygame.quit()
        # ЧЕ ТО ДОБАВИТЬ НУЖНО В ОПЦИЯХ 

        # OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        # SCREEN.fill("white")

        # OPTIONS_TEXT = pygame.font.SysFont("silver", 50).render("This is the OPTIONS screen.", True, "Black")
        # OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(640, 260))
        # SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)

        # OPTIONS_BACK = Button(image=None, pos=(640, 460), 
        #                     text_input="BACK", font=pygame.font.SysFont("silver", 50), base_color="Black", hovering_color="Green")

        # OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        # OPTIONS_BACK.update(SCREEN)

        # for event in pygame.event.get():
        #     if event.type == pygame.QUIT:
        #         pygame.quit()
        #         sys.exit()
        #     if event.type == pygame.MOUSEBUTTONDOWN:
        #         if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
        #             main_menu()

        # pygame.display.update()

def main_menu():
    while True:
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()
        TITLE = pygame.image.load("title.png")
        TITLE_RECT = TITLE.get_rect(center=(500, 150))

        PLAY_BUTTON = Button(image=pygame.image.load("frame.png"), pos=(200, 350), 
                            text_input="PLAY", font=pygame.font.Font("Daydream.ttf", 25), base_color=(215, 252, 212), hovering_color=(89,4,4))
        OPTIONS_BUTTON = Button(image=pygame.image.load("frame.png"), pos=(200, 500), 
                            text_input="OPTIONS", font=pygame.font.Font("Daydream.ttf", 21), base_color=(215, 252, 212), hovering_color=(89,4,4))
        QUIT_BUTTON = Button(image=pygame.image.load("frame.png"), pos=(200, 650), 
                            text_input="QUIT", font=pygame.font.Font("Daydream.ttf", 25), base_color=(215, 252, 212), hovering_color=(89,4,4))

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
                    play()
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    options()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

main_menu()