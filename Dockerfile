FROM alpine:3.8 as models
RUN apk update && apk upgrade && \
    apk add --no-cache bash git openssh
WORKDIR /models
RUN git clone https://huggingface.co/marianbasti/XTTS-v2-argentinian-spanish
ENTRYPOINT ["sleep 10"]

FROM python:3.9 as base
WORKDIR /app
COPY --from=models /models/XTTS-v2-argentinian-spanish .
RUN apt update
RUN apt-get install -y libsndfile1
COPY ./requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt
COPY . /app

ENTRYPOINT ["python"]
CMD ["main.py"]