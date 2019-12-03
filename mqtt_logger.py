import paho.mqtt.client as mqtt
import psycopg2
from psycopg2.extras import NamedTupleCursor
from datetime import datetime
from config import CFG

CACHE = []

def on_connect(client, userdata, flags, rc):
    print('Connected with result code {}'.format(rc))
    
    client.subscribe([('#', 0)])
    
def on_message(client, userdata, message):
    global TS
    global dbConn
    
    topic = message.topic
    payload = message.payload.decode('utf8')
    
    print('{}: {}'.format(topic, payload))
    
    CACHE.append((
        datetime.now(),
        topic,
        payload
    ))

client = mqtt.Client();
client.on_connect = on_connect
client.on_message = on_message
client.connect( CFG['mqtt']['host'],
                CFG['mqtt']['port'],
                60)

dbConn = psycopg2.connect(  host=CFG['db']['host'],
                            port=CFG['db']['port'],
                            dbname=CFG['db']['dbname'],
                            user=CFG['db']['user'],
                            password=CFG['db']['password'])
print('Connected to database')

while True:
    if len(CACHE) > 0:
        cursor = dbConn.cursor(cursor_factory=NamedTupleCursor)

        for row in CACHE:
            ts, topic, payload = row
            
            cursor.execute('SELECT COUNT(topic) FROM device.external_mqtt_broker_last_values WHERE topic=%s', (topic, ))
            r = cursor.fetchall()
            
            if r[0].count == 0:
                cursor.execute('INSERT INTO device.external_mqtt_broker_last_values(topic,message,ts) VALUES(%s,%s,%s)',
                               (topic, payload, ts))
            else:
                cursor.execute('UPDATE device.external_mqtt_broker_last_values SET message=%s, ts=%s WHERE topic=%s',
                               (payload, ts, topic))
            
            cursor.execute('INSERT INTO device.external_mqtt_broker_history(ts,topic,message) values(%s,%s,%s)', (ts, topic, payload))
            
        cursor.close()
        dbConn.commit()
        CACHE = []
        
    client.loop(0.01)

dbConn.close()

