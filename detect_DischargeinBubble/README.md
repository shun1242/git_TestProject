# 気中放電検出プログラム

## 概要

このプログラムは、気泡の輝度データと放電位置データを使用して、気中放電を検出します。検出結果はCSVファイルとして出力されます。

## 必要な環境

- Python 3.7以上
- 必要なライブラリ
  - pandas
  - numpy
  - openpyxl (Excelファイルの読み込みに必要)
  
インストール方法：
pip install pandas numpy openpyxl


## 使い方

1. `config.json` ファイルに必要なパラメータを設定します。
2. ターミナルで以下のコマンドを実行します。
python main.py

3. 設定ファイルが存在しない場合、プログラムがパラメータの入力を求めます。

## ファイル構成

- `main.py`：プログラムのエントリーポイント
- `config.py`：設定の管理
- `data_loader.py`：データの読み込み
- `processor.py`：データの処理と気中放電の検出
- `output_writer.py`：結果の出力
- `logger.py`：ロギングの設定
- `tests/`：ユニットテスト
- `config.json`：設定ファイル
- `app.log`：ログファイル
