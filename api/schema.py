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
        # get all student IDs enrolled in this course
        student_ids = list(
            StudentCourse.objects.using('postgres2').filter(course_id=self.id)
            .values_list("student_id", flat=True)
        )

        if not student_ids:
            return []

        # Return the students from Postgres1 (formerly MySQL replacement)
        return Student.objects.using('postgres1').filter(id__in=student_ids)


class StudentType(DjangoObjectType):
    courses = graphene.List(CourseType)  # <-- add courses list

    class Meta:
        model = Student
        fields = "__all__"

    def resolve_courses(self, info):
        # get all course IDs where this student is enrolled
        course_ids = StudentCourse.objects.using('postgres2').filter(
            student_id=self.id
        ).values_list("course_id", flat=True)

        return Course.objects.using('postgres2').filter(id__in=course_ids)


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
    course = graphene.Field(CourseType, id=graphene.Int(required=True))
    student_courses = graphene.List(StudentCourseType)

    def resolve_students(root, info):
        return Student.objects.using('postgres1').all()

    def resolve_student(root, info, id):
        return Student.objects.using('postgres1').get(id=id)

    def resolve_universities(root, info):
        return University.objects.using('postgres1').all()

    def resolve_courses(root, info):
        return Course.objects.using('postgres2').all()

    def resolve_course(root, info, id):
        return Course.objects.using('postgres2').get(id=id)

    def resolve_student_courses(root, info):
        return StudentCourse.objects.using('postgres2').all()


schema = graphene.Schema(query=Query)
