import random
import string

import mysql.connector
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect

from FirstApp.models import urls


def index(request):
    print('hello')
    print(request.POST)
    email = request.POST.get('email')
    password = request.POST.get('password')

    test = mysql.connector.connect(host='localhost', user='root',
                                   password='rajat@1234', database="db2")
    crs = test.cursor()
    crs.execute("select * from book")

    for a in crs:
        print(a)
    return HttpResponse("Hello,Index.")


def index1(request):
    print(request.POST)
    email = request.POST.get('email')
    password = request.POST.get('password')

    test = mysql.connector.connect(host='localhost', user='root',
                                   password='rajat@1234', database="DB2")
    print(test)
    crs = test.cursor()
    crs.execute("SHOW TABLES")
    for a in crs:
        print(a)
    return HttpResponse("Hello,Index1.")


def index2(request):
    return HttpResponse("Hello,Index2.")


def login(request):
    email = request.GET.get("email")
    password = request.GET.get("password")
    test = mysql.connector.connect(host='localhost', user='root',
                                   password='rajat@1234', database='db2')
    crs = test.cursor()
    query = "select password from user where email = '" + email + "'"
    crs.execute(query)
    data = crs.fetchone()
    dict = {}
    if data is None:
        dict["message"] = "you are not registered now"
    else:
        if data[0] == password:
            dict["message"] = "you are valid user"
        else:
            dict["message"] = "your password is not correct"

    return JsonResponse(dict)


def signup(request):
    email = request.GET.get("email")
    password = request.GET.get("password")
    test = mysql.connector.connect(host='localhost', user='root', password='rajat@1234',
                                   database='db2')
    crs = test.cursor()
    query = "select * from user where email = '" + email + "'"
    crs.execute(query)
    data = crs.fetchone()
    dict = {}
    if data is None:
        query = "insert into user values ('" + email + "','" + password + "')"
        crs.execute(query)
        test.commit()
        dict["message"] = "registered sucessfully"
        # return HttpResponse("registered successfully")
    else:
        dict["message"] = "you are already registered now"
        # return HttpResponse("you are already registered user")
    return JsonResponse(dict)


def getalluser(request):
    test = mysql.connector.connect(host='localhost', user='root', password='rajat@1234',
                                   database='db2')
    crs = test.cursor()
    query = "select * from user"
    crs.execute(query)
    data = crs.fetchall()
    dict = {}
    list = []
    if data is None:
        dict['message'] = "no registered user found"
    else:
        for l in data:
            d = {}
            d['email'] = l[0]
            d['password'] = l[1]
            list.append(d)
        dict['data'] = list
    return JsonResponse(dict)


def getStates(request):
    test = mysql.connector.connect(host='localhost', user='root', password='rajat@1234',
                                   database='db2')
    crs = test.cursor()
    query = "select * from states"
    crs.execute(query)
    data = crs.fetchall()
    dict = {}
    list = []
    if data is None:
        dict['message'] = 'States data is not available'
    else:
        for l in data:
            d = {}
            d['state_id'] = l[0]
            d['state_name'] = l[1]
            list.append(d)
        dict['states'] = list
        dict['ttl'] = len(list)

    return JsonResponse(dict)


def getDistrict(request, id):
    # stateID = request.GET.get("state_id")
    test = mysql.connector.connect(host='localhost', user='root', password='rajat@1234',
                                   database='db2')
    crs = test.cursor()
    query = "select * from district where state_id = '" + id + "'"
    crs.execute(query)
    data = crs.fetchall()
    dict = {}
    list = []
    if data is None:
        dict['message'] = "District are not available"
    else:
        for l in data:
            d = {}
            d['district_id'] = l[0]
            d['district_name'] = l[1]
            list.append(d)
            dict["districts"] = list
            dict["ttl"] = len(list)

    return JsonResponse(dict)


def shorturl(request):
    longurl = request.GET.get("longurl")
    customurl = request.GET.get("customurl")
    if customurl is None or customurl == "":
        while True:
            shorturl = generaterandomstring(5)
            data = urls.objects.filter(short_urls=shorturl)
            if len(data) == 0:
                url = urls(long_urls=longurl, short_urls=shorturl)
                url.save()
                break
    else:
        data = urls.objects.filter(short_urls=customurl)
        if len(data) == 0:
            url = urls(long_urls=longurl, short_urls=customurl)
            url.save()
        else:
            return HttpResponse("custom url already exist try something else")

    return HttpResponse("saved")


def generaterandomstring(size):
    letter = string.ascii_letters + string.digits
    shorturl = ""
    for i in range(size):
        shorturl = shorturl + "".join(random.choice(letter))
    return shorturl


def gotolongurl(request, shorturl):
    data = urls.objects.filter(short_url=shorturl)
    if len(data) == 0:
        return HttpResponse("Oops, This short url is not created through us")
    else:
        newdata = data[0]
        return redirect(newdata.long_url)
