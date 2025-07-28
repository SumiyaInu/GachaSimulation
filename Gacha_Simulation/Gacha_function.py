import random
import numpy as np
from math import ceil,floor


#M人がN回抽選、天井なし
def gacha(times=None, pool=None, prob=None):
    #抽選回数、ラインナップのデータと確率のデフォルト値
    if times is None:
        times = 100
    if pool is None:
        pool = ["N", "R", "SR", "UR"]
    if prob is None:
        prob = [0.55, 0.35, 0.075, 0.025]

    bag=[]
    array_pool = np.array(pool)
    array_prob=np.array(prob)


    gacha = np.random.choice(array_pool,size=times,replace=True,p=array_prob)
        #np.random.choice(抽選されるリストまたはマトリックス,size=(抽選人数,抽選回数),replace=重複できるかどうか（True=可，False=不可）,p=確率モジュール)
        #sizeに入った要素数により、生成された配列の次元数が異なります。この例では二次元配列になります
    bag.extend(gacha)
        #ベクトル化したbagを一度リストにしてextendを執行する
        #extend:リストに全ての要素を追加する / append:1つずつに追加する
    
    return bag

#M人がUR出るまでの回数、天井なし
def gacha_Until_Target(pool=None, prob=None):
    #ラインナップのデータと確率のデフォルト値
    if pool is None:
        pool = ["N", "R", "SR", "UR"]
    if prob is None:
        prob = [0.55, 0.35, 0.075, 0.025]


    bag=[]
    array_pool = np.array(pool)
    array_prob=np.array(prob)

    cnt = 0 
    while True:
        gacha = np.random.choice(array_pool,p=array_prob)
        cnt +=1
        if gacha == pool[-1]:
            bag.append(cnt)
            return cnt
        else :
            continue
    return cnt 


#M人がN回抽選、天井あり
def gacha_Pity(times=None, pool=None, prob=None):
    #抽選回数、ラインナップのデータと確率のデフォルト値
    if times is None:
        times = 100
    if pool is None:
        pool = ["N", "R", "SR", "UR"]
    if prob is None:
        prob = prob = [0.55, 0.35, 0.075, 0.025]

    array_pool = np.array(pool)
    array_prob=np.array(prob)
    # print(f"天井数は{floor(1/array_prob[-1]*2)}回です。")#天井数を表示
    pity=floor(1/array_prob[-1]*2)#天井は期待値2倍のガチャ回数に設定する


    gacha = np.random.choice(array_pool,size=times,replace=True,p=array_prob)
    if  np.sum(gacha==pool[-1]) < floor(times/pity) :#天井越えても引いたUR枚数0なら、1にする
        for i in range(floor(times/pity)):#回数分のループ、例：天井2倍の回数ガチャしてURが2枚以下だったら2枚にする
            nur_idx =np.where(gacha != pool[-1])[0]#UR以外のインデックスを取得
            rmv_idx = np.random.choice(nur_idx)#UR以外のインデックスからランダムに1つ選ぶ
            gacha[rmv_idx] = pool[-1]

    return gacha
        


#M人がUR出るまでの回数、天井あり
def gacha_Until_Target_Pity( pool=None, prob=None):
    #ラインナップのデータと確率のデフォルト値
    if pool is None:
        pool = ["N", "R", "SR", "UR"]
    if prob is None:
        prob = prob = [0.55, 0.35, 0.075, 0.025]



    array_pool = np.array(pool)
    array_prob=np.array(prob)
    pity = (1/array_prob[-1])*2 #天井数が期待値の2倍に設定する

    cnt = 0 
    while True:
        gacha = np.random.choice(array_pool,p=array_prob)   
        cnt +=1
        if gacha == pool[-1]:
            return cnt
        elif cnt >= pity :#天井数までカウントされたら、強制的に天井数を記入する
            return int(pity)



