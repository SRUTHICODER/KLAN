from ast import ClassDef
from msilib.schema import Class
from django.contrib import admin
from .models import *
# Register your models here.

class student_detailsAdmin(admin.ModelAdmin):
    list_display=("s_id","s_fname","s_lname","dob","gender","q_p","q_a","r_no","dept")

class professorDetailsAdmin(admin.ModelAdmin):
    list_display=("p_id","p_fname","p_lname","dob","gender","q_v","q_a","a_v","dept","domain")

class questionAdmin(admin.ModelAdmin):
    list_display=("s_id","q_id","q_text","domain","time")

class questionVerifiedAdmin(admin.ModelAdmin):
    list_display=("q_id","p_id","result")

class answerAdmin(admin.ModelAdmin):
    list_display=("q_id","s_id","a_id","a_text","up","down")

class answerVerifiedAdmin(admin.ModelAdmin):
    list_display=("a_id","p_id","result")

class timeOutAdmin(admin.ModelAdmin):
    list_display=("s_id","p_id","time","q_id","a_id","s_time")

class questionJpgAdmin(admin.ModelAdmin):
    list_display=("q_id","img_link")

class answerJpgAdmin(admin.ModelAdmin):
    list_display=("a_id","img_link")

class visterAdmin(admin.ModelAdmin):
    list_display=("live","total")

class nofAdmin(admin.ModelAdmin):
    list_display=("q_id","s_id","typ")

class libAdmin(admin.ModelAdmin):
    list_display=("s_id","q_id")

class quesPBNAAdmin(admin.ModelAdmin):
    list_display=("q_id",)

admin.site.register(student_details,student_detailsAdmin)
admin.site.register(professor_details,professorDetailsAdmin)
admin.site.register(question,questionAdmin)
admin.site.register(question_verified,questionVerifiedAdmin)
admin.site.register(answer,answerAdmin)
admin.site.register(answer_verified,answerVerifiedAdmin)
admin.site.register(time_out,timeOutAdmin)
admin.site.register(question_jpg,questionJpgAdmin)
admin.site.register(answer_jpg,answerJpgAdmin)
admin.site.register(visters,visterAdmin)
admin.site.register(nof,nofAdmin)
admin.site.register(lib,libAdmin)
admin.site.register(ques_pbna,quesPBNAAdmin)