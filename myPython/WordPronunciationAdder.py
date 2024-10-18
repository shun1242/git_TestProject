import csv

# 発音記号のテキストファイルを読み込み、辞書に格納する
def load_pronunciations(pronunciation_file):
    pronunciations = {}
    with open(pronunciation_file, 'r', encoding='utf-8') as file:
        for line in file:
            # 行をタブで分割
            parts = line.strip().split('\t')
            if len(parts) == 2:
                word, pronunciation = parts
                pronunciations[word] = pronunciation  # アポストロフィを削除しない
    return pronunciations

# CSVファイルを読み込み、単語と発音記号を第一列にまとめる
def add_pronunciations_to_csv(input_csv, output_csv, pronunciations):
    with open(input_csv, 'r', encoding='utf-8') as csv_in, \
         open(output_csv, 'w', newline='', encoding='utf-8') as csv_out:

        reader = csv.reader(csv_in)
        writer = csv.writer(csv_out)

        # ヘッダー行がある場合は読み込んでそのまま書き込む
        # ヘッダーがない場合はこの部分をコメントアウトしてください
        # header = next(reader)
        # writer.writerow(header)

        for row in reader:
            if len(row) > 0:
                word = row[0]
                pronunciation = pronunciations.get(word, '')
                if pronunciation:
                    # 単語と発音記号を一緒にする（例: word [pronunciation]）
                    word_with_pronunciation = f"{word} {pronunciation}"
                else:
                    word_with_pronunciation = word
                # 第一列を更新
                row[0] = word_with_pronunciation
                writer.writerow(row)

# メイン処理
def main():
    pronunciation_file = r"C:\Users\i1204\OneDrive - 岡山大学\Documents\英語_D\4000 Essential English Words\en_US.txt"  # 発音記号のテキストファイル名
    input_csv = r"C:\Users\i1204\OneDrive - 岡山大学\Documents\英語_D\4000 Essential English Words\4000 Essential English Words 1.csv"  # 元のCSVファイル名
    output_csv = r"C:\Users\i1204\OneDrive - 岡山大学\Documents\英語_D\4000 Essential English Words\output.csv"  # 出力するCSVファイル名

    # 発音記号をロード
    pronunciations = load_pronunciations(pronunciation_file)

    # CSVに発音記号を追加
    add_pronunciations_to_csv(input_csv, output_csv, pronunciations)

    print(f"新しいCSVファイル '{output_csv}' が作成されました。")

if __name__ == '__main__':
    main()
