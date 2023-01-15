import pygame
import os
import random

COLORS = {
    "gray" : (105, 105, 105),
    "blue" : (0, 0, 50),
    "white" : (255, 255, 255),
    "black" : (0, 0, 0),
    "green" : (0, 255, 0)
}
pygame.init()
WIDTH, HEIGHT = 1500, 844
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Try to fly")
font = pygame.font.SysFont("Arial", 20) 
buttons = []
CANNONWIDTH = 100
CANNONHEIGHT = 100
CANNON_WHEEL_IMAGE = pygame.image.load(os.path.join("Assets", "CannonWheel.png"))
CANNON_BARREL_IMAGE = pygame.image.load(os.path.join("Assets", "CannonBarrel.png"))

CANNON_FUSE_IMAGE = pygame.image.load(os.path.join("Assets", "CannonFuse.png"))
CANNON_WHEEL = pygame.transform.scale(CANNON_WHEEL_IMAGE, (CANNONWIDTH, CANNONHEIGHT))
FPS = 60

STARWIDTH, STARHEIGHT = 10, 10

STAR = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "Star.png")), (STARWIDTH, STARHEIGHT))

rotationmodifyer = 1
is_in_game = False
Ingame_Cannon_Rotation = 30
is_awaiting_cannon_angle_stop = False
has_cannon_angle_stopped = False
cannon_power_timer = 3 * FPS
is_awaiting_cannon_power_spam = False
cannon_power = 0
has_shot = False


PENGUINWIDTH, PENGUINHEIGHT = 100, 200
PENGUIN_IMAGE = pygame.image.load(os.path.join("Assets", "Penguin.png"))
PENGUIN = pygame.transform.scale(PENGUIN_IMAGE, (PENGUINWIDTH, PENGUINHEIGHT))

GRAVITATION = 0.3
PenguinDistance = 0
PenguinDistanceVel = 0
PenguinHeight = 0
PenguinHeightVel = 0
coordinates_now = [0, 0]
is_grounded = False
finalrot = 0

penguincords = (0, 0)

objs = []

stars = []

class Gameobj:

    def __init__(self, x_pos, y_pos, image, is_background, is_collectable = False):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.image = image
        self.is_background = is_background
        self.is_collectable = is_collectable

    def draw_if_needed(self):
        global coordinates_now
        if self.x_pos > coordinates_now[0] - WIDTH * 0.2 and self.x_pos < coordinates_now[0] + WIDTH + WIDTH * 0.2 and self.y_pos > coordinates_now[1] * HEIGHT * 0.2 and self.y_pos < coordinates_now[1] + HEIGHT + HEIGHT * 0.2:
            x_pos = self.x_pos - coordinates_now[0]
            y_pos = self.y_pos - coordinates_now[1]
            WIN.blit(self.image, (x_pos, y_pos))



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
    global is_awaiting_cannon_angle_stop
    is_awaiting_cannon_angle_stop = True
    global has_cannon_angle_stopped
    has_cannon_angle_stopped = False
    global has_shot
    has_shot = False
    global is_awaiting_cannon_power_spam
    is_awaiting_cannon_power_spam = True
    global cannon_power_timer
    cannon_power_timer = FPS * 3
    global is_grounded
    is_grounded = False
    for _ in range(100):
        stars.append(pygame.Rect(random.randint(-200, WIDTH + 200), random.randint(-200, HEIGHT + 200), STARWIDTH, STARHEIGHT))
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
        global Ingame_Cannon_Rotation
        global rotationmodifyer
        global is_awaiting_cannon_power_spam
        global PenguinDistanceVel
        global PenguinHeightVel
        global finalrot

        for star in stars:
            WIN.blit(STAR, (star.x, star.y))

        pygame.draw.rect(WIN, COLORS["black"], pygame.Rect(0, HEIGHT - HEIGHT * 0.2, WIDTH, HEIGHT * 0.2))
        



        if (is_awaiting_cannon_angle_stop == False) and (is_awaiting_cannon_power_spam == False):
            for star in stars:
                star.x -= PenguinDistanceVel
                star.y += PenguinHeightVel
                if star.x < -100:
                    star.x = WIDTH + 100
                if star.y < -300:
                    star.y = HEIGHT + 200
                elif star.y > HEIGHT + 300:
                    star.y = -200
            global cannon_wheel
            global CANNON_WHEEL
            global cannon_barrel
            global CANNON_BARREL
            global is_grounded
            
            if cannon_barrel.x > -500:
                cannon_barrel.x -= 1 * PenguinDistanceVel
            if cannon_barrel.y < HEIGHT + 500:
                cannon_barrel.y += 1 * PenguinHeightVel

            if cannon_wheel.x > -500:
                cannon_wheel.x -= 1 * PenguinDistanceVel
            if cannon_wheel.y < HEIGHT + 500:
                cannon_wheel.y += 1 * PenguinHeightVel
            
            if cannon_barrel.x > -500 and cannon_barrel.y < HEIGHT + 500:
                WIN.blit(CANNON_BARREL, (cannon_barrel.x, cannon_barrel.y))
            if cannon_wheel.x > -500 and cannon_wheel.y < HEIGHT + 500:
                WIN.blit(CANNON_WHEEL, (cannon_wheel.x, cannon_wheel.y))
            
            for obj in objs:
                obj.draw_if_needed()
            rot = PenguinHeightVel - 90
            if rot < -180:
                rot = -180
            if rot > -20:
                rot = -20
            if not is_grounded:
                global Penguin
                if Penguin.x != WIDTH / 2:
                    Penguin.x += 1
                if Penguin.y != int(HEIGHT / 2 - HEIGHT * 0.2):
                    Penguin.y -= 1
                coordinates_now[0] += PenguinDistanceVel
                coordinates_now[1] += PenguinHeightVel
                PenguinHeightVel -= GRAVITATION
                PenguinDistanceVel -= GRAVITATION * 0.2
                if PenguinDistanceVel < 0:
                    PenguinDistanceVel = 0
                if coordinates_now[1] <= 0:
                    
                    is_grounded = True
                WIN.blit(pygame.transform.rotate(PENGUIN, rot), (Penguin.x, Penguin.y))
                finalrot = rot
                
            else:
                PenguinDistanceVel = 0
                PenguinHeightVel = 0
                print(Penguin.y, HEIGHT * 0.2, HEIGHT)
                if Penguin.y < HEIGHT * 0.68:
                    Penguin.y += 10
                WIN.blit(pygame.transform.rotate(PENGUIN, finalrot), (Penguin.x, Penguin.y))
                



        else:
            Penguin = pygame.Rect(WIDTH * 0.1, (HEIGHT - CANNONHEIGHT - HEIGHT * 0.2) - 30 - Ingame_Cannon_Rotation * 3, PENGUINWIDTH, PENGUINHEIGHT)
            
            if not has_cannon_angle_stopped:
                Ingame_Cannon_Rotation += rotationmodifyer
            else:
                global cannon_power_timer
                if cannon_power_timer > 0:
                    cannon_power_timer -= 1
                    
                    is_awaiting_cannon_power_spam = True
                else:
                    is_awaiting_cannon_power_spam = False
                    global has_shot
                    has_shot = True
            if Ingame_Cannon_Rotation > 60:
                rotationmodifyer *= -1
            elif Ingame_Cannon_Rotation < 10:
                rotationmodifyer *= -1
            cannon_barrel = pygame.Rect(WIDTH * 0.1, (HEIGHT - CANNONHEIGHT - HEIGHT * 0.2) - 30 - Ingame_Cannon_Rotation * 3, CANNONWIDTH, CANNONHEIGHT)
            CANNON_BARREL = pygame.transform.rotate(pygame.transform.scale(CANNON_BARREL_IMAGE, (CANNONWIDTH * 3, CANNONHEIGHT)), Ingame_Cannon_Rotation)

            WIN.blit(CANNON_BARREL, (cannon_barrel.x, cannon_barrel.y))

            cannon_wheel = pygame.Rect(WIDTH * 0.1, HEIGHT - CANNONHEIGHT - HEIGHT * 0.2, CANNONWIDTH, CANNONHEIGHT)
            WIN.blit(CANNON_WHEEL, (cannon_wheel.x, cannon_wheel.y))
            PenguinHeightVel = cannon_power
            PenguinDistanceVel = cannon_power



def exit_game():
    pygame.quit()

def main():
    clock = pygame.time.Clock()
    draw_scene(screentype="mainmenu")
    RUN = True
    while RUN:
        for event in pygame.event.get():
            keys = pygame.key.get_pressed()
            if event.type == pygame.QUIT:
                RUN = False
            for button in buttons:
                button.click(event)
            global is_awaiting_cannon_angle_stop
            if is_awaiting_cannon_angle_stop:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_e:
                        print("Rotation festgelegt.")
                        global has_cannon_angle_stopped
                        has_cannon_angle_stopped = True
                        
                        is_awaiting_cannon_angle_stop = False
            if is_awaiting_cannon_power_spam:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_e:
                        print("Kraft wird erhöht.")
                        global cannon_power
                        cannon_power += 1


        if is_in_game:
            draw_scene("game")

        clock.tick(FPS)
        



        pygame.display.update()
    
    exit_game()

if __name__ == "__main__":
    main()
