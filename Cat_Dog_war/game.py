import pygame as pg, random, math
from Gaze_Model.Face_Detection.Face_Detection import DetectFace
from Gaze_Model.gaze_tracking.eyes_model import EyesModel
import cv2
import time
import keyboard
from Gaze_Model.Remove_BG_Remove.main import RemoveBackground as remove
import os
from datetime import datetime
import threading
os.environ['SDL_VIDEO_WINDOW_POS'] = "0,30" # screen init position
pg.init()
p1_score = 100
p2_score = 100
bar = 1 # power bar # 0~100
speed = 2
clock = pg.time.Clock() 
running = True
welcome = True
setting = False
photo_ok = False
game_start = False
game_over = False
judge_blink = False
button = True
button_c = 0
Round = 1
Round_c = 0
wind_vx = 0 # right+ left- (-3~3)
fade_out = True
over_c = 0
congrat = False
sprinkle = False
count = 5 # sprite sheet 張數
abs_path = os.path.abspath(os.path.dirname(__file__)) # this file absolute path
player = True # true=p1 false=p2
gravity = -25
vx = 60
wind_effect = 7
p1_throw = False
p2_throw = False
window = pg.display.Info()
w, h = window.current_w, window.current_h 
width, height = 750, 422
screen = pg.display.set_mode((width, height))
pg.display.set_caption("game")         
bg = pg.Surface(screen.get_size()) 
bg = bg.convert()
pg.mouse.set_visible(False)  # hide the cursor
class star(pg.sprite.Sprite):  
    # 速度、x,y座標、星星種類
    def __init__(self, vy, x, y, style, size):
        pg.sprite.Sprite.__init__(self)
        self.vy = vy
        self.x = x
        self.y = y
        self.size = size
        if style == 0:
            input_path = os.path.abspath(os.path.join(abs_path, "stars1.png"))
        elif style == 1:
            input_path = os.path.abspath(os.path.join(abs_path, "stars2.png"))
        else:
            input_path = os.path.abspath(os.path.join(abs_path, "stars3.png"))
        self.image = pg.image.load(input_path)
        self.image = pg.transform.scale(self.image, (size, size))
        bg.blit(self.image, (x,y))
    def update(self):  # move
        self.y += self.vy
        bg.blit(self.image, (self.x,self.y))
Allstars = pg.sprite.Group()  
def update():
    screen.blit(bg, (0,0))
    pg.display.update()     
def render_ScoreBar():
    pg.draw.rect(bg, (253,239,242),[50, 50, 250, 30], 0, border_radius=6) # 實心
    pg.draw.rect(bg, (43,43,43),[50, 50, 250, 30], 3, border_radius=6) # 外框 
    pg.draw.rect(bg, (233,84,107),[295-p1_score*2.4, 55, p1_score*2.4, 20], 0, border_radius=9) # score
    pg.draw.rect(bg, (253,239,242),[width-300, 50, 250, 30], 0, border_radius=6) 
    pg.draw.rect(bg, (43,43,43),[width-300, 50, 250, 30], 3, border_radius=6) 
    pg.draw.rect(bg, (233,84,107),[width-295, 55, p2_score*2.4, 20], 0, border_radius=9) 
def render_Wind():
    if wind_vx > 0:   
        gradientRect(bg, (90,200,255), (90-abs(wind_vx)*30,200-abs(wind_vx)*30, 255),pg.Rect(int(width/2), 105, abs(wind_vx)*30, 20)) # 風向
    elif wind_vx < 0:   
        gradientRect(bg, (90-abs(wind_vx)*30,200-abs(wind_vx)*30, 255),(90,200,255),pg.Rect(int(width/2)-abs(wind_vx)*30, 105, abs(wind_vx)*30, 20))
    else:   
        pg.draw.rect(bg, (44,169,225),[int(width/2)-3, 105, 8, 20], 0) 
    pg.draw.line(bg, (43,43,43),(int(width/2),100), (int(width/2), 130), 2)
    font = pg.font.SysFont("simhei", 25)
    text = font.render("wind", True, (0, 0, 0))
    rect = text.get_rect()
    rect.center = (int(width/2), 140)
    bg.blit(text, rect.topleft)
def render_Background(opacity):
    bg.fill((255,255,255))
    input_path = os.path.abspath(os.path.join(abs_path, "background.jpg"))
    image = pg.image.load(input_path) # 750*422
    image.set_alpha(opacity) # transparent: 0
    bg.blit(image, (0, 0)) 
def set_cursor():
    input_path = os.path.abspath(os.path.join(abs_path, "cursor.png"))
    MANUAL_CURSOR = pg.image.load(input_path)
    MANUAL_CURSOR = pg.transform.scale(MANUAL_CURSOR, (30, 30))
    bg.blit( MANUAL_CURSOR, ( pg.mouse.get_pos() ) ) 
def render_Player():
    global height, bg, abs_path
    input_path = os.path.abspath(os.path.join(abs_path, "Gaze_Model\Remove_BG_Remove\Capture\P1_Remove.png"))
    image = pg.image.load(input_path) # 257*374
    image = pg.transform.scale(image, (80, 116))
    if p1_throw and spritesheet>1:
        x = 135+(spritesheet-1)*35
        y = height-195
        bg.blit(image, (x, y)) 
    else:
        bg.blit(image, (135, height-200)) 
    input_path = os.path.abspath(os.path.join(abs_path, "Gaze_Model\Remove_BG_Remove\Capture\P2_Remove.png"))
    image = pg.image.load(input_path)
    image = pg.transform.scale(image, (80, 116))
    if p2_throw and spritesheet<3:
        x = width-215+(spritesheet-3)*35
        y = height-195
        bg.blit(image, (x, y)) 
    else:
        bg.blit(image, (width-215, height-200)) 
def render_Pitcher1():
    global height, spritesheet, bg
    input_path = os.path.abspath(os.path.join(abs_path, "spritesheet.png"))
    pitcher = pg.image.load(input_path) # 700*700*count
    pitcher = pg.transform.scale(pitcher, (count*150, 150))
    pitcher_w, pitcher_h = pitcher.get_width()/count, pitcher.get_height()
    bg.blit(pitcher, (150, height-125), pg.Rect((0+spritesheet*pitcher_w,0), (pitcher_w, pitcher_h)))
def render_Pitcher2():
    global height, spritesheet, bg
    input_path = os.path.abspath(os.path.join(abs_path, "spritesheet.png"))
    pitcher = pg.image.load(input_path) # 700*700*count
    pitcher = pg.transform.scale(pitcher, (count*150, 150))
    pitcher = pg.transform.flip(pitcher, True, False) 
    pitcher_w, pitcher_h = pitcher.get_width()/count, pitcher.get_height()
    bg.blit(pitcher, (450, height-125), pg.Rect((0+spritesheet*pitcher_w,0), (pitcher_w, pitcher_h)))
def render_p1_PowerBar():
    pg.draw.rect(bg, (253,239,242),[120, 210, 110, 20], 0) 
    pg.draw.rect(bg, (43,43,43),[120, 210, 110, 20], 2)  
    pg.draw.rect(bg, (39,74,120),[125, 213, bar, 14], 0) 
def render_p2_PowerBar():
    pg.draw.rect(bg, (253,239,242),[width-230, 210, 110, 20], 0) 
    pg.draw.rect(bg, (43,43,43),[width-230, 210, 110, 20], 2)  
    pg.draw.rect(bg, (39,74,120),[width-225, 213, bar, 14], 0) 
def render_p1_fish():
    global abs_path
    path = os.path.abspath(os.path.join(abs_path, "fish.png"))
    image = pg.image.load(path) 
    image = pg.transform.scale(image, (50, 39))
    bg.blit(image, (ball_x, ball_y)) 
def render_p2_fish():
    global abs_path
    path = os.path.abspath(os.path.join(abs_path, "DogFood.png"))
    image = pg.image.load(path) 
    image = pg.transform.scale(image, (50, 50))
    bg.blit(image, (ball_x, ball_y)) 
def gradientRect( window, left_colour, right_colour, target_rect ):
    colour_rect = pg.Surface( ( 2, 2 ) )                                   
    pg.draw.line( colour_rect, left_colour,  ( 0,0 ), ( 0,1 ) )           
    pg.draw.line( colour_rect, right_colour, ( 1,0 ), ( 1,1 ) )            
    colour_rect = pg.transform.smoothscale( colour_rect, ( target_rect.width, target_rect.height ) ) 
    bg.blit( colour_rect, target_rect )                                    
def blink():
    count = 0
    global judge_blink, running
    Blink = EyesModel([int(w-600), int(h-300)], [int(w-300), int(h-300)])
    while running:
        while game_start and running:
            if cv2.waitKey(3) != ord('q'): # ms
                text1P, text2P = Blink.open()
                if player:
                    if text1P == "Blinking":
                        count += 1
                        if count > 2:
                            if not p1_throw and not p2_throw:
                                judge_blink = True
                            count = 0
                    else:
                        count = 0
                else:
                    if text2P == "Blinking":
                        count += 1
                        if count > 2:
                            if not p1_throw and not p2_throw:
                                judge_blink = True
                            count = 0
                    else:
                        count = 0
        if game_over: cv2.destroyAllWindows()
    Blink = None  
t = threading.Thread(target = blink)
t.start()
global spritesheet
spritesheet = 0
while running:
    if (p1_throw or p2_throw) and pitch: clock.tick(8) 
    elif p1_throw or p2_throw: clock.tick(15) 
    elif game_over: clock.tick(10)
    else: clock.tick(30)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        elif event.type == pg.MOUSEBUTTONUP and welcome:
            pos = pg.mouse.get_pos()
            if pg.Rect.collidepoint(button_rect, pos):
                setting = True
                welcome = False
        elif event.type == pg.KEYUP:
            if event.key == pg.K_s and player:
                p1_throw = True
            elif event.key == pg.K_d and not player:
                p2_throw = True
    if judge_blink == True:
        judge_blink = False
        if player: p1_throw = True
        else: p2_throw = True
    if p1_score==0 or p2_score==0: 
        game_start = False
        game_over = True
    # 開始畫面
    if welcome:
        input_path = os.path.abspath(os.path.join(abs_path, "background.jpg"))
        image = pg.image.load(input_path) # 750*422
        bg.blit(image, (0, 0)) 
        pg.draw.rect(bg, (86, 84, 162), (int(width*0.35), int(height*0.35), int(width*0.3), int(width*0.1)), 5, int(width*0.03))
        if button:
            button_rect = pg.draw.rect(bg, (112, 108, 170), (int(width*0.365), int(height*0.35+width*0.015), int(width*0.27), int(width*0.07)), 0, border_radius=int(width*0.02))
        else:
            button_rect = pg.draw.rect(bg, (165, 154, 202), (int(width*0.365), int(height*0.35+width*0.015), int(width*0.27), int(width*0.07)), 0, border_radius=int(width*0.02))
        font = pg.font.SysFont("simhei", 40)
        text = font.render("Game start", True, (255, 255, 255))
        rect = text.get_rect()
        rect.center = (int(width*0.5), int(height*0.35+width*0.05))
        bg.blit(text, rect.topleft)
        if button_c == 10:
            button = not button
            button_c = 0
        button_c += 1
    # 拍大頭照
    elif setting:
        render_Background(200)
        font = pg.font.SysFont("simhei", 80)
        text = font.render("smile :)", True, (255, 255, 255))
        rect = text.get_rect()
        rect.center = (int(width*0.5), int(height*0.5))
        bg.blit(text, rect.topleft)
        update()
        # Detect 1P face
        _1P_Face = DetectFace("1P")
        while 1:
            for i in range(50):
                if cv2.waitKey(1) == ord('q'):
                    break
                _1P_Face.open(1 + i // 6)
                time.sleep(0.001)
            confirm = _1P_Face.capture("P1.png")
            if confirm: break
        _1P_Face = None
        ReMove = remove("P1.png", "P1_Remove.png")
        ReMove = None
        # Detect 2P face
        _2P_Face = DetectFace("2P")
        while 1:
            for i in range(50):
                if cv2.waitKey(1) == ord('q'):
                    break
                _2P_Face.open(1 + i // 6)
                time.sleep(0.001)
            confirm = _2P_Face.capture("P2.png")
            if confirm: break
        cv2.destroyAllWindows()
        ReMove = remove("P2.png", "P2_Remove.png")
        ReMove = None
        setting = False
        game_start = True
    elif game_start:
        render_Background(200)
        render_ScoreBar()
        render_Wind()
        render_Player()
        # p1
        if player:
            render_Pitcher1()
            render_p1_PowerBar()
            # attack bar          
            if not p1_throw:
                if bar>=99 or bar<=0: speed*=-1
                bar += speed 
                render_p1_PowerBar()
                ball_x = 255
                ball_y = 170
                ball_vy = bar
                pitch = True
                spritesheet = 0
            # people animate
            elif pitch:
                if spritesheet<4: spritesheet += 1
                else: 
                    spritesheet = 4 # for p2
                    pitch = False
            # throw animate
            else:
                # ball flying
                if ball_y <= 200:
                    ball_x += vx + wind_vx*wind_effect
                    ball_vy += gravity
                    ball_y -= ball_vy
                    render_p1_fish()
                # ball arrive
                else: 
                    if ball_x>(width-230) and ball_x<(width-170): p2_score-=20
                    bar = 1
                    player = not player
                    # change wind
                    if Round_c==0: ran = random.randint(2, 4)
                    Round_c += 1
                    if Round_c==ran: 
                        wind_vx = random.randint(-3, 3)
                        Round_c = 0
                    p1_throw = False
        # p2
        else:
            # render all
            render_Pitcher2()
            render_p2_PowerBar()
            # attack bar
            if not p2_throw:
                if bar>=99 or bar<=0: speed*=-1
                bar += speed 
                render_p2_PowerBar()
                ball_x = width-305
                ball_y = 170
                ball_vy = bar
                pitch = True
                spritesheet = 4
            # people animate
            elif pitch:
                if spritesheet>0: spritesheet -= 1
                else: 
                    spritesheet = 0 # for p1
                    pitch = False
            # throw animate
            else:
                # ball flying
                if ball_y <= 200:
                    ball_x -= vx - wind_vx*wind_effect
                    ball_vy += gravity
                    ball_y -= ball_vy
                    render_p2_fish()
                # ball arrive
                else:
                    if ball_x>120 and ball_x<180: p1_score-=20
                    bar = 1
                    player = not player
                    # change wind
                    if Round_c==0: ran = random.randint(2, 4)
                    Round_c += 1
                    if Round_c==ran: 
                        wind_vx = random.randint(-3, 3)
                        Round_c = 0
                    p2_throw = False
    elif game_over:
        over_c += 1
        if fade_out:
            bg.set_alpha(10)
            bg.fill((255,255,255))   
            if over_c == 20: 
                fade_out = False
                congrat = True
        elif congrat:
            bg.set_alpha(255)
            render_Background(100)
            if p1_score==0: 
                input_path = os.path.abspath(os.path.join(abs_path, "Gaze_Model\Remove_BG_Remove\Capture\P2_Remove.png"))
            else: 
                input_path = os.path.abspath(os.path.join(abs_path, "Gaze_Model\Remove_BG_Remove\Capture\P1_Remove.png"))
            image = pg.image.load(input_path) # 257*374
            image = pg.transform.scale(image, (178, 262))
            bg.blit(image, (int(width/2-79), int(height/2-150))) 
            if over_c > 30:
                input_path = os.path.abspath(os.path.join(abs_path, "crown.png"))
                image = pg.image.load(input_path)
                image = pg.transform.scale(image, (130, 130))
                bg.blit(image, (int(width/2-65), 30))
            if over_c > 40:
                input_path = os.path.abspath(os.path.join(abs_path, "medal.png"))
                image = pg.image.load(input_path)
                image = pg.transform.scale(image, (80, 80))
                bg.blit(image, (int(width/2+30), int(height/2+70)))
                if over_c > 30: sprinkle = True
            if sprinkle:
                if over_c % 3 == 0:
                    s = star(random.randint(5, 15), random.randint(0,screen.get_width()-30), 0, random.randint(0, 2), random.randint(30, 50)) 
                    Allstars.add(s)  # add to group
                for spr in Allstars:
                    spr.update()

    if not game_over: set_cursor()
    update()
t.join()
cv2.destroyAllWindows()
pg.quit()           