import matplotlib.pyplot as plt
import pandas as pd
import glob
from matplotlib.ticker import FormatStrFormatter

# 日本語のフォント設定
#plt.rcParams['font.family'] = 'MS Gothic' #全体のフォントを設定 windows標準の日本語フォント
plt.rcParams['font.family'] = 'IPAexGothic'  # IPAexゴシックを指定 macの場合IPAexGothicを入れて使う


# 同じ階層のすべてのCSVファイルのリストを取得
csv_files = glob.glob('*.csv')

for filename in csv_files:
    # データを読み込む
    print(f"reading:{filename}")
    #今回のデータが5列目から始まるので skiprows=4 で4列飛ばす
    data = pd.read_csv(filename, delimiter=",", header=None, skiprows=4, encoding='shift_jis') 

    
    # データを x と y のリストに分ける
    x = data[0].tolist()
    y = data[1].tolist()

    # 図のサイズを指定
    plt.figure(figsize=[8, 4.5])

    # yのデータを1000倍にスケーリング (VをmVに変換)
    y = [value * 1000 for value in y]

    # 散布図を作成
    plt.scatter(x, y, c='black', marker='o')
    plt.xlabel("距離[mm]", fontsize = 24)
    plt.ylabel("電圧実行値R[mV]", fontsize = 24)

    # y軸の目盛りを小数点以下2桁で表示
    plt.gca().yaxis.set_major_formatter(FormatStrFormatter('%.2f'))


    # 最大,最小値を決定
    plt.xlim(87.5, 187.5) #x軸
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)

    # 縦線を描画
    x_value_for_vertical_line = float(137.5)
    plt.axvline(x=x_value_for_vertical_line, color='red', linestyle='--')

    plt.text(0.05, 0.95, filename, transform=plt.gca().transAxes, ha="left", va="top")

    # 上と左の余白を狭くする
    plt.subplots_adjust(left=0.12, right=0.97, top=0.97, bottom=0.16)

    # 散布図をPNGとして保存
    output_filename = filename.replace(".csv", ".png")
    plt.savefig(output_filename, format='png', dpi = 300)
    plt.close()

    # 保存されたファイル名を表示してユーザーに通知
    print(f"散布図は {output_filename} として保存されました。")

