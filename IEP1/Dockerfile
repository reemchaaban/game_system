FROM python:3.10-slim

WORKDIR /app

COPY ./app.py /app/app.py
COPY ./utils /app/utils
COPY ./model /app/model
COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["python", "app.py"]