import pandas as pd
import logging
import numpy as np

class DataLoader:
    def __init__(self, config):
        self.config = config

    def load_bubble_data(self):
        logger = logging.getLogger(__name__)
        try:
            bubble_data = pd.read_excel(self.config.bubble_path, header=None)
            logger.info("気泡の輝度データを読み込みました。")
            return bubble_data.values
        except Exception as e:
            logger.error("気泡の輝度データの読み込みに失敗しました: %s", e)
            raise

    def load_spark_data(self):
        logger = logging.getLogger(__name__)
        try:
            # 最初の数行をスキップしてデータ部分のみを読み込む
            spark_data = pd.read_csv(self.config.spark_path, header=None, skiprows=6, na_values='*', keep_default_na=False)
            logger.info("放電位置データを読み込みました。")
            return spark_data
        except Exception as e:
            logger.error("放電位置データの読み込みに失敗しました: %s", e)
            raise
