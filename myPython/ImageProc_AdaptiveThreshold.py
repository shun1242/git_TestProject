import cv2
import os
from tkinter import filedialog
from tkinter import Tk

# ファイルダイアログで画像を選択させる
def select_image():
    root = Tk()
    root.withdraw()  # Tkinterのウィンドウを表示しないようにする
    file_path = filedialog.askopenfilename(title="画像を選択してください", filetypes=[("画像ファイル", "*.png;*.jpg;*.jpeg;*.bmp")])
    return file_path

# ユーザーから適応的二値化のパラメータを入力させる
def get_parameters():
    print("適応的二値化のパラメータを入力してください。")
    
    # ブロックサイズの入力（奇数で3以上の整数）
    while True:
        try:
            block_size = int(input("ブロックサイズ（奇数、3以上の整数）: "))
            if block_size % 2 == 1 and block_size >= 3:
                break
            else:
                print("エラー: ブロックサイズは3以上の奇数である必要があります。")
        except ValueError:
            print("エラー: 整数を入力してください。")
    
    # 定数Cの入力（整数）
    while True:
        try:
            C = float(input("定数C（閾値から引く値、小数も可）: "))
            break
        except ValueError:
            print("エラー: 数値を入力してください。")
    
    # 適応方法の選択
    print("適応方法を選択してください。")
    print("1: 平均値（ADAPTIVE_THRESH_MEAN_C）")
    print("2: ガウシアン（ADAPTIVE_THRESH_GAUSSIAN_C）")
    while True:
        method = input("選択（1または2）: ")
        if method == '1':
            adaptive_method = cv2.ADAPTIVE_THRESH_MEAN_C
            method_name = 'MEAN'
            break
        elif method == '2':
            adaptive_method = cv2.ADAPTIVE_THRESH_GAUSSIAN_C
            method_name = 'GAUSSIAN'
            break
        else:
            print("エラー: 1または2を入力してください。")
    
    # 閾値タイプの選択
    print("閾値タイプを選択してください。")
    print("1: 白黒反転なし（THRESH_BINARY）")
    print("2: 白黒反転（THRESH_BINARY_INV）")
    while True:
        thresh_type = input("選択（1または2）: ")
        if thresh_type == '1':
            threshold_type = cv2.THRESH_BINARY
            thresh_name = 'BINARY'
            break
        elif thresh_type == '2':
            threshold_type = cv2.THRESH_BINARY_INV
            thresh_name = 'BINARY_INV'
            break
        else:
            print("エラー: 1または2を入力してください。")
    
    return block_size, C, adaptive_method, threshold_type, method_name, thresh_name

# 適応的二値化を行い、結果を保存する
def adaptive_thresholding(image_path, params):
    block_size, C, adaptive_method, threshold_type, method_name, thresh_name = params
    
    # 画像を読み込む
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    
    # 適応的二値化を適用
    binary_img = cv2.adaptiveThreshold(img, 255, adaptive_method, threshold_type, block_size, C)
    
    # 保存するファイル名を作成
    base_name = os.path.basename(image_path)
    dir_name = os.path.dirname(image_path)
    name, ext = os.path.splitext(base_name)
    output_name = f"{name}_output_{method_name}_{thresh_name}_B{block_size}_C{C}{ext}"
    output_path = os.path.join(dir_name, output_name)
    
    # 二値化した画像を保存
    cv2.imwrite(output_path, binary_img)
    print(f"処理された画像が保存されました: {output_path}")

if __name__ == "__main__":
    image_path = select_image()
    if image_path:
        params = get_parameters()
        adaptive_thresholding(image_path, params)
    else:
        print("画像が選択されませんでした。")