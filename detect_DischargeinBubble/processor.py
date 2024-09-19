import logging
import numpy as np
import pandas as pd

class Processor:
    """
    データの処理と気中放電の検出を行うクラス
    """
    def __init__(self, config, bubble_data, spark_data):
        self.config = config
        self.bubble_data = bubble_data
        self.spark_data = spark_data
        self.result_data = None

    def process(self):
        """
        データを処理し、気中放電を検出する。
        """
        logger = logging.getLogger(__name__)
        logger.info("データの処理を開始します。")

        # パラメータの取得
        bGray = self.config.bGray
        frame_offset = self.config.frame
        pLength = self.config.pLength
        Image_size = self.config.Image_size
        y2 = self.config.y2
        start_frame = self.config.start_frame

        # 気泡データのサイズ
        bubble_rows, bubble_cols = self.bubble_data.shape

        # 放電位置データのコピーを作成
        spark_data = self.spark_data.copy()

        # 欠損値をNaNに変換
        spark_data.replace({'*': np.nan}, inplace=True)

        # 列名を設定
        num_columns = spark_data.shape[1]
        columns = ['Time']
        num_points = (num_columns - 1) // 3  # 放電位置のポイント数
        for i in range(1, num_points + 1):
            columns.extend([f'P{i}(X)', f'P{i}(Y)', f'P{i}(Area)'])
        spark_data.columns = columns

        # 結果を格納するリスト
        result_rows = []

        # 各行（時間ごとのデータ）の処理
        for index, row in spark_data.iterrows():
            time = row['Time']
            new_row = {'Time': time}
            has_spark = False  # 気中放電が検出されたかどうか

            for i in range(1, num_points + 1):
                y_value = row.get(f'P{i}(Y)', np.nan)

                if pd.isna(y_value):
                    # 欠損値の場合
                    new_row[f'P{i}(X)'] = '*'
                    new_row[f'P{i}(Y)'] = '*'
                    new_row[f'P{i}(Area)'] = '*'
                    continue

                # 放電位置の計算
                Discharge_p = ((y_value) - (Image_size - y2) * pLength) / pLength
                Discharge_p = int(round(Discharge_p))

                # フレーム番号の計算
                k = index + start_frame
                k_frame = k - frame_offset

                # インデックスの範囲チェック
                if 0 <= Discharge_p < bubble_rows and 0 <= k_frame < bubble_cols:
                    bubble_value = self.bubble_data[Discharge_p, k_frame]
                    if bubble_value >= bGray:
                        # 気中放電と判定
                        new_row[f'P{i}(X)'] = row[f'P{i}(X)']
                        new_row[f'P{i}(Y)'] = y_value
                        new_row[f'P{i}(Area)'] = row[f'P{i}(Area)']
                        has_spark = True
                    else:
                        # 気中放電ではない場合
                        new_row[f'P{i}(X)'] = '*'
                        new_row[f'P{i}(Y)'] = '*'
                        new_row[f'P{i}(Area)'] = '*'
                else:
                    # インデックス範囲外の場合
                    new_row[f'P{i}(X)'] = '*'
                    new_row[f'P{i}(Y)'] = '*'
                    new_row[f'P{i}(Area)'] = '*'

            if has_spark:
                # 気中放電が検出された行のみ追加
                result_rows.append(new_row)

        # 結果のデータフレームを作成
        self.result_data = pd.DataFrame(result_rows, columns=columns)
        logger.info("データの処理が完了しました。")
        return self.result_data
