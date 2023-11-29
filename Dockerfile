FROM python:3.12

RUN apt-get update && apt-get install -y \
    wireguard

EXPOSE 8000

COPY . /app

WORKDIR /app

RUN pip install -r requirements.txt 

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
