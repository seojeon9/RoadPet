import random
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import Kind, RoaddogInfo, Sido, Survey
from .module import kmeans_recom
from .module import content_recom
from sklearn.cluster import KMeans
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import joblib
from django.urls import reverse


# Create your views here.
def index(request):

    return render(request, 'accounts/index.html')


def about_us(request):
    return render(request, 'roaddog/about_us.html')


def recommend(request):
    # print('')
    # 1. 사용자가 전달한 별점 점수 가져오기
    # 2. 별점점수를 군집화 모듈로 전송(함수호출)
    # 3. 군집화모듈에서 군집레이블 결정후 몇번 레이블인지 반환
    # 4. 반환된 레이블과 같은 군집의 강아지 정보를 파일이나 디비에서 얻어오기
    # 5. 동일 군집 강아지 중 랜덤하게 선택
    # 6. 디비에서 선택된 강아지 세부 정보 추출
    # 7. 추출된 정보를 템플릿으로 전송
    # weight = request.POST['weight']
    # age = request.POST['age']
    # friendly = request.POST['friendly']
    # health = request.POST['health']
    # print(kmeans_recom.recommend([[weight,age,friendly,health]]))

    #######################################
    # db에서 해당 라벨의 강아지 중 랜덤 3개 가져와서 보여주기
    roaddog = list(RoaddogInfo.objects.filter(label=1).values())
    random_roaddog = random.sample(roaddog, 3)
    content = {'roaddog': random_roaddog}
    print(content)
    return render(request, 'roaddog/recommend.html', content)


def presurvey(request):

    return render(request, 'roaddog/presurvey.html')


def search(request):
    sido = list(Sido.objects.values())
    kind = list(Kind.objects.values())
    roaddog = list(RoaddogInfo.objects.values())
    content = {'sidos': sido,
               'kinds': kind,
               'roaddogs': roaddog}
    # print(content)
    return render(request, 'roaddog/search.html', content)


def search_filter(request):
    sido = request.GET['sido']
    kind = request.GET['kind']
    # 쿼리문
    # SIGUNGU의 SIDO_CD = sido의 SIGUNGU_CD
    # SHLETER의 SIGUNGU_CD의 CARE_ID
    # ROADDOG_INFO의 CARE_ID
    # &
    # ROADDOB_INFO의 KIND_NM = kind

    # roaddog =
    content = {'sidos': sido,
               'kinds': kind,
               #    'roaddogs': roaddog
               }
    # print(content)
    return render(request, 'roaddog/search.html', content)


def survey(request):

    if request.method == 'GET':
        print('get request')
        return render(request, 'roaddog/survey.html')

    user = request.user
    weight = request.POST['weight']
    age = request.POST['age']
    friendly = request.POST['friendly']
    health = request.POST['health']

    survey = Survey.objects.filter(username=user)

    if not survey:
        survey = Survey(username=user.username, weight_cd=weight,
                        age_cd=age, health_cd=health, attr_cd=friendly)
        survey.save()
    else:
        survey = survey[0]

        survey.weight_cd = weight
        survey.age_cd = age
        survey.attr_cd = friendly
        survey.health_cd = health

        survey.save()

    return render(request, 'roaddog/recommend.html')


def detail_info(request):
    # 선택된 강아지 아이디 얻어오기
    # 디비에서 해당 아이디 강아지 상세정보 가져오기
    # 유사도 테이블에서 선택된 강아지와 유사도가 놑은 강아지 아이디 찾기
    # 디비에서 유사도가 높은 강아지들 정보 얻어오기(10개) - 상세페이지 넘어가게
    # 템플릿에 강아지 정보 전송
    return render(request, 'roaddog/detail_info.html')


def survey_submit(request):

    return HttpResponseRedirect(reverse('recommend'))
