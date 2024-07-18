import os
from moviepy.editor import VideoFileClip, concatenate_videoclips
from tkinter import Tk, filedialog, messagebox
import sys
from pymediainfo import MediaInfo

def select_video_files():
    root = Tk()
    root.withdraw()  # Hide the root window
    video_files = filedialog.askopenfilenames(
        title="動画ファイルを選択してください",
        filetypes=[("Video files", "*.mp4 *.avi *.mov *.mkv *.flv")]
    )
    return list(video_files)

def load_video_clips(video_files):
    clips = []
    first_clip = VideoFileClip(video_files[0])
    target_resolution = first_clip.size
    target_format = os.path.splitext(video_files[0])[1][1:]  # 元のファイル形式を取得
    target_fps = first_clip.fps  # 元のフレームレートを取得

    total_video_bitrate = 0
    total_audio_bitrate = 0
    codec = 'libx264'  # デフォルトコーデック

    for file in video_files:
        clip = VideoFileClip(file)
        if clip.size != target_resolution:
            raise ValueError(f"解像度が異なります: {file} は異なる解像度 {clip.size} です（期待する解像度: {target_resolution}）")
        if clip.fps != target_fps:
            raise ValueError(f"フレームレートが異なります: {file} は異なるフレームレート {clip.fps} です（期待するフレームレート: {target_fps}）")
        clips.append(clip)
        
        video_bitrate, audio_bitrate, file_codec = get_bitrates_and_codec(file)
        total_video_bitrate += video_bitrate if video_bitrate is not None else 0
        total_audio_bitrate += audio_bitrate if audio_bitrate is not None else 0
        if file_codec and file_codec != 'YUY2':  # 不適切なコーデックを除外
            codec = file_codec
    
    print(f"Total Video Bitrate: {total_video_bitrate}")  # デバッグ用に出力
    print(f"Total Audio Bitrate: {total_audio_bitrate}")  # デバッグ用に出力
    
    return clips, target_fps, target_format, total_video_bitrate, total_audio_bitrate, codec

def get_bitrates_and_codec(video_file):
    media_info = MediaInfo.parse(video_file)
    video_bitrate = None
    audio_bitrate = None
    codec = None
    for track in media_info.tracks:
        if track.track_type == 'Video':
            video_bitrate = track.bit_rate // 1000 if track.bit_rate else None  # kbpsに変換
            codec = track.codec_id if track.codec_id else None
        if track.track_type == 'Audio':
            audio_bitrate = track.bit_rate // 1000 if track.bit_rate else None  # kbpsに変換
    return video_bitrate, audio_bitrate, codec

def concatenate_videos(clips, output_path, target_fps, total_video_bitrate, total_audio_bitrate, codec):
    final_clip = concatenate_videoclips(clips, method="compose")
    final_clip.write_videofile(
        output_path, 
        fps=target_fps, 
        codec=codec if codec != 'YUY2' else 'libx264',  # 常にサポートされるコーデックを使用する
        audio_codec="aac", 
        bitrate=f"{total_video_bitrate}k",  # ビットレートの単位を確認する
        audio_bitrate=f"{total_audio_bitrate}k",  # ビットレートの単位を確認する
        preset="medium"  # 品質を確保するために調整
    )

def main():
    while True:
        video_files = select_video_files()
        if not video_files:
            print("ファイルが選択されていません。")
            sys.exit()
        
        try:
            clips, target_fps, target_format, total_video_bitrate, total_audio_bitrate, codec = load_video_clips(video_files)
        except ValueError as e:
            messagebox.showerror("エラー", str(e))
            continue

        output_folder = os.path.dirname(video_files[0])
        output_filename = f"combined_video.{target_format}"
        output_path = os.path.join(output_folder, output_filename)
        
        concatenate_videos(clips, output_path, target_fps, total_video_bitrate, total_audio_bitrate, codec)
        messagebox.showinfo("成功", f"動画は正常に {output_path} に保存されました")
        break

if __name__ == "__main__":
    main()
