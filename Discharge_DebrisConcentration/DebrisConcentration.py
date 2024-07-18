import numpy as np
import os

#####入力

# #読み込みたいcsvファイルのパス
file_path = "D:\Discharge_DebrisConcentration\ON00\On00_1-6399frame_Debris_result_Y65.csv"

#評価したいフレーム数（時間幅）
frame_start = 1
frame_end = 6399

#工作物高さ方向に何分割するか
div_num = 10

output_dir = 'D:\Discharge_DebrisConcentration'

#####

# CSVファイルを読み込み
read_df = np.genfromtxt(file_path, delimiter=',', dtype='f')
df = read_df[frame_start-1:frame_end,:]
row, col = df.shape
col = 420
print(row, col)

parcel_len = int(col / div_num)

out_arr = np.array([])

for i in range(1, div_num+1):
    df1 = df[:,(i-1)*parcel_len:i*parcel_len]
    out_arr = np.append(out_arr, (np.sum(df1))/(parcel_len*row))


# csvファイルで出力
output_file_path = os.path.join(output_dir, "Debris_histogram.csv")
np.savetxt(output_file_path,
           X = out_arr,
           delimiter = ","
)
