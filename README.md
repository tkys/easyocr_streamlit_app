# easyocr_streamlit_app

### get model 

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
