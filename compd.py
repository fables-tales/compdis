#!/bin/env python

import socket, re, shlex

HOST = "localhost"
PORT = 6379

def get_parts(data):
    lexer = shlex.shlex(data, posix=True)
    lexer.whitespace_split = True
    return tuple(lexer)

def pub_all():
	s.sendall('PUBLISH cheese 0')

def move():
	print('Moving')

red_mod_coms = ['APPEND',
		'BLPOP',
		'BRPOP',
		'BRPOPLPUSH',
		'DECR',
		'DECRBY',
		'DEL',
		'FLUSHALL',
		'FLUSHDB',
		'HDEL',
		'HINCRBY',
		'HMSET',
		'HSET',
		'HSETNX',
		'INCR',
		'INCRBY',
		'LINSERT',
		'LPOP',
		'LPUSH',
		'LPUSHX',
		'LREM',
		'LSET',
		'LTRIM',
		'MSET',
		'MSETNX',
		'RPOP',
		'RPOPLPUSH',
		'RPUSH',
		'RPUSHX',
		'SADD',
		'SDIFFSTORE',
		'SET',
		'SETBIT',
		'SETEX',
		'SETNX',
		'SETRANGE',
		'SINTERSET',
		'SORT',
		'SPOP',
		'SREM',
		'SUNIONSTORE',
		'ZADD',
		'ZINCRBY',
		'ZINTERSTORE',
		'ZREM',
		'ZREMRANGEBYRANK',
		'ZREMRANGEBYSCORE',
		'ZUNIONSTORE'	]

red_spec[	'MOVE':move(),
		'RENAME':move(),
		'RENAMENX':move(),
		'SELECT':pub_all(),
		'SHUTDOWN':quit(),
		'SLAVEOF':pub_all(),
		'SMOVE':move()	]

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST,PORT))

s.sendall('MONITOR\r\n')
while True:
	data = s.recv(1024)
	print 'Rec:', repr(data)
	parts = get_parts(data)
	print parts
	if parts is None:
		continue
	if parts[1].upper() in red_mod_coms:
		for i in range(red_mod_coms)
		s.sendall('PUBLISH {0} UPDATE\r\n'.format(parts[2]))

