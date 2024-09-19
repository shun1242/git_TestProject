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

<<<<<<< HEAD
save_frame_range(r"E:\ObservedMovie\20240905_APZ\Re_APZ_10000_1_conbined_10000frame.avi",
                 0, 10000, 1,
                 r"E:\ObservedMovie\20240905_APZ\Re_APZ_10000_1_conbined_10000frame_frame", "img")
=======
save_frame_range(r"F:\ObservedMovie\20240905_APZ\Re_APZ_10000_1_conbined_10000frame_差分.avi",
                 0, 6400, 1,
                 r"F:\ObservedMovie\20240905_APZ\frame", "img")
>>>>>>> a531586bf5a6a1aff55901f45cbbb12c8c133a85
