import cv2
import numpy as np
import os
import pandas as pd
from tkinter import filedialog
from tkinter import Tk

def main():
    # フォルダ選択ダイアログを表示
    root = Tk()
    root.withdraw()
    folder_selected = filedialog.askdirectory()
    
    if not folder_selected:
        print("フォルダが選択されませんでした。")
        return
    
    # 画像ファイルのパスを取得
    images = [os.path.join(folder_selected, f) for f in os.listdir(folder_selected) if f.endswith(('.png', '.jpg', '.jpeg', '.bmp'))]
    if not images:
        print("選択されたフォルダに画像が見つかりません。")
        return

    # 画像データを格納する配列を初期化
    sum_array = None
    count = 0
    
    # 画像を一つずつ処理
    for image_path in images:
        try:
            # 画像を読み込み
            img = cv2.imread(image_path)
            if img is None:
                raise ValueError(f"画像 {image_path} が読み込めませんでした。")
            
            # 画像がRGBの場合はグレースケールに変換
            if img.ndim == 3:
                img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            
            # 画像サイズの確認と配列の初期化
            if sum_array is None:
                sum_array = np.zeros_like(img, dtype=np.float64)
            elif img.shape != sum_array.shape:
                raise ValueError(f"画像 {image_path} のサイズが異なります。")

            # 輝度値を配列に加算
            sum_array += img
            count += 1
        
        except Exception as e:
            print(f"エラーが発生しました: {e}")
            continue

    # 画像が一枚も処理されなかった場合
    if count == 0:
        print("処理する画像がありませんでした。")
        return

    # 平均輝度値を計算
    average_array = sum_array / count

    # 0-255の範囲に正規化（必要に応じて）
    average_array = np.clip(average_array, 0, 255).astype(np.uint8)

    # CSVファイルに出力
    output_path = os.path.join(folder_selected, "output.csv")
    pd.DataFrame(average_array).to_csv(output_path, header=None, index=None)
    print(f"処理が完了しました。結果は {output_path} に保存されました。処理した画像の数：{count}")


if __name__ == "__main__":
    main()
