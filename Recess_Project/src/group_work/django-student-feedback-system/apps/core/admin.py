from django.contrib import admin
from .models import Student, Course,Campus_facilities,Instructor

admin.site.register(Student)
admin.site.register(Course)
admin.site.register(Campus_facilities)
admin.site.register(Instructor)