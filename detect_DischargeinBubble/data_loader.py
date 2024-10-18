import pandas as pd
import logging
import numpy as np
import os

class DataLoader:
    """
    データの読み込みを行うクラス
    """
    def __init__(self, config):
        self.config = config

    def load_bubble_data(self):
        logger = logging.getLogger(__name__)
        try:
            # 気泡の輝度データを読み込む
            bubble_data = pd.read_excel(self.config.bubble_path, header=None)
            logger.info("気泡の輝度データを読み込みました。")

            # 行を逆転させる
            bubble_data = bubble_data.iloc[::-1].reset_index(drop=True)
            logger.info("気泡の輝度データの行を逆転させました。")

            return bubble_data.values
        except Exception as e:
            logger.error("気泡の輝度データの読み込みに失敗しました: %s", e)
            raise

    def load_spark_data(self):
        logger = logging.getLogger(__name__)
        try:
            if not os.path.exists(self.config.spark_path):
                logger.error("放電位置データファイルが存在しません: %s", self.config.spark_path)
                raise FileNotFoundError(f"放電位置データファイルが存在しません: {self.config.spark_path}")

            # ヘッダー行を読み込むために skiprows=5 と header=0 を指定
            spark_data = pd.read_csv(
                self.config.spark_path,
                skiprows=5,
                encoding='cp932',
                na_values='*',
                keep_default_na=False,
                header=0
            )
            logger.info("放電位置データを読み込みました。")
            return spark_data
        except Exception as e:
            logger.error("放電位置データの読み込みに失敗しました: %s", e)
            raise