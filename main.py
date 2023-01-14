import pygame
import os


COLORS = {
    "gray" : (105, 105, 105),
    "blue" : (0, 0, 50),
    "white" : (255, 255, 255),
    "black" : (0, 0, 0)
}
pygame.init()
WIDTH, HEIGHT = 1500, 844
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Try to fly")
font = pygame.font.SysFont("Arial", 20) 
buttons = []
CANNONWIDTH = 100
CANNONHEIGHT = 100
CANNON_IMAGE = pygame.image.load(os.path.join("Assets", "Cannon.png"))
CANNON = pygame.transform.scale(CANNON_IMAGE, (CANNONWIDTH, CANNONHEIGHT))
is_in_game = False

FPS = 60

class Button:

    def __init__(self, text, pos, font, clickevent, bg = "black"):
        self.x, self.y = pos
        self.font = pygame.font.SysFont("Arial", font)
        self.clickevent = clickevent
        self.change_text(text, bg)
        buttons.append(self)

    def change_text(self, text, bg = "black"):
        self.text = self.font.render(text, 1, pygame.Color("White"))
        self.size = self.text.get_size()
        self.surface = pygame.Surface(self.size)
        self.surface.fill(bg)
        self.surface.blit(self.text, (0, 0))
        self.rect = pygame.Rect(self.x, self.y, self.size[0], self.size[1])

    def show(self):
        WIN.blit(self.surface, (self.x, self.y))

    def click(self, event):
        x, y = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:
                if self.rect.collidepoint(x, y):
                    print("ich wurd geklickt :o")
                    self.clickevent()

def change_to_game_scene():
    buttons.clear()
    draw_scene("game")

def change_to_settings_scene():
    buttons.clear()
    draw_scene("settings")

def change_to_upgrades_scene():
    buttons.clear()
    draw_scene("upgrades")

def change_to_stats_scene():
    buttons.clear()
    draw_scene("stats")

def quitgame():
    exit_game()


def draw_scene(screentype):
    if screentype == "mainmenu":
        WIN.fill((COLORS["gray"]))
        testbutton = Button("try to fly", (WIDTH * 0.8, HEIGHT * 0.85), 80, change_to_game_scene)
        testbutton.show()
        settingsbutton = Button("Settings", (WIDTH * 0.55, HEIGHT * 0.85), 80, change_to_settings_scene)
        settingsbutton.show()
        upgradesbutton = Button("Upgrades", (WIDTH * 0.3, HEIGHT * 0.85), 80, change_to_upgrades_scene)
        upgradesbutton.show()
        statsbutton = Button("Stats", (WIDTH * 0.15, HEIGHT * 0.85), 80, change_to_stats_scene)
        statsbutton.show()
        quitbutton = Button("Quit", (WIDTH * 0.01, HEIGHT * 0.85), 80, quitgame)
        quitbutton.show()
    

    if screentype == "game":
        global is_in_game
        is_in_game = True
        WIN.fill((COLORS["white"]))
        pygame.draw.rect(WIN, COLORS["black"], pygame.Rect(0, HEIGHT - HEIGHT * 0.2, WIDTH, HEIGHT * 0.2))
        cannon = pygame.Rect(WIDTH * 0.05, HEIGHT - CANNONHEIGHT - HEIGHT * 0.2, CANNONWIDTH, CANNONHEIGHT)
        WIN.blit(CANNON, (cannon.x, cannon.y))
        shot_rotation = pygame.Rect(cannon.x + CANNONHEIGHT, cannon.y, 200, 10)
        pygame.draw.rect(WIN, COLORS["gray"], shot_rotation)
        #TODO Das shot_rotation drehen
        

def exit_game():
    pygame.quit()

def main():
    clock = pygame.time.Clock()
    draw_scene(screentype="mainmenu")
    RUN = True
    while RUN:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                RUN = False
            for button in buttons:
                button.click(event)

        if is_in_game:
            draw_scene("game")

        clock.tick(FPS)
        



        pygame.display.update()
    
    exit_game()

if __name__ == "__main__":
    main()
