import unittest
import pandas as pd
import numpy as np
from processor import Processor
from config import Config

class TestProcessor(unittest.TestCase):
    def setUp(self):
        # テスト用の設定
        self.config = Config()
        self.config.bGray = 100
        self.config.frame = 2
        self.config.pLength = 1.0
        self.config.Image_size = 10
        self.config.y2 = 2
        self.config.start_frame = 0

        # テスト用のデータ
        self.bubble_data = np.array([
            [50, 120, 80],
            [90, 110, 130],
            [70, 95, 105],
            [85, 125, 115],
            [60, 100, 90]
        ])

        data = {
            'Time': [0, 1, 2],
            'P1(X)': [np.nan, 5, 5],
            'P1(Y)': [np.nan, 7, 8],
            'P1(Area)': [np.nan, 100, 110],
        }
        self.spark_data = pd.DataFrame(data)

    def test_process(self):
        processor = Processor(self.config, self.bubble_data, self.spark_data)
        result = processor.process()

        # 結果の検証
        expected_data = {
            'Time': [1],
            'P1(X)': [5],
            'P1(Y)': [7],
            'P1(Area)': [100],
        }
        expected_df = pd.DataFrame(expected_data)
        pd.testing.assert_frame_equal(result.reset_index(drop=True), expected_df.reset_index(drop=True))

if __name__ == '__main__':
    unittest.main()
