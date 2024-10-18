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
        self.total_sparks = 0  # 元の放電総数をカウントする属性
        self.total_gas_discharges = 0  # 気中放電の総数をカウントする属性

    def process(self):
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

        # 放電位置データのコピーを作成
        spark_data = self.spark_data.copy()

        # 欠損値をNaNに変換
        spark_data.replace({'*': np.nan}, inplace=True)

        # 列名の確認
        logger.info(f"放電位置データの列名: {spark_data.columns.tolist()}")

        # 時間列の名前を取得（日本語対応）
        time_column_name = '時間' if '時間' in spark_data.columns else 'Time'

        # データの列名を取得
        all_columns = spark_data.columns.tolist()
        position_columns = [col for col in all_columns if col != time_column_name]
        num_points = len(position_columns) // 3

        # 結果の列名を設定
        columns = [time_column_name]
        for i in range(1, num_points + 1):
            columns.extend([f'P{i}(X)', f'P{i}(Y)', f'P{i}(Area)'])

        # 結果を格納するリスト
        result_rows = []

        # 各行の処理
        for index, row in spark_data.iterrows():
            time = row[time_column_name]
            new_row = {time_column_name: time}

            for i in range(1, num_points + 1):
                x_col = f'P{i}(X)'
                y_col = f'P{i}(Y)'
                area_col = f'P{i}(Area)'

                y_value = row.get(y_col, np.nan)

                if not pd.isna(y_value):
                    # 放電が存在する場合、元の放電数をカウント
                    self.total_sparks += 1

                    # 放電位置の計算
                    Discharge_p = ((y_value) - (Image_size - y2) * pLength) / pLength
                    Discharge_p = int(round(Discharge_p))

                    # フレーム番号の計算
                    k = index  # 放電位置データのフレーム番号
                    k_frame = k - frame_offset  # 気泡の輝度データの列インデックス

                    # インデックスの範囲チェック
                    if 0 <= Discharge_p < bubble_rows and 0 <= k_frame < bubble_cols:
                        bubble_value = self.bubble_data[Discharge_p, k_frame]
                        if bubble_value >= bGray:
                            # 気中放電と判定
                            new_row[x_col] = row[x_col]
                            new_row[y_col] = y_value
                            new_row[area_col] = row[area_col]
                            self.total_gas_discharges += 1  # 気中放電数をカウント
                        else:
                            # 気中放電ではない場合
                            new_row[x_col] = '*'
                            new_row[y_col] = '*'
                            new_row[area_col] = '*'
                    else:
                        # インデックス範囲外の場合
                        new_row[x_col] = '*'
                        new_row[y_col] = '*'
                        new_row[area_col] = '*'
                else:
                    # 欠損値の場合
                    new_row[x_col] = '*'
                    new_row[y_col] = '*'
                    new_row[area_col] = '*'

            result_rows.append(new_row)

        # 結果のデータフレームを作成
        self.result_data = pd.DataFrame(result_rows, columns=columns)
        logger.info("データの処理が完了しました。")
        return self.result_data