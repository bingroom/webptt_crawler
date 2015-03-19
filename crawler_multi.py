import sys
import subprocess
import thread
import time


fin = open("boardlist.txt")
content = fin.read()
boards = content.split('\n')

def crawl(cmd):
	subprocess.call(cmd, shell=True)


#print boards
exe = "python crawler.py "
n = 5
for i in xrange(0,len(boards)/n+1):
	count = 0
	j = i * n
	p = 0
	while j<len(boards) and count < n:
		#print boards[j]
		p = subprocess.Popen(exe+boards[j], shell=True)
		j += 1
		count += 1
	print '---'
	p.communicate()

#for board in boards:
	#subprocess.call(exe+board, shell=True)
	#subprocess.Popen(exe+board, shell=True)
	"""
	try:
		thread.start_new_thread(crawl(exe+board))
		print "start %s" % board
	except:
		print "fail in %s" % board
	"""
	