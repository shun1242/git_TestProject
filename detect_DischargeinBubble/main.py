import sys
import logging
from config import Config
from data_loader import DataLoader
from processor import Processor
from output_writer import OutputWriter
from logger import setup_logging

def main():
    # ロギングの設定
    setup_logging()
    logger = logging.getLogger(__name__)

    logger.info("プログラムを開始します。")

    # 設定の読み込み
    config = Config()
    config.load()

    # データの読み込み
    data_loader = DataLoader(config)
    bubble_data = data_loader.load_bubble_data()
    spark_data = data_loader.load_spark_data()

    # データの処理
    processor = Processor(config, bubble_data, spark_data)
    result_data = processor.process()

    # 結果の出力とデータの可視化
    output_writer = OutputWriter(config)
    output_writer.write(result_data)

    logger.info("プログラムが正常に終了しました。")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logging.exception("エラーが発生しました: %s", e)
        sys.exit(1)