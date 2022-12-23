FROM python:3.10

EXPOSE 5000

RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y python3-pip

WORKDIR /home/python

RUN pip install pyright

COPY requirements.txt .
RUN pip3 install -r requirements.txt

CMD ["flask", "run", "--host", "0.0.0.0"]
