import cv2
import os
import numpy as np
import tkinter as tk
import csv
from tkinter import filedialog

# 正規化
def norm(u):
    r_max = np.max(u)
    r_min = np.min(u)
    reconst = ((u-r_min)/(r_max-r_min))
    return reconst

#####################################################
# CSV形式の輝度値データをカラー画像に変換（0:最大の輝度値で正規化　，1：指定の輝度値で正規化）
normalization = 1
# 指定の輝度値を入力
n = 30

#####################################################
# カラー画像保存用のフォルダ’CSV_color’を作成
holo_path = os.path.dirname(os.path.abspath(__file__))+'/CSV_color/'
os.makedirs(holo_path, exist_ok=True)

#####################################################
# tkアプリウィンドウの非表示
tk.Tk().withdraw()
# ファイルダイアログを表示して選択した”画像のパス”と”ファイル名”を取得
filepath = filedialog.askopenfilename()
filename = os.path.splitext(os.path.basename(filepath))[0]

#####################################################
# CSVファイルをリスト配列としてインポート
try:
    with open(filepath, newline='', encoding="utf-8-sig") as file:  # 修正: filepath を使用
        csvfile = list(csv.reader(file))
except FileNotFoundError:
    print("指定されたファイルが見つかりません。: " + filepath)
    exit()

for i in range(len(csvfile)):
    csvfile[i] = [int(j) for j in csvfile[i]]

# CSVファイルをNumpy形式の2次元配列に変換
img_grayscale = np.array(csvfile)
img_grayscale = img_grayscale.astype("uint8")

n_max = np.max(img_grayscale)
n_min = np.min(img_grayscale)

cv2.imshow('Inputted image', cv2.resize(img_grayscale, dsize=None, fx=1, fy=1))


#####################################################
if normalization == 0:
    n = 255
    img_grayscale = (norm(img_grayscale)) * 255
    img_grayscale = img_grayscale.astype("uint8")

    name = str(filename)

elif normalization == 1:
    # 輝度値n以上の値があればnに変換して正規化
    if np.max(img_grayscale) >= n:
        img_grayscale = np.where(img_grayscale >= n, n, img_grayscale)
        img_grayscale = (norm(img_grayscale)) * 255
        img_grayscale = img_grayscale.astype("uint8")
    # 輝度値n以上の値がなければnを上限に正規化
    else:
        img_grayscale = ((img_grayscale-n_min)/(n-n_min)) * 255
        img_grayscale = img_grayscale.astype("uint8")

    name = str(filename) + '_{:.0f}'.format(n)

cv2.imshow('Normalized image', cv2.resize(img_grayscale, dsize=None, fx=1, fy=1))


#####################################################
# グレースケール画像をカラー画像に変換
img_colored = cv2.applyColorMap(img_grayscale, cv2.COLORMAP_JET)

# カラー画像の表示
cv2.imshow('Colored image', cv2.resize(img_colored, dsize=None, fx=1, fy=1))

cv2.waitKey(0)


#####################################################
# 画像データの書き出し
print('ファイルパス：　' + filepath)
print('ファイル名　：　' + filename)
print('最大の輝度値：　' + str(n_max))
print('最小の輝度値：　' + str(n_min))
print('正規化の範囲：　' + '{:.0f}'.format(n))

# カラー画像を保存
cv2.imwrite(holo_path+name+'.bmp', img_colored)