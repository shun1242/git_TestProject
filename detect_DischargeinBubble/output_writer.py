import os
import logging
import datetime
import pandas as pd

class OutputWriter:
    """
    結果の出力とデータの可視化を行うクラス
    """
    def __init__(self, config, processor):
        self.config = config
        self.processor = processor  # Processor インスタンスを受け取る

    def write(self, result_data):
        logger = logging.getLogger(__name__)
        try:
            # 出力ディレクトリを取得
            output_dir = self.config.output_path
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
                logger.info(f"出力ディレクトリを作成しました: {output_dir}")

            # ファイル名を自動生成（例: result_YYYYMMDD_HHMMSS.csv）
            now = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
            output_file = f"result_{now}.csv"
            output_path = os.path.join(output_dir, output_file)

            # 気中放電率の計算
            total_gas_discharges = self.processor.total_gas_discharges
            total_sparks = self.processor.total_sparks
            if total_sparks > 0:
                gas_discharge_rate = total_gas_discharges / total_sparks
            else:
                gas_discharge_rate = 0.0

            # パラメータ情報をヘッダーとして作成
            header_lines = [
                f"# bGray: {self.config.bGray}, frame: {self.config.frame}, pLength: {self.config.pLength}",
                f"# Image_size: {self.config.Image_size}, y2: {self.config.y2}",
                f"# Total Gas Discharges: {total_gas_discharges}, Total Sparks in Original CSV: {total_sparks}",
                f"# Gas Discharge Rate: {gas_discharge_rate:.4f}",
                "#"  # 空行を追加してヘッダーを5行にする
            ]

            # ヘッダーをファイルに書き込む
            with open(output_path, 'w', encoding='utf-8-sig') as f:
                for line in header_lines:
                    f.write(f"{line}\n")

            # データをCSV形式で追記
            result_data.to_csv(output_path, mode='a', index=False, encoding='utf-8-sig')
    
            logger.info(f"結果をファイルに書き込みました: {output_path}")

            # 保存したファイルのパスを返す（後で可視化で使用）
            return output_path
        except Exception as e:
            logger.error("結果の書き込みに失敗しました: %s", e)
            raise