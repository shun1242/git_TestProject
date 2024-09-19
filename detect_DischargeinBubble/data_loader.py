import pandas as pd
import logging
import numpy as np

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
        """
        放電位置データを読み込む。
        """
        logger = logging.getLogger(__name__)
        try:
            # 先頭の6行をスキップし、データ部分のみを読み込む
            spark_data = pd.read_csv(
                self.config.spark_path,
                header=None,
                skiprows=6,
                na_values='*',
                keep_default_na=False,
                encoding='cp932'  # または 'shift_jis' を試してください
            )
            logger.info("放電位置データを読み込みました。")
            return spark_data
        except Exception as e:
            logger.error("放電位置データの読み込みに失敗しました: %s", e)
            raise
