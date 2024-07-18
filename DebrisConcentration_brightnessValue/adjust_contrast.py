import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog
import os

# ダイアログを表示して画像ファイルを選択
root = tk.Tk()
root.withdraw()
file_paths = filedialog.askopenfilenames(title="画像ファイルを選択してください", filetypes=(("画像ファイル", "*.jpg *.jpeg *.png *.bmp *.gif"), ("すべてのファイル", "*.*")))

if not file_paths:
    print("画像ファイルが選択されていません。プログラムを終了します。")
    exit()

# フォルダを作成するディレクトリのパス
output_folder = "output_images"

# フォルダが存在しない場合は作成
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

n = 0     
# 画像ごとに処理を行う
for file_path in file_paths:
  
    # 画像を読み込む
    image = cv2.imread(file_path)

    if image is None:
        print(f"画像ファイル '{file_path}' の読み込みに失敗しました。次の画像に進みます。")
        continue

    # 画像に対する処理を記述
    grayscale_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    image_arr = np.array(grayscale_image)

    a = (image_arr - 200) / (255 - 200)
    new_image_arr = a * (255 - 120) + 120

    # 新しいフォルダ内に保存するファイルパス
    new_image_filename = os.path.join(output_folder, f"new_{n}.png")
    
    # 画像を保存
    cv2.imwrite(new_image_filename, new_image_arr)
    
    n += 1

# すべての画像の処理が終了したらプログラムを終了
print("すべての画像の処理が終了しました。")
