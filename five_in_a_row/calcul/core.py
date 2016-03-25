"wuziqi core"
import time
from random import randint
from threading import Thread
from time import sleep

__author__ = "caoliang"

class Core():
    def __init__(self):

        #棋盘：0为空位，1为玩家落子，2为电脑落子
        self.table   = [([0] * 15) for i in range(15)]

        self.busy        = 0
        self.who_win     = 0  

        #上一步行棋的位置
        self.last        = [-1,-1]

        #上一步行棋在4个方向上的其他棋子数
        self.last_pcs_dirction   = [0,0,0,0]
        self.five_pcs = [([0] * 2) for i in range(5)]

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
            self.last = pos
            self.test_player()
            return 1
        return 0

    def computer_take(self):
        if self.busy == 0 :
            self.busy = 1
            task = Thread(target=self.computer_cal,args=(0,))
            task.start()
            return 1
        return 0
    def computer_cal(self,tmp):
        x = 0
        y = 0
        old_score = 0

        for j in range(15):
            for i in range(15):
                if self.table[i][j] == 0:
                    new_score = self.cal_single_pcs_value(self.table,[i,j],2)
                    if  new_score > old_score:
                        x=i
                        y=j
                        old_score = new_score

        if old_score == 0:
            while True:
                x = randint(5,11)
                y = randint(5,11)
                if self.table[x][y]==0:
                    print("!",x,y)
                    break
        self.cal_single_pcs_value_debug(self.table,(x,y),2)       
        self.table[x][y] = 2
        self.last = [x,y]
        self.test_computer()
        self.busy = 0

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
        self.last_pcs_dirction = self.cal_sum_arround(self.table,self.last)
        for i in range(4):
            if self.last_pcs_dirction[i] >=4:
                self.who_win = 1 
                break

    def test_computer(self):
        self.last_pcs_dirction = self.cal_sum_arround(self.table,self.last,2)
        for i in range(4):
            if self.last_pcs_dirction[i] >=4:
                self.who_win = 2 
                break

    def get_chess_type(self,table=[],pos = (0,0),key = 1):
        x,y = pos
        chess_type = ['' for i in range(8)]

        #判断 8个方向上的棋子数
        for i in range(1,15):
            if (x-i) < 0:
                break                
            elif table[x-i][y] == key :
                chess_type[0] = chess_type[0] + 'a'
            elif table[x-i][y] == 0 :
                chess_type[0] = chess_type[0] + '?'
            else:
                break

        for i in range(1,15):
            if (x-i) < 0 or  y-i < 0:
                break
            elif table[x-i][y-i] == key :
                chess_type[1] = chess_type[1] + 'a'
            elif table[x-i][y-i] == 0 :
                chess_type[1] = chess_type[1] + '?'
            else:
                break

        for i in range(1,15):
            if (y-i) < 0 :
                break
            elif table[x][y-i] == key :
                chess_type[2] = chess_type[2] + 'a'
            elif table[x][y-i] == 0 :
                chess_type[2] = chess_type[2] + '?'
            else:
                break

        for i in range(1,15):
            if (x+i)>14 or (y-i) < 0 :
                break
            elif table[x+i][y-i] == key :
                chess_type[3] = chess_type[3] + 'a'
            elif table[x+i][y-i]  == 0 :
                chess_type[3] = chess_type[3] + '?'
            else:
                break
        # 后4个方向

        for i in range(1,15):
            if (x+i)>14:
                break
            elif table[x+i][y] == key :
                chess_type[4] = chess_type[4] + 'a'
            elif table[x+i][y] == 0 :
                chess_type[4] = chess_type[4] + '?'
            else:
                break

        for i in range(1,15):
            if (x+i)>14 or (y+i)>14:
                break
            elif table[x+i][y+i] == key:
               chess_type[5] = chess_type[5] + 'a'
            elif table[x+i][y+i] == 0:
               chess_type[5] = chess_type[5] + '?'
            else:
                break

        for i in range(1,15):
            if (y+i)>14:
                break
            elif table[x][y+i] == key:
                chess_type[6] = chess_type[6] + 'a' 
            elif table[x][y+i] == 0:
                chess_type[6] = chess_type[6] + '?'
            else:
                break
        for i in range(1,15):
            if (x-i)<0 or (y+i)>14:
                break
            elif table[x-i][y+i] == key:
                chess_type[7] = chess_type[7] + 'a'
            elif table:
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
