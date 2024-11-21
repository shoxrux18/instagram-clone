FROM python:3.12-slim-bullseye

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y netcat

RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install --default-timeout=100 -r requirements.txt

COPY ./entrypoint.sh .
RUN sed -i 's/\r$//g' /usr/src/app/entrypoint.sh
RUN chmod +x /usr/src/app/entrypoint.sh

COPY . .

ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
