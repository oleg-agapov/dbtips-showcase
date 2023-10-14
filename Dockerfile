FROM python:3.11
COPY requirements.txt /app/
WORKDIR /app
RUN pip install -r requirements.txt
ENTRYPOINT [ "bash" ]
