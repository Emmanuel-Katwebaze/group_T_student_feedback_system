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

     # ADMIN INSTRUCTORS
    path('admin_dashboard/instructors', views.admin_instructors,
         name='admin-dashboard-instructors'),
     path('add_instructor', views.add_instructor, name='add_instructor'),
    path('delete_instructor/<int:pk>', views.delete_instructor, name='delete_instructor'),
    path('update_instructor/<int:instructor_id>',
         views.update_instructor, name='update_instructor'),

]

