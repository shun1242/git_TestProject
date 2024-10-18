import cv2
import os
from tkinter import filedialog
from tkinter import Tk

# ファイルダイアログで動画を選択させる
def select_video():
    root = Tk()
    root.withdraw()  # Tkinterのウィンドウを表示しないようにする
    file_path = filedialog.askopenfilename(title="動画ファイルを選択してください", filetypes=[("動画ファイル", "*.avi;*.mp4;*.mov")])
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
    
    # 定数Cの入力（整数または小数）
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

# 動画の全フレームに適応的二値化を適用し、保存する
def process_video(video_path, params):
    block_size, C, adaptive_method, threshold_type, method_name, thresh_name = params
    
    # 動画の読み込み
    cap = cv2.VideoCapture(video_path)
    
    # 動画のプロパティを取得
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    # 保存するファイル名を作成
    base_name = os.path.basename(video_path)
    dir_name = os.path.dirname(video_path)
    name, ext = os.path.splitext(base_name)
    output_name = f"{name}_output_{method_name}_{thresh_name}_B{block_size}_C{C}{ext}"
    output_path = os.path.join(dir_name, output_name)
    
    # 動画の書き込み準備
    fourcc = cv2.VideoWriter_fourcc(*'XVID')  # コーデックを指定（環境に合わせて変更する場合があります）
    out = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height), isColor=False)
    
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    current_frame = 0
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # 進行状況を表示
        current_frame += 1
        print(f"処理中... ({current_frame}/{frame_count})", end='\r')
        
        # グレースケールに変換
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # 適応的二値化を適用
        binary_frame = cv2.adaptiveThreshold(gray, 255, adaptive_method, threshold_type, block_size, C)
        
        # フレームを書き込み
        out.write(binary_frame)
    
    # リソースを解放
    cap.release()
    out.release()
    print(f"\n処理された動画が保存されました: {output_path}")
    
if __name__ == "__main__":
    video_path = select_video()
    if video_path:
        params = get_parameters()
        process_video(video_path, params)
    else:
        print("動画が選択されませんでした。")
