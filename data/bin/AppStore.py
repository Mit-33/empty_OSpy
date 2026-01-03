import pygame
import sys
import urllib3

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

lstApp:list[str] = []
lstSurf:list[pygame.Surface] = []
firstElem = ""

def init():
    global posZero,lstApp,lstSurf,firstElem
	#only constants arn't redifined here
    posZero = (44, 72)
    lstApp = urllib3.request("GET","http://www.mixart.fr/OSpy/appList.txt").data.decode().split("\n")
    firstElem = lstApp[0]
    lstSurf = []
    for name in lstApp:
        lstSurf += pygame.font.SysFont("Arial",32).render(name, False, pygame.color.Color("black")),

def update(screen:pygame.Surface,eventGet:list[pygame.event.Event]):
    global lstApp, lstSurf
    for event in eventGet:
        if event.type == pygame.MOUSEWHEEL:
            if len(lstApp) > 16:
                if event.y < 0 and lstApp[15] != lstApp[lstApp.index(firstElem)-1]:
                    lstApp += [lstApp.pop(0)]
                elif event.y > 0 and lstApp[0] != firstElem:
                    lstApp = [lstApp.pop(-1)] + lstApp
                lstSurf = []
                for name in lstApp:
                    lstSurf += pygame.font.SysFont("Arial",32).render(name, False, pygame.color.Color("black")),

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                for i,surf in enumerate(lstSurf,start=1):
                    if surf.get_rect(x=posZero[0]+0,y=posZero[1]+i*surf.get_height()).collidepoint(event.pos):
                        app = lstApp[i-1].split(" ")[0]
                        print("app:",app)
                        if app == "OSpy.exe":
                            with open("OSpy.exe.py","w") as file:
                                file.write(urllib3.request("GET","http://www.mixart.fr/OSpy/OSpy.exe.py").data.decode().replace("\r",""))
                        else:
                            with open("data/bin/"+app+".py","w") as file:
                                file.write(urllib3.request("GET","http://www.mixart.fr/OSpy/"+app+".py").data.decode().replace("\r",""))
                            with open("data/bin/.apps","a+") as file:
                                f = file.tell()
                                file.seek(0)
                                if "data/bin/"+app+":" not in file.read():
                                    file.seek(f)
                                    file.write("\ndata/bin/"+app+":data/bin/Python.png")
                        break
    screen.fill("#FFFF00")

    for i,surf in enumerate(lstSurf,start=1):
        screen.blit(surf,(0,i*surf.get_height()))

    
    
    
def quit():
    pass
if __name__ == "__main__":
    screen = pygame.display.set_mode(size,pygame.RESIZABLE)

    init()

    posZero = (0, 0)

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

