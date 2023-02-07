FROM python:3.9.16-slim-buster
ENV secret=
ENV DATABASE_USERNAME=
ENV DATABASE_PORT=
ENV DATABASE_HOSTNAME=
ENV DATABASE_PASSWORD=
ENV DATABASE_NAME=
ENV openapi_url='/openapi/v1/'
ENV docs_url='/docs'
ENV redoc_url='/redoc'
WORKDIR /code
COPY ./requirements.txt /code/requirements.txt
RUN apt-get update -y
RUN apt-get install -y --no-install-recommends curl gcc g++ gnupg unixodbc-dev
RUN apt-get install default-libmysqlclient-dev build-essential -y
RUN pip install --no-cache-dir -r /code/requirements.txt
COPY ./app /code/app
COPY ./migrations /code/migrations
COPY ./alembic.ini /code/alembic.ini
COPY ./ssl /code/ssl
RUN alembic upgrade head
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080", "--ssl-keyfile", "/code/ssl/localhost.key", "--ssl-certfile", "/code/ssl/localhost.crt", "--log-config", "log.ini"]