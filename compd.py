#!/bin/env python

import socket

HOST = "localhost"
PORT = 6379

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST,PORT))

s.sendall('MONITOR\r\n')
while True:
	data = s.recv(1024)
	print 'Rec:', repr(data)
	if 'INCR' in repr(data):
		s.sendall('PUBLISH cheese 2\r\n')
