# Gacha_simulation_01.pyをベクトル化して、より効率的なプログラムを作ってみる
import random
import numpy as np
# list	易於新增、刪除項目	資料筆數不確定、內容異質時
# np.array	支援向量運算、效率高	當資料都是數字且會做統計或圖表分析時最佳
from Gacha_function import gacha
from Gacha_function import gacha_Pity  

from collections import Counter#collectionsモジュールを利用しカウンターする

# ラインナップ
pool = ["N","R","SR","UR"]
array_pool = np.array(pool)
prob = [0.55,0.35,0.075,0.025]#確率係数/重み
array_prob=np.array(prob)

print("このプログラムは、スマホゲームのガチャ（抽選）をシミュレーションするものです。\n"
      "ラインナップは N、R、SR、UR の4種類で、確率はそれぞれ 0.55、0.35、0.075、0.025 です。\n"
      "シミュレーションでは天井の有無を選択できます（天井の初期値は期待値の2倍に設定されています）。\n"
      "合計で 1000人 × 入力された回数分の実行します。\n"
      "試行の結果から平均、標準偏差、信頼区間などの統計量を計算し、\n"
      "分布図や箱ひげ図、抽選成功率の収束グラフ、各プレイヤーの抽選結果（.csv）を出力します。\n"
      "（※収束図は14976回のベルヌーイ試行を行います。）\n"
      "----------------------------------------------------------------------------------------")

gacha_times =int(input("まずは試験回数は入力ください。"))
player_num = 1000 #int(input("プレイヤー数:"))

player_result_list=[]
player_result_UR=[]

gacha_mode = input("天井の有無を選択してください。(y/n)").strip().lower()#天井あるかと決める


#抽選の動作
if gacha_mode == 'n':#天井なし

    for i in range(1,int(player_num)+1):

        
        player_result=gacha(gacha_times,array_pool,array_prob)#ガッチャ関数
        array_bag = np.array(player_result)
        # print(f"プレイヤー{i}の結果：Nカード{np.sum(array_bag=="N")}枚、Rカード{np.sum(array_bag=="R")}枚、SRカード{np.sum(array_bag=="SR")}枚、URカード{np.sum(array_bag=="UR")}枚")
        player_result_UR.append(int(np.sum(array_bag=="UR")))
        player_bag={
            'Player':i,
            'N':int(np.sum(array_bag=="N")),
            'R':int(np.sum(array_bag=="R")),
            'SR':int(np.sum(array_bag=="SR")),
            'UR':int(np.sum(array_bag=="UR"))
        }
        player_result_list.append(player_bag)
    

elif gacha_mode == 'y':#天井あり
    for i in range(1,int(player_num)+1):        
        player_result=gacha_Pity(gacha_times,array_pool,array_prob)#ガッチャ関数
        array_bag = np.array(player_result)
        # print(f"プレイヤー{i}の結果：Nカード{np.sum(array_bag=="N")}枚、Rカード{np.sum(array_bag=="R")}枚、SRカード{np.sum(array_bag=="SR")}枚、URカード{np.sum(array_bag=="UR")}枚")
        player_result_UR.append(int(np.sum(array_bag=="UR")))
        player_bag={
            'Player':i,
            'N':int(np.sum(array_bag=="N")),
            'R':int(np.sum(array_bag=="R")),
            'SR':int(np.sum(array_bag=="SR")),
            'UR':int(np.sum(array_bag=="UR"))
        }
        player_result_list.append(player_bag)


#統計量を加えて
import scipy.stats as stats
from math import ceil,floor

#基本統計量
print(f"{gacha_times}回引いたらURの期待値{prob[-1]*gacha_times}\n{gacha_times}回引いたらURの確率{1-(1-prob[-1])**gacha_times}")
print(f"URカードを最も多く引いた人の枚数は{np.max(player_result_UR)}\n最も少なく引いた人の枚数は{np.min(player_result_UR)}")
print(f"標準偏差：{np.std(player_result_UR,ddof=1)},標準誤差{stats.sem(player_result_UR)}\n中央値：{np.median(player_result_UR)}\n平均：{np.mean(player_result_UR)}")

#信頼区間　stats.t.interval(信頼度,自由度,平均,標準誤差) > このデータはタプる
CI = stats.t.interval(0.95, player_num-1, loc=np.mean(player_result_UR), scale=stats.sem(player_result_UR))
CI_float = (round(float(CI[0]),2), round(float(CI[1]),2))
print(f"95%の信頼区間は{CI_float}です")

if gacha_mode == 'n':#天井ありの時
    non_urset = [x for x in player_result_UR if x == 0]#URを引かなかった人のリスト
    print(f"URを引かなかった人の人数は{len(non_urset)}人です。")
    print(f"URを引かなかった人の割合は{round(len(non_urset)/player_num*100,2)}%です。")



print(f"2倍標準偏差区間は{max(0,round(np.mean(player_result_UR)-2*np.std(player_result_UR,ddof=1),2))}~{round(np.mean(player_result_UR)+np.std(player_result_UR,ddof=1)*2,2)}です")
print(f"いわば、引いたUR枚数が{max(0,floor(np.mean(player_result_UR)-2*np.std(player_result_UR,ddof=1)))}以下の人は爆死だと言える。UR枚数が{ceil(np.mean(player_result_UR)+np.std(player_result_UR,ddof=1)*2)}以上の人は神引きだと言える。")
#標準偏差を計算するとき、ライブラリを使いたい場合普通のリストならstatisticsを使う。ベクトル化した場合はNumPyのを使う。
#np.std(配列名,ddof=0 or 1);ddof:自由度はnかn-1


#最頻値
from scipy import stats
mode = stats.mode(player_result_UR)
print(f"最頻値は{mode[0]}、出現回数は{mode[1]}です")

#歪度
from scipy.stats import skew
skewness = skew(player_result_UR)
if skewness > 0.5:
    print(f"歪度：{skewness}>0.5、数値が右に偏っている")
elif skewness < 0:
    print(f"歪度：{skewness}<-0.5、数値が左に偏っている")
elif -0.5<skewness<0.5:
    print(f"歪度：{skewness}、数値は正規分布に近似する")


#尖度
from scipy.stats import kurtosis
kurt = kurtosis(player_result_UR)
if kurt > 0.5:
    print(f"尖度：{kurt}>0.5。データが特定の値に集中している")
elif kurt < 0.5:
    print(f"尖度：{kurt}<0.5。データが特定の値に集中していない")


#データ自体が正規分布かどうかを判別する「jarque-bera検定」
#P値が0.05以上なら正規分布とみなす
jb_test = stats.jarque_bera(player_result_UR)

if jb_test.pvalue >= 0.05:
    print(f"P値は{jb_test.pvalue:.2f}。P値は0.05以上なのでデータは正規分布とみなせる")
else:
    print(f"P値は{jb_test.pvalue:.2f}。P値は0.05以下なのでデータは正規分布とみなせない")

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

fig = plt.figure(figsize=(12, 8))
gs = gridspec.GridSpec(2, 2, height_ratios=[3, 1])
plt.rcParams['font.family'] = 'Microsoft JhengHei' #フォント

#標準曲線図のサイズ

#ベルヌーイ試行を行う。
#大数の法則により、p=0.025で95%CI(S=1.96),誤差が0.1の場合には
# S√V = S√(p(1-p)/n) ≦ep ⇒ 試行回数 n ≧ (1/p - 1 )*(S/e)**2 
# 故で、n≧ (1/0.025 - 1) * (1.96/0.1)**2 = 39 * 384.16 = 14975.24 , 最低14976回の試行が必要です
#https://mtkn.hatenablog.com/entry/2015/02/03/193000

Bernoulli_test_times = 14976#ベルヌーイ試行の回数
results = np.random.binomial(1, array_prob[-1], size=Bernoulli_test_times)
#累積された確率
cumulative_success_rate = np.cumsum(results) / (np.arange(1,Bernoulli_test_times + 1))
theoretical = [array_prob[-1]] * Bernoulli_test_times#理論上の成功確率(期待値)

#理論値を計算する
n_values = np.arange(1, Bernoulli_test_times + 1)
SE= np.sqrt(array_prob[3] * (1 - array_prob[3]) / n_values)
upper_bound = array_prob[3] + SE
lower_bound = array_prob[3] - SE


# グラフ
main_graph=plt.subplot(gs[0,:]) 
main_graph.plot(cumulative_success_rate, label='実行結果')
main_graph.plot(theoretical, linestyle='--', color='red', label='設定された当たり確率')#理論値

plt.fill_between(n_values, lower_bound, upper_bound, color='red', alpha=0.2, label='±1σ 範囲')#重なった部分（1倍標準誤差区間）
main_graph.set_xlabel('試行回数')
main_graph.set_ylabel('成功確率')
main_graph.set_title('抽選成功率の収束グラフ')
main_graph.legend()#標線
main_graph.grid(True)


#図のサイズを高さ8と幅4インチにロックし、図を分別に表せる
max_ur=np.max(player_result_UR)
left_graph=plt.subplot(gs[1,0])#左下のグラフ
left_graph.hist(player_result_UR,bins=np.arange(0,max_ur+2)-0.5,color="orange",edgecolor="black")
#np.arange(0, max_ur + 2) - 0.5：0からmax_ur+2までの等差数列を生成し、それらを-0.5して、整数に枠線の中にする
#arange:等差数列を生成する
left_graph.set_xlabel("UR枚数")
left_graph.set_ylabel("人数")
left_graph.set_title(f"1000人で{gacha_times}回のガチャを引いてUR枚数分布図")
left_graph.grid(True)


#箱ひげ図
import seaborn as sns


right_graph=plt.subplot(gs[1,1])#右下のグラフ
sns.boxplot(x=player_result_UR)
right_graph.set_xlabel("UR枚数")
right_graph.set_ylabel("人数")
right_graph.set_title(f"1000人で{gacha_times}回のガチャを引いてUR枚数分布図")
right_graph.grid(True)
plt.tight_layout()#グラフの間隔を調整

import os 
import sys

def get_output_dir():
    try:
        # 判斷是否為打包後的執行檔
        if getattr(sys, 'frozen', False):
            base_path = os.path.dirname(sys.executable)
        else:
            base_path = os.path.dirname(os.path.abspath(__file__))
        
        # 建立輸出資料夾
        output_dir = os.path.join(base_path, 'Output_data')
        os.makedirs(output_dir, exist_ok=True)
        print(f"輸出目錄：{output_dir}")  # 加入此行來確認路徑
        return output_dir
    except Exception as e:
        print(f"建立輸出資料夾時發生錯誤：{str(e)}")
        return os.getcwd()  # 如果發生錯誤，使用當前目錄

# 使用輸出路徑
try:#如果無法執行，則改為執行except的內容
    #グラフを保存する
    output_dir = get_output_dir()
    #出力ディレクトリを作成
    filename = f'gacha_simulation_{player_num}players_{gacha_times}times.png'
    filepath = os.path.join(output_dir, filename)
    plt.savefig(filepath)
    print(f"グラフを{filepath}に保存しました。")


    #CSVデータにセーブする
    import csv

    csv_path = os.path.join(output_dir, 'gacha_result.csv')

    with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Player', 'N', 'R', 'SR', 'UR']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in player_result_list:
            writer.writerow(row)
            
    print(f"CSVを{filepath}に保存しました。")
    print("Enterを押して終了")
    input()



except Exception as e:
    print(f"データセーフエラー：{str(e)}")
    print("Enterを押して終了")
    input()



























