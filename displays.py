#!/bin/env python

import socket

HOST = "localhost"
PORT = 6379

BASE = 'org.srobo'

subscriber = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
subscriber.connect((HOST,PORT))

actor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
actor.connect((HOST,PORT))

def setup():
	print 'Setting up'
	actor.sendall('LPUSH {0} displays\r\n'.format(BASE))
	actor.sendall('LPUSH {0}.displays count locations\r\n'.format(BASE))
	actor.sendall('SET {0}.displays.count 0\r\n'.format(BASE))
	actor.sendall('LPUSH {0}.displays.locations FL FR BL BR DR\r\n'.format(BASE))
	subscriber.sendall('PSUBSCRIBE {0}.displays.*\r\n'.format(BASE))
	print 'Setup complete'

def new_screen(count):
	actor.sendall('LPUSH {0}.displays screen{1}\r\n'.format(BASE,count))
	actor.sendall('LPUSH {0}.displays.screen{1} state team score\r\n'.format(BASE,count))

setup()

while True:
	pass


