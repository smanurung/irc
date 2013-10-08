#!/usr/bin/env python
import pika
import time	#memanggil method sleep

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

#queue declaration is idempotent
channel.queue_declare(queue='task_queue',durable=True);

print '[*] waiting for messages. to exit press CTRL + C'

def callback(ch,method,properties,body):
	print "[x] Received %r" % (body,)
	time.sleep(body.count('.'))
	print "[x] Done"
	ch.basic_ack(delivery_tag=method.delivery_tag)	#each worker must acknowledge their results

channel.basic_qos(prefetch_count=1)

#queue must have existed; if not, error
channel.basic_consume(callback,queue='task_queue')

#never-ending loop
channel.start_consuming()
