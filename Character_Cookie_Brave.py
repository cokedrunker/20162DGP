#__author__ = 'rowell'
import random
from pico2d import *

class Brave_Cookie:
    def __init__(self):
        self.image = load_image('Brave_Cookie_Run_Jump_Slide.png')      #이미지 로드
        self.x , self.y = 150, 150      #그려줄 좌표 초기화
        self.frame = 0      #프레임 값.
        self.Control_motion = 0

        self.Change_Y = 0
        self.Chang_Y_D = 0
        self.up = True

    def Frame(self):
        if self.Control_motion == 0 :
            self.frame = (self.frame + 1 ) % 3
        elif self.Control_motion == 1: #1단 점프일 때
            self.frame = 0
        elif self.Control_motion == 3 :
            if self.up == True:
                self.frame = (self.frame + 1) % 4
            else :
                self.frame = 5
        elif self.Control_motion == 2 :
            self.frame = (self.frame + 1 ) % 2

    def Running(self):
        self.Control_motion = 0
    def Jump(self):
        self.Control_motion = 1
    def Slide(self):
        self.Control_motion = 2
    def Jump_Double(self):
        self.Control_motion = 3

    def Jump_Change_Ysize(self) :
        global Jumping

        if self.Control_motion == 1 :   #점프 중으로 바뀌었을 때.
            if self.Change_Y < 5 :
                if self.up == True :
                    self.Change_Y += 1
                    self.y += 30
                elif self.up == False:
                    self.Change_Y -= 1
                    self.y -= 30
                    if self.Change_Y == 0 :
                        self.y = 150
                        self.Control_motion = 0
                        Jumping = 0
                        self.up = True
            elif self.Change_Y == 5 :
                    self.up = False
                    self.Change_Y -= 1
                    self.y -= 30
        if self.Control_motion == 3 :   #더블점프 중으로 바뀌었을 때.
            if self.up == True :    #위로 올라가는 중이었을때만.
                if self.Chang_Y_D < 4 :
                    self.Chang_Y_D +=1
                    self.y += 30
                if self.Chang_Y_D == 4 :    #아래로 꺼졍
                    self.Chang_Y_D -=1
                    self.y -= 30
                    self.up = False
            if self.up == False :   #아래로 내려가는 중
                if self.Chang_Y_D != 0 :
                    if self.Chang_Y_D > 0 :
                        self.Chang_Y_D -=1
                        self.y -= 30
                if self.Chang_Y_D == 0 :
                    if self.Change_Y > 0 :
                        self.Change_Y -= 1
                        self.y -= 30
                if self.Chang_Y_D == 0 and self.Change_Y == 0 :
                    self.y = 150
                    self.Control_motion = 0
                    self.frame = 0
                    Jumping = 0
                    self.up = True

    def draw(self):
        if self.Control_motion == 0:
            self.image.clip_draw(self.frame * 120, 382-135 ,120 ,135 , self.x , self.y)
        elif self.Control_motion == 1:
            self.image.clip_draw(0, 382-135-165 ,140 ,165 , self.x , self.y)
        elif self.Control_motion == 3:
            self.image.clip_draw(self.frame * 140, 382-135-165 ,140 ,165 , self.x , self.y)
        elif self.Control_motion == 2 :
            self.image.clip_draw(self.frame * 170, 382-135-165-80 ,170 ,80 , self.x , self.y-40)

    def ReDifine_Frame(self):
         self.frame = 0


class Ground1:
    def __init__(self):
        self.image = load_image('grass.png')      #이미지 로드



    def draw(self):
        self.image.draw(400,50)

class Main_Back:
    def __init__(self):
        self.image = load_image('main_back.png')  # 이미지 로드

    def draw(self):
        self.image.draw(400, 300)




def handle_events():        #조작.
    global running      #함수가 작동 중인지 여부 확인.

    global Sliding      # 슬라이딩 중 다른 조작 못 하게.
    global Jumping      # 점프 중 다른 조작 못 하게.
    #용쿠 조작 추가.
    global BraveCookie
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False
        # 쿠키 조작.
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_UP :
                if Jumping == 0:
                    BraveCookie.Jump()
                    Jumping += 1
                elif Jumping == 1:
                    BraveCookie.ReDifine_Frame()
                    BraveCookie.Jump_Double()
            elif event.key == SDLK_DOWN and Jumping == 0:
                BraveCookie.Slide()
                Sliding += 1
        if event.type == SDL_KEYUP :
            if Sliding != 0 :
                BraveCookie.Running()
                Sliding = 0


open_canvas()

BraveCookie = Brave_Cookie()
Back1=Ground1()
Back0=Main_Back()

running = True
Sliding = 0
Jumping = 0

while running:
    handle_events()

    BraveCookie.Frame()
    BraveCookie.Jump_Change_Ysize()

    clear_canvas()
    Back0.draw()
    Back1.draw()


    BraveCookie.draw()

    update_canvas()

    delay(0.08)

close_canvas()