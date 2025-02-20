FROM python:3.12-slim-bookworm

ENV FLASK_CONTEXT=production
ENV PYTHONUNBUFFERED=1
ENV PATH=$PATH:/home/flaskapp/.local/bin

RUN useradd --create-home --home-dir /home/flaskapp flaskapp

RUN apt-get update && \
    apt-get install -y \
    curl \
    iputils-ping \
    python3-dev \
    build-essential \
    libpq-dev \
    python3-psycopg2 && \
    apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /home/flaskapp

USER flaskapp
RUN mkdir app

COPY ./app ./app
COPY ./app.py .
COPY ./uwsgi.ini .  

ADD requirements.txt ./requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["uwsgi", "--wsgi-file","app.py", "uwsgi.ini"]  