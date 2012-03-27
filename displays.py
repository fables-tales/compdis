#!/bin/env python

import socket, redis, threading, re

HOST = "localhost"
PORT = 6379
DB = 0

BASE = 'org.srobo'

types = ['zone0', 'zone1', 'zone2', 'zone3', 'door']

actor = redis.Redis(host=HOST, port=PORT, db=DB)

def setup():
	print 'Setting up'
	actor.set('{0}.displays.count'.format(BASE), '0')
	for i in range(len(types)):
		actor.zadd('{0}.displays.screens'.format(BASE),types[i],0)
	print 'Setup complete'


setup()


while True:
	pass


