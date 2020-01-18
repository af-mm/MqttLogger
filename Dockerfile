FROM python:3.7

WORKDIR /MqttLogger

COPY src requirements.txt ./

RUN pip3 install -r requirements.txt

ENV MQTT_BROKER_HOST=localhost \
	MQTT_BROKER_PORT=1024 \
	MQTT_LOGIN=MqttLogger \
	MQTT_PSWD=None \
	DB_HOST=localhost \
	DB_PORT=1025 \
	DB_USER=postgres \
	DB_PSWD=1234 \
	DB_NAME=IoTSystemDB \
	DB_LAST_VALUES_TABLE=mqtt_broker_last_values \
	DB_HISTORY_TABLE=mqtt_broker_history

CMD [ "python3", "-u", "./mqtt_logger.py" ]
