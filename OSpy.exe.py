from types import ModuleType
from typing import Any
import pygame
import sys
from lib.OSexplorer import OSexplorer



class Main():
    def __init__(self):
        self.fpslist = []
        self.nfps = 0
        self.timeloop = 0
        self.fps = 0

        self._children:dict[str,list] = {}
        self.eventGet:list[pygame.event.Event] = []
        
        self.iconSize = 64
        self.userName:str = "User1"
        self.windowList:list[Window] = []
        
        self.taskbar = TaskBar((0,screen.get_height()-self.iconSize//2),(screen.get_width(),self.iconSize//2)) # type: ignore
        fe = OSexplorer()
        fe.cd(f"data/usr/{self.userName}/Desk")
        OSexplorer()
        for file in fe.ls():
            data:str|bytes = fe.open(file)
            if type(data) is str:
                if file.endswith(".link"):
                    """
                    data:
                    file of app
                    file of icon
                    """
                    #print(data.splitlines()[1:])
                    goto:str
                    icon:str
                    goto,icon = data.splitlines()
                    moduleName = goto.split(".")[0].replace("/",".")
                    #print(moduleName)
                    exec(f"import {moduleName}")
                    self.appendChild(icon,sys.modules[moduleName],True)
        
        fe = OSexplorer()
        fe.cd(f"data/bin")
        """
        data:
        file of app:file of icon
        file of app2:file of icon2
        ...
        """
        data:str|bytes = fe.open("apps")
        if type(data) is str:
            for item in data.splitlines():
                goto:str
                icon:str
                goto,icon = item.split(":")
                moduleName = goto.split(".")[0].replace("/",".")
                #print(moduleName)
                if moduleName.split(".")[-1] not in self._children:
                    exec(f"import {moduleName}")
                    self.appendChild(icon,sys.modules[moduleName],False)



    def appendChild(self,icon:str,moduleExe:ModuleType,fromDesk:bool):
        #moduleExe.init() mustn't has kwargs
        args:list[str] = moduleExe.listArgs
        #print(args)
        for i,item in enumerate(args):
            args[i] = eval(f"self.{item}")
        #print(args)
        if fromDesk:
            obj = Icon(icon,self.iconSize,moduleExe,(10+(10+self.iconSize)*(len(self._children)),0),*args)
        else:
            obj = icon
        self._children[f"{moduleExe.__name__}".split(".")[-1]] = [obj,moduleExe]
        #print(self._children)
    
#    def exec(self,moduleExe):
#        moduleExe.main()
    
    def update(self):
        updateIcon = True

        for event in self.eventGet:
            if event.type == pygame.QUIT:
                print("max:",max(self.fpslist),"fps, min:",min(self.fpslist),"fps")
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    print("max:",max(self.fpslist),"fps, min:",min(self.fpslist),"fps")
                    pygame.quit()
                    sys.exit()
        
        surf=pygame.Surface(screen.get_size())
        surf.fill("#0000FF")
            
            
        windowList = self.windowList.copy()
        
        
        for window in windowList:
            
            key = f"{window.module.__name__}".split(".")[-1]
            if window.exitTest(self.eventGet):
                self.taskbar.removeIcon(key)
                del self._children[key][2]
                self.windowList.remove(window)
                if type(self._children[key][0]) is Icon:
                    self._children[key][0].isopen = False
            else:
                test = window.update(self.eventGet, windowList[-1] is window)
                if test[0]:
                    self.windowList.remove(window)
                        #print("rm")
                        #print(*(item.module.__name__ for item in self.windowList))
                    self.windowList += window,
                
                    updateIcon = False
                        #print("add")
                        #print(*(item.module.__name__ for item in self.windowList))
                #print("window:",window.module.__name__)
                #print(*(item.module.__name__ for item in windowList))
                if test[1]:
                    app, args = test[1]
                    if app == "end":
                        del self._children[key][2]
                        self.windowList.remove(window)
                        if type(self._children[key][0]) is Icon:
                            self._children[key][0].isopen = False
                    else:
                        print(app, args)

                        if app in self._children:
                            if len(self._children[app]) < 3:
                                icon:Icon|str = self._children[app][0]
                                if type(icon) is Icon:
                                    icon.isopen = True
                                moduleExe = self._children[app][1]
                                moduleExe.init(*args)
                                window = Window(moduleExe,moduleExe.size)
                                self._children[app] += [window]
                                if type(icon) is str:
                                    self.taskbar.addIcon(app,pygame.transform.scale\
                                                         (pygame.image.load("data\\bin\\"+icon).convert_alpha(),\
                                                          (self.iconSize//2,)*2))
                                elif type(icon) is Icon:
                                    self.taskbar.addIcon(app,pygame.transform.scale\
                                                         (pygame.image.load(icon.path).convert_alpha(),\
                                                          (self.iconSize//2,)*2))
                
        #print(*(item.module.__name__ for item in self.windowList))

        for key,value in self._children.items():
            obj:str|Icon = value[0]
            if type(obj) is Icon:
                moduleExe:ModuleType = value[1]
                collision = obj.main(self.eventGet if updateIcon else [])
                
                surf.blit(obj.surf,obj.pos)
                surf.blit(obj.surfText,(obj.pos[0]-5,obj.pos[1]+obj.size))
            
                if collision:
                    if len(self._children[key]) < 3:
                        window = Window(moduleExe,moduleExe.size)
                        self._children[key] += [window]
                        self.taskbar.addIcon(key,pygame.transform.scale(obj.surf,(self.iconSize//2,)*2))
                        self.windowList.append(window)
                    window = self._children[key][2]
                    self.windowList.remove(window)
                    self.windowList.append(window)
                    
            
            if len(self._children[key]) > 2 and value[2] not in self.windowList:
                self.windowList += value[2],
                
        for window in self.windowList:
            if window.isvisible:
                for key in window.zindex:
                    value = window.elements[key]
                    surf.blit(value[0],value[1])

        app = self.taskbar.update(self.eventGet)

        if app:
            window:Window = self._children[app][2]
            window.toggleVisibility()

            if window.isvisible:
                self.windowList.remove(window)
                self.windowList += window,

        surf.blit(self.taskbar.surf,self.taskbar.pos)

        screen.blit(surf,(0,0))

        if self.timeloop + 1000 < pygame.time.get_ticks():
            self.fps = 1//((pygame.time.get_ticks()-self.nfps)/1000)
            self.timeloop = pygame.time.get_ticks()
            print("FPS:",self.fps)
            self.fpslist += self.fps,
        self.nfps = pygame.time.get_ticks()

class Icon():
    def __init__(self,path:str,size:int,moduleExe:ModuleType,pos:tuple[int,int],*args):
        #OSexplorer()
        self.isopen:bool = False
        self.pos = pos
        self.path = path
        self.size = size
        self.module = moduleExe
        self.surf = pygame.transform.scale(pygame.image.load(self.path).convert_alpha(),(size,size))
        self.surfText = pygame.font.SysFont("Arial",16).render(f"{self.module.__name__}".split(".")[-1],True,pygame.color.Color("black"))
        self.args = args
    
    def main(self,eventGet:list[pygame.event.Event]):
        for event in eventGet:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if self.surf.get_rect(x=self.pos[0],y=self.pos[1]).collidepoint(event.pos):
                        if not self.isopen:
                            self.module.init(*self.args)
                        self.isopen:bool = True
                        return True
        return False

class Window:
    def __init__(self,moduleExe:ModuleType,size:list[int]):
        self.pos:tuple[int,int] = moduleExe.posZero
        
        self.module = moduleExe
        
        self.size = size
        
        self.elements:dict[str,tuple[pygame.Surface,tuple[int,int],str]] = {}
        self.elements["windowSurf"] = pygame.Surface((2*4+size[0],4+size[1]+32)),(self.pos[0]-4,self.pos[1]-32),"white"
        self.elements["screen"] = pygame.Surface(size),self.pos,"black"
        self.elements["titleSurf"] = pygame.font.SysFont("Arial",18).render(f"{self.module.__name__}".split(".")[-1],\
        True,pygame.color.Color("black")),(self.pos[0]+32,self.pos[1]-25),""
        
        self.elements["minusSurf"] = pygame.font.SysFont("Arial",24).render("-",\
        True,pygame.color.Color("black")),((self.pos[0]+self.size[0]+4)-32*3,self.pos[1]-32),""
        self.elements["exitSurf"] = pygame.Surface((32,32)),((self.pos[0]+self.size[0]+4)-32,self.pos[1]-32),"red"
        self.zindex = ["windowSurf","screen","titleSurf","minusSurf","exitSurf"]
        
        self.posClick:tuple[int,int] = (0,0)
        self.goto:bool = False
        self.isvisible = True
        
    def update(self,eventGet:list[pygame.event.Event],canMove:bool):
        isClicked:bool = False
        if self.isvisible:
            for event in eventGet:
                if canMove:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1 and pygame.Rect((self.pos[0]-4,self.pos[1]-32),(2*4+self.size[0],32)).collidepoint(event.pos):
                            self.goto = True
                            self.posClick = event.pos
                    
                    if event.type == pygame.MOUSEBUTTONUP:
                        if event.button == 1:
                            self.goto = False
                            minusSurf = self.elements["minusSurf"]
                            if minusSurf[0].get_rect(x=minusSurf[1][0],y=minusSurf[1][1]).collidepoint(event.pos):
                                self.hide()
                
                    if self.goto:
                        if self.posClick and (event.type in (pygame.MOUSEBUTTONDOWN,pygame.MOUSEMOTION))\
                            and event.pos != self.posClick:
                            self.pos = event.pos[0] - (self.posClick[0] - self.pos[0]), event.pos[1] - (self.posClick[1] - self.pos[1])
                            self.module.posZero = self.pos # type: ignore
                            #print("self.pos:",self.pos,"self.posClick:",self.posClick,"event.pos:",event.pos)
                                
                            self.posClick = event.pos
                        
                        self.elements["windowSurf"] = pygame.Surface((2*4+self.size[0],4+self.size[1]+32)),(self.pos[0]-4,self.pos[1]-32),"white"
                        self.elements["screen"] = pygame.Surface(self.size),self.pos,"black"
                        self.elements["titleSurf"] = pygame.font.SysFont("Arial",18).render(f"{self.module.__name__}".split(".")[-1],\
                        True,pygame.color.Color("black")),(self.pos[0]+32,self.pos[1]-25),""
                        
                        self.elements["minusSurf"] = pygame.font.SysFont("Arial",24).render("-",\
                        True,pygame.color.Color("black")),((self.pos[0]+self.size[0]+4)-32*3,self.pos[1]-32),""
                        self.elements["exitSurf"] = pygame.Surface((32,32)),((self.pos[0]+self.size[0]+4)-32,self.pos[1]-32),"red"
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.elements["windowSurf"][0].get_rect(x=self.pos[0]-4, y=self.pos[1]-32).collidepoint(event.pos):
                        isClicked = True
                        #print("is",self.module.__name__)
            
            for key in self.zindex:
                value = self.elements[key]
                if value[2] and type(value[2]) is str:
                    value[0].fill(pygame.color.Color(value[2]))
            
            update:tuple[str,tuple[Any]] = self.module.update(self.elements["screen"][0],eventGet if canMove else [])
            
            return isClicked, update if canMove else None
        self.module.update(self.elements["screen"][0],[])
        return isClicked,None
    
    def show(self):
        self.isvisible = True
    
    def hide(self):
        self.isvisible = False
    
    def toggleVisibility(self):
        self.isvisible = not self.isvisible

    def exitTest(self,eventGet:list[pygame.event.Event]):
        exitSurf = self.elements["exitSurf"]
        for event in eventGet:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if exitSurf[0].get_rect(x=exitSurf[1][0],y=exitSurf[1][1]).collidepoint(event.pos):
                        self.module.quit()
                        return True
        return False

class TaskBar:
    def __init__(self,pos:tuple[int,int],size:tuple[int,int]):
        surf = pygame.Surface((size[1],)*2)
        surf.fill("#5050FF")
        self.apps:dict[str,pygame.Surface] = {"Unknown":surf}
        self.zindex:list[str] = ["Unknown"]
        self.pos = pos
        self.size = size
        self.surf = pygame.Surface(size)
    
    def addIcon(self,name:str,surf:pygame.Surface):
        self.apps[name] = surf
        self.zindex += name,
        print(self.apps,self.zindex)

    def removeIcon(self,name:str):
        del self.apps[name],self.zindex[self.zindex.index(name)]

    def update(self,eventGet:list[pygame.event.Event]):
        toReturn:str|None = None
        for event in eventGet:
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    if event.pos[1] > self.pos[1] and\
                        event.pos[0]//self.size[1] < len(self.zindex):
                        toReturn = self.zindex[event.pos[0]//self.size[1]]

        self.surf.fill("#FFFFFF")

        if self.apps:
            count = 0
            for name in self.zindex:
                self.surf.blit(self.apps[name],(self.size[1]*count,0))
                count += 1
        
        return toReturn



        

#def collision_test(obj1,obj2):
#    if \
#    ((obj1.x+1 <= obj2.x + obj2.surf.get_width()) and (obj1.x + obj1.surf.get_width() >= obj2.x-1)) and \
#    ((obj1.y+1 <= obj2.y + obj2.surf.get_height()) and (obj1.y + obj1.surf.get_height() >= obj2.y-1)) :
#       return True
#   return False

pygame.init()

screen = pygame.display.set_mode((1024, 768),pygame.FULLSCREEN | pygame.SCALED)

timer = pygame.time.Clock()

main = Main()

error = None

game_on = True

while game_on:
    if not error:
        try:
            main.eventGet = pygame.event.get()
            main.update()
        except Exception as e:
            error = e
            print(e)
    elif error:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                #raise error
                pygame.quit()
                sys.exit()
        screen.fill("#0000FF")
        screen.blit(pygame.font.SysFont("Monospace",16,True).render(type(error).__name__+": "+str(error),True,"#FFFFFF"),\
                    (0,screen.get_height()//2))
    pygame.display.update()
    timer.tick(60)
    
