import math
import random
import pyxel
from enum import Enum,auto

WIDTH = 192
HEIGHT = 256    
FPS=60

#爆発のベース色
EXPLODE_COL = 10

#オブジェクト管理リスト
Bullet_list = []    #弾丸管理リスト

#Explode_list = []   #爆風管理リスト
#Missile_List = []    #ミサイル管理リスト

class STATE(Enum):
    TITLE=0,
    PLAY=auto(),
    GAMEMENU=auto(),
    QUIT=auto()
#------------------------------------------------------------------------------
#レティクル管理クラス
class Reticle():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.alive = True
        self.__visible = True
    
    def update(self):
        pass
        
    def draw(self, mx, my):
        #非表示
        if self.visible == False:
            return
        #Reticle描画
        pyxel.blt(mx, my, 0, 0, 0,16,16,15)
    
    @property
    def visible(self):
        return self.__visible
    
    @visible.setter
    def visible(self, visible):
        self.__visible = visible

#------------------------------------------------------------------------------
#砲弾管理クラス        
class Explode():
    def __init__(self, ex, ey, rad, col1, col2):
        self.x = ex
        self.y = ey
        self.rad = rad
        self.col1 = col1
        self.col2 = col2

#------------------------------------------------------------------------------
#砲弾管理クラス        
class Bullet():
    def __init__(self, bx, by, tx, ty, speed, col):

        self.x_pos = self.start_x = bx
        self.y_pos = self.start_y = by
        self.color = col
        
        _AREA = 3
        #着弾座標評価範囲
        self.tx1 = tx - _AREA
        self.ty1 = ty - _AREA
        self.tx2 = tx + _AREA
        self.ty2 = ty + _AREA

        self.alive = True        
        
        #射点からターゲットまでの距離計算
        dist_x = tx - bx
        dist_y = ty - by

        #ターゲットまでの偏角計算
        rag = math.atan2(dist_y, dist_x) #ラジアン角ね

        print("angle:" + str(rag))

        #xy方向のfps毎の移動量計算
        self.vx = math.cos(rag) * speed
        self.vy = math.sin(rag) * speed
    
        print ("cos:" + str(math.cos(30)))
    
    def update(self):
        
        self.x_pos += self.vx
        self.y_pos += self.vy
        
    #    print("pos=" + str(self.x_pos) + ":" + str(self.y_pos))
    #    print("Target=" + str(self.tx) + ":" + str(self.ty))
        
        #弾着判定
        if self.tx1 <= self.x_pos and self.y_pos >= self.ty1:
            if self.tx2 >= self.x_pos and self.y_pos <= self.ty2: 
                #pass
                #爆風オブジェクト生成
#                Explode(self.x_pos, self.y_pos, 50, 0.5, 1, EXPLODE_COL) #半径50 速度0.5
                
                #砲弾オブジェクト破棄           
                self.alive = False
                print("Explode")
                
        #誘爆判定
        #if pyxel.pget(self.x_pos, self.y_pos) == EXPLODE_COL:
                #爆風オブジェクト生成
#                Explode(self.x_pos, self.y_pos, 50, 0.5, 1, EXPLODE_COL) #半径50 速度0.5
                
                #砲弾オブジェクト破棄           
        #        self.alive = False        
        
        #画面外に出たらオブジェクト破棄
        if self.y_pos < 0 or HEIGHT < self.y_pos:
            self.alive = False
            print("Out of Screen 01")
        if self.x_pos < 0 or WIDTH < self.x_pos:
            self.alive = False
            print("Out of Screen 02")
    
    def draw(self):
        pyxel.pset(self.x_pos, self.y_pos, 7)
        #pyxel.rect(self.x_pos - 1, self.y_pos - 1, 2, 2, self.color)

#リスト化されているオブジェクトの更新処理呼び出し
def update_list(list):
    for elem in list:
        elem.update()

#リスト化されているオブジェクトの描画処理呼び出し
def draw_list(list):
    for elem in list:
        elem.draw()

#リスト化されているオブジェクトで破棄されたモノのガベコレ
def cleanup_list(list):
    i = 0
    while i < len(list):
        elem = list[i]
        if not elem.alive:
            list.pop(i)
        else:
            i += 1

#ゲームメインクラス        
class GameMain:
    #--------------------------------------------------------------------------------
    #Pyxel initialize
    #--------------------------------------------------------------------------------
    def __init__(self):
        self.GameState = STATE.TITLE

        self.QuitCount = 0

        #レティクルクラス生成
        self.reticle = Reticle(-100, -100)
        self.reticle.visible = False
        

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

        if pyxel.btnp(pyxel.KEY_Z) == True:
            #if(self.bullet_a <= 0):return   #残弾数チェック
            Bullet_list.append(
                Bullet(128, 240, pyxel.mouse_x, pyxel.mouse_y, 3, 11)
            )
            #self.bullet_a -= 1   

        #リスト化されたオブジェクトの更新処理だよ
        update_list(Bullet_list)

        #削除フラグ立ってるオブジェクトを消すよ
        cleanup_list(Bullet_list)
     
        
    #--------------------------------------------------------------------------
    #draw game play
    def draw_play(self):
        pyxel.cls(0)

        #レティクル描画
        self.reticle.draw(pyxel.mouse_x-8,pyxel.mouse_y-8)

        #pyxel.text(0,20, "pyxel.mouse_x",7)

        pyxel.text(0, 10, str(pyxel.mouse_x) + ":" + str(pyxel.mouse_y), 2)
        #pyxel.text(0, 20, str(pyxel.frame_count), 2)

        #print(pyxel.MOUSE_POS_X)

        #リスト化されたオブジェクトの描画処理
        draw_list(Bullet_list)    


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
            self.reticle.visible = True

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
