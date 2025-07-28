import random
import numpy as np
from collections import Counter #collectionsモジュールを利用しカウンターする
from Gacha_function import gacha_Until_Target
from Gacha_function import gacha_Until_Target_Pity  

print("このプログラムは、スマホゲームのガチャをシミュレーションするものです。\n"
      "ラインナップは N、R、SR、UR の4種類で、確率はそれぞれ 0.55、0.35、0.075、0.025 です。\n"
      "シミュレーションでは、URカードを1枚引き当てるまでの回数を記録し、合計1000人分の試行回数が記録されます。\n"
      "天井の有無を選択できます（天井の初期値は期待値の2倍に設定されています）。\n"
      "各試行について、平均、標準偏差、信頼区間などの統計量を計算し、\n"
      "分布図、箱ひげ図、各プレイヤーの抽選結果（.csv）を出力します。\n"
      "----------------------------------------------------------------------------------------")


#ラインナップ
# pool = list([str(x) for x in input("ラインナップ内容:").split(",")])#["N","R","SR","UR"]
pool = ["N","R","SR","UR"]
array_pool = np.array(pool)


# prob = list([float(x) for x in input("確率係数:").split(",")])

# if sum(prob) != 1:
#     while True:
#         print("確率の合計は1ではない。")
#         prob = list([float(x) for x in input("確率係数:").split(",")])
#         if sum(prob) == 1:
#             break
prob = [0.55,0.35,0.075,0.025]#
array_prob=np.array(prob)

player_num =1000
gacha_counts_until_ur=[]
np.array(gacha_counts_until_ur)

#一枚のURを引いたら止まる、そのガチャ回数を記録する

gacha_mode = input("天井の有無を選択してください。(y/n):").strip().lower()

if gacha_mode == 'n':
    for i in range(1,int(player_num)+1):
        Until_UR_Count = gacha_Until_Target(array_pool,array_prob)
        player_bag={
        'Player':i,
        'Gacha_Count':Until_UR_Count
    }
        gacha_counts_until_ur.append(Until_UR_Count)


elif gacha_mode == 'y':
    print(f"天井数は{int(1/array_prob[-1]*2)}回です")
    for i in range(1,int(player_num)+1):
        Until_UR_Count = gacha_Until_Target_Pity(pool=array_pool, prob=array_prob)
        player_bag={
            'Player':i,
            'Gacha_Count':Until_UR_Count
        }
        gacha_counts_until_ur.append(Until_UR_Count)







#プレイヤーごとにURカードを引きあたるまでのガチャ回数を記録

#基本統計量
#毎回引いた結果は必ず「引きあたる」と「外れ」なので、こういう行為は複数回の「ベルヌーイ試行」であり、
#正規分布より、幾何分布のほうが適切なのです。（データが右偏り、歪度＜-1）
import scipy.stats as stats
import pandas as pd
from math import ceil,floor

print(f"1枚{array_pool[-1]}所要回数の期待値{ceil(round(float(1/array_prob[-1]),1))}\n期待値数のガチャを引いて、URカードを引いた確率は{1-((1-float(array_prob[-1]))**ceil(round(float(1/array_prob[-1]),1))):.2%}")
print(f"最も少ない回数でURを引きあたるプレイヤーは{np.min(gacha_counts_until_ur)}回で引いた\n最も多い回数でURを引きあたるプレイヤーは{np.max(gacha_counts_until_ur)}回で引いた")
print(f"標準偏差：{np.std(gacha_counts_until_ur,ddof=1)},標準誤差{stats.sem(gacha_counts_until_ur)}\n中央値：{np.median(gacha_counts_until_ur)}\n平均：{np.mean(gacha_counts_until_ur)}")

#信頼区間　stats.t.interval(信頼度,自由度,平均,標準誤差) > このデータはタプる
#標準偏差を計算するとき、ライブラリを使いたい場合普通のリストならstatisticsを使う。ベクトル化した場合はNumPyのを使う。
#np.std(配列名,ddof=0 or 1);ddof:自由度はnかn-1
CI = stats.t.interval(0.95, player_num-1, loc=np.mean(gacha_counts_until_ur), scale=stats.sem(gacha_counts_until_ur))
CI_float = (round(float(CI[0]),2), round(float(CI[1]),2))
print(f"95%の信頼区間は{CI_float}です")

#最頻値
from scipy import stats
mode = stats.mode(gacha_counts_until_ur)
print(f"最頻値：{mode}")

#歪度

from scipy.stats import skew
skewness = skew(gacha_counts_until_ur)
if skewness > 0.5:
    print(f"歪度：{skewness}>0.5、数値が右に偏っている")
elif skewness < 0:
    print(f"歪度：{skewness}<-0.5、数値が左に偏っている")
elif -0.5<skewness<0.5:
    print(f"歪度：{skewness}、数値は正規分布に近似する")


#尖度
from scipy.stats import kurtosis
kurt = kurtosis(gacha_counts_until_ur)
if kurt > 0.5:
    print(f"尖度：{kurt}>0.5。データが特定の値に集中している")
elif kurt < 0.5:
    print(f"尖度：{kurt}<0.5。データが特定の値に集中していない")


#データ自体が正規分布かどうかを判別する「jarque-bera検定」
#P値が0.05以上なら正規分布とみなす
jb_test = stats.jarque_bera(gacha_counts_until_ur)
print(jb_test)
if jb_test.pvalue >= 0.05:
    print(f"P値は{jb_test.pvalue:.3f}。0.05以上なのでデータは正規分布とみなせる")
else:
    print(f"P値は{jb_test.pvalue:.3f}。0.05以下なのでデータは正規分布とみなせない")#:.3f 小数点3位まで表示される

#正規分布ではないので、標準偏差の2倍などより、四分位数か百分位数のほうがいい
print(f"10パーセンタイル{np.percentile(gacha_counts_until_ur,10,interpolation='linear')}\n90パーセンタイル{np.percentile(gacha_counts_until_ur,90,interpolation='linear')}")
print(f"いわば、URカードが{ceil(np.percentile(gacha_counts_until_ur,10,interpolation='linear'))}回以下で引きあたるの人は神引きだと言える。{floor(np.percentile(gacha_counts_until_ur,90,interpolation='linear'))}回以上で引きあたるの人は爆死だと言える。")


#プレイヤーがURカードを引いた枚数を記入し、棒グラフにする
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec


fig = plt.figure(figsize=(10, 8))#図のサイズ
gs = gridspec.GridSpec(2, 1, height_ratios=[1, 1])#画面を2行2列に分割して、上の重さは3、下の重さは1にする
plt.rcParams['font.family'] = 'Microsoft JhengHei' #フォント
#図のサイズを高さ8と幅4インチにロックし、図を分別に表せる
max_ur=np.max(gacha_counts_until_ur)
up_graph =plt.subplot(gs[0,:])#上のグラフ

up_graph.hist(gacha_counts_until_ur,bins=np.arange(0,max_ur+2)-0.5,color="orange",edgecolor="black")
#np.arange(0, max_ur + 2) - 0.5：0からmax_ur+2までの等差数列を生成し、それらを-0.5して、整数に枠線の中にする
#arange:等差数列を生成する
up_graph.set_xlabel("ガチャ回数")
up_graph.set_ylabel("人数")
up_graph.set_title("試行回数の分布図")
up_graph.legend()#標線
up_graph.grid(True)


#箱ひげ図
import seaborn as sns
down_graph = plt.subplot(gs[1,:])#下のグラフ
sns.boxplot(x=gacha_counts_until_ur)
down_graph.set_xlabel("ガチャ回数")
down_graph.set_ylabel("人数")
down_graph.set_title("試行回数の箱ひげ図")
down_graph.legend()#標線
plt.grid(True)

plt.tight_layout()#グラフの間隔を調整

import os 
import sys
def get_output_dir():
    try:
        # 判斷是否為打包後的執行檔
        if getattr(sys, 'frozen', False):#frozen屬性是PyInstaller打包後的執行檔才有的
            base_path = os.path.dirname(sys.executable)
        else:
            base_path = os.path.dirname(os.path.abspath(__file__))
        #若這個sys物件有frozen屬性(被打包)則使用目前(.exe)的路徑，否則使用當前檔案(.py)的路徑

        # 建立輸出資料夾
        output_dir = os.path.join(base_path, 'Output_data')#在路徑base_path下建立名為Output_data的資料夾 (型態為字串(a路徑,b資料夾名))
        os.makedirs(output_dir, exist_ok=True)#使用 os.makedirs 建立該資料夾，若已存在則不會報錯（exist_ok=True）
        return output_dir
    except Exception as e:
        print(f"建立輸出資料夾時發生錯誤：{str(e)}")
        return os.getcwd()  # 如果發生錯誤，使用當前目錄
    

# 使用輸出路徑
try:
    output_dir = get_output_dir()
    #グラフを保存する
    #current_dir = os.path.dirname(os.path.abspath(__file__))#フィルダー位置を特定する
    # 出力ディレクトリを作成
    #output_dir = os.path.join(current_dir, 'Output_data')
    #if not os.path.exists(output_dir):
    #    os.makedirs(output_dir)

    filename = f'gacha_simulation_{player_num}players_UntilGet.png'
    filepath = os.path.join(output_dir, filename)
    plt.savefig(filepath)
    print(f"グラフを{filepath}に保存しました。")


    # CSVデータにセーブする
    import csv
    csv_path = os.path.join(output_dir, 'players_UntilGetUR_result.csv')

    with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Player', 'Gacha_Count']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for i, count in enumerate(gacha_counts_until_ur, start=1):
            writer.writerow({'Player': i, 'Gacha_Count': count})

    print("CSVデータに 出力終了。")
    print("Enterを押して終了")
    input()



except Exception as e:
    print(f"アウトプットエラー：{str(e)}")

