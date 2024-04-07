FROM python:3.12.0-slim-bullseye

WORKDIR /app

COPY ./requirements.txt .
RUN pip install -r ./requirements.txt -i https://mirrors.aliyun.com/pypi/simple/ --no-cache-dir

COPY . .

CMD ["gunicorn", "main:app", "-c", "gunicorn.py"]