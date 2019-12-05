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
        datetime.utcnow(),
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

countLastValueTopicQuery = 'SELECT COUNT(topic) FROM {} WHERE topic=%s'.format(CFG['db']['table_last_values'])
insertLastValueQuery = 'INSERT INTO {}(topic,message,ts) VALUES(%s,%s,%s)'.format(CFG['db']['table_last_values'])
updateLastValueQuery = 'UPDATE {} SET message=%s, ts=%s WHERE topic=%s'.format(CFG['db']['table_last_values'])
insertHistoryQuery = 'INSERT INTO {}(ts,topic,message) values(%s,%s,%s)'.format(CFG['db']['table_history'])
    
while True:    
    if len(CACHE) > 0:
        cursor = dbConn.cursor(cursor_factory=NamedTupleCursor)

        for row in CACHE:
            ts, topic, payload = row
            
            cursor.execute(countLastValueTopicQuery, (topic, ))
            r = cursor.fetchall()
            
            if r[0].count == 0:
                cursor.execute(insertLastValueQuery, (topic, payload, ts))
            else:
                cursor.execute(updateLastValueQuery, (payload, ts, topic))
            
            cursor.execute(insertHistoryQuery, (ts, topic, payload))
            
        dbConn.commit()
        cursor.close()
        CACHE = []
        
    client.loop(0.01)

dbConn.close()

