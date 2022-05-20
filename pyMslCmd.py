import pyxel
from enum import Enum,auto

WIDTH = 192
HEIGHT = 256    
FPS=30

class STATE(Enum):
    TITLE=0,
    PLAY=auto(),
    GAMEMENU=auto(),
    QUIT=auto()


#ゲームメインクラス        
class GameMain:


    #--------------------------------------------------------------------------------
    #Pyxel initialize
    #--------------------------------------------------------------------------------
    def __init__(self):
        self.GameState = STATE.TITLE

        self.QuitCount = 0

        

        pyxel.init(WIDTH, HEIGHT, title="PyMissleCommand",fps=FPS,quit_key=pyxel.KEY_NONE)
        pyxel.load("./assets/pyMslCmd.pyxres")
        #pyxel.image(0).load(0, 0, "assets/pyxel_logo_38x16.png")
        pyxel.run(self.update, self.draw)

    #--------------------------------------------------------------------------------
    #Pyxel Update
    #--------------------------------------------------------------------------------
    def update(self):
        match self.GameState:
            case STATE.TITLE:
                self.update_title()
            case STATE.PLAY:
                self.update_play()
                #print ("Play")
            case STATE.GAMEMENU:
                self.update_menu()
            case STATE.QUIT:
                self.update_quit()
            case _:
                print("default")

    #--------------------------------------------------------------------------------
    #Pyxel Update
    #--------------------------------------------------------------------------------
    def draw(self):
        match self.GameState:
            case STATE.TITLE:
                self.draw_title()
            case STATE.PLAY:
                self.draw_play()
                #print ("Play")
            case STATE.GAMEMENU:
                print ("GameMenu")
                #self.draw_menu()
            case STATE.QUIT:
                self.draw_quit()
            case _:
                print("default")
#        pyxel.cls(0)
        #pyxel.text(10, 10, "Missle Command for Pyxel", pyxel.frame_count % 16)
        #pyxel.blt(61, 66, 0, 0, 0, 38, 16)
#        pyxel.line(0,0,WIDTH,HEIGHT,3)

    #--------------------------------------------------------------------------
    #--------------------------------------------------------------------------
    #update game play
    def update_play(self):
        mouse_x = pyxel.mouse_x
        mouse_y = pyxel.mouse_y
        #pyxel.mouse(True)
        
    #--------------------------------------------------------------------------
    #draw game play
    def draw_play(self):
        pyxel.cls(0)
        #pyxel.pset(pyxel.mouse_x, pyxel.mouse_y,7)
        pyxel.blt(pyxel.mouse_x-8, pyxel.mouse_y-8,0,0, 0, 16,16, 15)

        #pyxel.text(0,20, "pyxel.mouse_x",7)

        pyxel.text(0, 10, str(pyxel.mouse_x) + ":" + str(pyxel.mouse_y), 2)
        #pyxel.text(0, 20, str(pyxel.frame_count), 2)

        #print(pyxel.MOUSE_POS_X)

    #--------------------------------------------------------------------------
    #--------------------------------------------------------------------------
    def update_title(self):
        #print(STATE.TITLE)

        if pyxel.btnp(pyxel.KEY_Q):
            self.QuitCount = 0
            self.GameState = STATE.QUIT
            pyxel.cls(0)
        elif pyxel.btnp(pyxel.KEY_S):
            self.GameState = STATE.PLAY
            pyxel.cls(0)

    def draw_title(self):
        pyxel.cls(0)
        pyxel.text(10,10,"Missle Command",1)

        pyxel.text(10,16,"S:Game Start",7)
        pyxel.text(10,32,"Q:Quit",7)

    #--------------------------------------------------------------------------
    def update_menu(self):
        if pyxel.btnp(pyxel.KEY_ESCAPE):
            self.GameState = STATE.MENU

    def draw_menu(self):
        pyxel.cls(0)
        pyxel.text(10,10,"Mene",1)

    #--------------------------------------------------------------------------
    #Quit Sequence
    def update_quit(self):
        
        if self.QuitCount < FPS*2:
            self.QuitCount += 1
        else:
            pyxel.quit()

    def draw_quit(self):
        #print(self.QuitCount)
        pyxel.text(0,0, "Thank you Playgame!", 7)
        #pyxel.text





GameMain()
