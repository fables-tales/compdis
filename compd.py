#!/bin/env python

import socket

HOST = "localhost"
PORT = 6379

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

red_spec[	'MOVE',
		'RENAME',
		'RENAMENX',
		'SELECT',
		'SHUTDOWN',
		'SLAVEOF',
		'SMOVE'		]

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST,PORT))

s.sendall('MONITOR\r\n')
while True:
	data = s.recv(1024)
	print 'Rec:', repr(data)
	if 'INCR' in repr(data):
		s.sendall('PUBLISH cheese 2\r\n')
