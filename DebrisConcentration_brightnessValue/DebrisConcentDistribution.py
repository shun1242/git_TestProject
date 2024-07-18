import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog
import os

####ここを入力する
x1, y1 = 50, 65
x2, y2 = 570, 66
####


# ダイアログを表示して画像ファイルを選択
root = tk.Tk()
root.withdraw()
file_paths = filedialog.askopenfilenames(title="画像ファイルを選択してください", filetypes=(("画像ファイル", "*.jpg *.jpeg *.png *.bmp *.gif"), ("すべてのファイル", "*.*")))


if not file_paths:
    print("画像ファイルが選択されていません。プログラムを終了します。")
    exit()

# 出力するフォルダのパス
selected_file_path = file_paths[0]
output_dir = '/'.join(selected_file_path.split('/')[:-1])
output_file_path = os.path.join(output_dir, "result.csv")

output_arr = None  # 初期値をNoneに設定

# 画像ごとに処理を行う
for file_path in file_paths:
    
    # 画像を読み込む
    image = cv2.imread(file_path)

    if image is None:
        print(f"画像ファイル '{file_path}' の読み込みに失敗しました。次の画像に進みます。")
        continue

    # グレースケールに変換し，輝度値を抽出
    grayscale_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    image_arr = np.array(grayscale_image)

    # 任意の位置における輝度値を抽出
    arr_Add = image_arr[y1:y2, x1:x2]

    # output_arrがNoneの場合、arr_Addをコピーして初期化
    if output_arr is None:
        output_arr = arr_Add.copy()
    else:
        # output_arrがNoneでない場合、行方向に連結
        output_arr = np.vstack([output_arr, arr_Add])

    # output_arrがNoneのままだとエラーになる可能性があるため、空の場合は空の配列を作成
    if output_arr is None:
        output_arr = np.empty((0, x2 - x1), dtype=image_arr.dtype)
    

print("行列Aの大きさ:", output_arr.shape)

# 輝度値から加工粉濃度を算出
processed_arr = np.where(output_arr > 222, 
                         10.997 - 4.5687 * np.log10(output_arr), 
                         77.496 - 32.887 * np.log10(output_arr)
                )

np.savetxt(output_file_path,
           X = processed_arr,
           delimiter = ","
)


# すべての画像の処理が終了したらプログラムを終了
print("すべての画像の処理が終了しました。")
