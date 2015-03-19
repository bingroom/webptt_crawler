#!/usr/bin/python
# -*- coding: utf-8 -*-

# usage: python parser.py [board_name]

import lxml.etree as etree
import sys
import re
import os

import glob


reload(sys)
sys.setdefaultencoding('utf-8')


def r_segment(content, pre, post):
	pre_index = content.find(pre)
	start = pre_index + len(pre)
	post_index = content[start:].rfind(post)
	end = start+post_index
	if pre_index == -1 or post_index == -1:
		return -1
	else:
		return content[start:end].strip()

PUNCTUATION_TABLE = [
	# start,  stop
	(0x2000, 0x206f),  # General Punctuation
	(0x3000, 0x303f),  # CJK Symbols and Punctuation
	(0xff00, 0xffef),  # Halfwidth and Fullwidth Forms
	(0x00, 0x2f),  # ascii special charactors
	# (0x30, 0x39), # number 0~9
	(0x3a, 0x40),  # ascii special charactors
	(0x5b, 0x60),  # ascii special charactors
	(0x7b, 0xff),  # ascii special charactors
]
PUNCTUATION_RANGE = reduce(lambda x, y: x.union(y), [
						   range(start, stop + 1) for start, stop in PUNCTUATION_TABLE], set())


def isCH(uchar):
	if uchar >= u'\u4e00' and uchar <= u'\u9fa5':
		return True
	else:
		return False


def isNUM(uchar):
	if uchar >= u'\u0030' and uchar <= u'\u0039':
		return True
	else:
		return False


def isEN(uchar):
	if (uchar >= u'\u0041' and uchar <= u'\u005a') or (uchar >= u'\u0061' and uchar <= u'\u007a'):
		return True
	else:
		return False


def isOther(uchar):
	if not (isCH(uchar) or isNUM(uchar) or isEN(uchar)):
		return True
	else:
		return False


def get_author(dom):
	name = '_unknown_'
	try:
		name = dom.xpath('div/span[2]')[0].text
		name = name[:name.find("(")].strip()
		name = unicode(name)

	except BaseException as e:
		print(type(e), str(e))
		return '_unknown_'

	##check ID format
	for ch in name:
		if isEN(ch) or isNUM(ch):
			continue
		else:
			return '_unknown_'

	return name

if len(sys.argv) < 2:
	print 'Usage: python push_parser.py [Boardname(case sensitive!)]'
	sys.exit(0)

##read raw data
board_name = sys.argv[1]

in_dir = 'raw_data/'+board_name
if not os.path.exists(in_dir):
	print 'Board \"' + board_name + '\"" does not exist in folder \"raw_data\"'
	sys.exit(0)

if not os.path.exists('output_push'):
	os.makedirs('output_push')

brd_dir = 'output_push/'+board_name
if not os.path.exists(brd_dir):
	os.makedirs(brd_dir)

print 'Start parsing pushes in '+brd_dir+'\n...'

board_name = sys.argv[1]

##read raw data
f_list = []
for f in glob.glob('raw_data/'+board_name+'/*.*'):
	f_list.append(f)

output = {}
dict_name = {}
c = 0


for f in f_list:
	#f = '/Users/joekaojoekao/Desktop/webptt/LoL/raw/M.1269633958.A.4E9.txt'
	#f = '/Users/joekaojoekao/PycharmProjects/push/M.1269633958.A.4E9.txt'
	fin = open(f, 'rb')
	post_id = f.split('\\')[-1].split('.txt')[0]
	content = fin.read()
	parser = etree.XMLParser(recover=True)
	dom = etree.fromstring(content, parser)

	"""
	#kill system msg
	for ele in dom.xpath("/div/span[@class='f2']"):
		ele.getparent().remove(ele)
	"""

	## get post author & id
	author = get_author(dom)
	#print post_id, author

	## choose right(of this post) push list
	target_string = u'※ 發信站:'
	real_push_order = content.count(target_string)

	count = 0
	push_list = []
	tmp = []
	#content_txt = dom.xpath("//div[@class='push'][*]/node()")
	#for s in content_txt:
		#print s.text
	push_path = "//div[@class='push'][*]/node()"# "//*[contains(.,'" + target_string + "')][" + str(real_push_order) + "]/following::div[@class='push']/span"
	for s in dom.xpath(push_path):
		for t in s.text.split():
			tmp.append(t)
		count += 1
		if count % 4 == 0:
			push_list.append(tmp)
			tmp = []

	out_path = brd_dir+'/'+post_id+'.txt'
	fout = open(out_path, 'wb')


	for p in push_list:
		push_info = p[0] + '\t' + p[1]+'\t'+p[3][0:]+'\n'# +'\t'+p[4]+'\t'+p[5]+'\n'
		#print push_info
		fout.write(push_info)
	#push_dict = {}

	#break

	fout.close()

print '\nDone.'
sys.exit(0)