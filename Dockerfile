FROM python:3.12-slim-bullseye

WORKDIR /home/app/web/

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y netcat

RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install --default-timeout=100 -r requirements.txt

COPY ./entrypoint.sh .
RUN sed -i 's/\r$//g' /home/app/web/entrypoint.sh
RUN chmod +x /home/app/web/entrypoint.sh

COPY . .

ENTRYPOINT ["/home/app/web/entrypoint.sh"]
