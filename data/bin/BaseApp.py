import pygame
import sys
path = sys.path[0]
if path.endswith("bin"):
    suppr = True
    
elif path.endswith("OSpy"):
    suppr = False

if path.count("/"):
    var = "/".join(path.split("/")[:-2]) if suppr else path
    sys.path += [var + "/lib"]
    
elif path.count("\\"):
    var = "\\".join(path.split("\\")[:-2]) if suppr else path
    sys.path += [var + "\\lib"]


pygame.init()

""" required variables """
#30*32,40*16
size = (960,640)
posZero = (44, 72)
listArgs = []

class Player:
    def __init__(self):
        self.info = {}
        self.info["x"] = 0
        self.info["y"] = 0
        self.surf = pygame.Surface((32,32))
player = Player()

def init():
    global player,posZero
	#only constants arn't redifined here
    posZero = (44, 72)
    player = Player()

def update(screen:pygame.Surface,eventGet:list[pygame.event.Event]):
    for event in eventGet:
        if event.type == pygame.KEYDOWN:
            pass
    
    screen.fill("black")
    player.surf.fill(pygame.color.Color("red"))
    screen.blit(player.surf,(player.info["x"],player.info["y"]))
    
def quit():
    global player
    del player

if __name__ == "__main__":

    screen = pygame.display.set_mode(size,pygame.RESIZABLE)

    init()

    timer = pygame.time.Clock()


    game_on = True

    while game_on:
        eventGet = pygame.event.get()
        for event in eventGet:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            

        update(screen,eventGet)
        pygame.display.update()
        timer.tick(60)

