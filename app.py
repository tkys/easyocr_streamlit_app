import numpy as np
import streamlit as st
import easyocr
import cv2
import pandas as pd
import base64
from PIL import Image

# OCRモデルを初期化
reader = easyocr.Reader(['ja', 'en'],
                        model_storage_directory="./model",
                        gpu=False)

# Streamlitアプリの設定
st.set_page_config(
    page_title="OCR-DEMO",
    page_icon="📚",
    layout="wide"
)


st.sidebar.title("📚OCR-DEMO")

st.sidebar.markdown(
    """
    このアプリでは、アップロードした画像中のテキストを自動的に検出し、テーブルとして表示します。\n
    """
)

st.sidebar.markdown(
    """
    ---
    """
)
# 言語の選択
languages = st.sidebar.multiselect("OCRに使用する言語を選択してください", ['ja', 'en'], default=['ja'])

# 画像ファイルのアップロード
uploaded_file = st.sidebar.file_uploader("画像をアップロードしてください。", type=['jpg', 'png'])

# ページのタイトルと説明を表示
st.title("OCR-DEMO")

if uploaded_file is not None:
    # アップロードされた画像を読み込む
    image = Image.open(uploaded_file)

    # 画像を表示
    col1, col2, col3 = st.columns(3)
    with col1:
        st.subheader("アップロードされた画像")
        st.image(image, use_column_width=True)

    # 画像のコピーを作成して、矩形を描画
    image_with_rectangles = np.array(image.copy())

    # OCRを実行し、結果を取得
    result = reader.readtext(image_with_rectangles)

    # 検出結果の表示
    with col3:
        st.subheader("検出結果 [text,座標,score]")
        # 結果をテーブル形式で表示
        result_df = pd.DataFrame(result, columns=["bbox", "text", "score"])
        #result_df['id'] = result_df.index
        st.dataframe(result_df[["text", "bbox", "score"]])

    for detection in result:
        # 文字列、座標、スコアの取得
        text = detection[1]
        bbox = detection[0]
        score = detection[2]

        # 矩形を描画
        bbox = np.array(bbox).astype(int)
        cv2.rectangle(image_with_rectangles, (bbox[0][0], bbox[0][1]), (bbox[2][0], bbox[2][1]), (0, 255, 0), 2)

    # 矩形を描画した画像を表示
    with col2:
        st.subheader("矩形を描画した画像")
        st.image(image_with_rectangles, use_column_width=True)

    # 結果をCSVに保存してダウンロードリンクを表示

        st.markdown("---")
        csv = result_df[["text", "bbox", "score"]].to_csv(index=False)
        b64 = base64.b64encode(csv.encode()).decode()
        st.markdown(f'<a href="data:file/csv;base64,{b64}" download="result.csv">⬇️結果をダウンロード</a>', unsafe_allow_html=True)
