#!/usr/bin/python
# -*- coding: UTF-8 -*-

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

#author: Andrzej Skalski

import sys, re

class mochitest:
	def __init__(self, filename):		
		self.regex_swaps = [
			('address', 'address: 0x([0-9]|[a-f]){12}', 'address: *removed*'),
			('at', '@ 0x([0-9]|[a-f]){12}','@ *removed*'),
			('ms', '[0-9]+ms', '*removed*ms')
			]
			
		self.d = {}
		self.l = {}
		
		self.loadFromFile(filename)

	def processLine(self, line):
		sline = line.split(" | ")
		
		if len(sline) not in [2,3]:
			raise Exception('Line division failed in "' + line + '"')
			
		number = sline[0]
		number = int(number[0:number.find(" ")])
		
		prefix = sline[0]
		message = prefix[prefix.find(' ') + 1:]
		if len(sline) == 3:
			message += " | " + sline[2]
		
		for regex_swap in self.regex_swaps:
			message = re.sub(regex_swap[1], regex_swap[2], message)
		
		testname = sline[1].strip()
		
		if testname in self.d.keys():
			self.d[testname].append(message)
			self.l[testname].append(number)
		else:
			self.d[testname] = [message]
			self.l[testname] = [number]
	
	def get_right_lines(self, fle):
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

	def loadFromFile(self, filename):
		f = open(filename, "r")
		rl = self.get_right_lines(f)
		for line in rl:
			#these two tests make sure that we process only test-results
			if line.startswith("0 INFO SimpleTest START"):
				continue
			if line.strip().endswith("Shutdown"):
				break				
			self.processLine(line)	
		f.close()
		
