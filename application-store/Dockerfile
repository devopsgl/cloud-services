FROM python:alpine3.20
WORKDIR /app
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY *.py ./
ENTRYPOINT [ "python3", "main.py" ]