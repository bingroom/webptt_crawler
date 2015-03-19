import bs4
import urllib2
import sys
import os
import re
import time
import json
import mechanize

def write_to_raw(post_id, content):
	raw_path = os.path.join(post_id + ".txt")
	try:
		raw_file = open(raw_path, 'wb')	
		raw_file.write(content.encode('utf-8'))
	except:
		print "Warning: write to raw failed"
	raw_file.close()
	"""
	with open(raw_path, 'r') as f:
		webpage = f.read().decode('utf-8')

	soup = bs4.BeautifulSoup(webpage)
	print soup
	"""
def r_segment(content, pre, post):
     pre_index = content.find(pre)
     start = pre_index + len(pre)
     post_index = content[start:].rfind(post)
     end = start+post_index
     if pre_index == -1 or post_index == -1:
          return -1
     else:
          return content[start:end].strip()

def handle_over18(url):
	br = mechanize.Browser()
	r = br.open(url)
	br.select_form(nr=0)
	#br.form.set_all_readonly(False)
	req = br.click()
	r = br.open(req)
	#page = bs4.BeautifulSoup(r.read())
	#return page
	#print r.read()
	#print "ok"
	return r.read()


reload(sys)
sys.setdefaultencoding('utf-8')
board_name = sys.argv[1]
#board_name = "ks97-301"
url = 'http://www.ptt.cc/bbs/' + board_name + '/index.html'
page_url = lambda n: 'http://www.ptt.cc/bbs/' + board_name + '/index' + str(n) + '.html'
post_url = lambda id: 'http://www.ptt.cc/bbs/' + board_name + '/' + id + '.html'


## fetched files will be stored under the directory "./fetched/BOARDNAME/"
path = os.path.join('raw_data', board_name)
try:
	os.makedirs(path)
except: 
	sys.stderr.write('Warning: "%s" already existed\n' % path)
os.chdir(path)



sys.stderr.write('Crawling "%s" ...\n' % board_name)

## determine the total number of pages for this board
page = bs4.BeautifulSoup(urllib2.urlopen(url).read())
## handle over18 pages
#print page.find_all("div")[0]
if len(page.find_all("div", class_='over18-notice')) > 0:
#	print '----------------------------'
#if any("警告︰您即將進入之看板內容需滿十八歲方可瀏覽。" in s for s in page.contents):
	#print "ok"
	page = bs4.BeautifulSoup(handle_over18(url))
#print page
#print page.find(id='action-bar-container')
#sys.exit(0)

num_pages = int(page.find(id='action-bar-container').contents[1].contents[3].contents[3].get('href').split('/')[3].split('.')[0].split('index')[1]) + 1
num_pages += 1
sys.stderr.write('Total number of pages: %d\n' % num_pages)

## a mapping from post_id to number of pushes
num_pushes = dict()
counter = 0
output_json = {}
doc = 0
movie_index = {}


for n in xrange(1, num_pages):
	try:
		page = bs4.BeautifulSoup(urllib2.urlopen(page_url(n)).read())
		if len(page.find_all("div", class_='over18-notice')) > 0:
			page = bs4.BeautifulSoup(handle_over18(page_url(n)))

	except:
		sys.stderr.write('Error occured while fetching %s\n' % page_url(n))
		continue
	## iterate through posts on this page
	sys.stderr.write('Fetching page %s ...\n' % n)

	for tr in page.find_all('div'):
		## For instance: "M.1368632629.A.AF7"
		post_score = ""
		post_id = ""
		
		if len(tr) == 9 and counter != 0:
			#print tr.contents[1].contents[0].string
			#sys.exit(0)
			try:
				#print len(tr.contents[1].contents[0])
				if len(tr.contents[1]) > 0:
					post_score = tr.contents[1].contents[0]
					if len(post_score) > 1:
						continue
					else:
						post_score = tr.contents[1].contents[0].string
				post_id = tr.contents[5].contents[1].get('href').split('/')[-1][:-5]
			except:
				post_id = ""
		elif len(tr) == 9:
			counter = counter + 1
		else:
			continue

		#post_id = "M.1350631118.A.702"
		if post_id != "":
		
			## Fetch the post content
			#sys.stderr.write('Fetching %s ...\n' % post_id)
			
		
			try:
				post = bs4.BeautifulSoup(urllib2.urlopen(post_url(post_id)).read())
				if len(post.find_all("div", class_='over18-notice')) > 0:
					post = bs4.BeautifulSoup(handle_over18(post_url(post_id)))
			except:
				sys.stderr.write('Error occured while fetching %s\n' % post_url(post_id))
				continue
			
			try:
				json_data = {}
				for content in post.find(id='main-container').contents:
					length = len(content)
					if len(content) > 1:
						write_to_raw(post_id, content)
						title = content.contents[2].contents[1].string.encode('utf-8')
						#print title.encode('cp950')
			except:
				sys.stderr.write('main-container not found in %s\n' % post_url(post_id))
			## delay for a little while in fear of getting blocked
			time.sleep(0.5)