import os
from moviepy.editor import VideoFileClip, concatenate_videoclips
from tkinter import Tk, filedialog, simpledialog, messagebox
import sys

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

    for file in video_files:
        clip = VideoFileClip(file)
        if clip.size != target_resolution:
            raise ValueError(f"解像度が異なります: {file} は異なる解像度 {clip.size} です（期待する解像度: {target_resolution}）")
        clips.append(clip)
    
    return clips, first_clip.fps

def get_frame_rate(default_fps):
    root = Tk()
    root.withdraw()  # Hide the root window
    frame_rate = simpledialog.askfloat("フレームレート", "希望のフレームレートを入力してください:", initialvalue=default_fps)
    return frame_rate if frame_rate else default_fps

def concatenate_videos(clips, output_path, target_fps):
    final_clip = concatenate_videoclips(clips, method="compose")
    final_clip.write_videofile(output_path, fps=target_fps, codec="libx264", audio_codec="aac")

def main():
    while True:
        video_files = select_video_files()
        if not video_files:
            print("ファイルが選択されていません。")
            sys.exit()
        
        try:
            clips, default_fps = load_video_clips(video_files)
        except ValueError as e:
            messagebox.showerror("エラー", str(e))
            continue

        target_fps = get_frame_rate(default_fps)
        
        output_folder = os.path.dirname(video_files[0])
        output_filename = "combined_video.mp4"
        output_path = os.path.join(output_folder, output_filename)
        
        concatenate_videos(clips, output_path, target_fps)
        messagebox.showinfo("成功", f"動画は正常に {output_path} に保存されました")
        break

if __name__ == "__main__":
    main()
