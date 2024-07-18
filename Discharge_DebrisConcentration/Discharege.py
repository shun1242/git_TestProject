import numpy as np
import pandas as pd
import os

#####入力

# #読み込みたいcsvファイルのパス
file_path = "D:\Discharge_DebrisConcentration\ON00.csv"

#評価したいフレーム数（時間幅）
frame_start = 1
frame_end = 6399

#放電発生範囲
discharge_max = 12000
discharge_min = 1000

#工作物高さ方向に何分割するか
div_num = 10

output_dir = 'D:\Discharge_DebrisConcentration'

#####

# CSVファイルを読み込み，y座標のみを抽出
read_df = np.genfromtxt(file_path, delimiter=',',skip_header=6, dtype='f')
df = read_df[:,2::3]

# 評価したいフレーム数までのデータのみを抽出し，1次元配列に
df1 = df[frame_start-1:frame_end,:]
ravel_array = df1.ravel()

# array変換
read_data = np.array(ravel_array)
data = read_data[read_data != 'nan']

# ヒストグラム
hist, bin_edges = np.histogram(data, bins=div_num, range=(discharge_min,discharge_max), density=False)
hist_reverse = np.flipud(hist)
sum = np.sum(hist_reverse)
percentage_arr = hist_reverse / sum

# histをcsvファイルに
output_file_path = os.path.join(output_dir, "Discharge_histogram.csv")
np.savetxt(output_file_path,
           X = percentage_arr,
           delimiter = ","
)

print(hist)
print(hist_reverse)
print(percentage_arr)