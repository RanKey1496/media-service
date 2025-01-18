FROM python:3.9 as base
WORKDIR /app
RUN apt update
COPY ./requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt
COPY . /app

CMD ["python", "-u","src/main.py"]