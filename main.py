import pygame
import os
import random
import json
import base64

COLORS = {
    "gray" : (105, 105, 105),
    "blue" : (0, 0, 50),
    "white" : (255, 255, 255),
    "black" : (0, 0, 0),
    "green" : (0, 255, 0),
    "nightsky" : (7, 11, 52)
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
COINWIDTH, COINHEIGHT = 50, 50

STAR = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "Star.png")), (STARWIDTH, STARHEIGHT))
COIN = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "Silvercoin.png")), (COINWIDTH, COINHEIGHT))

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
coins_this_round = 0
cash = 0

penguincords = (0, 0)

objs = []

stars = []
coins = []

upgrades = {
    "bettercannon" : {
        "cost" : 10,
        "level" : 1,
        "costinc" : 1.5
    },
    "airresistance" : {
        "cost" : 10,
        "level" : 1,
        "costinc" : 1.55
    },
    "antigravityboots" : {
        "cost" : 10,
        "level" : 1,
        "costinc" : 1.8
    },
    "morecoins" : {
        "cost" : 10,
        "level" : 1,
        "costinc" : 3.5
    },
    "rocketboost" : {
        "cost" : 7000,
        "level" : 1,
        "costinc" : 0.5,
        "unlocked" : False
    },
    "rocketboostcooldown" : {
        "cost" : 10,
        "level" : 1,
        "costinc" : 5
    },
    "strongerrocketboost" : {
        "cost" : 10,
        "level" : 1,
        "costinc" : 7
    }
}


def save():
    #TODO: Speichern einbauen
    #Dinge die gespeichert werden sollen:
    #Geld
    #Einstellungen
    #Alle statistiken
    global cash

    savegamedict = {}

    savegamedict["cash"] = cash
    savegamedict["upgrades"] = upgrades


    with open("savegame.json", "w") as file:
        json.dump(savegamedict, file)

def load():
    #TODO: Laden einbauen
    #Alles was gespeichert wird soll auch geladen werden
    global cash
    global upgrades
    try:
            with open('savegame.json', 'r') as file:
                data = json.load(file)
                cash = data["cash"]
                upgrades = data["upgrades"]
    except:
        raise
    

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
    global cash
    global coins_this_round
    cash += coins_this_round
    save()
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
    global coordinates_now
    coordinates_now = [0, 0]
    coins_this_round = 0
    global PenguinDistanceVel
    PenguinDistanceVel = 0
    global PenguinDistance 
    PenguinDistance = 0
    global PenguinHeightVel
    PenguinHeightVel = 0
    global PenguinHeight
    PenguinHeight = 0
    global cannon_power
    cannon_power = 0

    for _ in range(100):
        stars.append(pygame.Rect(random.randint(-200, WIDTH + 200), random.randint(-200, HEIGHT + 200), STARWIDTH, STARHEIGHT))
    for _ in range(7 + upgrades["morecoins"]["level"]):
        coins.append(pygame.Rect(random.randint(-200, WIDTH + 200), random.randint(-200, HEIGHT + 200), COINWIDTH, COINHEIGHT))
    draw_scene("game")

def change_to_settings_scene():
    save()
    buttons.clear()
    global is_in_game
    is_in_game = False
    draw_scene("settings")

def change_to_upgrades_scene():
    save()
    buttons.clear()
    global is_in_game
    is_in_game = False
    draw_scene("upgrades")

def change_to_stats_scene():
    save()
    buttons.clear()
    global is_in_game
    is_in_game = False
    draw_scene("stats")

def change_to_main_menu():
    global cash
    global coins_this_round
    cash += coins_this_round
    coins_this_round = 0
    save()
    buttons.clear()
    global is_in_game
    is_in_game = False
    draw_scene("mainmenu")

def quitgame():
    save()
    exit_game()



def draw_scene(screentype):
    global cash
    global upgrades

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
    

    elif screentype == "game":
        global is_in_game
        is_in_game = True
        WIN.fill((COLORS["nightsky"]))
        global Ingame_Cannon_Rotation
        global rotationmodifyer
        global is_awaiting_cannon_power_spam
        global PenguinDistanceVel
        global PenguinHeightVel
        global coins_this_round
        global Penguin
        global finalrot

        for star in stars:
            WIN.blit(STAR, (star.x, star.y))

        for coin in coins:
            WIN.blit(COIN, (coin.x, coin.y))

        pygame.draw.rect(WIN, COLORS["black"], pygame.Rect(0, HEIGHT - HEIGHT * 0.2, WIDTH, HEIGHT * 0.2))
        
        font = pygame.font.SysFont("Arial", 30)
        text = font.render(f"text: {int(PenguinDistanceVel)} Km/H", 1, pygame.Color("White"))
        WIN.blit(text, (WIDTH * 0.1, HEIGHT - HEIGHT * 0.15))
    
        font = pygame.font.SysFont("Arial", 30)
        text = font.render(f"Height: {int(coordinates_now[1] / 100)}m", 1, pygame.Color("White"))
        WIN.blit(text, (WIDTH * 0.1, HEIGHT - HEIGHT * 0.1))

        font = pygame.font.SysFont("Arial", 30)
        text = font.render(f"Traveled Distance: {int(coordinates_now[0] / 100)}m", 1, pygame.Color("White"))
        WIN.blit(text, (WIDTH * 0.3, HEIGHT - HEIGHT * 0.15))

        font = pygame.font.SysFont("Arial", 30)
        text = font.render(f"Coins collected: {int(coins_this_round)}", 1, pygame.Color("White"))
        WIN.blit(text, (WIDTH * 0.3, HEIGHT - HEIGHT * 0.1))



        if (is_awaiting_cannon_angle_stop == False) and (is_awaiting_cannon_power_spam == False):
            for star in stars:
                star.x -= PenguinDistanceVel
                star.y += PenguinHeightVel
                if star.x < -100:
                    star.x = WIDTH + random.randint(10, 200)
                if star.y < -300:
                    star.y = HEIGHT + random.randint(10, 200)
                elif star.y > HEIGHT + 300:
                    star.y = random.randint(-200, -10)
            for coin in coins:
                coin.x -= PenguinDistanceVel
                coin.y += PenguinHeightVel
                if coin.x < -100:
                    coin.x = WIDTH + 100
                if coin.y < -300:
                    coin.y = HEIGHT + 200
                elif coin.y > HEIGHT + 300:
                    coin.y = -200
                if coin.colliderect(Penguin):
                    coin.x = -50
                    coin.y = -50
                    
                    coins_this_round += 1

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
            if rot < -130:
                rot = -130
            if rot > -50:
                rot = -50
            if not is_grounded:
                print(coordinates_now)
                if Penguin.x != WIDTH / 2:
                    Penguin.x += 1
                if Penguin.y != int(HEIGHT / 2 - HEIGHT * 0.2):
                    Penguin.y -= 1
                coordinates_now[0] += PenguinDistanceVel
                coordinates_now[1] += PenguinHeightVel
                PenguinHeightVel -= GRAVITATION / (1 + (upgrades["antigravityboots"]["level"] / 8))
                PenguinDistanceVel -= (GRAVITATION * 0.2)  / (1 + (upgrades["airresistance"]["level"] / 8))

                WIN.blit(pygame.transform.rotate(PENGUIN, rot), (Penguin.x, Penguin.y))
                finalrot = rot
                if int(coordinates_now[1]) < HEIGHT- HEIGHT * 0.2:
                    print("runter!!")
                    print(Penguin.y)
                    if Penguin.y < HEIGHT * 0.6:
                        print("alles gut!")
                        if Penguin.y + PenguinDistanceVel < HEIGHT * 0.6 and not coordinates_now[1] - PenguinDistanceVel <= 0:
                            Penguin.y += PenguinDistanceVel
                        elif coordinates_now[1] - PenguinDistanceVel <= 0:
                            print("WEG!!!")
                            Penguin.y = HEIGHT * 0.6
                        else:
                            Penguin.y = HEIGHT * 0.6
                if PenguinDistanceVel < 0:
                    PenguinDistanceVel = 0
                if coordinates_now[1] <= 0:
                    is_grounded = True
            else:
                PenguinDistanceVel = 0
                PenguinHeightVel = 0

                WIN.blit(pygame.transform.rotate(PENGUIN, finalrot), (Penguin.x, Penguin.y))
                pygame.draw.rect(WIN, COLORS["black"], pygame.Rect(WIDTH / 2 - (WIDTH * 0.3), HEIGHT / 2 - (HEIGHT * 0.2), WIDTH * 0.6, HEIGHT * 0.2))
                font = pygame.font.SysFont("Arial", 30)
                text = font.render(f"Du bist stecken geblieben. Du hast {coins_this_round} Münzen eingesammelt!", 1, pygame.Color("White"))
                WIN.blit(text, (WIDTH / 2 - (WIDTH * 0.3), HEIGHT / 2 - (HEIGHT * 0.2)))
                backtomenubutton = Button("Back to menu", (WIDTH / 2 - (WIDTH * 0.3), HEIGHT / 2 - (HEIGHT * 0.2) + HEIGHT * 0.05), 50, change_to_main_menu)
                backtomenubutton.show()
                restartbutton = Button("restart", (WIDTH / 2 - (WIDTH * 0.1), HEIGHT / 2 - (HEIGHT * 0.2) + HEIGHT * 0.05), 50, change_to_game_scene)
                restartbutton.show()





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
            PenguinHeightVel = cannon_power + 50
            PenguinDistanceVel = cannon_power + 30

    elif screentype == "upgrades":
        #TODO Upgrades hinzufügen
        #Upgrade Ideen:
        #Bessere Kanone => Mehr CannonPower pro Klicken
        #Ergodynamischerer Pinguin => Weniger Luftwiederstand
        #Anti-Gravitations-Schuhe => Weniger Anziehungskraft
        #Mehr Münzen
        #Raketenboost => Ein Boost um sich bisschen nach vorne zu boosten
        #Raketenboost cooldown verringern
        #Raketenboost besser machen
        WIN.fill((COLORS["gray"]))
        
        def upgradecannon():
            global cash
            if upgrades["bettercannon"]["cost"] <= cash:
                cash -= upgrades["bettercannon"]["cost"]
                upgrades["bettercannon"]["cost"] = int(upgrades["bettercannon"]["costinc"] * upgrades["bettercannon"]["cost"])
                upgrades["bettercannon"]["level"] += 1
                change_to_upgrades_scene()

        btn = Button(f"Better Cannon", (WIDTH * 0.05, HEIGHT * 0.1), 60, upgradecannon)
        btn.show()
        font = pygame.font.SysFont("Arial", 60)
        text = font.render(f"Costs: {upgrades['bettercannon']['cost']}", 1, pygame.Color("White"))
        WIN.blit(text, (WIDTH * 0.05, HEIGHT * 0.17))

        def lessAirResistance():
            global cash

            if upgrades["airresistance"]["cost"] <= cash:
                cash -= upgrades["airresistance"]["cost"]
                upgrades["airresistance"]["cost"] = int(upgrades["airresistance"]["costinc"] * upgrades["airresistance"]["cost"])
                upgrades["airresistance"]["level"] += 1
                change_to_upgrades_scene()


        btn = Button(f"less air resistance", (WIDTH * 0.55, HEIGHT * 0.1), 60, lessAirResistance)
        btn.show()
        font = pygame.font.SysFont("Arial", 60)
        text = font.render(f"Costs: {upgrades['airresistance']['cost']}", 1, pygame.Color("White"))
        WIN.blit(text, (WIDTH * 0.55, HEIGHT * 0.17))

        def lessAirResistance():
            global cash

            if upgrades["antigravityboots"]["cost"] <= cash:
                cash -= upgrades["antigravityboots"]["cost"]
                upgrades["antigravityboots"]["cost"] = int(upgrades["antigravityboots"]["costinc"] * upgrades["antigravityboots"]["cost"] )
                upgrades["antigravityboots"]["level"] += 1
                change_to_upgrades_scene()
                

        btn = Button(f"Anti-Gravity-Boots", (WIDTH * 0.05, HEIGHT * 0.3), 60, lessAirResistance)
        btn.show()
        font = pygame.font.SysFont("Arial", 60)
        text = font.render(f"Costs: {upgrades['antigravityboots']['cost']}", 1, pygame.Color("White"))
        WIN.blit(text, (WIDTH * 0.05, HEIGHT * 0.37))

        def morecoins():
            global cash

            if upgrades["morecoins"]["cost"] <= cash:
                cash -= upgrades["morecoins"]["cost"]
                upgrades["morecoins"]["cost"] = int(upgrades["morecoins"]["costinc"] * upgrades["morecoins"]["cost"])
                upgrades["morecoins"]["level"] += 1
                change_to_upgrades_scene()


        btn = Button(f"more coins", (WIDTH * 0.55, HEIGHT * 0.3), 60, morecoins)
        btn.show()
        font = pygame.font.SysFont("Arial", 60)
        text = font.render(f"Costs: {upgrades['morecoins']['cost']}", 1, pygame.Color("White"))
        WIN.blit(text, (WIDTH * 0.55, HEIGHT * 0.37))

        def rocketboost():
            global cash

            if upgrades["rocketboost"]["cost"] <= cash:
                cash -= upgrades["rocketboost"]["cost"]
                upgrades["rocketboost"]["unlocked"] = True
                change_to_upgrades_scene()

        
        if upgrades['rocketboost']['unlocked']:
            btn = Button(f"unlocked", (WIDTH * 0.05, HEIGHT * 0.5), 60, change_to_upgrades_scene)
        else:
            btn = Button(f"rocketboost", (WIDTH * 0.05, HEIGHT * 0.5), 60, rocketboost)
        btn.show()
        font = pygame.font.SysFont("Arial", 60)
        text = font.render(f"Costs: {upgrades['rocketboost']['cost']}", 1, pygame.Color("White"))
        WIN.blit(text, (WIDTH * 0.05, HEIGHT * 0.57))

        def lessrocketboostcooldown():
            global cash

            if upgrades["rocketboostcooldown"]["cost"] <= cash:
                cash -= upgrades["rocketboostcooldown"]["cost"]
                upgrades["rocketboostcooldown"]["cost"] = int(upgrades["morecoins"]["costinc"] * upgrades["rocketboostcooldown"]["cost"])
                upgrades["rocketboostcooldown"]["level"] += 1
                change_to_upgrades_scene()


        btn = Button(f"less Rocketboost cooldown", (WIDTH * 0.55, HEIGHT * 0.5), 60, lessrocketboostcooldown)
        btn.show()
        font = pygame.font.SysFont("Arial", 60)
        text = font.render(f"Costs: {upgrades['rocketboostcooldown']['cost']}", 1, pygame.Color("White"))
        WIN.blit(text, (WIDTH * 0.55, HEIGHT * 0.57))

        def strongerrocketboost():
            global cash

            if upgrades["strongerrocketboost"]["cost"] <= cash:
                cash -= upgrades["strongerrocketboost"]["cost"]
                upgrades["strongerrocketboost"]["cost"] *= int(upgrades["morecoins"]["costinc"])
                upgrades["strongerrocketboost"]["level"] += 1
                change_to_upgrades_scene()

        btn = Button(f"stronger Rocketboost", (WIDTH * 0.05, HEIGHT * 0.7), 60, strongerrocketboost)
        btn.show()
        font = pygame.font.SysFont("Arial", 60)
        text = font.render(f"Costs: {upgrades['strongerrocketboost']['cost']}", 1, pygame.Color("White"))
        WIN.blit(text, (WIDTH * 0.05, HEIGHT * 0.77))

        font = pygame.font.SysFont("Arial", 60)
        text = font.render(f"Your Couins: {cash}", 1, pygame.Color("White"))
        WIN.blit(text, (WIDTH * 0.05, HEIGHT * 0.01))



        backButton = Button("Back", (WIDTH * 0.05, HEIGHT - HEIGHT * 0.15), 80, change_to_main_menu)
        backButton.show()
        

    elif screentype == "settings":
        #TODO: Einstellungen hinzufügen
        #Dinge die eingestellt werden müssen:
        #Audio
        #Auflösung
        #Fullscreen, Windowed und Borderless
        #
        pass

    elif screentype == "stats":
        #TODO: Stats einbauen
        #Dinge die getrackt werden sollen:
        #Weiteste distanz
        #höchste distanz
        #male geflogen
        #gesammte distanz
        #gesammt geld gesammelt
        #beste geschwindigkeit
        #
        pass


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
                        cannon_power += upgrades["bettercannon"]["level"]


        if is_in_game:
            draw_scene("game")

        clock.tick(FPS)
        



        pygame.display.update()
    
    exit_game()

if __name__ == "__main__":
    load()
    main()
