FROM python:3.8.12-slim-buster

WORKDIR /usr/data_upload

COPY requirements.txt .
RUN pip install -r requirements.txt

ADD main.py .
ADD src ./src
RUN mkdir data

ENTRYPOINT ["python", "main.py"]