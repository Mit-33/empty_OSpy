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
    
#print(sys.path)
try:
    from lib.OSexplorer import OSexplorer
except:
    pass
from lib.OSexplorer import OSexplorer

pygame.init()

_oe:OSexplorer

""" required variables """
#20*32,30*16
size = (640,480)
posZero = (44, 72)
listArgs = ["userName"]


userName = ""
baseFont = pygame.font.SysFont("Arial", 32)
filePath = ""
filePathSurf:pygame.Surface
fileList:list[str] = []
textList:list[pygame.Surface] = []
#backSurf = baseFont.render("<--", False, pygame.color.Color("black"), pygame.color.Color("white"))
canClick = True
debug = False
select = 0
rename = ""
firstElem = ""
appExt = []


def init(_userName=""):
    global _oe, userName, posZero, filePath, filePathSurf, fileList, textList,\
        canClick, backSurf, debug, select, rename, firstElem, appExt,posZero
    posZero = (44, 72)
    userName = _userName
    _oe = OSexplorer()
    print(_oe.path,f"data\\usr\\{userName}")
    print(_userName)
    if _userName:
        #fe = OSexplorer()
        #fe.cd("data/bin")
        backSurf = pygame.transform.scale(pygame.image.load("data\\bin\\FileExplorer\\backButton.png").convert_alpha(),(32,32))
        """
        appExt

        extention1:app1
        extention2:app2
        ...
        extention n:app n
        
        """
        with open("data\\bin\\FileExplorer\\appExt") as f:
            appExt = f.readlines()

        for i,item in enumerate(appExt):
            if item.count("\n"):
                appExt[i] = item[:-1]
        #fe.cd("../..")
        #del fe
        _oe.cd(f"data\\usr\\{userName}")
        fileList = _oe.ls()
        #print("Run by OSpy")
    else:
        #print(_fe.path)
        userName = "User1"
        posZero = (0, 0)
        _oe.cd("../usr/User1/")
        print("Run alone")
        fileList = _oe.ls()
    # print(_fe.path)
    fileList.sort(key=mySortFunc)
    filePath = userName
    filePathSurf = baseFont.render(filePath, False, pygame.color.Color("black"), pygame.color.Color("white"))
    textList = []
    for name in fileList:
        textList += baseFont.render(name, False, pygame.color.Color("black")),
    canClick = True
    debug = False
    select = 0
    rename = ""
    firstElem = fileList[0]
    
def mySortFunc(any):
    lst = []
    for item in any:
        lst += ord(item.upper())*2-(0 if item.isupper() else 1),
    return lst

def update(screen:pygame.Surface,eventGet:list[pygame.event.Event]):
    global filePath, filePathSurf, fileList, textList, canClick, debug, select, rename, firstElem
    indexClick:int = 0
    toReturn = None

    for event in eventGet:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_KP0 or event.key == pygame.K_0:
                debug = True
            
            if select:
                if event.key == pygame.K_DELETE:
                    try:
                        _oe.rmfile(fileList[select-1])
                    except PermissionError:
                        _oe.rmdir(fileList[select-1])
                    
                    fileList = _oe.ls()
                    fileList.sort(key=mySortFunc)
                    firstElem = fileList[0]
                    textList = []
                    for name in fileList:
                        textList += baseFont.render(name, False, pygame.color.Color("black")),
                
                if rename:
                    if event.key == pygame.K_RETURN:
                        _oe.rename(rename, fileList[select-1])
                        rename = ""
                        
                        textList = []
                        for name in fileList:
                            textList += baseFont.render(name, False, pygame.color.Color("black")),
                        textList[select-1] = baseFont.render(fileList[select-1], False, pygame.color.Color("black"), (250, 250, 250))
                
                if event.key == pygame.K_F1 and not rename:
                    rename = fileList[select-1]
                    fileList[select-1] = ""
                    
                    textList = []
                    for name in fileList:
                        textList += baseFont.render(name, False, pygame.color.Color("black")),
                    textList[select-1] = baseFont.render(fileList[select-1], False, pygame.color.Color("black"), (0, 0, 255))
                
                
        if event.type == pygame.KEYUP:
            if rename:
                if len(pygame.key.name(event.key)) == 1:
                    fileList[select-1] += event.unicode
                
                if event.key == pygame.K_BACKSPACE:
                    fileList[select-1] = fileList[select-1][:-1]
                    
                textList = []
                for name in fileList:
                    textList += baseFont.render(name, False, pygame.color.Color("black")),
                textList[select-1] = baseFont.render(fileList[select-1], False, pygame.color.Color("black"), (0, 0, 255))
                
        if event.type == pygame.MOUSEWHEEL:
            if len(fileList) > 11:
                if event.y < 0 and fileList[11] != fileList[fileList.index(firstElem)-1]:
                    fileList += [fileList.pop(0)]
                elif event.y > 0 and fileList[0] != firstElem:
                    fileList = [fileList.pop(-1)] + fileList
                textList = []
                for name in fileList:
                    textList += baseFont.render(name, False, pygame.color.Color("black")),


        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                canClick = True
                #print("canClick")
        
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 3:
                _oe.mkfile("untitled.txt")
                fileList = _oe.ls()
                fileList.sort(key=mySortFunc)
                firstElem = fileList[0]
                textList = []
                for name in fileList:
                    textList += baseFont.render(name, False, pygame.color.Color("black")),
            
            if event.button == 1 and canClick:
                if fileList:
                    maxText = max(fileList,key=baseFont.size)
                    #print(max(fileList,key=baseFont.size))
                    #print(*map(baseFont.size,fileList))
                    if pygame.Rect(posZero[0] + 10, posZero[1] + baseFont.size(filePath)[1] + 10  ,\
                      baseFont.size(maxText)[0], len(textList) * baseFont.size(maxText)[1] - 10 ).collidepoint(event.pos):
                        indexClick:int =  (event.pos[1] - posZero[1]) // ( baseFont.size(maxText)[1])
                        #print(indexClick)
                        
                        #print(fileList)
                        #print(fileList[indexClick-1])
                        #print(tuple(textList[indexClick-1].get_at((0, 0))))
                        if tuple(textList[indexClick-1].get_at((0, 0))) == (250, 250, 250, 255) and not rename:
                            try:
                                #print("fe",fileList[indexClick-1])
                                #print(_oe.path,fileList[indexClick-1])
                                _oe.cd(fileList[indexClick-1])
                            except FileNotFoundError as e:
                            #    for item in dir(e):
                            #        try:
                            #            if not item.startswith("__"):
                            #                print(item," = ",getattr(e,item))
                            #        except AttributeError:
                            #            print("Attribut",item,"non accessible")
                                #toReturn = "TextEditor",("data/" + ("usr/" if _fe.path.count("usr") else "")  + filePath + "/" + fileList[indexClick-1],)
                                for i, item in enumerate(appExt):
                                    if item.find(fileList[indexClick-1].split(".")[-1]) < item.find(":") and\
                                        item.count(fileList[indexClick-1].split(".")[-1]):
                                        toReturn = item.split(":")[-1],(_oe.path + "\\" + fileList[indexClick-1],)
                                        #print("toReturn perso",toReturn)
                                        #print(fileList[indexClick-1].split(".")[-1],item)
                                        break
                                    else:
                                        toReturn = "TextEditor",(_oe.path + "\\" + fileList[indexClick-1],)
                            else:
                                select = 0
                                if filePath:
                                    if fileList[indexClick-1] == userName:
                                        filePath = userName
                                    else:
                                        if _oe.path.count("/"):
                                            filePath += ("/" if _oe.path.count("/")-1 else "") + fileList[indexClick-1]
                                            
                                        elif _oe.path.count("\\"):
                                            filePath += ("\\" if _oe.path.count("\\")-1 else "") + fileList[indexClick-1]
                                else:
                                    filePath += fileList[indexClick-1]
                                fileList = _oe.ls()
                                fileList.sort(key=mySortFunc)
                                firstElem = fileList[0]
                                filePathSurf = baseFont.render(filePath, False, pygame.color.Color("black"), pygame.color.Color("white"))
                                textList = []
                                for name in fileList:
                                    textList += baseFont.render(name, False, pygame.color.Color("black")),
                        else:
                            textList = []
                            for name in fileList:
                                textList += baseFont.render(name, False, pygame.color.Color("black")),
                            textList[indexClick-1] = baseFont.render(fileList[indexClick-1], False, pygame.color.Color("black"), (250, 250, 250))
                            #print("heightlight")
                            select = indexClick
                    elif rename:
                        _oe.rename(rename, fileList[select-1])
                        rename = ""
                    
                    elif select:
                        textList = []
                        for name in fileList:
                            textList += baseFont.render(name, False, pygame.color.Color("black")),
                    
                if filePath != userName or debug:
                    if backSurf.get_rect(x=posZero[0]+screen.get_width()-backSurf.get_width(), y=posZero[1]).collidepoint(event.pos):
                        _oe.cd("..")
                        if ((filePath.count("/") == 1 or filePath.count("\\") == 1) and\
                        (filePath.find("/") == 2 or filePath.find("\\") == 2)):
                            filePath = _oe.path

                        elif _oe.path.count("/"):
                            filePath = "/".join(filePath.split("/")[:-1])
                            
                        elif _oe.path.count("\\"):
                            filePath = "\\".join(filePath.split("\\")[:-1])
                        
                        if filePath == "" :
                            filePath = _oe.path
                        fileList = _oe.ls()
                        fileList.sort(key=mySortFunc)
                        firstElem = fileList[0]
                        filePathSurf = baseFont.render(filePath, False, pygame.color.Color("black"), pygame.color.Color("white"))
                        textList = []
                        for name in fileList:
                            textList += baseFont.render(name, False, pygame.color.Color("black")),
                    
                canClick = False
                
    
    screen.fill(pygame.color.Color("gray"))
    screen.blit(filePathSurf, (10, 10))
    screen.blit(backSurf, (screen.get_width()-baseFont.size("<--")[0], 0))
    for i, surf in enumerate(textList, start=1):
        screen.blit(surf, (10, i*(baseFont.size(userName)[1])+10))
    
    return toReturn
    

def quit():
    global _oe, userName, filePath, filePathSurf, fileList, textList, canClick, debug, select, rename, firstElem
    del _oe, userName, filePath, filePathSurf, fileList, textList, canClick, debug, select, rename, firstElem
    

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
