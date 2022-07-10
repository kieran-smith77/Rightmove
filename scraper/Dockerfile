FROM python:3

RUN apt update
RUN apt upgrade -y

WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD [ "python", "./main.py" ]