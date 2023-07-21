# easyocr_streamlit_app

[OCR-DEMO.webm](https://github.com/tkys/easyocr_streamlit_app/assets/24400946/daab04f1-8dbc-4b98-b245-6e55a2549df9)

### get pre-trained ocr-language-model files

```
mkdir ./model

#japanese model
wget https://github.com/JaidedAI/EasyOCR/releases/download/v1.3/japanese_g2.zip
unzip japanese_g2.zip -d ./model

#english model
wget https://github.com/JaidedAI/EasyOCR/releases/download/v1.3/english_g2.zip
unzip english_g2.zip -d ./model

```

### run app
```
streamlit run app.py
```
