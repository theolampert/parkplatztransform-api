FROM python:3.9-alpine3.12

COPY ./requirements.txt /app/requirements.txt

RUN \
 apk add --no-cache postgresql-libs geos && \
 apk add --no-cache --virtual .build-deps gcc g++ musl-dev postgresql-dev && \
 python3 -m pip install --quiet -r /app/requirements.txt --no-cache-dir && \
 apk --purge del .build-deps

COPY ./app /app

EXPOSE 80

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]

