
import pygame
from globalvar import gv

def loadimg(file_loc,size = (0,0)):
    img = pygame.image.load(file_loc).convert_alpha()
    return pygame.transform.smoothscale(img,size)

class Button():
    def __init__(self, btn_file_loc = (None,None,None),size=(0,0),position=(0,0)):
        self.screen = gv.g_screen
        self.position = position
        self.button_pushed = 0
        self.border_x = (position[0],position[0]+size[0])
        self.border_y = (position[1],position[1]+size[1])

        self.static_img = loadimg(btn_file_loc[0],size)
        self.focus_img = loadimg(btn_file_loc[1],size)
        self.down_img = loadimg(btn_file_loc[2],size)

    def ptr_not_in_border(self,pos):
        if self.border_x[0] <= pos[0] <= self.border_x[1] and \
                self.border_y[0] <= pos[1] <= self.border_y[1]:
            return False
        else:
            return True
    def update(self,func):
        mouse_pos = pygame.mouse.get_pos()
        event_happen = 0

        #���ָ��δ�ڰ�ť�߽��⣬���ƾ�̬ͼ��
        if self.ptr_not_in_border(mouse_pos) == True:
            self.screen.blit(self.static_img,self.position)
            self.button_state = 0

        #���ڱ߽��ڣ��жϰ����Ƿ���
        else:

            #����������£�������״̬��1�����ư���ͼ��
            if pygame.mouse.get_pressed()[0] == 1:
                self.screen.blit(self.down_img,self.position)
                self.button_pushed = True       
            
            #����δ���£��ж��Ƿ�Ϊ���¸�̧���˲��         
            else:

                if self.button_pushed == False: 
                    self.screen.blit(self.focus_img,self.position)  
                else:
                    self.button_pushed = False
                    event_happen = 1
                    func()            
        return event_happen

class ProgressBar():
    def __init__(self,file_loc,size,pos,len):
        self.screen = gv.g_screen
        self.img = loadimg(file_loc,size)
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
            self.screen.blit(self.img,(self.level_position,self.vertical_position))
        else:
            self.level_position -= 1
            if self.level_position < self.border[0]:
                self.level_position = self.border[0]
                self.direction = 1
            self.screen.blit(self.img,(self.level_position,self.vertical_position))


def pixpos_to_table(pos = (0,0)):
    i=(pos[0] - gv.g_pos_grid_start[0] + 5)//gv.g_width_grid
    j=(pos[1] - gv.g_pos_grid_start[1] + 5)//gv.g_width_grid
    return (i,j)

def teble_to_pixpos(pos = (0,0)):
    return [pos[0]*gv.g_width_grid + gv.g_pos_grid_start[0] - 2,
            pos[1]*gv.g_width_grid + gv.g_pos_grid_start[1] - 2]

def draw_table_pl_first(core,w_img,b_img):
    for i in range(15):
        for j in range(15):
            if core.table[i][j] == 2:   #white                
                gv.g_screen.blit(w_img,teble_to_pixpos((i,j)))
            if core.table[i][j] == 1:   #black
                gv.g_screen.blit(b_img,teble_to_pixpos((i,j)))

    if core.last[0] > -1:
        circle_pos = teble_to_pixpos(core.last)
        x = circle_pos[0] + 12
        y = circle_pos[1] + 12

        pygame.draw.circle(gv.g_screen,(200,0,0),(x,y),4)

def draw_table_cp_first(core,w_img,b_img):
    for i in range(15):
        for j in range(15):
            if core.table[i][j] == 1:   #white                
                gv.g_screen.blit(w_img,teble_to_pixpos((i,j)))
            if core.table[i][j] == 2:   #black
                gv.g_screen.blit(b_img,teble_to_pixpos((i,j)))

    if core.last[0] > -1:
        circle_pos = teble_to_pixpos(core.last)
        x = circle_pos[0] + 12
        y = circle_pos[1] + 12

        pygame.draw.circle(gv.g_screen,(200,0,0),(x,y),4)

def draw_five(core):
    for i in range(5):
        circle_pos = teble_to_pixpos(core.five_pcs[i])
        x = circle_pos[0] + 12
        y = circle_pos[1] + 12
        pygame.draw.circle(gv.g_screen,(200,0,0),(x,y),4)

class GetInput():
    def __init__(self):
        #error �������Χ
        self.border_x = (gv.g_pos_grid_start[0],gv.g_size_grid + gv.g_pos_grid_start[0])
        self.border_y = (gv.g_pos_grid_start[1],gv.g_size_grid + gv.g_pos_grid_start[1])

        self.last_position = [0,0]
        self.mouse_kdown = 0

    def scan(self):
        return_data = (-1,0,0)
        mouse_status = pygame.mouse.get_pressed()[0]

        #��갴�����£���¼λ�ã����������Ѿ�����
        if mouse_status == 1:
            self.mouse_kdown = 1
            self.last_position = pygame.mouse.get_pos()

        #���̧���ж��Ƿ�Ӱ��µ�˲��̧��
        else :
            #��Ч�������ж�λ��
            if self.mouse_kdown == 1:
                self.mouse_kdown = 0
                pos = pygame.mouse.get_pos()
                if self.ptr_in_border(pos) ==  1:
                    return_data = (1,pos[0],pos[1])
                else:
                    #������Ч����Ϊ̧���˲���Ƶ��˱߽�֮��
                    pass

        return return_data

    def ptr_in_border(self,pos):
        if (self.border_x[0] - 4) <= pos[0] <= (self.border_x[1] + 4) and \
                (self.border_y[0] - 4) <= pos[1] <= (self.border_y[1] + 4 ):
            return 1
        else:
            return 0
