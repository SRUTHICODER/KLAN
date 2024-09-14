from django.db import models

# Create your models here.
class student_details(models.Model):
    s_id=models.AutoField(primary_key=True,unique=True)
    s_fname=models.CharField(max_length=25)
    s_lname=models.CharField(max_length=25)
    dob=models.DateField()
    gender=models.CharField(max_length=15)
    q_p=models.IntegerField() 
    q_a=models.IntegerField()
    r_no=models.CharField(max_length=8) 
    dept=models.CharField(max_length=50)

class professor_details(models.Model):
    p_id=models.AutoField(primary_key=True,unique=True)
    p_fname=models.CharField(max_length=25)
    p_lname=models.CharField(max_length=25)
    dob=models.DateField()
    gender=models.CharField(max_length=15)
    q_v=models.IntegerField() 
    q_a=models.IntegerField() 
    a_v=models.IntegerField() 
    dept=models.CharField(max_length=50)
    domain=models.CharField(max_length=50)

class question(models.Model):
    s_id=models.ForeignKey(student_details,on_delete=models.CASCADE)
    q_id=models.AutoField(primary_key=True,unique=True)
    q_text=models.CharField(max_length=500)
    domain=models.CharField(max_length=50)
    time=models.DateTimeField()
    result=models.CharField(max_length=5)
    
class question_verified(models.Model):
    q_id=models.ForeignKey(question,on_delete=models.CASCADE)
    p_id=models.ForeignKey(professor_details,on_delete=models.CASCADE)
    result=models.CharField(max_length=5)

class answer(models.Model):
    q_id=models.ForeignKey(question,on_delete=models.CASCADE)
    s_id=models.ForeignKey(student_details,on_delete=models.CASCADE)
    a_id=models.AutoField(primary_key=True,unique=True)
    a_text=models.CharField(max_length=250)
    up=models.IntegerField()
    down=models.IntegerField()

class answer_verified(models.Model):
    a_id=models.ForeignKey(answer,on_delete=models.CASCADE)
    p_id=models.ForeignKey(professor_details,on_delete=models.CASCADE)
    result=models.CharField(max_length=5)

class time_out(models.Model):
    s_id=models.ForeignKey(student_details,on_delete=models.CASCADE)
    p_id=models.ForeignKey(professor_details,on_delete=models.CASCADE)
    time=models.DateTimeField()
    q_id=models.ForeignKey(question,on_delete=models.CASCADE,null=True)
    a_id=models.ForeignKey(answer,on_delete=models.CASCADE,null=True)
    s_time=models.DateField()

class question_jpg(models.Model):
     q_id=models.ForeignKey(question,on_delete=models.CASCADE)
     img_link=models.CharField(max_length=250)
    
class answer_jpg(models.Model):
    a_id=models.ForeignKey(answer,on_delete=models.CASCADE)
    img_link=models.CharField(max_length=250)

class visters(models.Model):
    live=models.IntegerField()
    total=models.IntegerField()

class nof(models.Model):
    q_id=models.ForeignKey(question,on_delete=models.CASCADE) 
    s_id=models.ForeignKey(student_details,on_delete=models.CASCADE)
    typ=models.IntegerField()

class lib(models.Model):
    s_id=models.ForeignKey(student_details,on_delete=models.CASCADE)
    q_id=models.ForeignKey(question,on_delete=models.CASCADE)

class ques_pbna(models.Model):
    q_id=models.ForeignKey(question,on_delete=models.CASCADE)
