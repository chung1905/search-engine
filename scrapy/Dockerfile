FROM python:3-alpine

WORKDIR /usr/src/app

ARG pkgs=".build-deps gcc musl-dev jpeg-dev zlib-dev libffi-dev cairo-dev pango-dev gdk-pixbuf-dev libxml2-dev libxslt-dev libressl-dev python3-dev"
RUN apk add --no-cache --virtual ${pkgs}
RUN pip install --no-cache-dir scrapy pymongo

CMD [ "scrapy", "crawl", "wikipedia_com",  "-o", "/usr/src/data/wikipedia_com.jsonl", "-t", "jsonlines" ]
