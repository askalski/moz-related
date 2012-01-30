#!/usr/bin/python2.7
# -*- coding: UTF-8 -*-

import sys
import codecs

fstates = codecs.open("StateList.h", "r", "utf-8")

state_name_number = []

for line in fstates:
	if line.startswith("STATE"):
		comma = line.find(",")
		enc = line.find(")")
		name = line[6:comma]
		number = int(line[comma+1:enc])
		#print "" + name + " " + number
		state_name_number.append( (name, number) ) 

fstates.close()


xp = codecs.open("nsIAccessibleStates.idl", "r", "utf-8")

xpnum = []
numxp = {}
numextxp = {}
xpweird = []

for line in xp:
	line = line.strip()
	if not line.startswith("const"):
		continue
	
	line = line[line.find("long") + 6:].split()
	statename = line[0]
	statenumbin = line[2][:-1]
	if statenumbin.startswith("0x"):
		statenumint = int(statenumbin, 	0)
		xpnum.append( (statename, statenumint) )
		
		if statename.startswith("EXT"):
			numextxp[statenumint] = statename
		else:
			numxp[statenumint] = statename
	else:
		xpweird.append( (statename, statenumbin) )
	print statename , statenumbin, statenumint

xp.close()

print numxp
print numextxp


#script assumes that nsStateMap contains only a portion of file copied from within the definiton of static const AtkStateMap gAtkStateMap[]
ns = codecs.open("nsStateCut.h", "r","utf-8")

nss = []

for line in ns:
	line = line.strip()
	if not line.startswith("{"):
		continue
#{ ATK_STATE_OPAQUE,                         kMapDirectly },   // states::OPAQUE                  = 1 << 39
	comma = line.find(",")
	key = line[2:comma].strip()
	closure = line.find("}")
	val = line[comma+1:closure].strip()
	comm = line.find("//")
	suf = line[comm+3:]
	statename = suf[suf.find("states::") + 8: suf.find(" ")].strip()
	statenum = int(suf[suf.find("<<") + 2:].strip())
	if not ( (statename, statenum)  in state_name_number ):
		print "incorrect record, ignoring : " + str( (statename, statenum) ) 
		continue
	
	xpstatenum = 1 << statenum
	
	print "xpstatenum: " + str(xpstatenum)
	if statenum >= 31:
		xpstatename = numextxp[xpstatenum >> 31]
	else:
		xpstatename = numxp[xpstatenum]
	nss.append( (statename, statenum, key, val, xpstatename, xpstatenum) )
	
ns.close()

for ns in nss:
	print "STATE(" + str(ns[0]) +", " + str(ns[1]) + ", " + str(ns[2]) + ", " + str(ns[3]) + ", " + str(ns[4]) + ")" #+ ", \t" + str(ns[5]) + "[" + str(2**(ns[1])) +"]"
	
	dname = ""
	if ns[1] < 31:
		dname = "STATE_" + ns[0]
	else:
		dname = "EXT_STATE_" + ns[0]
	
	#if not unicode(dname) == unicode(ns[4]):
	#	print "not compatible names : ("+ str(ns[1]) +") \"" + dname + '" and "' + ns[4] + '".'
	

#print state_name_number
#print nss

