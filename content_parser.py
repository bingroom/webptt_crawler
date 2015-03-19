#!/usr/bin/python
# -*- coding: utf-8 -*-


import lxml.etree as etree
import sys
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


if len(sys.argv) < 2:
	print 'Usage: python content_parser.py [Boardname(case sensitive!)]'
	sys.exit(0)

##read raw data
board_name = sys.argv[1]

in_dir = 'raw_data/'+board_name
if not os.path.exists(in_dir):
	print 'Board \"' + board_name + '\"" does not exist in folder \"raw_data\"'
	sys.exit(0)

if not os.path.exists('output'):
	os.makedirs('output')

brd_dir = 'output/'+board_name
if not os.path.exists(brd_dir):
	os.makedirs(brd_dir)

print 'Start parsing content in '+brd_dir+'\n...'
index = {}
brd_info = []
for f in glob.glob(in_dir + "/*.*"):
	fin = open(f, 'rb')
	content = fin.read()
	parser = etree.XMLParser(recover=True)
	dom = etree.fromstring(content, parser)
	author = "_unknown_"
	try:
		author = dom.xpath('div/span[2]')[0].text
		author = author[:author.find("(")].strip()
		author = unicode(author)
		
		p_id = r_segment(f, '\\', '.txt')	
		#board = dom.xpath('div/span[2]')[1].text
		title =  dom.xpath('div/span[2]')[2].text
		date = dom.xpath('div/span[2]')[3].text
	
	except BaseException as e:
		author = "_unknown_"
		print(type(e), str(e))
	
	index[p_id] = {'author':author, 'title':title, 'date':date} 
	data_list = []
	i = 0
	post = []
	for s in dom.xpath("/div[@id='main-content']/*"):
		tag = s.tag
		attr = s.attrib
		text = s.text
		if text is None:
			text = ""
		tail = s.tail
		if tail is None:
			tail = ""
		full = text + tail
		if len(full) > 0:
			if "批踢踢實業坊(ptt.cc)" in full and "發信站" in full:
				break
			post.append(full)
			data = {'attr':attr, 'content':full}
			data_list += data
		i += 1

	# print p_id
	# print author, title, date
	# for s in post:
	# 	print s
	# print '----'
	
	out_dir = brd_dir + '/' + author
	if not os.path.exists(out_dir):
		os.makedirs(out_dir)

	out_path = out_dir+'/'+p_id+'.txt'
	fout = open(out_path, 'wb')
	for s in post:
		fout.write(s)
	fout.close()

	info_line = p_id+'\t'+author+'\t'+title+'\t'+date+'\n'
	brd_info.append(info_line)

fout_info = open(brd_dir+'/post_info.txt', 'wb')
for line in brd_info:
	fout_info.write(line)
fout_info.close()

print '\nDone.'
sys.exit(0)
