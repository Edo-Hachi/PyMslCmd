import random
import math
import pyxel

#ウィンドウ定数
SCR_WIDTH = 255
SCR_HEIGHT = 255
SCR_FPS = 60

#スプライト定数
SP_WIDTH = 16
SP_HEIGHT = 16

IMG_BANK0 = 0
IMG_BANK1 = 1
IMG_BANK2 = 2

#スプライト番号
SP_RATICLE = 0
SP_CLEAR_COL = 0   #透明色番号

#オブジェクト管理リスト
Explode_list = []   #爆風管理リスト
Bullet_list = []    #弾丸管理リスト
Missile_List = []    #ミサイル管理リスト

#砲弾、ミサイル速度
BULLET_SPEED = 3
MISSILE_SPEED = 1

#爆発のベース色
EXPLODE_COLOR = 10

#ゲーム遷移定数
STATE_TITLE = 0
STATE_PLAY = 1
STATE_GAMEOVER = 2

#リスト化されているオブジェクトの更新処理
def update_list(list):
    for elem in list:
        elem.update()

#リスト化されているオブジェクトの描画処理
def draw_list(list):
    for elem in list:
        elem.draw()

#リスト化されているオブジェクトのガベコレ
def cleanup_list(list):
    i = 0
    while i < len(list):
        elem = list[i]
        if not elem.alive:
            list.pop(i)
        else:
            i += 1        

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
        angle = math.atan2(dist_y, dist_x)
        
        #xy方向のfps毎の移動量計算
        self.vx = math.cos(angle) * speed/2
        self.vy = math.sin(angle) * speed/2
        
    def update(self):
        
        self.x_pos += self.vx
        self.y_pos += self.vy
        
    #    print("pos=" + str(self.x_pos) + ":" + str(self.y_pos))
    #    print("Target=" + str(self.tx) + ":" + str(self.ty))
        
        #if self.tx == int(self.x_pos) and self.ty == int(self.y_pos):
        #弾着判定
        if self.tx1 <= self.x_pos and self.y_pos >= self.ty1:
            if self.tx2 >= self.x_pos and self.y_pos <= self.ty2: 
                
                #爆風オブジェクト生成
                Explode(self.x_pos, self.y_pos, 50, 0.5, 1, EXPLODE_COLOR) #半径50 速度0.5
                
                #砲弾オブジェクト破棄           
                self.alive = False
                
        #誘爆判定
        if pyxel.pget(self.x_pos, self.y_pos) == EXPLODE_COLOR:
                #爆風オブジェクト生成
                Explode(self.x_pos, self.y_pos, 50, 0.5, 1, EXPLODE_COLOR) #半径50 速度0.5
                
                #砲弾オブジェクト破棄           
                self.alive = False        
        
        #画面外に出たらオブジェクト破棄
        if self.y_pos < 0 or SCR_HEIGHT < self.y_pos:
            self.alive = False
        if self.x_pos < 0 or SCR_WIDTH < self.x_pos:
            self.alive = False
    
    def draw(self):
        #pyxel.pset(self.x_pos, self.y_pos, 11)
        pyxel.rect(self.x_pos - 1, self.y_pos - 1, 2, 2, self.color)

#ミサイル管理クラス(砲弾クラス継承)
class Missile(Bullet):
    def draw(self):
        pyxel.rect(self.x_pos - 1, self.y_pos - 1, 2, 2, self.color)
        pyxel.line(self.start_x, self.start_y, self.x_pos, self.y_pos, self.color)


#レティクル管理クラス
class Reticle():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.alive = True
        self.visible = True
    
    def update(self):
        pass
        
    def draw(self):
        #非表示
        if self.visible == False:
            return
        
        #Reticle描画
        #pyxel.blt(self.x, self.y, 0, 0, 0, self.w, self.h, 0)
        pyxel.blt(
            pyxel.mouse_x - SP_WIDTH / 2,
            pyxel.mouse_y - SP_HEIGHT / 2,
            IMG_BANK0,  
            0,
            0,
            SP_WIDTH,
            SP_HEIGHT,
            SP_CLEAR_COL,
        )

#爆発描画クラス
class Explode():
    def __init__(self, x, y, r, s, col1, col2):
        self.x = x
        self.y = y
        self.max_radius = r
        self.radius = 1
        self.speed = s
        self.color1 = col1
        self.color2 = col2
        self.alive = True
        
        Explode_list.append(self)
    
    def update(self):
        self.radius += self.speed
        
        if self.radius >= self.max_radius:
            self.alive = False
    
    def draw(self):
        if self.radius % 3:
            pyxel.circ(self.x, self.y, self.radius, self.color2)
        else:
            pyxel.circ(self.x, self.y, self.radius, self.color1)
            
        #pyxel.circb(self.x, self.y, self.radius, 8)
        
        pyxel.circb(self.x, self.y, self.radius, 13)

#ゲームメインクラス        
class gamemain:
    
    #--------------------------------------------------------------------------------
    #Pyxelイニシャライズ
    #--------------------------------------------------------------------------------
    def __init__(self):
        pyxel.init(SCR_WIDTH, SCR_HEIGHT, title="Defender", fps=SCR_FPS, quit_key=pyxel.KEY_Q)
        pyxel.load("./assets/defender.pyxres")
        
        #レティクルクラス生成
        self.reticle = Reticle(-100, -100)
        
        #ゲームステート初期化
        self.game_state = STATE_TITLE
        
        #砲台弾数
        self.bullet_a = 10
        self.bullet_b = 10
        self.bullet_c = 10
        
        pyxel.run(self.update, self.draw)

    #--------------------------------------------------------------------------------
    #Pyxel UpDateイベント処理
    #--------------------------------------------------------------------------------
    def update(self):
        
        #[Q]キーで強制終了
        #if pyxel.btnp(pyxel.KEY_Q):
        #    pyxel.quit()
        
        #ゲームステート毎のupdate処理
        if self.game_state == STATE_TITLE:
            self._update_title()
        
        #ゲームプレイ中            
        elif self.game_state == STATE_PLAY:        
            self._update_play()
        
        elif self.game_state == STATE_GAMEOVER:
            pass
            
       
    #--------------------------------------------------------------------------------
    #Pyxel Drawイベント処理
    #--------------------------------------------------------------------------------
    def draw(self):
        
        #タイトル
        if self.game_state == STATE_TITLE:
            pyxel.cls(0)
            pyxel.text(100, 100,"DEFENDER", 7)
            pyxel.text(100, 120,"PUSH ENTER", 7)
        
        #ゲーム実行中
        elif self.game_state == STATE_PLAY:
            self._draw_play()
        
        #ゲームオーバー中            
        elif self.game_state == STATE_GAMEOVER:
            pass      
    
    ##-------------------------------------------------------------------------------
    #タイトル画面でのupdate処理    
    ##-------------------------------------------------------------------------------
    def _update_title(self):
        #[Q]キーで終了
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        elif pyxel.btnp(pyxel.KEY_S):
            self.game_state = STATE_PLAY
            #砲台弾数初期化
            self.bullet_a = 10
            self.bullet_b = 10
            self.bullet_c = 10

    ##-------------------------------------------------------------------------------
    #ゲームプレイ中のupdate処理
    ##-------------------------------------------------------------------------------
    def _update_play(self):
        
        """
        #マウスLが押されたら弾丸発射
        if pyxel.btnp(pyxel.MOUSE_LEFT_BUTTON) == True:
            Bullet_list.append(
                Bullet(120, 255, pyxel.mouse_x, pyxel.mouse_y, 5)
            
            )
        """
        if pyxel.btnp(pyxel.KEY_Z) == True:
            if(self.bullet_a <= 0):return   #残弾数チェック
            Bullet_list.append(
                Bullet(10, 240, pyxel.mouse_x, pyxel.mouse_y, BULLET_SPEED, 11)
            )
            self.bullet_a -= 1
            
        elif pyxel.btnp(pyxel.KEY_X) == True:
            if(self.bullet_b <= 0):return      #残弾数チェック
            Bullet_list.append(
                Bullet(120, 240, pyxel.mouse_x, pyxel.mouse_y, BULLET_SPEED, 11)
            )
            self.bullet_b -= 1
            
        elif pyxel.btnp(pyxel.KEY_C) == True:      #残弾数チェック
            if(self.bullet_c <= 0):return
            Bullet_list.append(
                Bullet(230, 240, pyxel.mouse_x, pyxel.mouse_y, BULLET_SPEED ,11)
            )
            self.bullet_c -= 1
            
        elif pyxel.btnp(pyxel.KEY_M) == True:
            msl_sx = random.randint(1, SCR_WIDTH)   #ミサイル発生時のX座標
            msl_ex = random.randint(1, SCR_WIDTH)   #ミサイル着弾目標地点のX座標
                        
            Missile_List.append(
                Missile(msl_sx, 0, msl_ex, SCR_HEIGHT, MISSILE_SPEED, 8)
            )
        
        #Debug 2秒毎にミサイル発生
        if pyxel.frame_count % 120 == 0:
            msl_sx = random.randint(1, SCR_WIDTH)   #ミサイル発生時のX座標
            msl_ex = random.randint(1, SCR_WIDTH)   #ミサイル着弾目標地点のX座標
                        
            Missile_List.append(
                Missile(msl_sx, 0, msl_ex, SCR_HEIGHT, MISSILE_SPEED, 8)
            )                        

        #リスト化されたオブジェクト更新    
        update_list(Bullet_list)
        update_list(Explode_list)
        update_list(Missile_List)
                
        #リスト化されたオブジェクトのガベコレ
        cleanup_list(Bullet_list)
        cleanup_list(Explode_list)
        cleanup_list(Missile_List)

    ##-------------------------------------------------------------------------------
    #ゲームプレイ中のdraw処理
    ##-------------------------------------------------------------------------------    
    def _draw_play(self):
        pyxel.cls(0)

        pyxel.text(0, 0, str(pyxel.mouse_x) + ":" + str(pyxel.mouse_y), 2)
        pyxel.text(0, 10, str(pyxel.frame_count), 2)

        #ダミー砲台位置（３つ）        
        pyxel.text(10, 230, "ZZZ", 7)
        pyxel.text(120, 230, "XXX", 7)
        pyxel.text(230, 230, "CCC", 7)
        
        #残弾数
        pyxel.text(10, 240, "^:" + str(self.bullet_a), 7)
        pyxel.text(120, 240, "^:" + str(self.bullet_b), 7)
        pyxel.text(230, 240, "^:" + str(self.bullet_c), 7)        
        
        #レティクル描画
        self.reticle.draw()

        #リスト化されたオブジェクトの描画処理
        draw_list(Bullet_list)    
        draw_list(Explode_list)
        draw_list(Missile_List)  

gamemain()
