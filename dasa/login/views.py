from audioop import reverse
from time import time
from unittest import result
from urllib import response
from django.http import  HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from mysqlx import Result
from .models import *
import datetime

def set_cookie(response, key, value, days_expire=30):
    if days_expire is None:
        max_age = 365 * 24 * 60 * 60  
    else:
        max_age = days_expire * 24 * 60 * 60
    expires = datetime.datetime.strftime(
        datetime.datetime.utcnow() + datetime.timedelta(seconds=max_age),
        "%a, %d-%b-%Y %H:%M:%S GMT",
    )
    response.set_cookie(
        key,
        value,
        max_age=max_age,
        expires=expires
    )

# Create your views here.
def login(request): 
    if 'username' in request.COOKIES and 'passwd' in request.COOKIES and 'log' in request.COOKIES:
        if request.COOKIES['log'] == 's':
            data=student_details.objects.filter(s_fname=request.COOKIES['username'],r_no=request.COOKIES['passwd'])
            if data:
                return HttpResponseRedirect(reverse('home'))
            else:
                return render(request,"login.html")
        else:
            data=professor_details.objects.filter(p_fname=request.COOKIES['username'],p_lname=request.COOKIES['passwd'])
            if data:
                return HttpResponseRedirect(reverse('prohome'))
            else:
                return render(request,"login.html")
    else:
        return render(request,"login.html")

def again(request):
    return render(request,"login.html")

def ask(request):
    if 'username' in request.COOKIES and 'passwd' in request.COOKIES and 'log' in request.COOKIES:
        if request.COOKIES['log'] == 's':
            data=student_details.objects.filter(s_fname=request.COOKIES['username'],r_no=request.COOKIES['passwd'])
            if request.method=="GET":
                if data:
                    return render(request,"ask.html")
                else:
                    return HttpResponseRedirect(reverse('login'))
            if request.method=="POST":
                text=request.POST["ansBox"]
                domain=request.POST["dom"]
                link_text=request.POST["lin"]
                li=question.objects.all()
                ob1=question.objects.create(s_id=data[0],q_text=text,domain=domain,time=datetime.datetime.now(),result="false")
                if ob1 not in li:
                    question.save(ob1)
                if link_text.strip():
                    ob2=question_jpg.objects.create(q_id=ob1,img_link=link_text)
                    question_jpg.save(ob2)
                data[0].q_p+=1
                data[0].save()
                return HttpResponseRedirect(reverse('home'))
    return HttpResponseRedirect(reverse('login'))
    
def answer_page(request):
    if 'username' in request.COOKIES and 'passwd' in request.COOKIES and 'log' in request.COOKIES:
        if request.COOKIES['log'] == 's':
            data=student_details.objects.filter(s_fname=request.COOKIES['username'],r_no=request.COOKIES['passwd'])
            if data:
                return render(request,"answer_page.html",{
                    "ques":ques_pbna.objects.all()
                })
    return HttpResponseRedirect(reverse('login'))

def notf(request):
    if 'username' in request.COOKIES and 'passwd' in request.COOKIES and 'log' in request.COOKIES:
        if request.COOKIES['log'] == 's':
            data=student_details.objects.filter(s_fname=request.COOKIES['username'],r_no=request.COOKIES['passwd'])
            if data:
                if request.method=="GET":
                    da=nof.objects.filter(s_id=data[0])
                    print(da)
                    return render(request,'nof.html',{
                        "nof": da

                    })
    return HttpResponseRedirect(reverse('login'))    

def ques(request,q_id):
    if 'username' in request.COOKIES and 'passwd' in request.COOKIES and 'log' in request.COOKIES:
        if request.COOKIES['log'] == 's':
            data=student_details.objects.filter(s_fname=request.COOKIES['username'],r_no=request.COOKIES['passwd'])
            if data:
                if request.method=="GET":
                    data0=question.objects.filter(q_id=q_id)
                    data1=answer.objects.filter(q_id=data0[0])
                    data2=question_jpg.objects.filter(q_id=data0[0])
                    data3=answer_jpg.objects.all()
                    if data2:
                        return render(request,"question.html",{
                            "ques": data0[0],
                            "ans": data1,
                            "q_img": data2[0],
                            "a_img": data3,
                            "ver": answer_verified.objects.all()
                        })
                    else:
                        return render(request,"question.html",{
                            "ques": data0[0],
                            "ans": data1,
                            "q_img": "ans",
                            "a_img": data3
                        })
                if request.method=="POST":
                    pass
    return HttpResponseRedirect(reverse('login'))

def home(request):
    if 'username' in request.COOKIES and 'passwd' in request.COOKIES and 'log' in request.COOKIES:
        if request.COOKIES['log'] == 's':
            data=student_details.objects.filter(s_fname=request.COOKIES['username'],r_no=request.COOKIES['passwd'])
            if data:
                data1=question_verified.objects.filter(result="true")
                return render(request,"mainLogin.html",{
                    "question": data1,
                    "data":data[0]
                })
            else:
                return HttpResponseRedirect(reverse('login'))
    return HttpResponseRedirect(reverse('login'))


def check(request):
    if request.method=="POST":
        usname=request.POST["username"]
        passwd=request.POST["passwd"]
        opt=request.POST["sel"]
        if opt=="student":
            data=student_details.objects.filter(s_fname=usname,r_no=passwd)
        else:
            data=professor_details.objects.filter(p_fname=usname,p_lname=passwd)
        if data :
            if opt=="student":
                response=HttpResponseRedirect(reverse('home'))
                set_cookie(response,'username', usname)
                set_cookie(response,'passwd', passwd)
                set_cookie(response,'log','s')
                return response
            else:
                response=HttpResponseRedirect(reverse('prohome'))
                set_cookie(response,'username', usname)
                set_cookie(response,'passwd', passwd)
                set_cookie(response,'log','p')
                return response
        else:
            return HttpResponseRedirect(reverse("again"))

def logout(request):
    response=HttpResponseRedirect(reverse('login'))
    response.delete_cookie("username")
    response.delete_cookie("passwd")
    response.delete_cookie("log")
    return response

def filt(request):
    if 'username' in request.COOKIES and 'passwd' in request.COOKIES and 'log' in request.COOKIES:
        if request.COOKIES['log'] == 's':
            data=student_details.objects.filter(s_fname=request.COOKIES['username'],r_no=request.COOKIES['passwd'])
            if data:
                if request.method=="POST":
                    dept=request.POST["filter_dept"]
                    domain=request.POST["filter_domain"]
                    if dept == "dept" and domain == "domain":
                        return HttpResponseRedirect(reverse('answer_page'))
                    ques=ques_pbna.objects.all()
                    return render(request,"ans_page_fit.html",{
                        "ques": ques,
                        "dept": dept,
                        "domain": domain
                    })
    return HttpResponseRedirect(reverse('login'))

def liba(request):
    if 'username' in request.COOKIES and 'passwd' in request.COOKIES and 'log' in request.COOKIES:
        if request.COOKIES['log'] == 's':
            data=student_details.objects.filter(s_fname=request.COOKIES['username'],r_no=request.COOKIES['passwd'])
            if data:
                if request.method=="GET":
                    return render(request,"lib.html",{
                        "libb": lib.objects.filter(s_id=data[0])
                    })
    return HttpResponseRedirect(reverse('login'))

def answer1(request,q_id):
    if 'username' in request.COOKIES and 'passwd' in request.COOKIES and 'log' in request.COOKIES:
        if request.COOKIES['log'] == 's':
            data=student_details.objects.filter(s_fname=request.COOKIES['username'],r_no=request.COOKIES['passwd'])
            if data:
                if request.method=="GET":
                    data1=ques_pbna.objects.all()
                    a=0
                    for da in data1:
                        if da.q_id.q_id==q_id:
                            a=1
                    if a==1:
                        data2=question.objects.filter(q_id=q_id)
                        data3=question_jpg.objects.filter(q_id=data2[0])
                        if data3:
                            return render(request,'ans_add.html',{
                                "que": data2[0],
                                "img": data3[0]
                            })
                        else:
                            return render(request,'ans_add.html',{
                                "que": data2[0],
                                "img": "abc"
                            })
                if request.method=="POST":
                    ans_text=request.POST["ansBox"]
                    img_link=request.POST["lin"]
                    data1=question.objects.filter(q_id=q_id)
                    obj1=answer.objects.create(q_id=data1[0],s_id=data[0],a_text=ans_text,up=0,down=0)
                    answer.save(obj1)
                    obj3=nof.objects.create(q_id=data1,s_id=data1.s_id,typ=1)
                    nof.save(obj3)
                    if img_link.strip():
                        obj2=answer_jpg.objects.filter(a_id=obj1,img_link=img_link)
                        answer_jpg.save(obj2)
                    data[0].q_a+=1
                    data[0].save()
    return HttpResponseRedirect(reverse('login'))


def pro_home(request):
    if 'username' in request.COOKIES and 'passwd' in request.COOKIES and 'log' in request.COOKIES:
        if request.COOKIES['log'] == 'p':
            data=professor_details.objects.filter(p_fname=request.COOKIES['username'],p_lname=request.COOKIES['passwd'])
            if data:
                if request.method=="GET":
                    da=question.objects.filter(result="false")
                    return render(request,'pro_home.html',{
                        "question":da,
                        "pro": data[0]
                    })
    return HttpResponseRedirect(reverse('login'))
def ques_ver(request,q_id):
    if 'username' in request.COOKIES and 'passwd' in request.COOKIES and 'log' in request.COOKIES:
        if request.COOKIES['log'] == 'p':
            data=professor_details.objects.filter(p_fname=request.COOKIES['username'],p_lname=request.COOKIES['passwd'])
            if data:
                if request.method=="GET":
                    data1=question.objects.filter(q_id=q_id)
                    if data1:
                        return render(request,'quesver.html',{
                            "question":data1[0],
                            "img": question_jpg.objects.filter(q_id=data1[0])
                        })
    return HttpResponseRedirect(reverse('login'))

def ans_list(request):
    if 'username' in request.COOKIES and 'passwd' in request.COOKIES and 'log' in request.COOKIES:
        if request.COOKIES['log'] == 'p':
            data=professor_details.objects.filter(p_fname=request.COOKIES['username'],p_lname=request.COOKIES['passwd'])
            if data:
                if request.method=="GET":
                    return render(request,'pro_ans.html',{
                        "question":ques_pbna.objects.all(),
                        "pro": data[0]
                    })
    return HttpResponseRedirect(reverse('login'))

def qagree(request):
    if 'username' in request.COOKIES and 'passwd' in request.COOKIES and 'log' in request.COOKIES:
        if request.COOKIES['log'] == 'p':
            data=professor_details.objects.filter(p_fname=request.COOKIES['username'],p_lname=request.COOKIES['passwd'])
            if data:
                if request.method=="POST":
                    i=request.POST["i"]
                    data1=question.objects.get(q_id=i)
                    obj1=ques_pbna.objects.create(q_id=data1)
                    li=ques_pbna.objects.all()
                    if obj1 not in li:
                        ques_pbna.save(obj1)
                    obj2=question_verified.objects.create(q_id=data1,p_id=data[0],result="true")
                    question_verified.save(obj2)
                    data[0].q_v+=1
                    data[0].save()
                    data1.result="true"
                    data1.save()
                    obj3=nof.objects.create(q_id=data1,s_id=data1.s_id,typ=0)
                    nof.save(obj3)
                    return HttpResponseRedirect(reverse('prohome'))
    return HttpResponseRedirect(reverse('login'))

def qaa(request):
    if 'username' in request.COOKIES and 'passwd' in request.COOKIES and 'log' in request.COOKIES:
        if request.COOKIES['log'] == 'p':
            data=professor_details.objects.filter(p_fname=request.COOKIES['username'],p_lname=request.COOKIES['passwd'])
            if data:
                if request.method=="POST":
                    i=request.POST["i"]
                    data1=question.objects.filter(q_id=i)
                    obj1=ques_pbna.objects.create(q_id=data1[0])
                    ques_pbna.save(obj1)
                    obj2=question_verified.objects.create(q_id=data1[0],p_id=data[0].p_id,result="true")
                    question_verified.save(obj2)
                    data[0].q_v+=1
                    data[0].save()
                    data1[0].result="true"
                    data1[0].save()
    return HttpResponseRedirect(reverse('login'))

def qd(request):
    if 'username' in request.COOKIES and 'passwd' in request.COOKIES and 'log' in request.COOKIES:
        if request.COOKIES['log'] == 'p':
            data=professor_details.objects.filter(p_fname=request.COOKIES['username'],p_lname=request.COOKIES['passwd'])
            if data:
                if request.method=="POST":
                    i=request.POST["i"]
                    data1=question.objects.get(q_id=i)
                    data1.delete()
                    data[0].q_v+=1
                    data[0].save()
                    return HttpResponseRedirect(reverse('prohome'))
    return HttpResponseRedirect(reverse('login'))

def proans(request,q_id):
    if 'username' in request.COOKIES and 'passwd' in request.COOKIES and 'log' in request.COOKIES:
        if request.COOKIES['log'] == 'p':
            data=professor_details.objects.filter(p_fname=request.COOKIES['username'],p_lname=request.COOKIES['passwd'])
            if data:
                if request.Method=="GET":
                    data1=question.objects.filter(q_id=q_id)
                    return render(request,"proans.html",{
                        "question": data1[0],
                        "img": question_jpg.objects.filter(q_id=data1[0])
                    })
                if request.method=="POST":
                    ans_text=request.POST["ansBox"]
                    img_link=request.POST["lin"]
                    data1=question.objects.filter(q_id=q_id)
                    obj1=answer.objects.create(q_id=data1[0],s_id=data[0],a_text=ans_text,up=0,down=0)
                    answer.save(obj1)
                    if img_link.strip():
                        obj2=answer_jpg.objects.filter(a_id=obj1,img_link=img_link)
                        answer_jpg.save(obj2)
                    data2=ques_pbna.objects.get(q_id=data1[0])
                    data2.delete()
                    obj3=answer_verified(a_id=obj1,p_id=data[0],result="true")
                    answer_verified.save(obj3)
                    data[0].q_a+=1
                    data[0].save()
                    return HttpResponseRedirect(reverse('prohome'))
    return HttpResponseRedirect(reverse('login'))

def ansver(request,q_id):
    if 'username' in request.COOKIES and 'passwd' in request.COOKIES and 'log' in request.COOKIES:
        if request.COOKIES['log'] == 'p':
            data=professor_details.objects.filter(p_fname=request.COOKIES['username'],p_lname=request.COOKIES['passwd'])
            if data:
                if request.method=="GET":
                    data1=question.objects.filter(q_id=q_id)
                    return render(request,"ansver.html",{
                        "question": data1[0],
                        "img": question_jpg.objects.filter(q_id=data1[0]),
                        "ans": answer.objects.filter(q_id=data1[0]),
                        "ansimg":answer_jpg.objects.all()
                    })
                if request.method=="POST":
                    ans_text=request.POST["ansBox"]
                    img_link=request.POST["lin"]
                    data1=question.objects.filter(q_id=q_id)
                    obj1=answer.objects.create(q_id=data1[0],s_id=data[0],a_text=ans_text,up=0,down=0)
                    answer.save(obj1)
                    if img_link.strip():
                        obj2=answer_jpg.objects.filter(a_id=obj1,img_link=img_link)
                        answer_jpg.save(obj2)
                    data2=ques_pbna.objects.get(q_id=data1[0])
                    data2.delete()
                    obj3=answer_verified(a_id=obj1,p_id=data[0],result="true")
                    answer_verified.save(obj3)
                    data[0].q_a+=1
                    data[0].save()
                    return HttpResponseRedirect(reverse('prohome'))
    return HttpResponseRedirect(reverse('login'))

def aa(request):
    if 'username' in request.COOKIES and 'passwd' in request.COOKIES and 'log' in request.COOKIES:
        if request.COOKIES['log'] == 'p':
            data=professor_details.objects.filter(p_fname=request.COOKIES['username'],p_lname=request.COOKIES['passwd'])
            if data:
                if request.method=="POST":
                    i=request.POST["i"]
                    j=request.POST["j"]
                    data1=question.objects.get(q_id=i)
                    data2=ques_pbna.objects.get(q_id=i)
                    data2.delete()
                    data3=answer.objects.get(a_id=j)
                    obj1=answer_verified.objects.create(a_id=data3,p_id=data[0],result="true")
                    answer_verified.save(obj1)
                    obj2=nof.objects.create(q_id=data1,s_id=data1.s_id,typ=2)
                    nof.save(obj2)
                    return HttpResponseRedirect(reverse('proans'))
    return HttpResponseRedirect(reverse('login'))


def ad(request):
    if 'username' in request.COOKIES and 'passwd' in request.COOKIES and 'log' in request.COOKIES:
        if request.COOKIES['log'] == 'p':
            data=professor_details.objects.filter(p_fname=request.COOKIES['username'],p_lname=request.COOKIES['passwd'])
            if data:
                if request.method=="POST":
                    return HttpResponseRedirect(reverse('proans'))
    return HttpResponseRedirect(reverse('login'))

def save(request):
    if 'username' in request.COOKIES and 'passwd' in request.COOKIES and 'log' in request.COOKIES:
        if request.COOKIES['log'] == 's':
            data=student_details.objects.filter(s_fname=request.COOKIES['username'],r_no=request.COOKIES['passwd'])
            if data:
                if request.method=="POST":
                    i=request.POST["i"]
                    data2=question.objects.get(q_id=i)
                    obj1=lib.objects.create(s_id=data[0],q_id=data2)
                    lib.save(obj1)
                    return HttpResponseRedirect(reverse('home'))
    return HttpResponseRedirect(reverse('login'))