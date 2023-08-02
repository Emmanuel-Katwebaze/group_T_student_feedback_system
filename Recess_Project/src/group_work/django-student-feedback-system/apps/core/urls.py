from django.urls import path
from . import views

urlpatterns = [
     
    # ADMIN URLS
    path('admin_signin', views.admin_signin, name='admin-signin'),
    path('admin_dashboard', views.dashboard, name='admin-dashboard'),
    
    # ADMIN STUDENTS
    path('admin_dashboard/students', views.admin_students,
         name='admin-dashboard-students'),
    path('add_student', views.add_student, name='add_student'),
    path('delete_student/<int:pk>', views.delete_student, name='delete_student'),
    path('update_student/<int:student_id>',
         views.update_student, name='update_student'),    
    path('admin_logout',
         views.admin_logout, name='admin_logout'),

    #ADMIN COURSES
        
    path('admin_dashboard/courses', views.admin_courses,
         name='admin-dashboard-courses'),
    path('add_course', views.add_course, name='add_course'),
    path('delete_course/<int:course_id>', views.delete_course, name='delete_course'),
    path('update_course/<int:course_id>',
         views.update_course, name='update_course'),    
    path('admin_logout',
         views.admin_logout, name='admin_logout'),
]

