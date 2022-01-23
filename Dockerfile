FROM python:3.8-slim-buster

COPY . .

WORKDIR /

CMD ["python", "log_parser/log_parser.py"]