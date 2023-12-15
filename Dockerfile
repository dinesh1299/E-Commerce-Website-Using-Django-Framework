# Use the official Python image
FROM python:3.10

RUN apt update &&\
    apt-get install -y git

WORKDIR /ecommerce

COPY . /ecommerce

RUN pip install -r requirements.txt

CMD ["python", "/ecommerce/manage.py runserver 0.0.0.0:8000"]
