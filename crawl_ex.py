# -*- coding: utf-8 -*-
from pattern import web
from BeautifulSoup import BeautifulSoup
from ghost import Ghost
import urllib2
import PyQt4

from ghost_crawl import KuKlueCrawler

# 저장할 파일변수
f = open('kucrawl.txt','w')

# range of new data format of kuklue
first = 32247
last = 35309

a = KuKlueCrawler(id='id',pw='pw')

for i in range(first,last+1):
	# i번째 lecture 평가 페이지 크롤링
	page, resource = a.main_search(lectureNum=i)
	page, resource = a.ghost.evaluate("document.getElementsByClassName('mainContent');")

	page = unicode(page[PyQt4.QtCore.QString(u'0')][PyQt4.QtCore.QString(u'outerHTML')]).encode('utf-8')

	lec = BeautifulSoup(page)
	for e in lec.findAll('br'):		# <br /> 태그 제거
		e.extract()

	lecInfo = lec.find('div',{'class':['lectureInfo box']})

	# 각 강의 정보 파일에 저장
	lectureName = lecInfo.find('div',{'class':['lec_name']}).find('span').text.encode('utf-8')
	f.write("lectureName : "+lectureName+'\n')

	profName = lecInfo.find('div','lec_profName').find('span').text.encode('utf-8')
	profName = profName.replace('\n',',')
	f.write("profName : "+profName+'\n')

	rating = lecInfo.find('div','lec_rating')
	total = rating.find('div', 'e total').find('div','right').text.encode('utf-8')
	f.write("total : "+total+'\n')

	difficulty = rating.find('div', 'e difficulty').find('div','right').text.encode('utf-8')
	f.write("difficulty : "+difficulty+'\n')

	studyTime = rating.find('div', 'e studyTime').find('div','right').text.encode('utf-8')
	f.write("studyTime : "+studyTime+'\n')

	attendance = rating.find('div', 'e attendance').find('div','right').text.encode('utf-8')
	f.write("attendance : "+attendance+'\n')

	grade = rating.find('div', 'e grade').find('div','right').text.encode('utf-8')
	f.write("grade : "+grade+'\n')

	achievement = rating.find('div', 'e achievement').find('div','right').text.encode('utf-8')
	f.write("achievement : "+achievement+'\n')


	info = lecInfo.find('div','lec_info').findAll('div',{'class':['e','e2']})
	for item in info:
		infoKey = item.find('span','subj').text.encode('utf-8')
		infoValue = item.find('span','content').text.encode('utf-8')
		f.write(infoKey+' : '+infoValue+'\n')
		

	# 각 사람에 대한 강의 평가 정보 파일에 저장
	lecContent = lec.find('div',{'class':['lectureEvalList']}).findAll('div',{'class':['content']})
	for item in lecContent:
		f.write('-Person-'+'\n')
		name = item.find('div',{'class':['wrInfo']}).text.encode('utf-8')
		name = name.split('님')[0]
		f.write('nickname : '+name+'\n')
		
		comment = item.find('div',{'class':['wrContent']}).text.encode('utf-8')
		f.write(comment+'\n')
		
		total = len(item.find('div',{'class':['e total']}).find('div','center').findAll('span','active'))
		f.write("total : "+str(total)+'\n')
		
		diff = len(item.find('div',{'class':['e difficulty']}).find('div','center').findAll('span','active'))
		f.write("difficulty : "+str(diff)+'\n')
		
		studyTime = len(item.find('div',{'class':['e studyTime']}).find('div','center').findAll('span','active'))
		f.write("studyTime : "+str(studyTime)+'\n')
		
		attendance = len(item.find('div',{'class':['e attendance']}).find('div','center').findAll('span','active'))
		f.write("attendance : "+str(attendance)+'\n')

		grade = len(item.find('div',{'class':['e grade']}).find('div','center').findAll('span','active'))
		f.write("grade : "+str(grade)+'\n')
		
		achievement = len(item.find('div',{'class':['e achievement']}).find('div','center').findAll('span','active'))
		f.write("achievement : "+str(achievement)+'\n')

	if i == last:		# 모두 끝낼 경우 &&&&& 라인 추가
		f.write('&&&&&'+'\n')
	else:				# 각 강의의 끝에 ===== 라인 추가
		f.write('====='+'\n')

f.close()
