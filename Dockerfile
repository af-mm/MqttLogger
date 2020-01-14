FROM python:3.7

WORKDIR /MqttLogger

COPY config.py .
COPY mqtt_logger.py .
COPY requirements.txt .

RUN pip3 install -r requirements.txt

ENV MQTT_BROKER_HOST localhost
ENV MQTT_BROKER_PORT 1024
ENV DB_HOST localhost
ENV DB_PORT 1025
ENV DB_USER postgres
ENV DB_PSWD 1234
ENV DB_NAME IoTSystemDB
ENV DB_LAST_VALUES_TABLE mqtt_broker_last_values
ENV DB_HISTORY_TABLE mqtt_broker_history

CMD [ "python3", "./mqtt_logger.py" ]
