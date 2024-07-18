import tkinter as tk
from tkinter import filedialog, simpledialog
import pandas as pd
from scipy.ndimage import uniform_filter
import os

def apply_average_filter(data, filter_size):
    array_data = data.values
    averaged_data = uniform_filter(array_data, size=filter_size, mode='nearest')
    return averaged_data

def select_file_and_filter():
    # ファイル選択ダイアログを開く
    root = tk.Tk()
    root.withdraw()  # GUIを非表示にする
    file_path = filedialog.askopenfilename(title='CSVファイルを選択してください', filetypes=[("CSV files", "*.csv")])
    
    if not file_path:
        print("ファイルが選択されませんでした。")
        return

    # フィルタサイズをユーザーに尋ねる
    filter_size = simpledialog.askinteger("フィルタサイズ入力", "平均化フィルタのサイズを入力してください (例: 3):",
                                          minvalue=1)
    if not filter_size:
        print("フィルタサイズが入力されませんでした。")
        return

    # CSVファイルを読み込む
    data = pd.read_csv(file_path)

    # 平均化フィルタの適用
    filtered_data = apply_average_filter(data, filter_size)

    # 保存先のファイル名を生成
    dirname = os.path.dirname(file_path)
    basename = os.path.basename(file_path)
    name_part = os.path.splitext(basename)[0]
    new_filename = f"{name_part}_AveragingFilter({filter_size}).csv"
    new_file_path = os.path.join(dirname, new_filename)

    # 結果をCSVで保存
    pd.DataFrame(filtered_data).to_csv(new_file_path, index=False)
    print(f"ファイルが保存されました: {new_file_path}")

select_file_and_filter()
