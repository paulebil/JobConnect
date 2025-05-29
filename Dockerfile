FROM python:3.12.3-slim

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

COPY ./requirements.txt /usr/src/app/

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . /usr/src/app/

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
