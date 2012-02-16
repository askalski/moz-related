#!/usr/bin/python
# -*- coding: UTF-8 -*-

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

#author: Andrzej Skalski

#2DO : feature: if a test hangs, there should be some time counter
# and keyboard shortcut to kill current test and continue

from mctest import mochitest
import sys, datetime, os, subprocess

def main():
	
	if len(sys.argv) < 2:
		print_info()
		sys.exit()
	
	if sys.argv[1] != 'run' and sys.argv[1] != 'analyse':
		print_info()
		sys.exit()
	
	if sys.argv[1] == 'run':
		run()
	
	if sys.argv[1] == 'analyse':
		analyse()

def mochitest_equal(mt1, mt2):
	if not len(set(mt1.d.keys()) - set(mt2.d.keys())) == 0:
		return False
		
	keys = set(mt1.d.keys())
	for key in keys:			
		v1 = mt1.d[key]
		v2 = mt2.d[key]
	
		if not res_equal(v1,v2):
			return False;
		return True

def res_equal(res1, res2):
	if len(res1) != len(res2):
		return False
	
	for i in range(0, len(res1)):
		if res1[i] != res2[i]:
			return False
	
	return True

def analyse():
	if not len(sys.argv) in [3]:
		print_info()
		sys.exit()
		
	testdir = sys.argv[2]
	
	if not os.path.exists(testdir):
		testdir = os.path.join(os.getcwd(), testdir)
		if not os.path.exists(testdir):
			raise Exception ("Testdir not found at \"" + objdir + "\".")
			
	print "Opening testdir \"" + testdir + "\"."
	
	files = os.listdir(testdir)
	
	tests = [f for f in files if f.endswith(".log")]
	
	test_results = {}
	for t in tests:
		print "Loading test \"" + t + "\"..."
		test_results[t] = mochitest(os.path.join(testdir,t))
	
	test_groups = []
	
	for (testname, testresult) in test_results.items():
		if len(test_groups) == 0:
			test_groups = [ ([testname], testresult) ]
			continue
		
		done = False
		# looking for similar results
		for (test_names, result) in test_groups:
			if mochitest_equal(testresult, result):
				test_names.append(testname)
				done = True
				break
		# no such group
		if done:
			break
		test_groups.append( ([testname], testresult) )
		
	if len(test_groups) == 1:
		print "All tests have given the same results. Hurray!"
	else:
		print "There are " + str(len(test_groups)) + " different result groups, as follows:"
		
		for i in range(0, len(test_groups)):
			print "Group #" + str(i) + ":"
			for name in test_groups[i][0]:
				print name
		
		print "You can use difftest to check how the results vary among the groups."
			
def run():
	if not len(sys.argv) in [5,6]:
		print_info()
		sys.exit()
		
	objdir = sys.argv[2]
	tests = sys.argv[3]
	num = int(sys.argv[4])
	
	if not os.path.exists(objdir):
		raise Exception ("Objdir not found at \"" + objdir + "\".")
	
	dnname = tests + " #" + str(num) + " @" + str(datetime.datetime.now())
	
	if len(sys.argv) == 6:
		dnname = sys.argv[5]
	
	fullpath = os.path.join(os.getcwd(), dnname)
	
	if os.path.exists(fullpath):
		raise Exception("Directory \"" + fullpath + "\" already exists.")
		
	os.makedirs(fullpath)
	
	for i in range(1, num+1):
		print "Running test no: " + str(i)
		
		output = None
		try:
			output = subprocess.check_output(["time", "make", "-C",objdir,tests])
		except subprocess.CalledProcessError as cpe:
			output = cpe.output + "\n\nreturn code: " + str(cpe.returncode)
		
		if output == None:
			raise Exception("Unable to capture any output!")
		
		subprocess.call(["mv", os.path.join(objdir, tests + ".log"), os.path.join(fullpath, tests + str(i) + ".log")])
		
		fout = open(os.path.join(fullpath, tests + str(i) + ".output"), "w")
		fout.write(output)
		fout.close()	
	
def print_info():
	print "flakefinder - flaky test finder. usage:"
	print "flakefinder run <obj-dir> <testgroup> <number_of_iterations> [non-default-outputdir]"
	print "flakefinder analyse <testdir>"
	
	
main()

