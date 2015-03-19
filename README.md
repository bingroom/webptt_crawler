# webptt_crawler

1. Running Environment: 

	Editor: Sublime Text

	Python version: 2.7.x
	
	OS: Windows 7
	
	Need-to-import packages:
		
		bs4 (beautifulsoup)
		
		lxml
		
		mechanize
		
		glob


2. Single board crawling (with customized start page, endless checking latest posts and crawling)

		$python crawler_auto.py [Boardname (case sensitive)] [Start page number]


3. Multiple boards crawling
	
	!!!!! Warning: due to network and multiple requests issues, very unstable.

	Modify "boardlist.txt" using Sublime Text (to avoid newline problem caused by Notepad), with each board separated by a newline ('\n' in C language, an "Enter" in editors)
	then,

		$python crawler_multi.py


4. To parse data
	
	Raw data must be stored in folder "raw_data", then execute following commands:

	(1) Parse contents arranged by authors, with "post_info.txt" which provides post_id, author, title, and datetime, using '\t' as the separator.
		The results are stored in folder "output".

		$python content_parser.py [Boardname (case sensitive)]


	(2) Parse pushes arranged by boards. Each post_id named file provides push_status, author, push_content, using '\t' as the separator.
		The results are stored in folder "output_push".

		$python push_parser.py [Boardname (case sensitive)] 




Feel free to ask any question -> joekaojoekao@gmail.com
