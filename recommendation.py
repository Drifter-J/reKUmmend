# -*- coding:utf-8 -*-

from math import sqrt


def sim_distance(person1, person2):
	si = ['difficulty','studyTime','attendance','grade']
	sum_of_squares = sum([pow(person1[item]-person2[item],2) for item in si])
	return 1/(1+sqrt(sum_of_squares))

#p1과 p2에 대한 피어슨 상관관계 계산
def sim_pearson(p1, p2):
	si = ['difficulty','studyTime','attendance','grade']
	n = len(si)

	#모든 선호도 합산
	sum1 = sum([p1[it] for it in si])
	sum2 = sum([p2[it] for it in si])

	#제곱의 합을 계산
	sum1Sq = sum([pow(p1[it],2) for it in si])
	sum2Sq = sum([pow(p2[it],2) for it in si])

	#곱의 합을 계산
	pSum = sum([p1[it]*p2[it] for it in si])

	#피어슨 점수 계산
	num = pSum-(sum1*sum2/n)
	den = sqrt((sum1Sq-pow(sum1,2)/n)*(sum2Sq-pow(sum2,2)/n))

	if den==0:
		return 0

	r = num/den
	return r

##### Recommend from other person #####
def topMatches(prefs, person, n=10, similarity=sim_pearson):
	scores=[(similarity(person, other),other) for other in prefs if other['nickName']!=person['nickName']]

	# 최고점이 상단에 오도록 정렬
	scores.sort()
	scores.reverse()
	return scores[0:n]
