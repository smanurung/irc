#!/usr/bin/env python

import pika		#gunakan pika rabbitmq client
import logging	#logging handler
import sys		#akses standard input

#set logging level
logging.getLogger('pika').setLevel(logging.DEBUG)

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='task_queue',durable=True)

message = ' '.join(sys.argv[1:]) or "Hello World!"

#default exchange = direct
#delivery_mode=2 ~> make message persistent
channel.basic_publish(exchange='',routing_key='hello',body=message,properties=pika.BasicProperties(delivery_mode=2,))

print "[x] Sent %r" % (message,)

connection.close()
