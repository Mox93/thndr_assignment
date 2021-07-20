FROM python:3

RUN pip install --upgrade pip && pip install paho-mqtt pydantic[dotenv] requests

ADD consumer.py /

ADD settings.py /

CMD [ "python", "/consumer.py" ]
