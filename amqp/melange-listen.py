from kombu import Connection, Exchange, Queue
from kombu.pools import connections
import kombu.connection
from pprint import pprint

options = {'queue_userid': 'guest', 'queue_virtual_host': '/', 'queue_hostname': 'localhost', 'port': 5672, 'ssl': False, 'queue_port': '5672', 'queue_transport': 'memory', 'queue_ssl': 'False', 'queue_password': 'guest'}
conn = connections[kombu.connection.BrokerConnection(
                                **options)].acquire()
queue = conn.SimpleQueue("melange_notifications.info", no_ack=False)

def process_message(body, message):
    print '='*80
    pprint(body)
    message.ack()

while True:
    try:
        msg = queue.get(block=True)
        body = msg.payload
        process_message(msg.body, msg)
    except KeyboardInterrupt:
        break
