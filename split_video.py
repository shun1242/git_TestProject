import moviepy.editor as mp
import tkinter as tk
from tkinter import filedialog
import os

def select_file():
    # ファイル選択ダイアログを表示してユーザーに動画ファイルを選択させる
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4;*.avi;*.mov")])
    return file_path

def split_video(file_path, num_splits):
    # 動画ファイルを読み込む
    video = mp.VideoFileClip(file_path)
    duration = video.duration  # 動画の全体の長さ（秒）
    segment_duration = duration / num_splits  # 各セグメントの長さを計算
    base_name, ext = os.path.splitext(file_path)  # ファイル名と拡張子を分離
    
    for i in range(num_splits):
        start_time = i * segment_duration  # 各セグメントの開始時間を計算
        end_time = (i + 1) * segment_duration if i < num_splits - 1 else duration  # 各セグメントの終了時間を計算
        
        # 動画の特定の部分を切り出す
        segment = video.subclip(start_time, end_time)
        output_filename = f'{base_name}_part{i+1}{ext}'  # 出力ファイル名を作成
        segment.write_videofile(output_filename, codec='libx264')  # 新しいファイルとして保存

def main():
    file_path = select_file()
    if not file_path:
        print("No file selected.")
        return
    
    num_splits = int(input("Enter the number of splits: "))  # 分割数をユーザーから入力
    split_video(file_path, num_splits)  # 動画を分割
    print("Video split completed.")

if __name__ == "__main__":
    main()
