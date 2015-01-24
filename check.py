#!/usr/bin/python

# For example you have solved 492 B in CodeForces.Now you want to test if offline(with out submitting).
# For this you can use this script.With the help of this script, you can test your code with official 
# test cases(small cases.i.e cases which does not contain '...' in them), test cases generated by your
# test.py and also with manual input.
# Before testing you need to :
#   -- have your compiled binary(with executable permitions)
#   -- have test.py (which generates test cases, it need to be present in your working directory)
# To run You can just type : 
#    python check.py
# Then it prompts for :
#   -- Contest Code(492 in this case)
#   -- Problem Code(B in this case)
#   -- Executable path(path to your compiled Binary)
#   -- Time Limit
#   -- Number of unofficial Cases with which your program need to be tested(inputs are generated with your test.py)
# After this, this script extracts accepted gnu c++ code, test cases from respective problem page, test 
# your program with those inputs(ncluding unofficial inputs).
# After testing it prints the stats, and ask for queries.
# Queries are :
#   -- Quit or q : To quit
#   -- Manual : Give Manual input(You need to type EOF in a new line after end of input)
#   -- Help : Print Query types.
#   -- ACC : Print accepted test case indexes
#   -- WA  : Print wrong answer case indexes
#   -- TLE : Print TLE case indexes
#   -- RTE : Print RTE case indexes
#   -- <Number> : Print the stats(Input,Output,Answer,execution time,verdict) of respective test case
# NOTE:
#      For now I did not take care of small bugs, exception handling,... These will be debugged soon.
# Report Bugs/clarifications : mail to -> achaitanyasai@gmail.com
# 


Help="""Quit or q : To quit\n
	Manual : Give Manual input(You need to type EOF in a new line after end of input)\n
	Help : Print Query types.\n
	ACC : Print accepted test case indexes\n
	WA  : Print wrong answer case indexes\n
	TLE : Print TLE case indexes\n
	RTE : Print RTE case indexes\n
	<Number> : Print the stats(Input,Output,Answer,execution time,verdict) of respective test case\n
"""
from urllib2 import *
from re import *
from sys import *
import BeautifulSoup
import time
import threading
import subprocess
import os

class Command(object):
	def __init__(self, cmd):
		self.cmd = cmd
		self.process = None

	def run(self, timeout):
		def target():
			global infile
			myinput=open('./in','r')
			myoutput=open('./Obtained','w')
			self.process = subprocess.Popen(self.cmd,bufsize=4096,shell=False,stdin=myinput,stdout=myoutput)
			self.process.communicate()
			myoutput.flush()
		return_code=0
		thread = threading.Thread(target=target)
		thread.start()
		thread.join(timeout)
		if thread.isAlive():
			return_code=123456
			try:
				self.process.terminate()
	 			thread.join()
	 		except AttributeError:
		 		pass
		else:
		 	return_code=self.process.returncode
		return return_code

def Extract(Contest_Code,Problem_Code):
	count=1
	while(count<1200):
		print "Connecting To CodeForces ...."
		Url='http://codeforces.com/problemset/status/'+str(Contest_Code)+'/problem/'+str(Problem_Code)+'/page/'+str(count)
		html=urlopen(Url,timeout=600).read()
		print "Connected"
		print "Parsing HTML ...."
		soup=BeautifulSoup.BeautifulSoup(html)
		TR=soup.findAll('tr')
		print "HTML Parsed"
		for i in TR:
			soup=BeautifulSoup.BeautifulSoup(str(i))
			TD=soup.findAll('td')
			l=0
			XX={}
			for j in TD:
				if(l==0):
					temp=j.contents
					XX[l]=temp[1]
					XX[l]=str(XX[l])
				elif(l==4):
					temp=j.contents
					XX[l]=str(temp[0])
				elif(l==7):
					if('GNU C++' in XX[4]):
						soup=BeautifulSoup.BeautifulSoup(XX[0])
						A=soup.findAll('a')
						for k in A:
							temp=k.contents[0]
							print "Required Solution Id Found : ",temp
							return str(temp)
				l+=1
				l%=8

def is_Number(x):
	try:
		int(x)
	except ValueError:
		return 0
	return 1

Contest_Code=raw_input('Contest Code : ').strip(' ').strip('\n')
Problem_Code=raw_input('Problem Code : ').strip(' ').strip('\n')
Executable=raw_input('Executable   : ').strip(' ').strip('\n')
TL=raw_input('Time Limit   : ').strip(' ').strip('\n')
Unofficial_Input=int(raw_input('Unofficial Cases : ').strip(' ').strip('\n'))

print "--------------------------------------------------------------------------"
Sol_Id=Extract(Contest_Code,Problem_Code)
print "Extracting Source Code ..."
Url='http://codeforces.com/contest/'+Contest_Code+'/submission/'+Sol_Id
html=urlopen(Url,timeout=600).read()
html=html.replace('\r','')
soup=BeautifulSoup.BeautifulSoup(html)
PRE=soup.findAll('pre')
print "Extracted"
print "Saving to acc_code.cpp ...."
In=str(PRE[0].contents[0])
In=In.replace('<pre>','').replace('</pre>','')
In=In.replace('&gt;','>')
In=In.replace('&lt;','<')
In=In.replace('&quot;','"')
In=In.replace('&amp;','&')
f=open('./acc_code.cpp','w')
f.write(In)
f.close()
print "Saved"
print "Compiling Source Code ...."
os.system('g++ ./acc_code.cpp -o acc_code')
print "Compiled"
print "--------------------------------------------------------------------------"
print "Testing .... "
L=len(PRE)
L1=L+Unofficial_Input
l=1
File_Index=1

Test_Cases={}
Accepted=[]
WA=[]
TLE=[]
RTE=[]
Time_Taken=0
while(l<L1):
	if(l<L):
		In=str(PRE[l])
		Out=str(PRE[l+1])
		l+=4
	else:
		os.system('python test.py > in')
		os.system('./acc_code < in > out')
		f=open('in','r')
		In=f.read()
		f.close()
		f=open('out','r')
		Out=f.read()
		f.close()
		l+=1
	In=In.replace('<pre>','').replace('</pre>','')
	In=In.replace('&gt;','>')
	In=In.replace('&lt;','<')
	In=In.replace('&quot;','"')
	In=In.replace('&amp;','&')
	Out=Out.replace('<pre>','').replace('</pre>','')
	Out=Out.replace('&gt;','>')
	Out=Out.replace('&lt;','<')
	Out=Out.replace('&quot;','"')
	Out=Out.replace('&amp;','&')
	if('...' not in In and '...' not in Out):
		print "     Test Case #"+str(File_Index)+" :"
		print
		if(l<L):
			f=open('in','w')
			f.write(In)
			f.close()
			f=open('out','w')
			f.write(Out)
			f.close()
		start_time=time.time()
		command = Command('./'+Executable)
		ret=command.run(timeout=int(TL))
		end_time=time.time()
		if(ret==0):
			print "        Execution Time : ",end_time-start_time,'s'
			Ver_Flag=0
			f1=open('./Obtained')
			x1=f1.read()
			f2=open('out')
			x2=f2.read()
			x2+='\n'
	  		if(len(x1)==len(x2)):
		  		for i in xrange(len(x1)):
			  		if(x1[i]!=x2[i]):
				  		Ver_Flag=1
				  		break
			else:
				Ver_Flag=1
			if(Ver_Flag==0):
				print "        Verdict        :  Correct Answer"
				f=open('./Obtained','r')
				x=f.read()
				f.close()
				Test_Cases[File_Index]=(In,Out,x,'ACC',end_time-start_time)
				Accepted.append(File_Index)
			else:
				print "        Verdict        :  Wrong Answer"
				f=open('./Obtained','r')
				x=f.read()
				f.close()
				Test_Cases[File_Index]=(In,Out,x,'WA',end_time-start_time)
				WA.append(File_Index)
			 	
		elif(ret==123456):
			print "        Execution Time : ",end_time-start_time,'s'
			print "        Verdict        :  Time Limit Exceeded"
			Test_Cases[File_Index]=(In,Out,'','TLE',end_time-start_time)
			TLE.append(File_Index)

		else:
			print "        Execution Time : ",end_time-start_time,'s'
		 	print "        Verdict        :  Run Time Error"
			Test_Cases[File_Index]=(In,Out,'','RTE',end_time-start_time)
			RTE.append(File_Index)
		File_Index+=1
		Time_Taken+=(end_time-start_time)
		print
print "--------------------------------------------------------------------------"
print "     Stats : "
print "           Total Cases     : ",File_Index-1-Unofficial_Input,'+',Unofficial_Input," = ",File_Index-1
print "           Time Taken      : ",Time_Taken,'s'
print "           Correct Answers : ",len(Accepted)
print "           Wrong Answers   : ",len(WA)
print "           TLE             : ",len(TLE)
print "           RTE             : ",len(RTE)
while(1):
	x=raw_input('Queries>> ').strip(' ').strip('\n')
	if(x=='Quit' or x=='q'):
		break
	elif(x=='ACC'):
		for i in Accepted:
			print i,
		print
	elif(x=='WA'):
		for i in WA:
			print i,
		print
	elif(x=='TLE'):
		for i in TLE:
			print i,
		print
	elif(x=='RTE'):
		for i in RTE:
			print i,
		print
	elif(x=='Help'):
	 	print Help
	elif(x=='Manual'):
		In=''
		while(1):
			x=raw_input()
			if(x=='EOF'):
				break
			else:
			 	In+=x
			 	In+='\n'
		f=open('in','w')
		f.write(In)
		f.close()
		os.system('./acc_code < in > out')
		start_time=time.time()
		command = Command('./'+Executable)
		ret=command.run(timeout=int(TL))
		end_time=time.time()
		if(ret==0):
			  print "        Execution Time : ",end_time-start_time,'s'
			  Ver_Flag=0
			  f1=open('./Obtained')
			  x1=f1.read()
			  f2=open('out')
			  x2=f2.read()
			  x2+='\n'
			  if(len(x1)==len(x2)):
				    for i in xrange(len(x1)):
			    		if(x1[i]!=x2[i]):
				    		Ver_Flag=1
						break
			  else:
				    Ver_Flag=1
			  if(Ver_Flag==0):
				print "        Verdict        :  Correct Answer"
				f=open('./Obtained','r')
				x=f.read()
				f.close()
				f=open('./out','r')
				y=f.read()
				f.close()
				print x
				print
				print y
		       	  else:
			       print "        Verdict        :  Wrong Answer"
			       f=open('./Obtained','r')
			       x=f.read()
			       f.close()
			       f=open('./out','r')
			       y=f.read()
			       f.close()
			       print x
			       print
			       print y
		elif(ret==123456):
			print "        Execution Time : ",end_time-start_time,'s'
			print "        Verdict        :  Time Limit Exceeded"
			f=open('./Obtained','r')
			x=f.read()
			f.close()

		else:
			 print "        Execution Time : ",end_time-start_time,'s'
			 print "        Verdict        :  Run Time Error"
			 f=open('./Obtained','r')
			 x=f.read()
	 		 f.close()
	elif(is_Number(x)==1):
		x=int(x)
		flag=0
		try:
			Test_Cases[x][0]
		except KeyError:
		 	flag=1
		if(flag==0):
			print "Input   : ",Test_Cases[x][0]
			print "Answer  : ",Test_Cases[x][1]
			print "OutPut  : ",Test_Cases[x][2]
			print "Verdict : ",Test_Cases[x][3]
			print "Ex Time : ",Test_Cases[x][4],'s'
		else:
		  	print "Try cases with in 1 to",File_Index-1
	else:
	  	print "Command Not Found try Help for list of commands."
