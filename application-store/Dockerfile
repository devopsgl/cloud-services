FROM python:alpine3.20
WORKDIR /app
COPY *.py ./
COPY requirements.txt ./
RUN pip install -r requirements.txt

ENTRYPOINT [ "python3", "main.py" ]