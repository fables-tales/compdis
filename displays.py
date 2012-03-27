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

def print_screens():
	for i in range(len(types)):
		score = actor.zscore('{0}.displays.screens'.format(BASE),types[i])
		if score == 0 or score == None:
			score = 'Not set'
		print('{0}:\t{1}'.format(types[i], score))
	scr = actor.zrange('{0}.displays.screens'.format(BASE),0,-1,False,True)
	if len(scr) == len(types):
		raw_input()
		return
	for i in range(len(scr)):
		str = scr[i][1]
		if scr[i][0] in types:
			continue
		if scr[i][1] == 0 or scr[i][0] == None:
			str = 'Not set'
		print('{0}:\t{1}'.format(scr[i][0],str))
	raw_input()

setup()

def assign():
	for i in range(len(types)):
		val = None
		while val is None:
			score = None
			str = raw_input('{0}: '.format(types[i]))
			if str == '':
				score = actor.zscore('{0}.displays.screens'.format(BASE),types[i])
				if score == None:
					print('No previous, please either give a value or run setup')
					continue
			else:
				try:
					score = int(str)
				except ValueError:
					print('Invalid screen number, please try again')
			val = actor.zadd('{0}.displays.screens'.format(BASE),types[i],score)

while True:
	pass


