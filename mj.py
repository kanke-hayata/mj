import numpy as np
import pandas as pd
import shanten

class Game:
    def __init__(self,virtual=True):
        if virtual: 
            self.player1 = Player(1,'E');self.player2 = Player(2,'S');self.player3 = Player(3,'W');self.player4 = Player(4,'N')
            self.players = [self.player1,self.player2,self.player3,self.player4]
            self.taku = Taku()
        else:
            pass
        #勝者を1,2,3,4,5で格納していく。5は流局
        self.winners = []
        self.virtual = virtual
        
    def start_game(self):
    
        if self.virtual:

            self.haipai()
            
            flag = False
            while not(selt.taku.yama.empty):
                #ツモ
                self.tsumo()
                
                #ツモアガリ
                if self.agari():
                    break

                #暗槓
                self.ankan()

                #打牌
                self.dahai()
                
                #ロン
                self.ron()
                
                #他家の鳴き
                self.naki()
                            
                # ここで次のツモの人に更新
                self.players = self.players[1:] + self.players[:1]
        
        else:
            while True:
                action = input()
                if action == 'pon':
                    pass
                # それ以外の場合は打牌だと言える
                else:
                    pass
            
        self.end_game()
    
    #勝利プレイヤーをwinnerslistの最後としてidで渡す。点数計算もここで行う
    def end_game(self):
        #点数計算 
        self.calculate()
        
        #game-setの判定をする 完成
        if self.game_set():
            self.result()
            return
        
        #連荘処理 完成
        self.renchan()
        
        #親をplayersの先頭にする処理
        self.players = self.players[self.players.index(self.oya()):] + self.players[:self.players.index(self.oya())]
        for p in self.players:
            p.next_game()
        self.taku.next_game()
        
        self.start_game()
    
    #王牌、ドラの処理もここでおこなう
    def haipai(self):
        if self.virtual:       
            for p in self.players:                                                              
                p.tehai = self.taku.yama[:13]
                self.taku.yama = self.taku.yama[13:]
            # 王牌の確保
            self.taku.wanpai = self.taku.yama[:14]
            self.taku.yama = self.taku.yama[14:]
            # ドラ
            self.taku.add_dora()
        else:
            return
        
    def tsumo(self):
        if self.virtual:
            self.players[0].tehai = pd.concat([self.players[0].tehai,self.taku.yama[:1]])
        else:
            pass
        
    def agari(self):
        if self.players[0].is_cpu:
            pass
        else:
            if self.virtual:
                if self.players[0].shanten()[0] == -1 and not(self.players[0].friten()):
                    while True:
                        print('agaru? yes/no')
                        if input() == 'yes':
                            self.winners.append(self.players[0].id)
                            return True
                        elif input() == 'no':
                            return False
                else:
                    return False
            else:
                pass
    
    def ankan(self):
        if self.players[0].is_cpu:
            pass:
        else:
            if self.virtual:
                if self.players[0].tehai.last(1).values[0] in self.players[0].tehai.value_counts()[self.players[0].tehai.value_counts()==4]:
                    while True:
                        print('ankansuru? yes/no')
                        if input() == 'yes':
                            self.
                            break
                        elif input() == 'no':
                            break
            else:
                pass

    def dahai(self):
        if self.players[0].is_cpu:
            pass
        else:
            if self.virtual:
                print(self.players[0].tehai)
                print('select sutehai by id')
                while True:
                    sutehai = self.players[0].tehai[self.players[0].tehai.index == int(input())]
                    if not sutehai.empty and sutehai.index.values[0] not in self.players[0].nakihai.index.values:
                        self.players[0].kawa = pd.concat([self.players[0].kawa,sutehai])
                        break
            else:
                pass
        
    def ron(self):
        if self.virtual:
            pass
        else:
            pass
    
    def naki(self):
        if self.virtual:
            pass
        else:
            pass
            
    #完成
    def game_set(self):
        #東4局
        if self.taku.kyoku == 4:
            #流局していてかつ親が聴牌もしていない
            if self.winners[-1]==5 and self.oya().shanten()[0] != 0:
                return True
            #親以外が勝利
            elif not(self.winners[-1] == self.oya().id):
                return True
            else: 
                return False
        else:
            return False
    
    #完成
    def renchan(self):
        #連荘かどうかによって処理を変える
        if self.winners[-1] == self.oya().id:
            self.taku.renchan +=1 
        elif self.winners[-1] == 5 and self.oya().shanten()[0] == 0:
            self.taku.renchan +=1
        else:
            self.taku.renchan = 0
            self.taku.kyoku += 1
            for p in self.players:
                p.cha_update()
                
    def oya(self):
        for p in self.players:
            if p.cha == self.taku.kaze:
                return p
            
    def player_by_id(self, i):
        for p in self.players:
            if p.id == i:
                return p
            
    def calculate(self):
        return
    
    def result(self):
        for p in players:
            print(p.score)

class Taku:
    def __init__(self):
        #東風戦
        self.kaze = 'E'
        self.yama_init()
        self.renchan = 0
        self.kyoku = 1
        self.dora = []
        self.wanpai = []
        
    def yama_init(self):
        self.yama = []
        for i in ['p','w','s']:
            for j in range(9):
                self.yama.append(str(j+1)+i)
        for i in range(7):
            self.yama.append(str(i+1)+'j')
        self.yama = self.yama*4
        
        self.yama = pd.Series(self.yama).sample(frac=1)

    def next_game(self):
        #self.kaze = {'E':'S','S':'W','W':'N','N':'E'}[self.kaze]
        self.yama_init()
        
    def add_dora(self):
        self.dora.append(self.wanpai[:1].values[0])
        self.wanpai = self.wanpai[1:]

class Player:
    def __init__(self,ID=0,cha=''):
        self.id = ID
        self.tehai = pd.Series([])
        self.nakihai = pd.Series([])
        self.naki = 0
        self.kawa = pd.Series([])
        self.cha = cha
        self.score = 20000
        self.riti = False
        self.is_cpu = False
        
    def cha_update(self):
        self.cha = {'E':'S','S':'W','W':'N','N':'E'}[self.cha]
    
    def next_game(self):
        self.tehai = pd.Series([])
        self.kawa = pd.Series([])
        
    # 0で聴牌。-1でアガリ
    def shanten(self):
        kokushi = 13; titoi=6; normal=8
        
        kokushi_te = self.tehai.isin(['1p','9p','1w','9w','1s','9s','1j','2j','3j','4j','5j','6j','7j'])
        kokushi -= kokushi_te.value_counts().shape[0] + min(1, kokushi_te.value_counts()[kokushi_te.value_counts() >= 2].shape[0])

        titoi -= self.tehai.value_counts()[self.tehai.value_counts() >= 2].shape[0] + max(0,(7-self.tehai.value_counts().shape[0]))

        normal_li = []
        for i in ['p','w','s']:
            ind = 0
            for j in self.tehai[self.tehai.str.contains(i)].values:
                ind += 5**(8-(int(j[0])-1))
            normal_li.append(shanten.table[ind])
        j = self.tehai[self.tehai.str.contains('j')].value_counts()
        men = []; toi = []
        for i in j[j==3].index:
            men.append([i[0],i[0],i[0]])
        for i in j[j==2].index:
            toi.append([i[0],i[0]])
        normal_li.append([[j[j==3].shape[0],men],[j[j==2].shape[0],toi],[j[j==2].shape[0],toi]])

        m = 0;m2 = 0;m3 = 0
        for i in normal_li:
            m += i[0][0]
            m2 += i[2][0]
            if i[2][0] >= 1:
                for j in i[2][1]:
                    if j[0] == j[1]:
                        m3 = 1
        if not(m2 >= (4-m)+1 and m3 == 1):
            m3 = 0
        m2 = min(4-m, m2)
        normal -= 2*m + m2 + m3
        return min(kokushi,titoi,normal), normal_li

    def friten(self):
        if self.tehai.tail(1).values[0] in self.kawa:
            return True
        return False
