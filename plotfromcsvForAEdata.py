import matplotlib.pyplot as plt
import pandas as pd
import glob, re, os
from matplotlib.ticker import FormatStrFormatter

# 日本語のフォント設定
plt.rcParams['font.family'] = 'MS Gothic'

# カレントディレクトリのサブディレクトリを含めたすべてのCSVファイルのリストを取得
csv_files = glob.glob('**/Wave_RF1_00000001.csv', recursive=True)

for filename in csv_files:
    print(f"読み込み中：{filename}")
    
    with open(filename, 'r', encoding='shift_jis') as f:
        # サンプリングレート、開始、終了時刻を読み込む
        contents = f.readlines()
        
        # 正規表現を使用して数値を抽出する
        sampling_rate_line = contents[0]
        match = re.search(r"([\d.]+E[\+\-]?[\d]+)|([\d.]+)", sampling_rate_line)
        if match:
            sampling_rate = float(match.group())
        else:
            raise ValueError("サンプリングレートが見つかりません。")

        start_time = float(re.search(r"[\d.]+", contents[1]).group())
        end_time = float(re.search(r"[\d.]+", contents[2]).group())

    # データを読み込む（5行目から開始）
    data = pd.read_csv(filename, delimiter=",", header=None, skiprows=5, encoding='shift_jis')
    y = data[0].values  # 電圧

    # X軸データを計算
    num_samples = len(y)
    time_interval = 1 / sampling_rate
    x = [start_time + i * time_interval for i in range(num_samples)]

    # グラフの設定
    plt.figure(figsize=[8, 4.5])
    y = [value/1000 for value in y]  # mVをVに変換
    plt.plot(x, y, color='black')
    plt.xlabel("時間[秒]", fontsize=24)
    plt.ylabel("電圧[V]", fontsize=24)
    plt.gca().yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)

    # グラフにファイル名と試験片の番号を表示（パスから試験片の番号を抽出）
    specimen_number = os.path.basename(os.path.dirname(filename))
    display_text = f"{specimen_number} - {os.path.basename(filename)}"
    plt.text(0.05, 0.95, display_text, transform=plt.gca().transAxes, ha="left", va="top", fontsize=12)

    plt.tight_layout()

    # グラフをPNGファイルとして保存（カレントディレクトリの'images'フォルダに）
    output_directory = 'images'  # 保存先ディレクトリを直接指定
    os.makedirs(output_directory, exist_ok=True)  # 出力先ディレクトリを作成（既に存在する場合はそのまま）
    output_filename = os.path.join(output_directory, f"{specimen_number}.png")  # 試験片の番号を使って出力ファイル名を構築
    plt.savefig(output_filename, format='png', dpi=300, bbox_inches='tight')  # 画像を保存
    plt.close()  # プロットウィンドウを閉じる

    print(f"折れ線グラフは {output_filename} として保存されました。")
