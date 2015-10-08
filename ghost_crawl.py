# -*- coding: utf-8 -*-
from pattern import web
from BeautifulSoup import BeautifulSoup
from ghost import Ghost
import urllib2

class KuKlueCrawler:
	# Class 생성자, id, pw로 KuKlue 로그인 시도
	def __init__(self, id, pw, displayFlag = False, download_images=False, prevent_download=["css"]):
		# 새 Ghost instance를 만들어서 사용합니다.
		self.ghost = Ghost(display = displayFlag, wait_timeout = 60)
		self.currentPage = None
		self.login(id, pw)

	# Class 소멸자
	def __del__(self):
		self.ghost.exit()
		del self.ghost

	# 요청한 url 접속
	def openPage(self, url):
		page, resource = self.ghost.open(url)
		self.ghost.wait_for_page_loaded()
		self.currentPage = url
		return page, resource

	# Login 하는 함수
	def login(self, id, pw):
		page, resource = self.openPage('http://klue.kr/')

		self.ghost.evaluate("""
		(function() {        
		  document.getElementById('mb_id').value = '%s';
		  document.getElementById('mb_pw').value = '%s';
		  document.getElementsByClassName('login')[0].click();
		})();
		""" % (id, pw), expect_loading = True)
 		return page, resource

 	# 특정 index에 대해 lecture page 접속
	def main_search(self, query=None, lectureNum=-1):
		if query is not None: 
			self.ghost.wait_for_selector('#topBar_search')

			self.ghost.fill("#sform", { "query": query })
			page, resource = self.ghost.fire_on('#sform', 'submit', expect_loading = True)
			
		if lectureNum != -1:
			page, resource = self.openPage('http://klue.kr/lecture.php?no='+str(lectureNum))

		return page, resource
