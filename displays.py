#!/bin/env python

import socket, redis

HOST = "localhost"
PORT = 6379
DB = 0

BASE = 'org.srobo'

actor = redis.Redis(host=HOST, port=PORT, db=DB)
subscriber = actor.pubsub()

def setup():
	print 'Setting up'
	actor.lpush('{0} displays'.format(BASE))
	actor.lpush('{0}.displays count locations'.format(BASE))
	actor.set('{0}.displays.count 0'.format(BASE))
	actor.lpush('{0}.displays.locations FL FR BL BR DR'.format(BASE))
	subscriber.psubscribe('{0}.displays.*'.format(BASE))
	print 'Setup complete'

def new_screen(count):
	actor.lpush('{0}.displays screen{1}'.format(BASE,count))
	actor.lpush('{0}.displays.screen{1} state team score'.format(BASE,count))

setup()

while True:
	pass


