#!/usr/bin/python
# -*- coding: UTF-8 -*-

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

#author: Andrzej Skalski

import sys, re, difflib

addr_regex = 'address: 0x([0-9]|[a-f]){12}'
addr_replacement = 'address: *removed*'

at_regex = '@ 0x([0-9]|[a-f]){12}'
at_replacement = '@ *removed*'

ms_regex = '[0-9]+ms'
ms_replacement = '*removed*ms'

def processLine(line, d):
	sline = line.split(" | ")
	
	if len(sline) not in [2,3]:
		print "Line division failed in"
		print line
		sys.exit(1)
		
	try:
		number = sline[0]
		number = int(number[0:number.find(" ")])
	except Exception as e:
		print '"' + line + '"'
		print e
		sys.exit(1)
	#d[number] = line
	
	prefix = sline[0]
	message = prefix[prefix.find(' ') + 1:]
	if len(sline) == 3:
		message += " | " + sline[2]
	
	message = re.sub(addr_regex, addr_replacement, message)
	message = re.sub(at_regex, at_replacement, message)
	message = re.sub(ms_regex, ms_replacement, message)
	testname = sline[1].strip()
	
	if testname in d.keys():
		d[testname].append(message)
	else:
		d[testname] = [message]
	

def get_right_lines(fle):
	rl = []
	right_line = ''
	for line in fle:		
		if line[0] in [str(x) for x in range(0,10)]:
			if len(right_line) > 0:
				rl.append(right_line)
			right_line = line
		else:
			right_line = right_line + line
	rl.append(right_line)
	return rl

def processFile(filename, dictionary):
	try:	
		f = open(filename, "r")
		rl = get_right_lines(f)
		for line in rl:
			#these two tests make sure that we process only test-results
			if line.startswith("0 INFO SimpleTest START"):
				continue
			if line.strip().endswith("Shutdown"):
				break
				
			processLine(line, dictionary)
			
		f.close()
	except Exception as e:
		print e
			

def res_equal(res1, res2):
	if len(res1) != len(res2):
		return False
	
	for i in range(0, len(res1)):
		if res1[i] != res2[i]:
			return False
	
	return True

#main code:

if len(sys.argv) < 3:
	print "Not enough arguments. You need to provide two files."
	sys.exit(1)
if len(sys.argv) > 3:
	print "Too many arguments. Program can process only two files."
	sys.exit(1)

f1d = {}
f2d = {}

processFile(sys.argv[1], f1d)
processFile(sys.argv[2], f2d)

keys = set(f1d.keys()) and set(f2d.keys())

for key in keys:	
	if key not in f1d:
		print 'no value for "' + str(key) + '" in "' + sys.argv[1] + '"'
		continue
	if key not in f2d:
		print 'no value for "' + str(key) + '" in "' + sys.argv[2] + '"'
		continue
		
	v1 = f1d[key]
	v2 = f2d[key]
	
	if not res_equal(v1,v2):
		print 'test results for "' + str(key) + '" differ. Diff:'
		for line in difflib.ndiff(v1,v2):
			print line,
		print '\n\n'
	
	#if v1 != v2:
	#	print 'test results for "' + str(key) + '" differs.'
	#	print '@' + v1 + '@'
	#	print '#' + v2 + '#'
	#	sys.exit(1)
