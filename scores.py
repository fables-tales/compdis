#!/bin/env python

import redis, shlex

HOST = "localhost"
PORT = 6379
DB = 0

BASE = 'org.srobo'

actor = redis.Redis(host=HOST, port=PORT, db=DB)

print("Please enter match data (space separated) in the following order:")
print("Match, Zone, Robot Tokens, Zone Tokens, Bucket Tokens, Bucket count")

def get_parts(data):
	lexer = shlex.shlex(data, posix=True)
	lexer.whitespace_split = True
	return tuple(lexer)

while True:
	str = raw_input("Score: ")
	try:
		p = get_parts(str)
		if not len(p) is 6:
			print("Incorrect number of values entered. Please try again")
			continue
		for i in range(len(p)):
			int(p[i])
		actor.hmset('{0}.scores.match.{1}.{2}'.format(BASE,p[0],p[1]),{'trobot':p[2],'tzone':p[3],'tbucket':p[4],'nbuckets':p[5]})
		print(p)
	except ValueError:
		print("Sorry, incorrectly entered. Please try again")
