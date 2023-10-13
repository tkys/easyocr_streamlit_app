import streamlit as st 
import sqlite3
from PIL import Image
from io import BytesIO

# データベースファイルのパス
db_path = "./crop_ocr_logs.db"

# クロップされた画像をデータベースから取得
conn = sqlite3.connect(db_path)
c = conn.cursor()
c.execute("SELECT * FROM cropped_images")
rows = c.fetchall()

# 各クロップ画像ごとに処理
for row in rows:
    image_data = row[3]
    image = Image.open(BytesIO(image_data))
    
    # この画像に対応するOCR結果を取得
    c.execute("SELECT * FROM crop_ocr_results WHERE image_id=?", (row[1],))
    ocr_results = c.fetchall()
    
    for idx, ocr_result in enumerate(ocr_results):
        text, bbox_str, score = ocr_result[2], ocr_result[3], ocr_result[4]
        
        # bbox_str を解析してバウンディングボックス座標を取得
        bbox = eval(bbox_str)
        
        # バウンディングボックス座標を使用してクロップ
        left, top, right, bottom = bbox[0][0], bbox[0][1], bbox[2][0], bbox[2][1]
        cropped_text_image = image.crop((left, top, right, bottom))
        
        # このクロップ画像を処理する（ここで何かしたい処理を追加）
        
        # OCR結果を表示
        st.markdown("---")
        st.write(f"image_UUID: {row[1]}")
        st.write(f"crop_id: {idx}")
        
        col1 ,col2,col3 = st.columns(3)
        with col1:
            st.image(cropped_text_image)
        with col2:
            st.write("text:", text)
        with col3:
            st.text(f"bbox:{bbox}")
            st.write("score:", score)

    
conn.close()
