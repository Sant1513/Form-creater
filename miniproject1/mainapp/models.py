from django.db import models

# Create your models here.
class User_details(models.Model):
    name=models.CharField(max_length=40)
    email=models.EmailField(unique=True)
    password=models.CharField(max_length=20)
    role=models.CharField(max_length=10)
    status=models.CharField(max_length=20,default="unaccept")
    def __str__(self):
        return self.name
    
class SubjectChoices(models.Model):
    subject_code=models.CharField(max_length=20)
    subject_name=models.CharField(max_length=40)
    def __str__(self):
        return self.subject_code