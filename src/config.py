import os

CFG = {
    'mqtt': {
        'host': os.getenv('MQTT_BROKER_HOST', 'localhost'),
        'port': int(os.getenv('MQTT_BROKER_PORT', '1024')),
        'login': os.getenv('MQTT_LOGIN', 'MqttLogger'),
        'password': os.getenv('MQTT_PSWD', '')
    },
    'db': {
        'host': os.getenv('DB_HOST', 'localhost'),
        'port': int(os.getenv('DB_PORT', '1025')),
        'user': os.getenv('DB_USER', 'postgres'),
        'password': os.getenv('DB_PSWD', '1234'),
        'dbname': os.getenv('DB_NAME', 'IoTSystemDB'),
        'table_last_values': os.getenv('DB_LAST_VALUES_TABLE', 'mqtt_broker_last_values'),
        'table_history': os.getenv('DB_HISTORY_TABLE', 'mqtt_broker_history')
    }
}

print(CFG)
