import cv2
import numpy as np
from matplotlib import pyplot as plt
from tkinter import filedialog
from tkinter import Tk
import csv
import os

# 画像ファイルを選択するためのファイルダイアログを作成
def select_image():
    root = Tk()
    root.withdraw()  # Tkinterのメインウィンドウを非表示
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp")])
    return file_path

# 輝度値ヒストグラムを計算し、度数分布表をCSVで保存する関数
def plot_histogram_and_save_csv(image_path):
    # 画像をグレースケールで読み込む
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    # ヒストグラムを計算
    hist = cv2.calcHist([image], [0], None, [256], [0, 256])

    # ヒストグラムをプロット
    plt.figure(figsize=(10, 6))
    plt.plot(hist, color='black')
    plt.title('Grayscale Histogram')
    plt.xlabel('Pixel Value')
    plt.ylabel('Frequency')
    plt.grid(True)
    plt.show()

    # CSVファイルに保存
    csv_file_name = os.path.splitext(os.path.basename(image_path))[0] + "_histogram.csv"
    with open(csv_file_name, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Pixel Value', 'Frequency'])  # ヘッダーを書き込み
        for i in range(256):
            writer.writerow([i, int(hist[i])])  # 輝度値とその度数をCSVに書き込み

    print(f"ヒストグラムの度数分布がCSVファイル '{csv_file_name}' に保存されました。")

# メイン処理
if __name__ == "__main__":
    image_path = select_image()
    if image_path:
        plot_histogram_and_save_csv(image_path)
    else:
        print("画像が選択されませんでした。")
