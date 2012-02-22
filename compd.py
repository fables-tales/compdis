#!/bin/env python

import socket, re

HOST = "localhost"
PORT = 6379

def get_parts(data):
    parts = re.compile('\+?(\d+\.\d+)\s+"([A-Z]+)"\s+"(.*)"')
    matches = parts.match(data)
    if matches is not None:
        return matches.groups()
    return None

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
	timestamp,cmd,key = parts
	print(cmd)
	if cmd in red_mod_coms:
		s.sendall('PUBLISH {0} 2\r\n'.format(key))

