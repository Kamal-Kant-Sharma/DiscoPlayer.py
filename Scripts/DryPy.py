import pygame, sys

class Canvas:
    def __init__(self, size: tuple = (500, 500), BGcolor: tuple = (250, 250, 250), fps: int = 60, clearBG: bool = True, translate: tuple = (0, 0), font: str = '',WinIcon=None,WinName=None):
        pygame.init()
        
        self.screen = pygame.display.set_mode(size)
        self.clock = pygame.time.Clock()
        self.fps = fps
        self.bgColor = BGcolor
        self.clearBG = clearBG
        self.offset = translate
        self.font = pygame.font.Font('freesansbold.ttf', 16)
        self.images = {}
        if WinIcon is not None:
            pygame.display.set_icon(pygame.image.load(WinIcon))
        if WinName is not None:
            pygame.display.set_caption(WinName)

        self.Mouse = Mouse(translate)
        self.Keyboard = Keyboard()
        
        self.funcs = []
        self.dt = 1/fps
        
    def LoadImage(self, key, filedir):
        self.images[key] = pygame.image.load(filedir).convert_alpha()
        
    def Stamp(self, imageKey, pos):
        self.funcs.append((self.Blit,(self.images[imageKey], pos)))
        
    def Blit(self, args):
        self.screen.blit(args[0], args[1])
        
    def Write(self, pos, text, color, BGcolor=None, antialiases=True):
        self.funcs.append((self.Text,(pos, text, antialiases, color, BGcolor)))
        
    def Text(self, args):
        self.screen.blit(self.font.render(args[1], args[2], args[3], args[4]), args[0])
    
    def Line(self, start: tuple = (0, 0), end: tuple = (0, 0), color: tuple = (0, 0, 0), width: int = 1):
        self.funcs.append((self.DrawLine, (color, start, end, width)))
    
    def DrawLine(self, args):
        pygame.draw.line(self.screen, args[0], [sum(x) for x in zip(args[1],self.offset)], [sum(x) for x in zip(args[2],self.offset)], args[3])
        
    def Circle(self, pos: tuple = (0,0), radius: int = 100, color: tuple = (0, 0, 0), width: int = 1):
        self.funcs.append((self.DrawCircle, (color, pos, radius, width)))
        
    def DrawCircle(self, args):
        pygame.draw.circle(self.screen, args[0], [sum(x) for x in zip(args[1],self.offset)], args[2], args[3])
        
    def Rect(self, topLeft: tuple = (0,0), bottomRight: tuple = (50, 50), color: tuple = (0,0,0), width: int = 1):
        self.funcs.append((self.DrawRect, (bottomRight, topLeft, color, width)))
    
    def DrawRect(self, args):
        pygame.draw.rect(self.screen, args[2], pygame.Rect(args[1], (args[0][0]-args[1][0], args[0][1]-args[1][1])), args[3])
        
    def Polygon(self, points: list, color: tuple = (0,0,0), width: int = 1):
        self.funcs.append((self.DrawPolygon, (points, color, width)))
        
    def DrawPolygon(self, args):
        pygame.draw.polygon(self.screen, args[1], args[0], args[2])
        
    def Run(self):
        try:
            self.dt = 1/self.clock.get_fps()
        except:
            self.dt = 0
        if self.clearBG:
            self.screen.fill(self.bgColor)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        for func in self.funcs:
            func[0](func[1])
        self.funcs = []
        pygame.display.update()
        self.clock.tick(self.fps)
        
class Keyboard:
    def GetKeyPressed(self):
        self.pressed = pygame.key.get_pressed()
    def IsKeyPressed(self,key):
        return self.pressed[pygame.key.key_code(key)]
        
class Mouse:
    def __init__(self, trans):
        self.trans = trans
    
    def GetPos(self):
        mx, my = pygame.mouse.get_pos()
        return (mx-self.trans[0], my-self.trans[1])
    
    def GetPressed(self):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                return True
            
        return False
