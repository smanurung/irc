#!/usr/bin/env python
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

#queue declaration is idempotent
channel.queue_declare(queue='hello');

print '[*] waiting for messages. to exit press CTRL + C'

def callback(ch,method,properties,body):
	print "[x] Received %r" % (body,)

#queue must have existed; if not, error
channel.basic_consume(callback,queue='hello',no_ack=True)

#never-ending loop
channel.start_consuming()
