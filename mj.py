import numpy as np
import pandas as pd
#import shanten

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

            while not(selt.taku.yama.empty):
                #ツモ
                self.tsumo()
                
                #ツモアガリ
                self.agari()
                
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
    
    #勝利プレイヤーを渡す。点数計算もここで行う
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
        if self.virtual:
            if self.players[0].shanten() == -1 and not(self.players[0].friten()):
                pass
        else:
            pass
    
    def dahai(self):
        if self.virtual:
            pass
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
            if self.winners[-1]==5 and self.oya().shanten() != 0:
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
        elif self.winners[-1] == 5 and self.oya().shanten() == 0:
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
        self.tehai = []
        self.nakihai = []
        self.naki = 0
        self.kawa = []
        self.cha = cha
        self.score = 20000
        self.riti = False
        self.is_cpu = False
        
    def cha_update(self):
        self.cha = {'E':'S','S':'W','W':'N','N':'E'}[self.cha]
    
    def next_game(self):
        self.tehai = []
        self.kawa = []
        
    # 0で聴牌。-1でアガリ
    def shanten(self):
        kokusi = 10; titoi=10; normal=10 
        return min(kokusi,titoi,normal)
    
    def 

    def friten(self):
        return False
