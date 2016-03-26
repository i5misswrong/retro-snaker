﻿"wuziqi core"
import time
from random import randint
from threading import Thread
from time import sleep
from copy import deepcopy

__author__ = "caoliang"
class Tree():
    def __init__(self, score = 0, pos = (-1,-1), ly = 0):
        self.score = score
        self.pos = pos
        self.ptr_sum = 0
        self.ptr = []
        self.layer = ly

    def add(self,pointer):
        self.ptr_sum = self.ptr_sum + 1
        pointer.layer = self.layer + 1
        self.ptr.append(pointer)

    def show(self):
        print("当前有：",self.ptr_sum,"个子节点")

    def find_ele(self,pos):
        for i in self.ptr:
            if pos == i.pos:
                return 1
        return 0



    def delete(self,ele):
        self.ptr_sum = self.ptr_sum - 1
        self.ptr.remove(ele)

def show_all(tr):
    print("layer: ",tr.layer,"score: ",tr.score,"pos: ",tr.pos)
    if tr.ptr_sum != 0:
        print('\n')
        for i in tr.ptr:
            show_all(i)

def show_layer(tr,ly):
    if tr.layer == ly:
        print("layer: ",tr.layer,"score: ",tr.score,"pos: ",tr.pos)
    if tr.ptr_sum != 0:
        for i in tr.ptr:
            show_layer(i,ly)

def copy_tree(new_tr,tr):
    for i in tr.ptr:
        new_tr.add(i)

def cut_branch_pl(new_tr,tr):
    li = []

    for i in tr.ptr:
        li = li + [i.score]            
    li.sort()    
    best_level = li[0]
    for i in tr.ptr:
        if i.score <= best_level:
            new_tr.add(i)

def cut_branch_pc(new_tr,tr):
    li = []

    for i in tr.ptr:
        li = li + [i.score] 
                   
    li.sort()
    li.reverse()

    valid_step = len(li) - 1
    if valid_step > 8:
        valid_step = 8

    best_level = li[valid_step]
    for i in tr.ptr:
        if i.score >= best_level:
            new_tr.add(i)
    

    #计算每一个子树的分值
def cal_sub(tr):
    if tr.ptr_sum == 0 :
        return tr.score
    else:
        score = tr.score
        for i in tr.ptr:
            score = score + cal_sub(i) 
        return score

    #寻找tr 所有子树中最大的一支,并弹出该子树
def cal_max_branch(tr):
    if tr.ptr_sum == 0:
        return tr
    else:
        max_score = -9000000     

        for i in tr.ptr:
            new_score = cal_sub(i)

            #统计最大值
            if new_score > max_score:
                max_score = new_score
                best_ptr = i                

        return best_ptr

class Core():
    def __init__(self,order):

        #棋盘：0为空位，1为玩家落子，2为电脑落子
        self.table   = [([0] * 15) for i in range(15)]

        self.busy        = 0
        self.who_win     = 0  

        #行棋的记录
        self.index   = 0
        self.step    = [([0] * 2) for i in range(226)]

        #上一步行棋在4个方向上的其他棋子数
        self.last_pcs_dirction   = [0,0,0,0]

        #评分表
        self.table_type =['aaaaa',
                          '?aaaa?',
                          'aaaa?',
                          'aaa?a',
                          'aa?aa',
                          '??aaa??',
                          'aaa??',
                          '?a?aa?',
                          'a??aa',
                          'a?a?a',
                          '???aa???',
                          'aa???',
                          '??a?a??',
                          '?a??a?']
        self.table_score=[8000000,
                          300000,
                          2500,
                          3000,
                          2600,
                          3000,
                          500,
                          800,
                          600,
                          550,
                          650,
                          150,
                          250,
                          200]  
        

    def player_take(self,pos = (0,0)):

        if self.table[pos[0]][pos[1]] == 0:
            self.table[pos[0]][pos[1]] = 1
            
            self.index = self.index + 1
            self.step[self.index] = pos

            self.test_player()
            if self.who_win == 0:
                self.computer_ctl()    
    
    #电脑走棋控制函数
    def computer_ctl(self):
        if self.busy == 0 :
            self.busy = 1
            if self.index<2:
                task = Thread(target=self.computer_take_first,args=(0,))
            else:
                task = Thread(target=self.computer_take,args=(0,))
            task.start()
            return 1
        return 0

    def computer_take_first(self,tmp):
        sleep(0.6)
        if self.index == 0:
            self.table[7][7] == 2
            self.index = self.index + 1
            self.step[self.index] = (7,7)

        elif self.index == 1:
            tab_map = [[0,-1],[0,1],[-1,0],[1,0],
                       [1,-1],[1,1],[-1,-1],[-1,1]]

            if self.step[1] == (7,7):                
                x,y = tab_map[randint(0,7)]
                self.table[7+x][7+y] = 2
                self.index = self.index + 1
                self.step[self.index] = (7+x,7+y)
                
            else:
                x , y = self.step[self.index]
                x = x - 7
                y = y - 7
                if x > 0:
                    x = 1
                if x < 0:
                    x = -1
                if y > 0:
                    y = 1
                if y < 0:
                    y = -1

                x = self.step[self.index][0]-x
                y = self.step[self.index][1]-y

                self.table[x][y] = 2
                self.index = self.index + 1
                self.step[self.index] = (x,y)
                
        else:
            print("Error! self.index out of range !")
        
        self.busy = 0
    
    def computer_take(self,tmp):

        top_map = Tree()
        self.com_tree(self.table,top_map,2,2,True)

        '''
        for i in top_map.ptr:
            print('\n')
            print("**** ",i.pos," **** ",i.score ," ****")
            show_layer(i,2)
        for i in top_map.ptr:
            print("\n\n add_score:",i.pos,cal_sub(i))
        '''
        x,y = self.search(top_map)

        self.table[x][y] = 2
        self.index = self.index + 1
        self.step[self.index] = [x,y]

        self.test_computer()
        self.busy = 0
    
    #填写树 order 代表接下来执棋的顺序 2：电脑  1：玩家
    def com_tree(self,table,top_map,order = 2,depth = 1,first=False):

        temp_root = Tree()

        for j in range(15):
            for i in range(15):
                if table[i][j] == 0:
                    score = self.cal_single_pcs_value(table,[i,j],order)
                    if score != 0:
                        if order == 1 :
                            score = -1 *score
                        node = Tree(score,(i,j))
                        temp_root.add(node)
        
        #自己这边的棋盘，价值大于0的落子点已经填入到树中
        #接下来把对对方有利的落子点，也添加到这里
        if order == 2:
            for j in range(15):
                for i in range(15):
                    if table[i][j] == 0:
                        score = self.cal_single_pcs_value(table,[i,j],1)
                        if score != 0 and temp_root.find_ele((i,j))==0:
                            node = Tree(0,(i,j))
                            temp_root.add(node)
        
            copy_tree(top_map,temp_root)
            #cut_branch_pc(top_map,temp_root)
        else:
            cut_branch_pl(top_map,temp_root)
                        
        #剪枝完毕，确认是否要进行下一次迭代
        dep = depth - 1
        if dep > 0:
            for i in top_map.ptr:
                tab = deepcopy(table)
                x,y = i.pos
                tab[x][y] = order
                if order == 2:
                    self.com_tree(tab,i,1,dep)
                else:
                    self.com_tree(tab,i,2,dep)

    def search(self,top_map):
        return cal_max_branch(top_map).pos
            
    def cal_sum_arround(self,table=[],pos = (0,0),key = 1):

        x,y = pos
        five_p = [0,0,0,0, 0,0,0,0]

        #判断 8个方向上的棋子数

        for i in range(1,5):
            if (x-i)> -1 and table[x-i][y] == key:
                five_p[0] = five_p[0] + 1
            else:
                break

        for i in range(1,5):
            if (x-i)>-1 and (y-i)>-1 and table[x-i][y-i] == key:
                five_p[1] = five_p[1] + 1
            else:
                break

        for i in range(1,5):
            if (y-i)>-1 and table[x][y-i] == key:
                five_p[2] = five_p[2] + 1
            else:
                break

        for i in range(1,5):
            if (x+i)<15 and (y-i)>-1 and table[x+i][y-i] == key:
                five_p[3] = five_p[3] + 1
            else:
                break

        for i in range(1,5):
            if (x+i)<15 and table[x+i][y] == key:
                five_p[4] = five_p[4] + 1
            else:
                break

        for i in range(1,5):
            if (x+i)<15 and (y+i)<15 and table[x+i][y+i] == key:
                five_p[5] = five_p[5] + 1
            else:
                break

        for i in range(1,5):
            if (y+i)<15 and table[x][y+i] == key:
                five_p[6] = five_p[6] + 1
            else:
                break
        for i in range(1,5):
            if (x-i)>-1 and (y+i)<15 and table[x-i][y+i] == key:
                five_p[7] = five_p[7] + 1
            else:
                break
        #--------------------------------------#
        dir=[0,0,0,0]
        for i in range(4):
            dir[i] = five_p[i] + five_p[i+4]
        return dir

    def test_player(self):
        self.last_pcs_dirction = self.cal_sum_arround(self.table,self.step[self.index])
        for i in range(4):
            if self.last_pcs_dirction[i] >=4:
                self.who_win = 1 
                break

    def test_computer(self):
        self.last_pcs_dirction = self.cal_sum_arround(self.table,self.step[self.index],2)
        for i in range(4):
            if self.last_pcs_dirction[i] >=4:
                self.who_win = 2 
                break

    def get_chess_type(self,table=[],pos = (0,0),key = 1):
        x,y = pos
        chess_type = ['' for i in range(8)]

        #判断 8个方向上的棋子数
        for i in range(1,5):
            if (x-i) < 0:
                break                
            elif table[x-i][y] == key :
                chess_type[0] = chess_type[0] + 'a'
            elif table[x-i][y] == 0 :
                chess_type[0] = chess_type[0] + '?'
            else:
                break

        for i in range(1,5):
            if (x-i) < 0 or  (y-i) < 0:
                break
            elif table[x-i][y-i] == key :
                chess_type[1] = chess_type[1] + 'a'
            elif table[x-i][y-i] == 0 :
                chess_type[1] = chess_type[1] + '?'
            else:
                break

        for i in range(1,5):
            if (y-i) < 0 :
                break
            elif table[x][y-i] == key :
                chess_type[2] = chess_type[2] + 'a'
            elif table[x][y-i] == 0 :
                chess_type[2] = chess_type[2] + '?'
            else:
                break

        for i in range(1,5):
            if (x+i)>14 or (y-i) < 0 :
                break
            elif table[x+i][y-i] == key :
                chess_type[3] = chess_type[3] + 'a'
            elif table[x+i][y-i]  == 0 :
                chess_type[3] = chess_type[3] + '?'
            else:
                break
        # 后4个方向

        for i in range(1,5):
            if (x+i)>14:
                break
            elif table[x+i][y] == key :
                chess_type[4] = chess_type[4] + 'a'
            elif table[x+i][y] == 0 :
                chess_type[4] = chess_type[4] + '?'
            else:
                break

        for i in range(1,5):
            if (x+i)>14 or (y+i)>14:
                break
            elif table[x+i][y+i] == key:
               chess_type[5] = chess_type[5] + 'a'
            elif table[x+i][y+i] == 0:
               chess_type[5] = chess_type[5] + '?'
            else:
                break

        for i in range(1,5):
            if (y+i)>14:
                break
            elif table[x][y+i] == key:
                chess_type[6] = chess_type[6] + 'a' 
            elif table[x][y+i] == 0:
                chess_type[6] = chess_type[6] + '?'
            else:
                break
        for i in range(1,5):
            if (x-i)<0 or (y+i)>14:
                break
            elif table[x-i][y+i] == key:
                chess_type[7] = chess_type[7] + 'a'
            elif table[x-i][y+i] == 0:
                chess_type[7] = chess_type[7] + '?'
            else:
                break
        #--------------------------------------#
        chess_type_4_dir = ['' for i in range(4)]
        
        for i in range(4):
            chess_type_4_dir[i] = chess_type[i][::-1] + 'a' + chess_type[i+4]
        return chess_type_4_dir

    def cal_single_pcs_value(self,table=[],pos = (0,0),key = 1):
        pcs_type = self.get_chess_type(table,pos,key)
        score = 0
        for i in range(4):
            for j in range(14):
                if pcs_type[i].find(self.table_type[j]) > -1 or \
                    pcs_type[i].find(self.table_type[j][::-1]) > -1:
                    score = score + self.table_score[j]
        return score

    def cal_single_pcs_value_debug(self,table=[],pos = (0,0),key = 1):
        pcs_type = self.get_chess_type(table,pos,key)
        print("pcs_type: ",pcs_type)
        score = 0
        for i in range(4):
            for j in range(14):
                if pcs_type[i].find(self.table_type[j]) > -1 or \
                    pcs_type[i].find(self.table_type[j][::-1]) > -1:
                    print(self.table_type[j])
                    score = score + self.table_score[j]
        print(score)
        return score


def test():
    print("core is running !")

if __name__=='__main__':
    test()
