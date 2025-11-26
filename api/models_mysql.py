from django.db import models

class Student(models.Model):
    id = models.IntegerField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    university_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'student'
        app_label = 'api_mysql'

class University(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'university'
        app_label = 'api_mysql'
