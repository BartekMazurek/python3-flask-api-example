FROM python:3.10

RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y python3-pip

WORKDIR /home/python

RUN pip install pyright

COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY . .

CMD ["python3", "app.py"]
