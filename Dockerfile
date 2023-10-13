FROM ubuntu:22.04

WORKDIR /app

RUN apt-get update && \
    apt-get -y upgrade

RUN apt-get install -y python3-pip
RUN  pip list

COPY requirements.txt /app
RUN  pip install -r requirements.txt

COPY ./ /app

EXPOSE 8501

ENTRYPOINT ["streamlit", "run"]
CMD ["crop_easyocr_v2.py" ,"--server.port" , "8501" ]
