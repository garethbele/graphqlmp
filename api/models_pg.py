from django.db import models

class Course(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    instructor = models.CharField(max_length=100)
    category = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'courses_course'
        app_label = 'api_pg'

class StudentCourse(models.Model):
    id = models.IntegerField(primary_key=True)
    student_id = models.IntegerField()
    course_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'courses_student'
        app_label = 'api_pg'
