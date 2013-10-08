#!/usr/bin/env python

import pika		#gunakan pika rabbitmq client
import logging	#logging handler

#set logging level
logging.getLogger('pika').setLevel(logging.DEBUG)

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='hello')

channel.basic_publish(exchange='',routing_key='hello',body='Hello smanurung!')

print "[x] Sent 'Hello World!'"

connection.close()
