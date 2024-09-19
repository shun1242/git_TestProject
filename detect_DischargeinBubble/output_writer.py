import logging
import matplotlib.pyplot as plt

class OutputWriter:
    """
    結果の出力とデータの可視化を行うクラス
    """
    def __init__(self, config):
        self.config = config

    def write(self, result_data):
        """
        結果をファイルに書き込み、データを可視化する。
        """
        logger = logging.getLogger(__name__)
        try:
            # パラメータ情報をファイルの冒頭に追加
            header_lines = [
                f"# bGray = {self.config.bGray}",
                f"# frame = {self.config.frame}",
                f"# pLength = {self.config.pLength}",
                f"# Image_size = {self.config.Image_size}",
                f"# y2 = {self.config.y2}",
            ]

            # 結果をCSVファイルに書き込む
            with open(self.config.output_path, 'w', encoding='utf-8') as f:
                for line in header_lines:
                    f.write(line + '\n')
                result_data.to_csv(f, index=False, header=True)
            logger.info("結果を出力ファイルに書き込みました。")

            # データの可視化
            self.visualize_data(result_data)
        except Exception as e:
            logger.error("結果の書き込みに失敗しました: %s", e)
            raise

    def visualize_data(self, result_data):
        """
        結果データを可視化し、プロットを保存する。
        """
        logger = logging.getLogger(__name__)
        try:
            # 欠損値を除いたデータを取得
            plot_data = []
            for index, row in result_data.iterrows():
                time = row['Time']
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
                plot_path = self.config.output_path.replace('.csv', '_plot.png')
                plt.savefig(plot_path)
                plt.close()
                logger.info("データの可視化が完了しました。プロットを %s に保存しました。", plot_path)
            else:
                logger.warning("可視化するデータがありません。")
        except Exception as e:
            logger.error("データの可視化に失敗しました: %s", e)
