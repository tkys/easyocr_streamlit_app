# easyocr_streamlit_app



[OCR-DEMO-Google-Chrome-2023-10-13-14-29-31.webm](https://github.com/tkys/easyocr_streamlit_app/assets/24400946/67328609-fde4-4305-ae5b-061683d4197c)


- [EasyOCR](https://github.com/JaidedAI/EasyOCR) :OCR
- [Streamlit-cropper](https://github.com/turner-anderson/streamlit-cropper) : to crop target image


## 0. get pre-trained ocr-language-model files

```
$ mkdir ./model

#japanese model
$ wget https://github.com/JaidedAI/EasyOCR/releases/download/v1.3/japanese_g2.zip
$ unzip japanese_g2.zip -d ./model

#english model
$ wget https://github.com/JaidedAI/EasyOCR/releases/download/v1.3/english_g2.zip
$ unzip english_g2.zip -d ./model

```
## 1. build docker image

```
$ docker build  --tag crop_easy_ocr .
```


## 2. run app
```
$ docker run -it -p 8501:8501  crop_easy_ocr:latest
```

Go to [http://localhost:8501](http://localhost:8501)



---

todo next 
- [x] docker image
- [ ] with ChatGPT4
