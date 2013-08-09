from kombu import Connection, Exchange, Queue
from pprint import pprint

nova_x = Exchange('nova', type='topic', durable=False)
info_q = Queue('notifications.info', exchange=nova_x, durable=False, 
               routing_key='notifications.info')

def process_msg(body, message):
    print '='*80
    pprint(body)
    message.ack()

connection_string = "amqp://guest:guest@localhost:5672//"
with Connection(connection_string) as conn:
    with conn.Consumer(info_q, callbacks=[process_msg]):
        while True:
            try:
                conn.drain_events()
            except KeyboardInterrupt:
                break
