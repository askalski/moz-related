#!/usr/bin/python2.7
# -*- coding: UTF-8 -*-

import sys
import codecs

rolesf = codecs.open("RolesCut.h", "r", "utf-8")

R = {}
rolelist = []

comment = []

for line in rolesf:
	line = line.strip()
	if line.startswith("/*") or line.startswith("*"):
		if line.startswith("/"):
			comment.append(line)
		else:
			comment.append(" " + line)
		continue
		
	
	if len(line) == 0:
		continue
	
	line = line.split("=")
	role = line[0].strip()
	number = line[1]
	if number[-1] == ',':
		number = number[:-1]
	number = int(number)
	
	R[role] = {}
	R[role]["num"] = number
	R[role]["main_comment"] = comment

	comment = []
	rolelist.append(role)
	
rolesf.close()

#print sorted(R.keys())


rolesmsaa = codecs.open("msaaRoleMap.h", "r" , "utf-8")
roleheader = None
for line in rolesmsaa:
	line = line.strip()
	
	if len(line) == 0:
		continue
		
	if line.startswith("// roles::"):
		roleheader = line[10:]
		continue
	
	if line.startswith("{"):
		first_comma = line.find(",")
		close = line.find("}")
		msaakey = line[1:first_comma].strip()
		msaaval = line[first_comma+1:close].strip()
		
		#print roleheader, msaakey, msaaval
		
		if not roleheader in R.keys():
			print "msaa role not found :" + str( (roleheader, msaakey, msaaval) )
			continue
		
		R[roleheader]["msaakey"] = msaakey
		R[roleheader]["msaaval"] = msaaval
		
rolesmsaa.close()


rolesatk = codecs.open("atkRoleMap.h", "r", 'utf-8')

for line in rolesatk:
	line = line.strip()
	if len(line) == 0:
		continue
	
	comma = line.find(",")
	rolenum = line.find("::")
	lastspace = line.rfind(" ")
	
	atkname = line[:comma].strip()
	rolename = line[rolenum+2:lastspace].strip()
	
	number = int(line[lastspace:])
	
	if not rolename in R.keys():
		print "atk role not found :" + str( (rolename, atkname, number) )
		continue
		
	if R[rolename]["num"] != number:
		print "incompatible numbers (atk vs roles): " + str(R[rolename]["num"]) + " and " + str(number) + " at " + rolename
		
	R[rolename]["atkname"] = atkname
		
	
	#print number, atkname, rolename
	
rolesatk.close()

rolesmac = codecs.open("macRoleMap.h", "r", "utf-8")

for line in rolesmac:
	line = line.strip()
	if len(line) == 0:
		continue
		
	comma = line.find(",")
	comment = line.find("//")
	macname = line[:comma].strip()
	
	suffix = line[comment+2:].strip()
	
	maccomment = None
	if "." in suffix:
		dot = suffix.find(".")
		maccomment = suffix[dot+2:]
		rolename = suffix[:dot]
	else:
		rolename = suffix
	
	assert(rolename.startswith("ROLE_"))
	rolename = rolename[5:] #cutting ROLE_ prefix
	
	#print macname, rolename, '"' + str(maccomment) + '"'
	
	if not rolename in R.keys():
		print "mac role not found :" + str( (rolename, macname, maccomment) )
		continue
		
	R[rolename]["macname"] = macname
	R[rolename]["maccomment"] = maccomment

rolesmac.close()

#keys : ['msaakey', 'main_comment', 'atkname', 'macname', 'num', 'maccomment', 'msaaval']

for role in rolelist:
	print("\n")
	
	for line in R[role]["main_comment"]:
		if line.strip() == "*/":
			if R[role]['maccomment'] != None:
				print " * \n * mac: " + R[role]['maccomment']
			
		print line
	
	
	print "ROLE(" + role + ", " + str(R[role]['num']) + ", " + R[role]['atkname'] + ", " + R[role]['macname'] + ", " + R[role]['msaakey'] + ", " + R[role]['msaaval'] + ")",


print "remamber to manually add comment from msaa about PANE role!"
