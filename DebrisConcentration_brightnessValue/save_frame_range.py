import cv2
import os

def save_frame_range(video_path, start_frame, stop_frame, step_frame, dir_path, basename):
    cap = cv2.VideoCapture(video_path)

    # ビデオファイルが正しく開けない場合、関数を終了する
    if not cap.isOpened():
        print(f"Error: Could not open video file {video_path}")
        return

    # フレームを保存するディレクトリを作成（既存の場合は無視）
    os.makedirs(dir_path, exist_ok=True)
    base_path = os.path.join(dir_path, basename)

    for n in range(start_frame, stop_frame, step_frame):
        cap.set(cv2.CAP_PROP_POS_FRAMES, n)
        ret, frame = cap.read()
        
        # フレームの読み込みが成功した場合
        if ret:
            # フレームをグレースケールに変換
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            # ファイル名を生成し、.bmp形式でフレームを保存
            file_path = '{}_{}.bmp'.format(base_path, n)
            cv2.imwrite(file_path, gray_frame)
        else:
            # フレームの読み込みが失敗した場合、関数を終了する
            print('処理が失敗しました。')
            return

    print('処理が完了しました。')

# 使い方の例
# save_frame_range('data/temp/sample_video.mp4',
#                  200, 300, 10,
#                  'data/temp/result_range', 'sample_video_img')

save_frame_range(r"D:\ObservedMovie\20240703_APZandW\AP(ON00)\ON00_2.avi",
                 0, 6400, 1,
                 r"D:\ObservedMovie\20240703_APZandW\AP(ON00)\_frame", "img")