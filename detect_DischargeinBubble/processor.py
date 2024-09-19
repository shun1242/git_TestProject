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

        # 気泡データのサイズ
        bubble_rows, bubble_cols = self.bubble_data.shape

        # 放電位置データの処理
        spark_data = self.spark_data.copy()
        spark_data.replace({'*': np.nan}, inplace=True)

        # 列名の設定（省略）

        # 結果を格納するリスト
        result_rows = []

        for index, row in spark_data.iterrows():
            time = row['Time']
            new_row = {'Time': time}
            has_spark = False

            # フレーム番号の計算
            k = index  # 放電位置データのフレーム番号
            k_frame = k - frame_offset  # 気泡の輝度データの列インデックス

            # 列インデックスの範囲チェック
            if k_frame < 0 or k_frame >= bubble_cols:
                continue  # 範囲外の場合は次の行へ

            for i in range(1, num_points + 1):
                y_value = row.get(f'P{i}(Y)', np.nan)

                if pd.isna(y_value):
                    # 欠損値の場合
                    new_row[f'P{i}(X)'] = '*'
                    new_row[f'P{i}(Y)'] = '*'
                    new_row[f'P{i}(Area)'] = '*'
                    continue

                # 放電位置の計算（元の計算式に戻す）
                Discharge_p = ((y_value) - (Image_size - y2) * pLength) / pLength
                Discharge_p = int(round(Discharge_p))

                # 行インデックスの範囲チェック
                if 0 <= Discharge_p < bubble_rows:
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
                    # 行インデックスが範囲外の場合
                    new_row[f'P{i}(X)'] = '*'
                    new_row[f'P{i}(Y)'] = '*'
                    new_row[f'P{i}(Area)'] = '*'

            if has_spark:
                result_rows.append(new_row)

        # 結果のデータフレームを作成
        self.result_data = pd.DataFrame(result_rows, columns=columns)
        logger.info("データの処理が完了しました。")
        return self.result_data