import json
import logging

class Config:
    """
    設定を管理するクラス
    """
    def __init__(self):
        # 各パラメータの初期化
        self.bGray = None
        self.frame = None
        self.pLength = None
        self.Image_size = None
        self.y2 = None
        self.bubble_path = None
        self.spark_path = None
        self.output_path = None
        self.config_file = "config.json"

    def load(self):
        """
        設定をファイルから読み込む。ファイルがない場合は手動入力を促す。
        """
        logger = logging.getLogger(__name__)

        # 設定ファイルの読み込み
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.bGray = data.get('bGray')
                self.frame = data.get('frame')
                self.pLength = data.get('pLength')
                self.Image_size = data.get('Image_size')
                self.y2 = data.get('y2')
                self.bubble_path = data.get('bubble_path')
                self.spark_path = data.get('spark_path')
                self.output_path = data.get('output_path')
                logger.info("設定ファイルを読み込みました。")
        except FileNotFoundError:
            logger.warning("設定ファイルが見つかりません。手動入力を行います。")
            self.manual_input()
        except json.JSONDecodeError:
            logger.error("設定ファイルの形式が正しくありません。")
            raise

        # パラメータの確認
        self.validate_parameters()

    def manual_input(self):
        """
        ユーザーからの手動入力でパラメータを設定する。
        """
        from tkinter import Tk
        from tkinter.filedialog import askopenfilename, asksaveasfilename

        Tk().withdraw()  # GUIウィンドウを表示しない

        # ユーザーにパラメータを入力してもらう
        self.bGray = int(input("輝度のしきい値を入力してください："))
        self.frame = int(input("フレーム数を入力してください："))
        self.pLength = float(input("ピクセル長（μm/ピクセル）を入力してください："))
        self.Image_size = int(input("画像サイズ（ピクセル数）を入力してください："))
        self.y2 = int(input("位置補正値を入力してください："))

        # ファイルの選択
        print("気泡の輝度データファイルを選択してください。")
        self.bubble_path = askopenfilename(title="気泡の輝度データファイルを選択")

        print("放電位置データファイルを選択してください。")
        self.spark_path = askopenfilename(title="放電位置データファイルを選択")

        print("出力ファイルの保存場所を選択してください。")
        self.output_path = asksaveasfilename(title="出力ファイルを保存", defaultextension=".csv")

    def validate_parameters(self):
        """
        必要なパラメータがすべて設定されているか確認する。
        """
        logger = logging.getLogger(__name__)

        required_params = {
            'bGray': self.bGray,
            'frame': self.frame,
            'pLength': self.pLength,
            'Image_size': self.Image_size,
            'y2': self.y2,
            'bubble_path': self.bubble_path,
            'spark_path': self.spark_path,
            'output_path': self.output_path
        }

        missing_params = [key for key, value in required_params.items() if value is None]
        if missing_params:
            logger.error("以下のパラメータが不足しています: %s", ', '.join(missing_params))
            raise ValueError("必要なパラメータが不足しています。")

        logger.info("すべてのパラメータが正常に設定されました。")
