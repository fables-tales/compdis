#!/bin/env python

import redis, shlex

HOST = "localhost"
PORT = 6379
DB = 0

BASE = 'org.srobo'

actor = redis.Redis(host=HOST, port=PORT, db=DB)

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

def print_match(match):
	print('Match {0}'.format(match))
	try:
		mat = split_match(actor.lindex('{0}.matches'.format(BASE), match - 1))
	except AttributeError:
		print('There is no expected match {0}'.format(match))
		return
	for i in range(4):
		zone = actor.hgetall('{0}.scores.match.{1}.{2}'.format(BASE,match,i))
		if zone == {}:
			print('Match data not stored for Match {0}, Zone {1}'.format(match,i))
			continue
		print('Zone {0} ({1}): {2}'.format(i,mat['teamz{0}'.format(i)],game_points([0,0,zone['trobot'],zone['tzone'],zone['tbucket'],zone['nbuckets']])))
		print('\tRobot:  {0}'.format(zone['trobot']))
		print('\tZone:   {0}'.format(zone['tzone']))
		print('\tBucket: {0}'.format(zone['tbucket']))
		print('\tNo. Buckets: {0}'.format(zone['nbuckets']))

def score():
	print("Please enter match data (space separated) in the following order:")
	print("Match, Zone, Robot Tokens, Zone Tokens, Bucket Tokens, Bucket count")
	while True:
		str = raw_input("Score: ")
		if str is '':
			return
		try:
			p = get_parts(str)
			if not len(p) is 6:
				print("Incorrect number of values entered. Please try again")
				continue
			for i in range(len(p)):
				int(p[i])
			if actor.hexists('{0}.scores.match.{1}.{2}'.format(BASE,p[0],p[1]),'trobot') or actor.hexists('{0}.scores.match.{1}.{2}'.format(BASE,p[0],p[1]),'tzone') or actor.hexists('{0}.scores.match.{1}.{2}'.format(BASE,p[0],p[1]),'tbucket') or actor.hexists('{0}.scores.match.{1}.{2}'.format(BASE,p[0],p[1]),'nbuckets'):
				print('Some details for this already exist, please check input or use modify mode')
				continue
			actor.hmset('{0}.scores.match.{1}.{2}'.format(BASE,p[0],p[1]),{'trobot':p[2],'tzone':p[3],'tbucket':p[4],'nbuckets':p[5]})
			match = split_match(actor.lindex('{0}.matches'.format(BASE),int(p[0]) - 1))
			actor.incr('{0}.scores.team.{1}'.format(BASE,match['teamz'+p[1]]),game_points(p))
			print('Game Score ({0}): {1}'.format(match['teamz'+p[1]],game_points(p)))
		except ValueError:
			print("Sorry, incorrectly entered. Please try again")

def results():
	while True:
		str = raw_input("Enter match number: ")
		if str is '':
			return
		try:
			print_match(int(str))
		except ValueError:
			print("Invalid match number, please try again")
		match = actor.hgetall('{0}.scores.match.{1}')

def modify():
	print('Modify')
	while True:
		str = raw_input('Match: ')
		if str == '':
			return
		try:
			match = int(str)
		except ValueError:
			print('Invalid match number, please try again')
		print_match(match)
		z = None
		trobot = None
		tzone = None
		tbucket = None
		nbuckets = None
		while z is None:
			str = raw_input('Zone: ')
			if str == '':
				z = -1
			try:
				z = int(str)
			except ValueError:
				print('Invalid zone number, please try again')
		if z == -1:
			continue
		zone = actor.hgetall('{0}.scores.match.{1}.{2}'.format(BASE,match,z))
		if zone == {}:
			print('Match data not stored for Match {0}, Zone {1}\nPlease use score mode to enter new scores'.format(match,z))
			continue
		print('Please enter new values, leave blank for unchanged')
		while trobot is None:
			str = raw_input('Robot: ')
			if str == '':
				trobot = zone['trobot']
				continue
			try:
				trobot = int(str)
			except ValueError:
				print('Invalid number, please try again')
		while tzone is None:
			str = raw_input('Zone: ')
			if str == '':
				tzone = zone['tzone']
				continue
			try:
				tzone = int(str)
			except ValueError:
				print('Invalid number, please try again')
		while tbucket is None:
			str = raw_input('Bucket: ')
			if str == '':
				tbucket = zone['tbucket']
				continue
			try:
				tbucket = int(str)
			except ValueError:
				print('Invalid number, please try again')
		while nbuckets is None:
			str = raw_input('No. Buckets: ')
			if str == '':
				nbuckets = zone['nbuckets']
				continue
			try:
				nbuckets = int(str)
			except ValueError:
				print('Invalid number, please try again')
		actor.hmset('{0}.scores.match.{1}.{2}'.format(BASE,match,z),{'trobot':trobot,'tzone':tzone,'tbucket':tbucket,'nbuckets':nbuckets})
		mat = split_match(actor.lindex('{0}.matches'.format(BASE), match - 1))
		actor.decr('{0}.scores.team.{1}'.format(BASE,mat['teamz{0}'.format(z)]),game_points([match,z,zone['trobot'],zone['tzone'],zone['tbucket'],zone['nbuckets']]))
		actor.incr('{0}.scores.team.{1}'.format(BASE,mat['teamz{0}'.format(z)]),game_points([match,z,trobot,tzone,tbucket,nbuckets]))
		print_match(match)

while True:
	print("Possible commands: \n[S]core\n[M]odify\n[R]esults\n[Q]uit")
	str = raw_input("CMD: ")
	str = str.capitalize()
	if str == 'S' or str == 'Score':
		score()
	elif str == 'M' or str == 'Modify':
		modify()
	elif str == 'R' or str == 'Results':
		results()
	elif str == 'Q' or str == 'Quit':
		quit()
