FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

COPY ./requirements.txt /app/

RUN pip install --upgrade pip && pip install -r requirements.txt

ENV MODULE_NAME="app"
ENV WORKER_CLASS="uvicorn.workers.UvicornH11Worker"

COPY ./app /app/app
