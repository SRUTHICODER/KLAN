from unicodedata import name
from django.urls import path
from . import views
urlpatterns=[
    path("",views.login,name="login"),
    path("home/",views.home,name="home"),
    path("check/",views.check,name="check"),
    path("jsd/",views.again,name="again"),
    path("ask/",views.ask,name="ask"),
    path("answer/",views.answer_page,name="answer_page"),
    path("notf/",views.notf,name="notf"),
    path("question/<int:q_id>",views.ques,name="ques"),
    path("logout",views.logout,name="logout"),
    path("filt",views.filt,name="filt"),
    path("lib/",views.liba,name="liba"),
    path("ans/<int:q_id>",views.answer1,name="answer1"),
    path("prohome/",views.pro_home,name="prohome"),
    path("proquever/<int:q_id>",views.ques_ver,name="ques_ver"),
    path("anslistp/",views.ans_list,name="anslistp"),
    path("quesagree/",views.qagree,name="qagree"),
    path("quesaa/",views.qaa,name="qaa"),
    path("quesd/",views.qd,name="qd"),
    path("proans/<int:q_id>",views.proans,name="proans"),
    path("ansver/<int:q_id>",views.ansver,name="ansver"),
    path("aa/",views.aa,name="aa"),
    path("ad/",views.ad,name="ad"),
    path("save/",views.save,name="save")
]