FROM python:3.12.7-alpine3.20

COPY ./requirements.txt /requirements.txt

RUN apk add --no-cache bash curl tzdata
RUN apk add --no-cache --virtual .build-deps gcc libc-dev linux-headers
RUN apk add --update busybox-suid
RUN rm -rf /var/cache/apk/*
RUN mkdir -p /etc/cron.d
RUN pip install -r /requirements.txt

RUN mkdir /app
WORKDIR /app
COPY ./task.py /app/task.py

RUN chmod +x /app/task.py

RUN echo "0 * * * * python /app/task.py >> /var/log/cron.log 2>&1" > /etc/cron.d/task-cron && \
    chmod 0644 /etc/cron.d/task-cron && \
    crontab /etc/cron.d/task-cron && \
    touch /var/log/cron.log

CMD ["sh", "-c", "sleep 60 && crond -f"]
