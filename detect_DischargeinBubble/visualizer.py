import pandas as pd
import matplotlib.pyplot as plt
import logging
import os

class Visualizer:
    def __init__(self, config):
        self.config = config

    def visualize_data(self, output_csv_path):
        """
        結果データを可視化し、プロットを保存する。
        """
        logger = logging.getLogger(__name__)
        try:
            # **ヘッダーをスキップしてデータを再読み込み**
            result_data = pd.read_csv(output_csv_path, comment='#', encoding='utf-8-sig')

            # 欠損値を除いたデータを取得
            plot_data = []
            for index, row in result_data.iterrows():
                time = row['時間'] if '時間' in result_data.columns else row['Time']
                for col in result_data.columns:
                    if '(Y)' in col and row[col] != '*':
                        y_value = float(row[col])
                        plot_data.append((time, y_value))

            if plot_data:
                # プロットの作成
                times, y_values = zip(*plot_data)
                plt.figure(figsize=(10, 6))
                plt.scatter(times, y_values, marker='o')
                plt.xlabel('時間')
                plt.ylabel('放電のY座標（μm）')
                plt.title('時間と放電位置の散布図')
                plt.grid(True)

                # プロットの保存
                # 出力CSVファイル名を基に画像ファイル名を生成
                output_dir = self.config.output_path
                base_filename = os.path.splitext(os.path.basename(output_csv_path))[0]
                plot_filename = f"{base_filename}_plot.png"
                plot_path = os.path.join(output_dir, plot_filename)

                plt.savefig(plot_path)
                plt.close()
                logger.info("データの可視化が完了しました。プロットを %s に保存しました。", plot_path)
            else:
                logger.warning("可視化するデータがありません。")
        except Exception as e:
            logger.error("データの可視化に失敗しました: %s", e)
            raise