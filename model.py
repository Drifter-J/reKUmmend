# -*- coding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

#Lecture Class
class Lecture(object):
	def __init__(self):
		self.lectureID = 0
		self.lectureName = ''
		self.profName = ''
		self.total = 0.0
		self.totalVariance = 0.0
		self.difficulty = 0.0
		self.studyTime = 0.0
		self.attendance = 0.0
		self.grade = 0.0
		self.achievement = 0.0
		
		self.comments = []			# 여기에 강의 정보 저장

	def __getitem__(self,attr):
		return getattr(self,attr)


# Person class
class Person(object):
	def __init__(self):
		self.nickName = ''
		# 해당 사람의 평균 점수
		self.total = 0.0
		self.difficulty = 0.0
		self.studyTime = 0.0
		self.attendance = 0.0
		self.grade = 0.0
		self.achievement = 0.0
		self.lectureList = []		# lectrueID를 담음

	def __getitem__(self,attr):
		return getattr(self, attr)