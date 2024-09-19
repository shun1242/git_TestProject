import logging

class OutputWriter:
    def __init__(self, config):
        self.config = config

    def write(self, result_data):
        logger = logging.getLogger(__name__)
        try:
            # パラメータ情報をファイルの冒頭に追加
            header_lines = [
                f"# bGray = {self.config.bGray}",
                f"# frame = {self.config.frame}",
                f"# pLength = {self.config.pLength}",
                f"# Image_size = {self.config.Image_size}",
                f"# y2 = {self.config.y2}",
                f"# start_frame = {self.config.start_frame}"
            ]

            # ファイルに書き込む
            with open(self.config.output_path, 'w', encoding='utf-8') as f:
                for line in header_lines:
                    f.write(line + '\n')
                result_data.to_csv(f, index=False, header=True)
            logger.info("結果を出力ファイルに書き込みました。")
        except Exception as e:
            logger.error("結果の書き込みに失敗しました: %s", e)
            raise
