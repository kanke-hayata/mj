"""
或る牌種においてそれのみの面子の数対子の数塔子の数を格納したハッシュテーブルの作成
待ち牌が既に４枚出ていて現実には聴牌ではないときのことは考慮していない
それは別で計算する
"""
import numpy as np
import sys

sys.setrecursionlimit(100)

def goshinsuu(n):
    ans = 0
    for i in range(8):
        d = int(n/(5**(8-i)))
        ans = ans*10 + d
        n -= d*(5**(8-i))
    ans = ans*10 + n
    ans = str(ans)
    for i in range(9-len(ans)):
        ans = '0' + ans
    return np.array(list(map(int, list(ans))))

"""
 手牌と面子のリストを渡すとその手牌で最大の面子数を教えてくれる
 最終的にはシャン点数を教えてくれるところまでが目標になっている。がそもそもどの組み合わせで与えられるかも教えないと意味ないのではと思ってしまう
必要なのは各牌種の面子の数。面子候補の数。そこから引けたら面子をさらに引く感じでやっていく
シャン点数とそれを実現する組み合わせを返すことにしようかと思っている
関数ではシャン点数も返さないと再起が回せなくなってしまっていると予想
ex) [[[000,123,333],[]],[]]
手事に具体的な面子候補、それで余った中からターツを抜く感じでやる
結局今持っている手牌をどのように分解するのかが大きな分かれ道になっている気がする
この関数では先に面子に分解してそれのリスト、雀頭作るときの雀頭とターツ。作らないときのターツで分けるとよしかもしれん
"""

#その手牌での面子数と具体的な面子を返してくれる関数
"""
def mentsu_n(tehai, mentsu):
    print(tehai)
    if np.any(tehai<=-1):
        return -1
    tmp = []
    for i in range(len(mentsu)):
        tehai[mentsu[i][0]] -=1 
        tehai[mentsu[i][1]] -=1 
        tehai[mentsu[i][2]] -=1
        #その面子を引いてみた上での面子数
        tmp.append(mentsu_n(tehai, mentsu))
        tehai[mentsu[i][0]] +=1 
        tehai[mentsu[i][1]] +=1 
        tehai[mentsu[i][2]] +=1
    return max(tmp) + 1
"""
#その手牌での面子数と具体的な面子を返してくれる関数
# [2,[]]
def mentsu_n(tehai, mentsu):
    tmp = [-1]
    men = [[]]
    for i in range(len(mentsu)):
        tehai[mentsu[i][0]] -=1 
        tehai[mentsu[i][1]] -=1 
        tehai[mentsu[i][2]] -=1
        if np.any(tehai<=-1):
            tehai[mentsu[i][0]] +=1 
            tehai[mentsu[i][1]] +=1 
            tehai[mentsu[i][2]] +=1
        else:
            ans = mentsu_n(tehai, mentsu)
            ans[1].append(mentsu[i])
            tmp.append(ans[0])
            men.append(ans[1])
            tehai[mentsu[i][0]] +=1 
            tehai[mentsu[i][1]] +=1 
            tehai[mentsu[i][2]] +=1
    return [max(tmp)+1,men[np.argmax(tmp)]]

def tatsu_n(tehai, tatsu):
    tmp = [-1]
    ta = [[]]
    for i in range(len(tatsu)):
        tehai[tatsu[i][0]] -=1 
        tehai[tatsu[i][1]] -=1 
        if np.any(tehai<=-1):
            tehai[tatsu[i][0]] +=1 
            tehai[tatsu[i][1]] +=1 
        else:
            ans = tatsu_n(tehai, tatsu)
            ans[1].append(tatsu[i])
            tmp.append(ans[0])
            ta.append(ans[1])
            tehai[tatsu[i][0]] +=1 
            tehai[tatsu[i][1]] +=1 
    return [max(tmp)+1,ta[np.argmax(tmp)]]

"""
def toitsu_n(tehai, tatsu, toitsu):
    tmp = [-1]
    ta = [[]]
    for i in range(len(toitsu)):
        tehai[toitsu[i][0]] -= 1
        tehai[toitsu[i][1]] -= 1
        if np.any(tehai<=-1):
            tehai[toitsu[i][0]] +=1
            tehai[toitsu[i][1]] +=1
        else:
            ans = tatsu_n(tehai, tatsu)
            ans[1].append(toitsu[i])
            tmp.append(ans[0])
            ta.append(ans[1])
            tehai[toitsu[i][0]] +=1
            tehai[toitsu[i][1]] +=1
    return [max(tmp)+1,ta[np.argmax(tmp)]]
"""

f = open('./shanten.py', mode='w')
f.write('table = [')
for i in range(5**9):
    print(i)
    tehai = goshinsuu(i)
    mentsu = []
    tatsu = []
    toitsu = []
    ans = []
    a = [0,[]]
    b = [0,[]]
    c = [0,[]]
    if sum(tehai) >= 15:
        f.write('0,')
        #f.write('[[0,[]],[0,[]],[0,[]]],') #メモリ削減のため
    else:
        # 面子の発見
        for j in [k for k in range(7) if tehai[k]>=1 and tehai[k+1]>=1 and tehai[k+2]>=1]:
            mentsu = mentsu + [[j,j+1,j+2]]
        for j in [k for k,x in enumerate(tehai) if x >=3]:
            mentsu = mentsu + [[j,j,j]]
        if len(mentsu) > 0:
            a = mentsu_n(tehai,mentsu)
            #面子を引いた中から探すので前処理
            for i in range(len(a[1])):
                tehai[a[1][i][0]] -= 1
                tehai[a[1][i][1]] -= 1
                tehai[a[1][i][2]] -= 1
        ans.append(a)
       #ターツ（ついでに対子）の発見 
        for j in [k for k,x in enumerate(tehai) if x >=2]:
            tatsu = tatsu + [[j,j]]
            toitsu = toitsu + [[j,j]]
        for j in [k for k in range(8) if tehai[k]>=1 and tehai[k+1]>=1]:
            tatsu = [[j,j+1]] + tatsu
            toitsu  = toitsu + [[j,j+1]]
        if len(tatsu) > 0:
            b = tatsu_n(tehai, tatsu)
        ans.append(b)
        if len(toitsu) > 0:
            c = tatsu_n(tehai, toitsu)
        ans.append(c)
        f.write(str(ans)+',')
f.write(']')
f.close

