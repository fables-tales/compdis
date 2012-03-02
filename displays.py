#!/bin/env python

import socket, redis, threading, re

HOST = "localhost"
PORT = 6379
DB = 0

BASE = 'org.srobo'

STATE_REG = 'register'
STATE_NOE = 'No Entry'
STATE_LEA = 'League'
STATE_MAT = 'Match'
STATE_SCO = 'Score'

actor = redis.Redis(host=HOST, port=PORT, db=DB)
subscriber = actor.pubsub()

def setup():
	print 'Setting up'
	actor.lpush('{0}'.format(BASE),'displays')
	actor.lpush('{0}.displays'.format(BASE), 'count', 'locations')
	actor.set('{0}.displays.count'.format(BASE), '0')
	actor.lpush('{0}.displays.locations'.format(BASE),'FL','FR','BL','BR','DR')
	print 'Setup complete'

def new_screen(count):
	print 'New Screen {0}'.format(count)
	actor.lpush('{0}.displays'.format(BASE),'screen{0}'.format(count))
	actor.lpush('{0}.displays.screen{1}'.format(BASE,count),'state','team','score')
	actor.set('{0}.displays.screen{1}.state', STATE_REG)

def subscribe():
	subscriber.psubscribe('{0}.displays.*'.format(BASE))
	for msg in subscriber.listen():
		#Decide what to do...
		if (msg['channel'] == '{0}.displays.count'.format(BASE) and re.match('^[0-9]*$',msg['data'])):
			new_screen(msg['data'])

setup()

sub_thread = threading.Thread(target=subscribe)
sub_thread.start()

while True:
	pass


