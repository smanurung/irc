#!/usr/bin/env python
import pika, thread, time

#constants
hostname='localhost'

#global variables
connection = pika.BlockingConnection(pika.ConnectionParameters(host=hostname))
channel=connection.channel()
result=channel.queue_declare(exclusive=True)
queue_name=result.method.queue

nick='027'
chList = []

#change to specified name
def changeName(name=''):
	global nick
	if(name.__len__()==0):
		nick='027-KLJ345K245'
	else:
		nick=name
	return

def callback(ch,method,properties,body):
	print "[x] %r" % (body,)

def startListening(dum1,dum2):
	global channel
	print 'Waiting for channel',ch,'...'
	channel.start_consuming()

while 1:
	cmd=raw_input('> ')
	param=cmd.split(' ')
	
	print 'command',param[0]
	if(param[0].strip()=='/EXIT'):
		print "program closed"
		break
	elif(param[0].strip()=='/NICK'):
		if(param.__len__()>1):
#			change as param
			changeName(param[1])
			print "Successfully change nickname to",nick
		else:
#			generate random nickname
			changeName()
			print "Generated random nickname: ",nick
	elif(param[0].strip()=='/JOIN'):
		if(param.__len__()>1):
			ch = param[1]

#			insert channel name to list
			if(not chList.__contains__(ch)):
				chList.append(ch)

#			declare exchange
			x = ch + 'X'
			channel.exchange_declare(exchange=x,type='fanout')

#			bind to queue with random name
			q = ch + 'Q'
			channel.queue_bind(exchange=x,queue=queue_name)
			
#			start listening mode on different thread
			channel.basic_consume(callback,queue=queue_name,no_ack=True)
			try:
				thread.start_new_thread(startListening,('',''))
			except Exception, errtxt:
				print errtxt
				print "Error: unable to start thread"
			print "Successfully join to channel",ch
			time.sleep(1)
		else:
			print "Error Format: /JOIN <channelname>"			
	elif(param[0].strip()=='/LEAVE'):
		if(param.__len__()>1):
			ch = param[1]
			if(chList.__contains__(ch)):
#				delete from chList
				idx = chList.index(ch)
				del chList[idx]
				
#				unbind queue
				x = ch + 'X'
				channel.queue_unbind(exchange=x,queue=queue_name)
				print "Successfully left channel",param[1]
			else:
				print "You never join that channel"
		else:
			print "Error Format: /LEAVE <channelname>"
	elif(param[0][0].strip()=='@'):
		if(param.__len__()>1):
			print "sending to channel",param[0]
		else:
			print "Error Format: NO Text Found. @<channelname> <text>"
