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

def split_match(data):
	a = data.split(',')
	res = {'mtime':a[0],
	       'teamz0':a[1],
	       'teamz1':a[2],
	       'teamz2':a[3],
	       'teamz3':a[4],
	       'matNo':a[5]}
	return res

def game_points(score):
	total = 0
	total += int(score[2])
	total += 2*int(score[3])
	total += 5*int(score[4])
	if int(score[5]) > 1:
		total *= int(score[5])
	return total

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
		match = split_match(actor.lindex('{0}.matches'.format(BASE),int(p[0]) - 1))
		actor.incr('{0}.scores.team.{1}'.format(BASE,match['teamz'+p[1]]),game_points(p))
		print('Game Score ({0}): {1}'.format(match['teamz'+p[1]],game_points(p)))
	except ValueError:
		print("Sorry, incorrectly entered. Please try again")
