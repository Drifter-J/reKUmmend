# -*- coding: utf-8 -*-

import sys,time, pickle
from model import Lecture, Person

reload(sys)
sys.setdefaultencoding('utf-8')


# Crawling한 txt파일을 읽어서 lecture Class, Person Class로 가공후 personList, lectureList에 담음
# g 변수는 flask에서 사용하는 전역변수
lectureList = []
lectureID = 0
personList = []
a = open('kucrawl.txt','r')
lectureLine = []
tic = time.time()	# text가공하는 시간 측정
# totalComment = 0	# Total Comment number

for lineIndex,line in enumerate(a):		# 한 줄 씩 읽음
	line = line[0:-1]		# 개행 문자 삭제
	if line == '&&&&&' or line=='=====':		# 끝나는 부분(=====는 한 강의 정보가 끝나는 부분, &&&&&는 전체 텍스트 다 읽음)
		oneLecture = Lecture()		# Lecture Class 생성
		oneLecture.lectureID = lectureID
		lectureID+=1

		# Lecture info setting
		for idx,oneLine in enumerate(lectureLine[:12]):
			attrName = oneLine.split(' : ')[0]
			attrValue = oneLine.split(' : ')[1]
			if attrValue=='정보없음':
				setattr(oneLecture,attrName,0)
			else:
				setattr(oneLecture,attrName,attrValue)

		"""
		----한 개 강의 정보 예시---
			lectureName : 시장경제와법
			profName : 김용중 교수님
			total : 3.27
			difficulty : 3.12
			studyTime : 3.31
			attendance : 4.69
			grade : 3.23
			achievement : 2.77
			개설학기 : 2014-2R
			과목코드 : JURA101-00
			학점 : 3학점
			이수구분 : 교양
			강의시간 : 금(5-6) 법학관신관201
			총 13줄이므로 115줄 코드에서 len(lectureLine)-13을 함
		---한 사람에 대한 평가 예시---
			-Person-
			nickname : fritner
			시장경제와 법은 자본주의 시장경제 체제에서...
			total : 4
			difficulty : 4
			studyTime : 4
			attendance : 4
			grade : 4
			achievement : 4
			한 사람에 대한 평가는 총 9줄이므로 commentNum은 나누기 9를 해줌
		"""

		commentNum = (len(lectureLine)-13)/9
		# totalComment+= commentNum		# totalComment 계산
		# Person info
		for idx in [i*9+14 for i in range(0,commentNum)]:		# 위에서 계산한 한 강의에 대한 평가(commentNum)만큼 반복
			nickName = lectureLine[idx].split(' : ')[1]
			usercomments={}
			#oneLecture.comments.append(lectureLine[idx+1])
			usercomments['nickname'] = lectureLine[idx].split(' : ')[1]
			usercomments['comment']=lectureLine[idx+1]		
			# for-else 문법은 for문 안에 있는 if문이 for문 다 돌때까지 true가 아닌 경우 그 다음 else에서 처리함
			# 사람 정보(각 평가에 대한 평균 값) 계산
			for personIdx in range(0,len(personList)):
				if personList[personIdx].nickName == nickName:		# 해당 nickName이 있는 경우
					usercomments['total']=float(lectureLine[idx+2].split(' : ')[1])
					if usercomments['total'] < 3 :
						usercomments['grade_poor']=True
					elif usercomments['total'] <5 :
						usercomments['grade_average']=True
					else :
						usercomments['grade_good']=True
					usercomments['difficulty']=float(lectureLine[idx+3].split(' : ')[1])
					usercomments['studyTime']=float(lectureLine[idx+4].split(' : ')[1])
					usercomments['attendance']=float(lectureLine[idx+5].split(' : ')[1])
					usercomments['grade']=float(lectureLine[idx+6].split(' : ')[1])
					usercomments['achievement']=float(lectureLine[idx+7].split(' : ')[1])
					prevCount = len(personList[personIdx].lectureList)
					personList[personIdx].total = (personList[personIdx].total*prevCount + float(lectureLine[idx+2].split(' : ')[1]))/(prevCount+1)
					personList[personIdx].difficulty = (personList[personIdx].difficulty*prevCount+float(lectureLine[idx+3].split(' : ')[1]))/(prevCount+1)
					personList[personIdx].studyTime = (personList[personIdx].studyTime*prevCount+float(lectureLine[idx+4].split(' : ')[1]))/(prevCount+1)
					personList[personIdx].attendance = (personList[personIdx].attendance*prevCount+float(lectureLine[idx+5].split(' : ')[1]))/(prevCount+1)
					personList[personIdx].grade = (personList[personIdx].grade*prevCount+float(lectureLine[idx+6].split(' : ')[1]))/(prevCount+1)
					personList[personIdx].achievement = (personList[personIdx].achievement*prevCount+float(lectureLine[idx+7].split(' : ')[1]))/(prevCount+1)
					personList[personIdx].lectureList.append(lectureID)
					# 수정하는 부분
					break
			else:		# personList에 있는 각 Person 객체에 해당 nickName이 없는 경우
				usercomments['total']=float(lectureLine[idx+2].split(' : ')[1])
				if usercomments['total'] < 3 :
					usercomments['grade_poor']=True
				elif usercomments['total'] < 5 :
					usercomments['grade_average']=True
				else :
					usercomments['grade_good']=True
				usercomments['difficulty']=float(lectureLine[idx+3].split(' : ')[1])
				usercomments['studyTime']=float(lectureLine[idx+4].split(' : ')[1])
				usercomments['attendance']=float(lectureLine[idx+5].split(' : ')[1])
				usercomments['grade']=float(lectureLine[idx+6].split(' : ')[1])
				usercomments['achievement']=float(lectureLine[idx+7].split(' : ')[1])

				onePerson = Person()
				onePerson.nickName = nickName
				onePerson.total = float(lectureLine[idx+2].split(' : ')[1])
				onePerson.difficulty = float(lectureLine[idx+3].split(' : ')[1])
				onePerson.studyTime = float(lectureLine[idx+4].split(' : ')[1])
				onePerson.attendance = float(lectureLine[idx+5].split(' : ')[1])
				onePerson.grade = float(lectureLine[idx+6].split(' : ')[1])
				onePerson.achievement = float(lectureLine[idx+7].split(' : ')[1])
				onePerson.lectureList.append(lectureID)
				personList.append(onePerson)
				
			oneLecture.comments.append(usercomments)	

		lectureList.append(oneLecture)	# 생성한 oneLecture를 lectureList를 담음


		if line =='=====':	# 해당 라인인 경우 ===== lectureLine을 초기화하고 그 다음 강의에 대해 계속 진행함
			lectureLine = []	# lectureLine 초기화
			continue
		else:					# 해당 라인이 &&&&&인 경우는 전체 다 읽은 경우
			del lectureLine		# 소멸
			break

	else:		# =====, &&&&& 모두 아닌 경우, 강의(평가) 정보이므로 line을 계속 lectureLine에 담음
		lectureLine.append(line)

# print len(personList)			# 사람 정보 갯수 출력
# print totalComment		# 전체 평가 수 출력
print "total time : %d" % int(time.time()-tic)		# 걸린 시간


# save objects
with open('objectData.pkl', 'wb') as output:
    pickle.dump(lectureList, output, pickle.HIGHEST_PROTOCOL)
    pickle.dump(personList, output, pickle.HIGHEST_PROTOCOL)
