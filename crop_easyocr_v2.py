import streamlit as st
from streamlit_cropper import st_cropper
from PIL import Image
import numpy as np
import easyocr
import cv2
import pandas as pd
import base64
import sqlite3
from io import BytesIO
import os
import uuid


#ログ用sqlite 
db_path = "./crop_ocr_logs.db"

def sqlite_init(db_path):
    # SQLiteデータベースの初期化とテーブル作成
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS cropped_images (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            image_id TEXT UNIQUE,  -- UUIDとして使用
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            image BLOB
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS crop_ocr_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            image_id TEXT,  -- UUIDとして使用
            text TEXT,
            bbox TEXT,
            score REAL,
            FOREIGN KEY (image_id) REFERENCES cropped_images (image_id)
        )
    ''')
    conn.commit()
    conn.close()

sqlite_init(db_path)



# OCR結果をデータベースに書き込む関数
def write_ocr_results_to_db(image_id, ocr_results):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    
    for result in ocr_results:
        text, bbox, score = result[1], result[0], result[2]
        bbox_str = str(bbox)  # バウンディングボックス情報を文字列に変換
        c.execute("INSERT INTO crop_ocr_results (image_id, text, bbox, score) VALUES (?, ?, ?, ?)", (image_id, text, bbox_str, score))
    
    conn.commit()
    conn.close()

# Cropされた画像をデータベースに保存する関数
def save_cropped_image_to_db(image_id,cropped_image):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    img_data = BytesIO()
    cropped_image.save(img_data, format="PNG")
    
    c.execute("INSERT INTO cropped_images (image_id, image) VALUES (?, ?)", (image_id, img_data.getvalue()))
    conn.commit()
    conn.close()
    
# ...


# 画像を保存するための一時ファイル
temp_image_path = "./temp_cropped_image.png"

# OCRモデルを初期化
reader = easyocr.Reader(['ja', 'en'], model_storage_directory="./model", gpu=False)

# Streamlitアプリの設定
st.set_page_config(page_title="OCR-DEMO", page_icon="📚", layout="wide")

#レイアウト
con_croppwer = st.container()
col1_crop, col2_crop = st.columns(2)
con_execute_ocr = st.container()
con_ocr = st.container()
col1_ocr, col2_ocr = st.columns(2)

# セッションステートを初期化
if 'image' not in st.session_state:
    st.session_state.image = None
if 'ocr_result' not in st.session_state:
    st.session_state.ocr_result = None

# OCR結果をキャッシュ
#@st.cache_data
def perform_ocr(_image):
    result = reader.readtext(np.array(_image))
    return result

# Crop Imageアプリのセクション
with con_croppwer:
    st.header("Crop and OCR Image")

    # Upload an image and set some options for demo purposes
    img_file = st.sidebar.file_uploader(label='Upload a file', type=['png', 'jpg'])
    realtime_update = st.sidebar.checkbox(label="Update in Real Time", value=True)
    box_color = st.sidebar.color_picker(label="Box Color", value='#0000FF')
    aspect_choice = st.sidebar.radio(label="Aspect Ratio", options=["1:1", "16:9", "4:3", "2:3", "Free"])
    aspect_dict = {
        "1:1": (1, 1),
        "16:9": (16, 9),
        "4:3": (4, 3),
        "2:3": (2, 3),
        "Free": None
    }
    aspect_ratio = aspect_dict[aspect_choice]

    if img_file:
        st.session_state.image = Image.open(img_file)

    if st.session_state.image:
        if not realtime_update:
            st.write("Double click to save crop")
        with col1_crop:
            cropped_img = st_cropper(st.session_state.image, realtime_update=realtime_update, box_color=box_color,
                                     aspect_ratio=aspect_ratio)
            cropped_img.save(temp_image_path, format="PNG")


        with col2_crop:
            if os.path.exists(temp_image_path):
                st.subheader("Cropされた画像")
                cropped_img = Image.open(temp_image_path)
                st.image(cropped_img, caption="Cropされた画像", use_column_width=True)

st.markdown("---")
# OCR Imageのセクション
with con_execute_ocr:
    col_btn_1,col_btn_2, col_btn_3= st.columns([1,1,4])
    with col_btn_1:
        execute_ocr = st.button("Run AI-OCR ", help="EasyOCR-ja @cpu/local")
    with col_btn_2:
        chatgpt_ocr = st.button("Run AI-OCR w/ ChatGPT", help="🥺Sorry! ChatGPT4-Vision APIのリリースをお待ちください.")
    with col_btn_3:
        pass

with con_ocr:
    

    if chatgpt_ocr:
        st.write("🥺Sorry! ChatGPT4-Vision APIのリリースまでお待ちください。")
    elif execute_ocr:
        st.markdown("---")
        if st.session_state.image:
            if os.path.exists(temp_image_path):
                cropped_img = Image.open(temp_image_path)
                st.session_state.ocr_result = perform_ocr(cropped_img)
                result = st.session_state.ocr_result



        if result:
            image_with_rectangles = np.array(cropped_img)
            for detection in result:
                text = detection[1]
                bbox = detection[0]
                score = detection[2]
                bbox = np.array(bbox).astype(int)
                image_with_rectangles = cv2.rectangle(image_with_rectangles, (bbox[0][0], bbox[0][1]), (bbox[2][0], bbox[2][1]), (0, 255, 0), 2)

            with col1_ocr:
                st.subheader("矩形を描画した画像")
                st.image(image_with_rectangles, caption="矩形を描画した画像", use_column_width=True)

            with col2_ocr:
                st.subheader("検出結果 [text,座標,score]")
                result_df = pd.DataFrame(result, columns=["bbox", "text", "score"])
                st.dataframe(result_df[["text", "bbox", "score"]])
                csv = result_df[["text", "bbox", "score"]].to_csv(index=False)
                b64 = base64.b64encode(csv.encode()).decode()
                st.markdown(f'<a href="data:file/csv;base64,{b64}" download="result.csv">⬇️結果をダウンロード</a>', unsafe_allow_html=True)


                # 新しいUUIDを生成
                image_id = str(uuid.uuid4()) 
                # クロップされた画像をデータベースに保存
                save_cropped_image_to_db(image_id,cropped_img)
                # OCR結果をデータベースに保存
                write_ocr_results_to_db(image_id, result)
                
                st.text("Save")
