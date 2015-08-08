
#python版本：v3.4.0:04f714765c13
#pygame版本：1.9.2a0
#运行环境：windows 8.1 x64

import pygame
from pygame.locals import *

from threading import Thread
from time import sleep
from sys import exit
from random import randint

from calcul import core
#按钮
#1、初始化需传入操作的scree对象，三幅图像的路径，分别为静态显示样式、
#       鼠标移动到按钮上的样式(focus)和按下时的样式，按钮的大小、按
#       钮的位置
#2、执行update(fun)方法来扫描按钮事件，鼠标按键抬起之时执行传入的函数fun
#3、若按键按下，抬起之后返回 1
class Button():
    def __init__(self,screen,file_loc_static,file_loc_focus,file_loc_down,size=(0,0),position=(0,0)):
        self.screen = screen
        self.position = position
        self.button_pushed = 0
        self.border_x = (position[0],position[0]+size[0])
        self.border_y = (position[1],position[1]+size[1])

        self.static_img = pygame.transform.smoothscale(pygame.image.load(file_loc_static).convert_alpha(),size)
        self.focus_img = pygame.transform.smoothscale(pygame.image.load(file_loc_focus).convert_alpha(),size)
        self.down_img = pygame.transform.smoothscale(pygame.image.load(file_loc_down).convert_alpha(),size)

    def update(self,fun):
        mouse_pos = pygame.mouse.get_pos()
        return_data = 0

        if self.isInBorder(mouse_pos):                  #如果鼠标指针落在按钮的区域内，检测事件
            mouse_btn = pygame.mouse.get_pressed()[0]
            if mouse_btn == 0:                              #鼠标左键未按下
                if self.button_pushed == 1:                     #鼠标按键抬起后的瞬间                    
                    self.button_pushed = 0
                    return_data = 1
                    fun()                                           #执行按钮函数
                else:                                           #鼠标已经抬起很久，绘制聚焦图标
                    self.screen.blit(self.focus_img,self.position)
            else:                                           #鼠标左键已经按下，绘制按下图标
                self.screen.blit(self.down_img,self.position)
                self.button_pushed = 1
        else:                                           #鼠标指针未落在按钮区域内，绘制静态图标
            self.screen.blit(self.static_img,self.position)
            self.button_state = 0
        return return_data

    def isInBorder(self,pos):
        if self.border_x[0] <= pos[0] <= self.border_x[1] and \
                self.border_y[0] <= pos[1] <= self.border_y[1]:
            return 1
        else:
            return 0

#进度条刷新
#1、file_loc为进度条文件路径，size为显示大小，pos为起点，len为左右横移长度
#2、每经过一帧时间，自动计算进度条显示位置
class ProgressBar():
    def __init__(self,screen,file_loc,size,pos,len):
        self.screen = screen
        self.img = pygame.transform.smoothscale(pygame.image.load(file_loc).convert_alpha(),size)
        self.border = [pos[0],pos[0] + len]
        self.vertical_position = pos[1]
        self.level_position = self.border[0]
        self.direction = 1
    def draw(self):
        if self.direction == 1:
            self.level_position += 1
            if self.level_position > self.border[1]:
                self.level_position = self.border[1]
                self.direction = 0
            screen.blit(self.img,(self.level_position,self.vertical_position))
        else:
            self.level_position -= 1
            if self.level_position < self.border[0]:
                self.level_position = self.border[0]
                self.direction = 1
            screen.blit(self.img,(self.level_position,self.vertical_position))

#扫描鼠标在pos=(x,y)为起点，size=(x,y)为大小的 矩形区域内的动作：
#1、在鼠标按键抬起的时候返回坐标
class Input():
    def __init__(self,pos,size,error = 4):
        self.border_x = (pos[0],pos[0]+size[0])
        self.border_y = (pos[1],pos[1]+size[1])
        self.error = error      
        self.last_position = [0,0]
        self.mouse_pushed_down = 0
    def scan(self):
        return_data = (-1,0,0)
        mouse_status = pygame.mouse.get_pressed()[0]

        if mouse_status == 1:                   #按键按下
            if self.mouse_pushed_down == 0:     #首次按下，记录鼠标坐标
                self.mouse_pushed_down = 1
                self.last_position = pygame.mouse.get_pos()
        else :                                      #按键抬起
            if self.mouse_pushed_down == 1:         #按键抬起之后首次扫描，处理事件
                self.mouse_pushed_down = 0          #清除“按键已经按下”标志
                mouse_pos = pygame.mouse.get_pos()
                if self.isInRect(mouse_pos,self.last_position,self.error) :
                    if self.isInBorder(mouse_pos) == 1:
                        return_data = (1,mouse_pos[0],mouse_pos[1])

        return return_data

    def isInBorder(self,pos):
        if self.border_x[0] <= pos[0] <= self.border_x[1] and \
                self.border_y[0] <= pos[1] <= self.border_y[1]:
            return 1
        else:
            return 0
    def isInRect(self,pos,rect_cen_pos,error):
        if rect_cen_pos[0] - error <= pos[0] <= rect_cen_pos[0] + error and \
                rect_cen_pos[1] - error <= pos[1] <= rect_cen_pos[1] + error :
            return 1
        else:
            return 0

def nop():
    return 1
def makeImg(file_loc,size = (0,0)):
    return pygame.transform.smoothscale(pygame.image.load(file_loc).convert_alpha(),size)
def playMusic(sound):
    pygame.mixer.music.load(sound)
    pygame.mixer.music.play()

# options
windows_x = 800
windows_y = 600

game_init = pygame.init()
screen = pygame.display.set_mode((windows_x,windows_y))
title = pygame.display.set_caption("CL的五子棋")
clock = pygame.time.Clock()

#玩家下子 将像素位置转换为落旗坐标
#start_pos 和 end_pos 参数分别为棋盘画面像素的坐标
def transPixToTable(mouse_pos,step_pix=30,start_pos = (170,60),end_pos = (610,500)):
    j=(mouse_pos[0]-start_pos[0] + 5)//30
    i=(mouse_pos[1]-start_pos[1] + 5)//30
    print(i,j)
    return (i,j)
 
#将所有的棋子画在棋盘上
#最后两个参数分别为 棋盘上两个格子相隔的像素数，最左上角的棋子 在整幅img中的起始坐标
def drawPieces(core,w_img,b_img,step_pix = 30,start_pos = (168,58)):
    for i in range(0,15):
        for j in range(0,15):
            if core.table[i][j] == 1:   #white                
                screen.blit(w_img,(j*step_pix+start_pos[0],i*step_pix+start_pos[1]))
            elif core.table[i][j] == 2: #black
                screen.blit(b_img,(j*step_pix+start_pos[0],i*step_pix+start_pos[1]))
    last = core.last
    if last != [-1,-1]:
        circle_pos = (last[1] * step_pix + start_pos[0] + 12 , last[0] * step_pix + start_pos[1] + 12)
        pygame.draw.circle(screen,(200,0,0),circle_pos,4)
def drawFivePieces(core,step_pix = 30,start_pos = (180,70)):
    for i in range(1,8):
        last = core.five_pieces[i]
        if last != [0,0]:
            circle_pos = (last[1] * step_pix + start_pos[0], last[0] * step_pix + start_pos[1])
            pygame.draw.circle(screen,(200,0,0),circle_pos,4)

#游戏界面处理模块
def game():
    size_btn = (80,40)
    pos_btn_back = (20,500)

    who_win = 0
    back_btn_down = 0
    #预渲染的资源
    grid_img = makeImg("img/grid.png",(windows_x,windows_y))
    w_img = makeImg("img/round_white.png",(24,24))
    b_img = makeImg("img/round_black.png",(24,24))
    think_img = makeImg("img/think.png",(120,60))
    back_btn = Button(screen = screen,\
                        file_loc_static = "img/btn_return.png",\
                        file_loc_focus = "img/btn_back_focus.png",\
                        file_loc_down = "img/btn_back_down.png",\
                        size = size_btn,\
                        position = pos_btn_back)
    computer_progress_bar = ProgressBar(screen,"img/round_white.png",(12,12),(655,56),35)
    player_progress_bar = ProgressBar(screen,"img/round_black.png",(12,12),(720,440),40)
    wzq_core = core.Core()
    grid_imput_area = Input((170,60),(610-170,500-60))

    while not back_btn_down:
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()

        screen.blit(grid_img,(0,0))

        if wzq_core.busy == 1:      #core忙，播放电脑思考进度条
            computer_progress_bar.draw()
        else:                       #core闲,检查谁获胜
            who_win = wzq_core.getWhoWin()
            if who_win != 0:            #胜负已分，跳出循环
                break
            else:                       #未分胜负，玩家落子(电脑在core忙时落子)
                mouse_input = grid_imput_area.scan()
                if mouse_input[0] == 1:                 #有效的鼠标输入
                    piece_positon = transPixToTable(mouse_input[1:])
                    grid_input = wzq_core.playerTakeStep(piece_positon)
                    if  grid_input == 1:                    #有效的棋盘输入(没有重复输入同一个落子点)
                        who_win = wzq_core.getWhoWin()
                        if who_win != 0 :            #胜负已分，跳出循环
                            break
                        else:                        #胜负仍未分，电脑后台计算下一步
                            cal = Thread(target = wzq_core.calNext, args = ("calculating",))
                            cal.start()

                if who_win != 2:        #如果玩家未胜利，播放玩家思考进度条
                    screen.blit(think_img,(680,420))        #绘制思考气泡
                    player_progress_bar.draw()


        back_btn_down = back_btn.update(nop)
        drawPieces(wzq_core,w_img,b_img)
        pygame.display.update()
        clock.tick(30)
    # 胜负已分，胜利界面：
    one_more_img = makeImg("img/one_more_time.png",(100,80))
    if who_win == 2:
        win_img = makeImg("img/win.png",(130,45))
    else:
        win_img = makeImg("img/win_2.png",(130,45))

    
    screen.blit(grid_img,(0,0))
    screen.blit(win_img,(300,495))
    screen.blit(one_more_img,(20,420))
    drawPieces(wzq_core,w_img,b_img)
    drawFivePieces(wzq_core)
    
    
    
    while not back_btn_down:
        pygame.event.get()
        back_btn_down = back_btn.update(nop)
        pygame.display.update()
        clock.tick(30)

#“关于”界面
def about():
    back_btn_down = 0
    pos_btn_back = (windows_x//2.5,windows_y//1.2)
    size_btn = (windows_x//6,windows_y//8)
    btn_back = Button(screen = screen,\
                        file_loc_static = "img/btn_return.png",\
                        file_loc_focus = "img/btn_back_focus.png",\
                        file_loc_down = "img/btn_back_down.png",\
                        size = size_btn,\
                        position = pos_btn_back)
    about_img = makeImg("img/about_background.png",(windows_x,windows_y))
    
    while not back_btn_down:
        pygame.event.get()
        screen.blit(about_img,(-1,-1))
        back_btn_down = btn_back.update(nop)
        pygame.display.update()
        clock.tick(30)
# MAIN
def main():
    
    size_btn = (133,75)    
    pos_btn_start = (200,400)    
    pos_btn_about = (400,400)

    btn_start = Button(screen = screen,\
                        file_loc_static = "img/btn_start_game.png",\
                        file_loc_focus = "img/btn_start_game_focus.png",\
                        file_loc_down = "img/btn_start_game_down.png",\
                        size = size_btn,\
                        position = pos_btn_start)

    btn_about = Button(screen = screen,\
                        file_loc_static = "img/btn_about.png",\
                        file_loc_focus = "img/btn_about_focus.png",\
                        file_loc_down = "img/btn_about_down.png",\
                        size = size_btn,\
                        position = pos_btn_about)

    home_page_img = makeImg("img/homepage.png",(windows_x,windows_y))
     
    
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()

        screen.blit(home_page_img,(0,0))

        btn_start.update(game)
        btn_about.update(about)
        
        pygame.display.update()
        clock.tick(30)



if __name__ == "__main__":
    main()
