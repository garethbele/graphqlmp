import graphene
from graphene_django import DjangoObjectType
from .models_mysql import Student, University
from .models_pg import Course, StudentCourse

class CourseType(DjangoObjectType):
    students = graphene.List(lambda: StudentType)  # <-- add students list

    class Meta:
        model = Course
        fields = "__all__"

    def resolve_students(self, info):
        # get all student IDs enrolled in this course (use .using() to query postgres_db)
        student_ids = list(StudentCourse.objects.using('postgres_db').filter(course_id=self.id).values_list("student_id", flat=True))

        # If there are no students, return an empty list to avoid unnecessary database calls
        if not student_ids:
            return []

        # Return the students from MySQL database based on the fetched student IDs
        return Student.objects.using('mysql_db').filter(id__in=student_ids)



class StudentType(DjangoObjectType):
    courses = graphene.List(CourseType)  # <-- add courses list

    class Meta:
        model = Student
        fields = "__all__"

    def resolve_courses(self, info):
        # get all course IDs where this student is enrolled
        course_ids = StudentCourse.objects.using('postgres_db').filter(
            student_id=self.id
        ).values_list("course_id", flat=True)

        return Course.objects.using('postgres_db').filter(id__in=course_ids)


class UniversityType(DjangoObjectType):
    class Meta:
        model = University
        fields = "__all__"


class StudentCourseType(DjangoObjectType):
    class Meta:
        model = StudentCourse
        fields = "__all__"




class Query(graphene.ObjectType):
    students = graphene.List(StudentType)
    student = graphene.Field(StudentType, id=graphene.Int(required=True))
    universities = graphene.List(UniversityType)
    courses = graphene.List(CourseType)
    course = graphene.Field(CourseType, id=graphene.Int(required=True))  # Add this line for querying a specific course
    student_courses = graphene.List(StudentCourseType)

    def resolve_students(root, info):
        return Student.objects.using('mysql_db').all()

    def resolve_student(root, info, id):
        return Student.objects.using('mysql_db').get(id=id)

    def resolve_universities(root, info):
        return University.objects.using('mysql_db').all()

    def resolve_courses(root, info):
        return Course.objects.using('postgres_db').all()

    def resolve_course(root, info, id):  # Resolver for querying a specific course by ID
        return Course.objects.using('postgres_db').get(id=id)

    def resolve_student_courses(root, info):
        return StudentCourse.objects.using('postgres_db').all()



schema = graphene.Schema(query=Query)
