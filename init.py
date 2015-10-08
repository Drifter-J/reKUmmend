# -*- coding: utf-8 -*-

from flask import Flask, request, g, redirect, url_for, render_template, jsonify

from pattern import web
from BeautifulSoup import BeautifulSoup
from ghost import Ghost
import urllib2, PyQt4
from ghost_crawl import KuKlueCrawler

import sys,json, pickle
from time import time,gmtime, strftime

from recommendation import topMatches, sim_pearson
from model import Lecture,Person


reload(sys)
sys.setdefaultencoding('utf-8')

# Server setting
app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('FLASKR_SETTINGS', silent=True)



# app이 실행되기 전 준비 단계
@app.before_request
def before_request():
	print strftime("%Y-%m-%d %H:%M:%S", gmtime())


# 서버가 teardown이 걸린 경우(Exception)
@app.teardown_request
def teardown_request(exception):
	print('Teardown arose!'.format(exception))
	print exception

# Log-in 하는 페이지
@app.route('/')
def form():
	return render_template('index.html')

# 로그인된 아이디와 비밀번호를 통해 kuklue의 내 정보를 크롤링하고 자신 정보와 저장된 lectureList, personList 이용하여 추천
@app.route('/recommend', methods=['POST'])
def view():
	# load Object data
	with open('objectData.pkl', 'rb') as input:
		lectureList = pickle.load(input)
		personList = pickle.load(input)

	# userId, userPw 받아옴
	userId = request.form['userId']
	userPw = request.form['userPw']
	# ghost 모듈을 이용하여 crawling
	a = KuKlueCrawler(id=userId,pw=userPw)
	page, resource = a.openPage('http://klue.kr/myLectureEval.php')
	page, resource = a.ghost.evaluate("document.getElementsByClassName('mainContent');")
	page = unicode(page[PyQt4.QtCore.QString(u'0')][PyQt4.QtCore.QString(u'outerHTML')]).encode('utf-8')

	lec = BeautifulSoup(page)

	lecContent = lec.find('div',{'class':['lectureEvalList']}).findAll('div',{'class':['content']})

	# 자신에 대한 Person 객체 생성
	me = Person()
	me.nickName = lecContent[0].find('div',{'class':['wrInfo']}).a.text.encode('utf-8')

	# 자신이 평가한 항목에 대해 평균 점수를 매김
	lectureCount = 0
	for item in lecContent:
		try:
			me.difficulty += len(item.find('div',{'class':['e difficulty']}).find('div','center').findAll('span','active'))
			me.total += len(item.find('div',{'class':['e total']}).find('div','center').findAll('span','active'))
			me.studyTime += len(item.find('div',{'class':['e studyTime']}).find('div','center').findAll('span','active'))
			me.attendance += len(item.find('div',{'class':['e attendance']}).find('div','center').findAll('span','active'))
			me.grade += len(item.find('div',{'class':['e grade']}).find('div','center').findAll('span','active'))
			me.achievement += len(item.find('div',{'class':['e achievement']}).find('div','center').findAll('span','active'))
			lectureCount+=1
		except:		# except가 뜨는 부분은 신형 데이터를 읽었을 경우
			me.difficulty /= lectureCount
			me.total /= lectureCount
			me.studyTime /= lectureCount
			me.attendance /= lectureCount
			me.grade /= lectureCount
			me.achievement /= lectureCount
			break


	# 유사도 계산 알고리즘에 넣고 결과값(유사한 사람) 반환
	result = topMatches(personList,me)

	classList = []

	# for calculating error
	totalCount = 0
	Etotal = 0.0
	Edifficulty = 0.0
	EstudyTime = 0.0
	Eattendance = 0.0
	Egrade = 0.0
	Eachievement = 0.0

	# 결과값에 대한 강의 정리
	for person in result:
		similarity = person[0]
		for lectureID in person[1].lectureList:
			for oneLecture in lectureList:
				if float(oneLecture.total)<2.5:
					continue
				if oneLecture.lectureID == lectureID:
					##### for calculating error #####
					Etotal += float(oneLecture.total)
					Edifficulty += float(oneLecture.difficulty)
					EstudyTime += float(oneLecture.studyTime)
					Eattendance += float(oneLecture.attendance)
					Egrade += float(oneLecture.grade)
					Eachievement += float(oneLecture.achievement)
					totalCount += 1
					#################################

					classList.append((similarity*float(oneLecture.total)/5,oneLecture))
					break

	Etotal /= totalCount
	Edifficulty /= totalCount
	EstudyTime /= totalCount
	Eattendance /= totalCount
	Egrade /= totalCount
	Eachievement /= totalCount

	print
	print "Total Eval Error : " + str(me.total-Etotal)
	print "difficulty Error : " + str(me.difficulty - Edifficulty)
	print "studyTime Error : " + str(me.studyTime - EstudyTime)
	print "attendance Error : " + str(me.attendance - Eattendance)
	print "grade Error : " + str(me.grade - Egrade)
	print "achievement Error " + str(me.achievement - Eachievement)
	print

	classList.sort(reverse=True)
	classList = [lecture[1] for lecture in classList]	# 유사도*total 점수 제거
	
	# page rendering
	return render_template('ShowLectures.html',classList=classList)



@app.route('/class', methods=['POST'])
def classPage():
	

	classNumber= int(request.form['lecID'])
	classInfo = {}
	classRatings = []

	with open('objectData.pkl', 'rb') as input:
		lectureList = pickle.load(input)

	lectureClass = lectureList[classNumber]
	classInfo = lectureClass.__dict__
	classRatings = lectureClass.comments

	return render_template('ShowRatings.html', lecture=classInfo, persons=classRatings, num_persons=len(classRatings))




# Execute the main program
if __name__ == '__main__':
	app.run()
