import urllib2
from bs4 import BeautifulSoup
import Queue

process_url_queue = Queue.Queue()
board_list = []
base_url = 'https://www.ptt.cc/'
#process_url_queue.put('https://www.ptt.cc/bbs/index.html')
process_url_queue.put('https://www.ptt.cc/bbs/2870.html')
def is_folder(link_dd):
	img_url = link_dd.find('img').get('src')
	return 'folder.gif' in img_url

def is_board(link_dd):
	img_url = link_dd.find('img').get('src')
	return 'f.gif' in img_url

def get_link_dd_url(link_dd):
	return link_dd.find('a').get('href')

def get_link_dd_name(link_dd):
	pass
if __name__ == '__main__':
	while not process_url_queue.empty():
		process_url = process_url_queue.get()
		try:
			page = urllib2.urlopen(process_url).read()
			soup = BeautifulSoup(page)
			link_dd_list = soup.find(id="mainContent").find(id="prodlist").find('dl').find_all('dd')
			for link_dd in link_dd_list:
				if is_folder(link_dd):
					print base_url + get_link_dd_url(link_dd)
					process_url_queue.put(base_url + get_link_dd_url(link_dd))
				elif is_board(link_dd):
					board_list.append(base_url + get_link_dd_url(link_dd))
				else:
					raise NameError
		except:
			pass
		print process_url_queue
		print board_list
		break
