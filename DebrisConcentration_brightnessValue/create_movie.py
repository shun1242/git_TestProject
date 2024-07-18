import cv2
import os

# 画像ファイルのディレクトリを指定します
image_directory = "D:\Python_movie\APZ3" #ここを変更
image_extension = '.bmp'  # 画像の拡張子

# 動画の出力フォルダを指定します（画像ディレクトリと同じフォルダに保存します）
output_folder = image_directory

# 動画の出力ファイル名を指定します
output_file = os.path.join(output_folder, 'output.avi')

# 動画の設定
fps = 30  # フレームレート
frame_size = (0, 0)  # 画像サイズを取得するための初期値

# 画像ファイルのリストを取得します
image_files = [f for f in os.listdir(image_directory) if f.endswith(image_extension)]

# 画像サイズを取得します
if image_files:
    sample_image = cv2.imread(os.path.join(image_directory, image_files[0]))
    frame_size = (sample_image.shape[1], sample_image.shape[0])

# 動画の書き込み器を作成します
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter(output_file, fourcc, fps, frame_size)

# 画像を読み込んで動画に書き込みます
for image_file in image_files:
    image_path = os.path.join(image_directory, image_file)
    frame = cv2.imread(image_path)
    out.write(frame)

# 動画を閉じてリソースを解放します
out.release()
cv2.destroyAllWindows()

print(f'動画 "{output_file}" を作成しました。')
