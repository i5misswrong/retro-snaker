"wuziqi core"
import time
from random import randint
__author__ = "caoliang"

class Core():
    def __init__(self):
        self.five_pieces = [([0] * 2) for i in range(9)]
        self.table = [([0] * 15) for i in range(15)]
        self.computer = [([0] * 15) for i in range(15)]
        self.player = [([0] * 15) for i in range(15)]
        self.computer_last = [0,0]
        self.player_last = [0,0]
        self.last = [-1,-1]
        self.busy = 0
        self.who_win = 0
        for i in range(15):
            for j in range(15):
                self.computer[i][j]=[0]*4
        for i in range(15):
            for j in range(15):
                self.player[i][j]=[0]*4
    def calNext(self,data):
        self.busy = 1
        self.analysisTable()
        self.computerTakeStep()
        self.busy = 0
        
    #分析棋盘
    def analysisTable(self):
        for i in range(15):
            for j in range(15):     #j为行
                if self.table[i][j] == 0:   #分析每一个空格，四个方向上落子的价值
                    single_pos = (i,j)                    
                    sum = [0,0,0,0]; #横，竖，左斜，右斜
                    sum[0] = self.analysisSingleDirCross(single_pos)
                    sum[1] = self.analysisSingleDirVertical(single_pos)
                    sum[2] = self.analysisSingleDirLeftbevel(single_pos) #\
                    sum[3] = self.analysisSingleDirRightbevel(single_pos)#/
                    self.computer[i][j] = sum
    def analysisSingleDirCross(self,pos,mod = 0 , pl_or_pc = 1):
        sum = mod        
        colu = pos[0]
        line = pos[1]
        while True:
            line -= 1
            if line == -1:
                break
            else:
                if self.table[colu][line] == pl_or_pc:
                    self.five_pieces[sum] = [colu,line]
                    sum += 1

                else:
                    break
        colu = pos[0]
        line = pos[1]        
        while True:
            line += 1
            if line==15:
                break
            else:
                if self.table[colu][line] == pl_or_pc:
                    self.five_pieces[sum] = [colu,line]
                    sum += 1
                else:
                    break
        return sum
    def analysisSingleDirVertical(self,pos,mod = 0 , pl_or_pc = 1):
        sum = mod        
        colu = pos[0]
        line = pos[1]
        while True:
            colu -= 1
            if colu == -1:
                break
            else:
                if self.table[colu][line] == pl_or_pc:
                    self.five_pieces[sum] = [colu,line]
                    sum += 1
                else:
                    break        
        colu = pos[0]
        line = pos[1]
        while True:
            colu += 1
            if colu==15:
                break
            else:
                if self.table[colu][line] == pl_or_pc:
                    self.five_pieces[sum] = [colu,line]
                    sum += 1
                else:
                    break
        return sum
    def analysisSingleDirLeftbevel(self,pos,mod = 0 , pl_or_pc = 1):
        sum = mod
        colu = pos[0]
        line = pos[1]
        while True:
            colu -= 1
            line -= 1
            if colu == -1 or line == -1:
                break
            else:
                if self.table[colu][line] == pl_or_pc:
                    self.five_pieces[sum] = [colu,line]
                    sum += 1
                else:
                    break
        colu = pos[0]
        line = pos[1]        
        while True:
            colu += 1
            line += 1
            if colu == 15 or line == 15:
                break
            else:
                if self.table[colu][line] == pl_or_pc:
                    self.five_pieces[sum] = [colu,line]
                    sum += 1
                else:
                    break
        return sum
    def analysisSingleDirRightbevel(self,pos,mod = 0 , pl_or_pc = 1):
        sum = mod
        colu = pos[0]
        line = pos[1]
        while True:
            colu -= 1
            line += 1
            if colu == -1 or line == 15:
                break
            else:
                if self.table[colu][line] == pl_or_pc:
                    self.five_pieces[sum] = [colu,line]
                    sum += 1
                else:
                    break
        colu = pos[0]
        line = pos[1]        
        while True:
            colu += 1
            line -= 1
            if colu == 15 or line == -1:
                break
            else:
                if self.table[colu][line] == pl_or_pc:
                    self.five_pieces[sum] = [colu,line]
                    sum += 1
                else:
                    break
        return sum

    def playerTakeStep(self,pos):
        i = pos[0]
        j = pos[1]
        if self.table[i][j] == 0:
            self.table[i][j] = 2
            self.player_last = [i,j]
            self.last = self.player_last
            return_data = 1
        else:
            return_data = 0
        self.playerCheckWin()
        return return_data
    def computerTakeStep(self):
        time.sleep(1)
        point_x = 0
        point_y = 0
        sum = 0
        for i in range(15):
            for j in range(15):
                for k in range(4):
                    if self.computer[i][j][k] > sum:
                        sum = self.computer[i][j][k]
                        point_x = i
                        point_y = j
        if sum == 0:
            point_x = randint(0,14)
            point_y = randint(0,14)

        if self.table[point_x][point_y] != 0:
            self.computer[point_x][point_y]=[0,0,0,0]
            self.computerTakeStep()
        else:
            self.table[point_x][point_y] = 1
            self.computer_last = [point_x,point_y]
        self.last = self.computer_last
        self.computerCheckWin()

    def playerCheckWin(self):
        sum = [0,0,0,0]
        #check player:
        sum[0] = self.analysisSingleDirCross(self.player_last,1,2)
        sum[1] = self.analysisSingleDirVertical(self.player_last,1,2)
        sum[2] = self.analysisSingleDirLeftbevel(self.player_last,1,2)
        sum[3] = self.analysisSingleDirRightbevel(self.player_last,1,2)
        for i in range(4):
            if sum[i] > 4:
                self.who_win = 2
    def computerCheckWin(self):
        sum = [0,0,0,0]
        #check computer:
        sum[0] = self.analysisSingleDirCross(self.computer_last,1,1)
        sum[1] = self.analysisSingleDirVertical(self.computer_last,1,1)
        sum[2] = self.analysisSingleDirLeftbevel(self.computer_last,1,1)
        sum[3] = self.analysisSingleDirRightbevel(self.computer_last,1,1)
        for i in range(4):
            if sum[i] > 4:
                self.who_win = 1
    def getWhoWin(self):
        return self.who_win
    def calWhere(self,dir):
        if dir == 0:
            pass
        elif dir == 1:
            pass
        elif dir == 2:
            pass
        else :
            pass

def test():
    print("core is running !")

if __name__=='__main__':
    test()