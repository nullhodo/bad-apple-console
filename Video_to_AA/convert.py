import cv2
import json

def convert_video_to_ascii_db(
    video_path: str,
    output_path: str,
    output_width: int,
    output_height: int,
    char_black: str = "Ｘ",
    # char_black: str = '■',
    char_white: str = "　",
):
    """
    白黒動画をフレームごとにアスキーアートに変換し、JSONファイルに保存する。

    Args:
        video_path (str): 入力する動画ファイルのパス。
        output_path (str): 出力するJSONファイルのパス。
        output_width (int): アスキーアートの幅（文字数）。
        output_height (int): アスキーアートの高さ（行数）。
        char_black (str, optional): 黒い部分に割り当てる文字。デフォルトは 'Ｘ'。
        char_white (str, optional): 白い部分に割り当てる文字。デフォルトは '　'(全角スペース)。
    """
    # 動画ファイルを読み込む
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"エラー: 動画ファイル '{video_path}' を開けません。")
        return

    # 全フレームのアスキーアートを格納するリスト
    all_ascii_frames = []

    print("動画の変換を開始します……")

    while True:
        # フレームを1枚読み込む
        ret, frame = cap.read()

        # 動画の終端に達したらループを抜ける
        if not ret:
            break

        # 1. 解像度を指定サイズに変更
        resized_frame = cv2.resize(
            frame, (output_width, output_height), interpolation=cv2.INTER_AREA
        )

        # 2. グレースケールに変換
        gray_frame = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2GRAY)

        # 3. 2値化で完全な白黒に変換
        # ピクセル値が127より大きい場合は255、そうでなければ0に
        _, binary_frame = cv2.threshold(gray_frame, 127, 255, cv2.THRESH_BINARY)

        # 現在のフレームのアスキーアートを格納する文字列
        ascii_frame_str = ""

        # 4. ピクセルを文字に変換
        for row in binary_frame:
            for pixel_value in row:
                if pixel_value == 0:  # 黒
                    ascii_frame_str += char_black
                else:  # 白
                    ascii_frame_str += char_white
            # 行の終わりで改行文字を追加
            ascii_frame_str += "\n"

        # リストに完成したフレームを追加
        all_ascii_frames.append(ascii_frame_str)

    # ビデオキャプチャを解放
    cap.release()

    # 5. データベース形式で保存
    db_content = {
        "settings": {
            "width": output_width,
            "height": output_height,
            "char_black": char_black,
            "char_white": char_white,
        },
        "frame_count": len(all_ascii_frames),
        "frames": all_ascii_frames,
    }

    try:
        with open(output_path, "w", encoding="utf-8") as f:
            # ensure_ascii=Falseで全角文字をそのまま保存
            json.dump(db_content, f, ensure_ascii=False, indent=2)
        print(f"変換が完了し、'{output_path}' に保存しました。")
    except IOError as e:
        print(f"エラー: ファイル '{output_path}' の書き込みに失敗しました。詳細: {e}")


if __name__ == "__main__":
    # --- 設定項目 ---
    INPUT_VIDEO = "original.mp4"  # ここに変換したい動画のパスを指定
    INPUT_VIDEO = "INPUTVIDEOPATH"

    OUTPUT_JSON = "OUTPUTJSONPATH"
    """
    ASCII_WIDTH = 80  # アスキーアートの幅
    ASCII_HEIGHT = 45 # アスキーアートの高さ
    """
    ASCII_WIDTH = 89  # アスキーアートの幅
    ASCII_HEIGHT = 50  # アスキーアートの高さ

    # 関数を実行
    convert_video_to_ascii_db(
        video_path=INPUT_VIDEO,
        output_path=OUTPUT_JSON,
        output_width=ASCII_WIDTH,
        output_height=ASCII_HEIGHT,
    )
