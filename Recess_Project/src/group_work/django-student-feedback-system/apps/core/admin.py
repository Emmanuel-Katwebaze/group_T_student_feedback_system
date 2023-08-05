from django.contrib import admin
from .models import Student, Course,CampusFacility,Instructor, Question, Form, FormCategory, StudentResponse

admin.site.register(Student)
admin.site.register(Course)
admin.site.register(CampusFacility)
admin.site.register(Instructor)
admin.site.register(Question)
admin.site.register(Form)
admin.site.register(FormCategory)
admin.site.register(StudentResponse)