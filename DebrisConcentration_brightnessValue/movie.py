import cv2
import numpy as np

# 動画ファイルの設定
video_1_path = r'C:\Users\i1204\Documents\Python\DebrisConcentration_brightnessValue\Video1.avi'
video_2_path = r'C:\Users\i1204\Documents\Python\DebrisConcentration_brightnessValue\Video2.avi'
frame_width = 640
frame_height = 480
frame_rate = 30
duration = 5  # 動画の長さ（秒）

# 動画ファイルの作成
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out1 = cv2.VideoWriter(video_1_path, fourcc, frame_rate, (frame_width, frame_height))
out2 = cv2.VideoWriter(video_2_path, fourcc, frame_rate, (frame_width, frame_height))

for _ in range(frame_rate * duration):
    # ランダムなフレームを生成
    frame1 = np.random.randint(0, 256, (frame_height, frame_width, 3), dtype=np.uint8)
    frame2 = np.ones((frame_height, frame_width, 3), dtype=np.uint8) * 255
    
    # フレームを動画ファイルに書き込む
    out1.write(frame1)
    out2.write(frame2)

# 動画ファイルをリリース
out1.release()
out2.release()

print(f"動画ファイル '{video_1_path}' と '{video_2_path}' が作成されました。")
