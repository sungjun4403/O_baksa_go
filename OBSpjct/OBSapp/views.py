from distutils.debug import DEBUG
from importlib.resources import path
from math import dist
from operator import indexOf, truediv
import re
from turtle import distance
from xml.dom.minicompat import NodeList
from django.shortcuts import redirect, render
from django.conf import settings
from .models import *
from plotly import *
from matplotlib  import *
import networkx as nx
import osmnx as ox
import requests
import matplotlib
import matplotlib.pyplot as plt
from plotly.offline import plot
import time
import sys
import os
from geopy.geocoders import Nominatim
import googlemaps
from django.utils import timezone
from PIL import Image
from io import BytesIO
import base64
import pandas as pd
import json
import datetime
import copy
import queue
import heapq

matplotlib.use('Agg')
ox.config(use_cache = True, log_console = True)
ox.__version__
sys.setrecursionlimit(10**7)


def home (request):
    return render(request, 'home.html')

def input (request):
    return render(request, 'input.html')

def get_options(request):
    ifsame = request.POST.get('ifsame')
    Destination = request.POST.get('Destination')
    Starting_Point = request.POST.get('Starting_Point')
    Max_Length = request.POST.get('Max_Length')
    ifMT1 = request.POST.get('MT1')
    ifCS2 = request.POST.get('CS2')
    #0 : postcode / 1 : address / 2 : detailAddress / 3 : extraAddress
    if Starting_Point[-1] == ')'and Starting_Point[0] == '(':
        Starting_Point.strip()
        Starting_Point = Starting_Point[1:-1]
        Starting_Point = " / " + str(Starting_Point) + " / " + " / "
    if Destination[-1] == ')'and Destination[0] == '(':
        Destination.strip()
        Destination = Destination[1:-1]
        Destination = " / " + str(Destination) + " / " + " / "

    Starting_Point_list = Starting_Point.split(" / ")
    Destination_Point_list = Destination.split(" / ")
    for p in range (0, len(Starting_Point_list)-1): Starting_Point_list[p] = str(Starting_Point_list[p]).strip()
    for q in range (0, len(Destination_Point_list)-1): Destination_Point_list[q] = str(Destination_Point_list[q]).strip()

    ADDRESS = Starting_Point_list[1]        
    address = Destination_Point_list[1]       

    #받을떄 좌표로 받으면 geocoding 스킵하는 로직 
    #SPL, DPL / 0 : location (lat, lng) / 1 : address / 2 : address_type
    SPL = [None] * 3        
    ADS = ADDRESS
    try:
        int(ADDRESS[5:9])
        SPLformat = "loc"
        ADDRESS = ADS
    except:
        SPLformat = "notloc"

    if SPLformat == "loc":
        SPL[0] = ADDRESS
        SPL[2] = 'location'
        print(str(SPL[0][:10]) + " " + str(SPL[0][12:])) 
        print("=================")
        print("location")
        print("=================")
    else:
        SPL = google_geocode(str(ADDRESS))
    
    DPL = [None] * 3
    ads = address
    try:        #좌표계 형식으로 들어왔는지 (37.xxxx, 127.zzzz)
        int(address[5:9])
        DPLformat = "loc"
        address = ads
    except:         #좌표계 아니라서 지오코딩 해줘야 되는지 
        DPLformat = "notloc"

    if DPLformat == "loc":      #좌표계 형식
        DPL[0] = address
        DPL[2] = 'location'
        print(str(DPL[0][:10]) + " " + str(DPL[0][12:])) 
        print("=================")
        print("location")
        print("=================")
    else:       #좌표계 아닌 형식 지오코딩
        DPL = google_geocode(str(address))
    
    if str(Max_Length).strip() == "" :      #Max_Length 아무값도 안들어왔을때 
        Max_Length = 1000
    
    #주변 편의점, 마트 
    if ifCS2 == "True":         #CS2 구하기로 했을때
        CS2 = forCS2(SPL, DPL, ifsame, Max_Length)
        CS2L = getlst(CS2)
    else:       #CS2 안구하기로 했을때
        CS2 = []
        CS2L = []

    if ifMT1 == "True":         #MT1 구하기로 했을때 
        MT1 = forMT1(SPL, DPL, ifsame, Max_Length)
        MT1L = getlst(MT1)
    else:       #MT1 안구하기로 했을때 
        MT1 = []
        MT1L = []

    get_map(ifsame, SPL, DPL, Max_Length, CS2L, MT1L, ifMT1, ifCS2, CS2, MT1)
    time.sleep(0.1)
    os.system("python manage.py collectstatic --no-input")
    
    CS2str0 = lstTostr(CS2, 0)
    CS2str1 = lstTostr(CS2, 1)
    CS2str2 = lstTostr(CS2, 2)
    CS2str3 = lstTostr(CS2, 3)
    CS2str4 = lstTostr(CS2, 4)
    CS2str5 = lstTostr(CS2, 5)
    CS2str6 = lstTostr(CS2, 6)
    CS2str7 = lstTostr(CS2, 7)
    CS2str8 = lstTostr(CS2, 8)
    CS2str9 = lstTostr(CS2, 9)
    CS2str10 = lstTostr(CS2, 10)
    CS2str11 = lstTostr(CS2, 11)
    
    MT1str0 = lstTostr(MT1, 0)
    MT1str1 = lstTostr(MT1, 1)
    MT1str2 = lstTostr(MT1, 2)
    MT1str3 = lstTostr(MT1, 3)
    MT1str4 = lstTostr(MT1, 4)
    MT1str5 = lstTostr(MT1, 5)
    MT1str6 = lstTostr(MT1, 6)
    MT1str7 = lstTostr(MT1, 7)
    MT1str8 = lstTostr(MT1, 8)
    MT1str9 = lstTostr(MT1, 9)
    MT1str10 = lstTostr(MT1, 10)
    MT1str11 = lstTostr(MT1, 11)

    return render(request, 'show_options.html', {
        'CS2' : CS2, 'lenCS2' : len(CS2), 'MT1' : MT1, 'lenMT1' : len(MT1), 'Max_Length' : Max_Length, 'ifMT1' : ifMT1, 'ifCS2' : ifCS2, 'SPL' : SPL, 'DPL' : DPL, 
        'CS2str0' : CS2str0, 'CS2str1':CS2str1, 'CS2str2':CS2str2, 'CS2str3': CS2str3, 'CS2str4':CS2str4, 'CS2str5':CS2str5, 'CS2str6':CS2str6, 'CS2str7':CS2str7, 'CS2str8':CS2str8, 'CS2str9':CS2str9, 'CS2str10':CS2str10, 'CS2str11': CS2str11,
        'MT1str0':MT1str0, 'MT1str1':MT1str1, 'MT1str2':MT1str2, 'MT1str3':MT1str3, 'MT1str4':MT1str4, 'MT1str5':MT1str5, 'MT1str6':MT1str6, 'MT1str7':MT1str7, 'MT1str8':MT1str8, 'MT1str9':MT1str9, 'MT1str10':MT1str10, 'MT1str11':MT1str11, 
        # 'options' : options
        }) 


def end(request):
    return render (request, 'end.html')


def search_CS2(SPL, DPL, ifsame, Max_Length):        #MT1, CS2, 
    loc = SPL[0].split(", ")
    rest_api_key = '39b09cd965f4787143f206403f3f370b'
    header = {'Authorization': 'KakaoAK ' + rest_api_key}
    params = {
        'x' : float(loc[1]), 
        'y' : float(loc[0]),
        'radius' : int(Max_Length), 
        'page' : 10,      #tochange
        'size' : 15,
        'sort' : 'distance', 
        } 
    keywords = '편의점'
    url = 'https://dapi.kakao.com/v2/local/search/keyword.json?query={}'.format(keywords)
    places = requests.get(url, headers=header, params=params).json()
    places = places.get('documents')
    lst = []
    # 0 : address_name / 1 : category_group_code / 2 : category_group_name / 3 : category_name / 4 : distance / 5 : id / 6 : phone / 7 : place_name / 8 : place_url / 9 : road_address_name / 10 : x / 11 : y
    for i in places:
        if i.get('category_group_code') == "CS2":
            to_append_list = []
            to_append_list.append(i.get('address_name'))
            to_append_list.append(i.get('category_group_code'))
            to_append_list.append(i.get('category_group_name'))
            to_append_list.append(i.get('category_name'))
            to_append_list.append(i.get('distance'))
            to_append_list.append(i.get('id'))
            to_append_list.append(i.get('phone'))
            to_append_list.append(i.get('place_name'))
            to_append_list.append(i.get('place_url'))
            to_append_list.append(i.get('road_address_name'))
            to_append_list.append(i.get('x'))
            to_append_list.append(i.get('y'))
            lst.append(to_append_list)
        else: pass
    return lst


def search_MT1(SPL, DPL, ifsame, Max_Length):        #MT1, CS2, 
    loc = SPL[0].split(", ")
    rest_api_key = '39b09cd965f4787143f206403f3f370b'
    header = {'Authorization': 'KakaoAK ' + rest_api_key}
    params = {
        'x' : float(loc[1]), 
        'y' : float(loc[0]),
        'radius' : int(Max_Length), 
        'page' : 10,      #tochange
        'size' : 15,
        'sort' : 'distance', 
        } 
    keywords = '마트'
    url = 'https://dapi.kakao.com/v2/local/search/keyword.json?query={}'.format(keywords)
    places = requests.get(url, headers=header, params=params).json()
    places = places.get('documents')
    lst = []
    # 0 : address_name / 1 : category_group_code / 2 : category_group_name / 3 : category_name / 4 : distance / 5 : id / 6 : phone / 7 : place_name / 8 : place_url / 9 : road_address_name / 10 : x / 11 : y
    for i in places:
        if i.get('category_group_code') == "CS2": pass
        elif i.get('category_group_code') == "PS3": pass
        elif i.get('category_group_code') == "SC4": pass
        elif i.get('category_group_code') == "AC5": pass
        elif i.get('category_group_code') == "PK6": pass
        elif i.get('category_group_code') == "OL7": pass
        elif i.get('category_group_code') == "SW8": pass
        elif i.get('category_group_code') == "BK9": pass
        elif i.get('category_group_code') == "CT1": pass
        elif i.get('category_group_code') == "AG2": pass
        elif i.get('category_group_code') == "PO3": pass
        elif i.get('category_group_code') == "AT4": pass
        elif i.get('category_group_code') == "AD5": pass
        elif i.get('category_group_code') == "FD6": pass
        elif i.get('category_group_code') == "CE7": pass
        elif i.get('category_group_code') == "HP8": pass
        elif i.get('category_group_code') == "PM9": pass
        else:
            to_append_list = []
            to_append_list.append(i.get('address_name'))
            to_append_list.append(i.get('category_group_code'))
            to_append_list.append(i.get('category_group_name'))
            to_append_list.append(i.get('category_name'))
            to_append_list.append(i.get('distance'))
            to_append_list.append(i.get('id'))
            to_append_list.append(i.get('phone'))
            to_append_list.append(i.get('place_name'))
            to_append_list.append(i.get('place_url'))
            to_append_list.append(i.get('road_address_name'))
            to_append_list.append(i.get('x'))
            to_append_list.append(i.get('y'))
            lst.append(to_append_list)
        
    return lst


def getlst (places):
    lst = []
    for place in places:
        to_append_lst = [] 
        to_append_lst.append(place[11])
        to_append_lst.append(place[10])
        lst.append(to_append_lst)
    
    return lst


def lstTostr(lst, indx):
    rslt = []
    prcs = []
    for i in range(0, len(lst), 1):
         prcs.append(lst[i][indx])
    rslt = str(prcs)
    rslt = rslt[1:-1]
    return rslt


def google_geocode (got_place):
    gmaps = googlemaps.Client(key = 'AIzaSyAawgC_tb1v8ro5BYuGs7BbhcuqYfI26ws')
    got_geocode = gmaps.geocode((got_place), language='ko')
    lst = got_geocode
    llst = []       #[0] : location x, y / [1] : formatted_address / [2] : address_type 
    loc_to_append = str(lst[0].get('geometry').get('location').get('lat'))
    loc_to_append = loc_to_append + ", " + str(lst[0].get('geometry').get('location').get('lng'))
    llst.append(loc_to_append)
    llst.append(lst[0].get('formatted_address'))
    llst.append(lst[0].get('types')[0])
    return llst


def get_map (ifsame, SPL, DPL, Max_Length, CS2L, MT1L, ifMT1, ifCS2, CS2, MT1):      #Starting_Point_List, Destination_List / each list contains 'formatted_addres', 'location', 'address_type'
    start = time.time() 
    
    #graph_from_address의 생성 포인트(중점)이 SPL, DPL 중점이 되도록(평균)
    SPLL = SPL[0].split(", ")
    DPLL = DPL[0].split(", ")
    SPLL[0] = float(SPLL[0])
    SPLL[1] = float(SPLL[1])
    DPLL[0] = float(DPLL[0])
    DPLL[1] = float(DPLL[1])
    spldplmiddlepoint = str((SPLL[0] + DPLL[0])/2) + ", " + str((SPLL[1] + DPLL[1])/2)

    G = ox.graph_from_address (spldplmiddlepoint, network_type = 'walk')        #get 이니까 저기 성남시 경기도 지역 부분을 변수로 

    spl = SPL[0].split(", ")
    spllat = float(str(spl[0]).strip())
    spllng = float(str(spl[1]).strip())
    orgn = ox.nearest_nodes(G, spllng, spllat)

    dpl = DPL[0].split(", ")
    dpllat = float(str(dpl[0]).strip())
    dpllng = float(str(dpl[1]).strip())
    dstn = ox.nearest_nodes(G, dpllng, dpllat)

    if len(CS2L) == 0:
        CS2L = [[]]
        CS2L[0].append(spllat)
        CS2L[0].append(spllng)
    if len(MT1L) == 0:
        MT1L = [[]]
        MT1L[0].append(dpllat)
        MT1L[0].append(dpllng)
    #nx.shortest_path_length(G, source=routes[p][i-1], target=routes[p][i], weight='length')
    #ox.shortest_path(G, orgn, dstn, weight = 'length')
    
    gotlst = getNodelst(G, CS2L, MT1L, CS2, MT1, ifCS2, ifMT1)      #0 : CS2_nodes / 1 : MT1_nodes
    CS2_nodes = gotlst[0]
    MT1_nodes = gotlst[1]
    CS2_nodes_7 = gotlst[2]
    MT1_nodes_7 = gotlst[3]
    
    DFSlst = DFSsearch(G, CS2_nodes, MT1_nodes, orgn, dstn, Max_Length, ifMT1, ifCS2)
    #DFSlst 0 : 모든 경우의 수 / 1 : 각 경우의 수 마다 길이 / 2 : 길이 순서 인덱스 리스트

    getOptionStr(DFSlst, CS2_nodes_7, MT1_nodes_7)

    routes = getRoutes(G, [3662605199, 4338819561])
    
    colorss = ['red', 'orange', 'yellow', 'green', 'blue', 'navy', 'violet', 'brown']       #빨주노초파남보갈
   
    if len(routes) == 0:
        ox.plot_graph(G, show = False, save = True, filepath = "OBSpjct/static/graphimage.png", node_size = 8)    
        graph_type = "not a route"
    elif len(routes) == 1:
        ox.plot_graph_route(G, routes[0], orig_dest_size=100, show = False, save = True, filepath = "OBSpjct/static/graphimage.png", route_linewidth = 5, node_size = 8)
        graph_type = "route"
    else:
        ox.plot_graph_routes(G, routes, route_colors = colorss[0:len(routes)], orig_dest_size=100, show = False, save = True, filepath = "OBSpjct/static/graphimage.png", route_linewidth = 5, node_size = 8)
        graph_type = "routes"
    

    end = time.time()       #프로세스 소요 시간 
    process_time = round(end - start, 4)
    
    

    print()
    print("===========================")
    print(str(process_time) + " sec")
    print(graph_type)
    print(orgn, dstn)
    print(CS2_nodes)
    print(MT1_nodes)
    print("===========================")
    print()


def forCS2(SPL, DPL, ifsame, Max_Length):
    rslt = []
    for p in range (0, int(Max_Length)+100, 100):
        src = search_CS2(SPL, DPL, ifsame,p)
        for q in range(0, len(src), 1):
            if src[q] not in rslt:
                rslt.append(src[q])
    return rslt


def forMT1(SPL, DPL, ifsame, Max_Length):
    rslt = []
    for p in range (0, int(Max_Length)+100, 100):
        src = search_MT1(SPL, DPL, ifsame, p)
        for q in range(0, len(src), 1):
            if src[q] not in rslt:
                rslt.append(src[q])
    return rslt


def DFSsearch(G, CS2_nodes, MT1_nodes, orgn, dstn, Max_Length, ifMT1, ifCS2):
    nodes_list = []
    if ifMT1 == "True": nodes_list += MT1_nodes
    if ifCS2 == "True": nodes_list += CS2_nodes
    ifvisited = [False]*len(nodes_list)
    rslt = []
    rslt_distance = []

    def jaguar(apxroute, n):        #재귀함수

        if n == len(nodes_list):
            rslt.append(copy.deepcopy(apxroute))
            return

        for i in range(len(nodes_list)):
            if not ifvisited[i]:
                ifvisited[i] = True
                apxroute.append(nodes_list[i])
                jaguar(apxroute, n+1)

                apxroute.pop()
                ifvisited[i] = False       

    jaguar([], 0)

    for p in range(0, len(rslt), 1):        #구한 노드 순서 맨 앞 맨 뒤에 orgn, dstn append 하는 메서드 
        rslt[p].insert(0, orgn)         #approximate route 맨 앞에 origin append
        rslt[p].insert(len(rslt[p]), dstn)      #approximate route 맨 뒤에 destination apped
    for q in range(0, len(rslt), 1):        #각 경우별 거리 합 구하는 로직. 다익스트라
        distanc = 0
        for x in range(1, len(rslt[q]), 1):
            distanc += nx.shortest_path_length(G, source=rslt[q][x-1], target=rslt[q][x], weight='length')
        rslt_distance.append(distanc)

    rslt_distance_c = copy.deepcopy(rslt_distance)      #순서 뽑기 위한 사본
    rslt_distance_c.sort()      

    rslt_distance_cc = copy.deepcopy(rslt_distance)     #사본 순서 리스트 seq에 중복 원소 인덱스 하나 반환 막기 위해
    
    rslt_distance_seq = []

    for x in range(0, len(rslt_distance), 1):
        indx = rslt_distance_cc.index(rslt_distance_c[x])
        rslt_distance_seq.append(indx)
        rslt_distance_cc[indx] = False      #이미 찾은건 False로. 다른 위치 같은 요소가 같은 인덱스 반환하는것 막기 위함, 0, 0, 5, 3, 4 ,2  -> 0, 1, 5, 3, 4, 2


    if rslt_distance.count(rslt_distance_c[0]) == 1:        #최단 경로가 하나일 떄 
        pass
    else:       #최단 경로가 하나가 아닐떄 
        pass
    
    rrslt = []

    for y in range(0, len(rslt_distance_seq), 1):       #순서대로 순서대로
        rrslt.append(rslt[rslt_distance_seq.index(y)])

    rtnlst = [rrslt, rslt_distance]

    return rtnlst


def getNodelst(G, CS2L, MT1L, CS2, MT1, ifCS2, ifMT1):      #get nearest_nodes 
    rslt = []
    cs2nodes = []
    mt1nodes = [] 
    cs2lat = []
    cs2lng = []
    mt1lng = []
    mt1lat = []
    cs2nodes_7 = []
    mt1nodes_7 = []

    for p in range(0, len(CS2L), 1):
        cs2lat.append(float(CS2L[p][0]))
        cs2lng.append(float(CS2L[p][1]))
        if ifCS2 == "True":
            cs2nodes_7.append(CS2[p][7])
    cs2nodes = ox.nearest_nodes(G, cs2lng, cs2lat)
    
    for q in range(0, len(MT1L), 1):
        mt1lat.append(float(MT1L[q][0]))
        mt1lng.append(float(MT1L[q][1]))
        if ifMT1 == "True":
           mt1nodes_7.append(MT1[q][7])
    mt1nodes = ox.nearest_nodes(G, mt1lng, mt1lat)

    rslt.append(cs2nodes)
    rslt.append(mt1nodes)
    rslt.append(cs2nodes_7)
    rslt.append(mt1nodes_7)

    return rslt 


def getRoutes(G, nodelist):
    routes = []
    for i in range(1, len(nodelist), 1):
        route = ox.shortest_path(G, nodelist[i-1], nodelist[i], weight = 'length')
        routes.append(route)
    return routes


def getOptionStr(SRClist, CS2_nodes_7, MT1_nodes_7):
    print(SRClist[0])
    print(len(SRClist[0]))