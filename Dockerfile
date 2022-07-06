FROM tiangolo/uwsgi-nginx-flask:flask
WORKDIR /app
COPY website .
RUN pip install -r requirements.txt
