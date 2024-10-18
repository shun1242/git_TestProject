import logging
import sys
from config import Config
from data_loader import DataLoader
from processor import Processor
from output_writer import OutputWriter
from visualizer import Visualizer

def main():
    logger = logging.getLogger(__name__)
    logger.info("プログラムを開始します。")

    config = Config()
    config.load()

    data_loader = DataLoader(config)
    bubble_data = data_loader.load_bubble_data()
    spark_data = data_loader.load_spark_data()

    processor = Processor(config, bubble_data, spark_data)
    result_data = processor.process()

    output_writer = OutputWriter(config, processor)  # Processor を渡す
    output_csv_path = output_writer.write(result_data)

    # データの可視化を実行
    visualizer = Visualizer(config)
    visualizer.visualize_data(output_csv_path)

    logger.info("プログラムが正常に終了しました。")

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        main()
    except Exception as e:
        logging.getLogger().error("エラーが発生しました: %s", e)
        sys.exit(1)