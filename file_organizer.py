"""ファイル自動振り分けツール

指定したフォルダ内のファイルを、拡張子ごとのフォルダに振り分けます。

使い方:
    1. このファイルと同じ場所に test_folder フォルダを作り、整理したいファイルを入れる
    2. python file_organizer.py を実行する
       (初期設定は確認のみで、ファイルは移動しません)
    3. 表示された内容を確認し、問題なければ DRY_RUN を False に変更して再実行する
"""

from pathlib import Path
import shutil

# ---------- 設定 ----------

# 整理するフォルダ(このファイルと同じ場所にある test_folder)
TARGET_DIR = Path(__file__).parent / "test_folder"

# True: 何が起きるか表示するだけで、ファイルは移動しない
# False: 実際にファイルを移動する
DRY_RUN = True

# 拡張子と振り分け先フォルダ名の対応表
CATEGORIES = {
    ".jpg": "画像", ".jpeg": "画像", ".png": "画像", ".gif": "画像",
    ".pdf": "PDF",
    ".docx": "Word", ".doc": "Word",
    ".xlsx": "Excel", ".xls": "Excel", ".csv": "CSV",
    ".pptx": "PowerPoint",
    ".txt": "テキスト",
    ".zip": "圧縮ファイル",
    ".mp4": "動画", ".mov": "動画",
    ".mp3": "音声",
}
OTHER_FOLDER = "その他"  # 対応表にない拡張子の振り分け先


# ---------- 処理 ----------

def unique_path(dest):
    """移動先に同名ファイルがあるとき、_1, _2 と番号を付けて上書きを避ける。"""
    if not dest.exists():
        return dest
    number = 1
    while True:
        candidate = dest.with_name(f"{dest.stem}_{number}{dest.suffix}")
        if not candidate.exists():
            return candidate
        number += 1


def organize(folder):
    """フォルダ内のファイルを、拡張子ごとのフォルダに振り分ける。"""
    if not folder.exists():
        print(f"フォルダが見つかりません: {folder}")
        return

    count = 0
    for item in folder.iterdir():
        # フォルダと隠しファイル(.で始まるもの)は対象外
        if not item.is_file() or item.name.startswith("."):
            continue

        # 拡張子は小文字にそろえる(.JPG も .jpg と同じ扱い)
        ext = item.suffix.lower()
        folder_name = CATEGORIES.get(ext, OTHER_FOLDER)

        dest_dir = folder / folder_name
        dest = unique_path(dest_dir / item.name)

        print(f"{item.name}  →  {folder_name}/{dest.name}")

        if not DRY_RUN:
            dest_dir.mkdir(exist_ok=True)
            shutil.move(str(item), str(dest))
        count += 1

    result = "確認のみ(ファイルは移動していません)" if DRY_RUN else "移動完了"
    print(f"\n{count} 件 {result}")


if __name__ == "__main__":
    organize(TARGET_DIR)