#python版本：v3.5.1:37a07cee5969
#pygame版本：1.9.2a0
#运行环境：windows  10.0.10586 x64
#编译器： Visual Studio Community 2015 14.0.24720.00 Update 1
#Python Tools for Visual Studio： 2.2.31124.00

import pygame
from pygame.locals import *

from threading import Thread
from time import sleep
from sys import exit
from random import randint

from calcul import core
from globalvar import gv
from sourceflie import sc

def nop():
    pass

def main():
    
    global_init()    

    btn_start = sc.Button(gv.g_btn_start_imgloc,gv.g_size_btn,gv.g_pos_btn_start)
    btn_about = sc.Button(gv.g_btn_about_imgloc,gv.g_size_btn,gv.g_pos_btn_about)

    surface_game()
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()

        gv.g_screen.blit(gv.g_home_img,(0,0))

        btn_start.update(surface_game)
        btn_about.update(surface_about)

        pygame.display.update()
        gv.g_clock.tick(30)

def global_init():

    pygame.init()

    #load icon & title
    pygame.display.set_icon(pygame.image.load(gv.g_icon_fileloc))
    pygame.display.set_caption(gv.g_wintitle)

    gv.g_screen  = pygame.display.set_mode(gv.g_size_win)    
    gv.g_clock   = pygame.time.Clock()

    gv.g_home_img = sc.loadimg(gv.g_home_img_fileloc,gv.g_size_win)

def surface_about():
        
    btn_back = sc.Button(gv.g_btn_back_imgloc,gv.g_size_btn,gv.g_pos_btn_back)

    about_bkgimg = sc.loadimg(gv.g_surfaceback_img_fileloc,gv.g_size_win)
    
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
        gv.g_screen.blit(about_bkgimg,(-1,-1))
        if btn_back.update(nop) == 1:
            break
        pygame.display.update()
        gv.g_clock.tick(30)

def surface_game():
    next_player  = 1

    if next_player==0:
        draw_pcs_tab = sc.draw_table_cp_first
    else:
        draw_pcs_tab = sc.draw_table_pl_first

    grid_img  = sc.loadimg("img/grid.png",gv.g_size_win)
    w_img     = sc.loadimg("img/round_white.png",(24,24))
    b_img     = sc.loadimg("img/round_black.png",(24,24))
    think_img = sc.loadimg("img/think.png",(120,60))
    back_btn  = sc.Button(gv.g_btn_gameback_imgloc,gv.g_size_btn_gameback,gv.g_pos_btn_gameback)

    computer_pgsbar = sc.ProgressBar("img/round_white.png",(12,12),(655,56),35)
    player_pgsbar   = sc.ProgressBar("img/round_black.png",(12,12),(720,440),40)
    
    wzqcore = core.Core(1)
    input_info = sc.GetInput();
    
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()

        gv.g_screen.blit(grid_img,(0,0))

        #绘制棋子
        draw_pcs_tab(wzqcore,w_img,b_img)
        
        #不为0时，已分胜负
        if wzqcore.who_win != 0:
            one_more_img = sc.loadimg("img/one_more_time.png",(100,80))
            if wzqcore.who_win == 1:
                win_img = sc.loadimg("img/win.png",(130,45))
            else:
                win_img = sc.loadimg("img/win_2.png",(130,45))
            #sc.draw_five(wzqcore)
            gv.g_screen.blit(win_img,(300,495))
            gv.g_screen.blit(one_more_img,(20,420))
            
        #未分胜负         
        else:
            #电脑落子  
            if wzqcore.busy == 1:
                computer_pgsbar.draw()

            #玩家落子
            else:
                input_status = input_info.scan()
                if input_status[0] == 1:
                    tab_pos = sc.pixpos_to_table((input_status[1],input_status[2]))        
                    wzqcore.player_take(tab_pos)
                    
                #绘制进度条
                gv.g_screen.blit(think_img,(680,420))
                player_pgsbar.draw()

        if back_btn.update(nop) == 1:
            break
        pygame.display.update()
        gv.g_clock.tick(30)

if __name__ == "__main__":
    main()
