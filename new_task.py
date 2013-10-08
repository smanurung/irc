#!/usr/bin/env python
import pika
import sys

connection=pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel=connection.channel()

message = ' '.join(sys.argv[1:]) or "Hello World!"

#delivery_mode=2 ~> for message persistence
channel.basic_publish(exchange='',routing_key='task_queue',body=message,properties=pika.BasicProperties(delivery_mode=2))

print "[x] Sent %r" % (message,)
connection.close()
