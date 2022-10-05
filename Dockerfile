FROM python:3.9
ENV secret=
ENV DATABASE_USERNAME=
ENV DATABASE_PORT=
ENV DATABASE_HOSTNAME=
ENV DATABASE_PASSWORD=
ENV DATABASE_NAME=
WORKDIR /code
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
COPY ./app /code/app
COPY ./migrations /code/migrations
COPY ./alembic.ini /code/alembic.ini
COPY ./ssl /code/ssl
RUN alembic upgrade head
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080", "--ssl-keyfile", "./localhost.key", "--ssl-certfile", "./localhost.crt"]