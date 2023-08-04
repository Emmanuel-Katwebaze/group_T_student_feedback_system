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


    #ADMIN COURSES
        
    path('admin_dashboard/courses', views.admin_courses,
         name='admin-dashboard-courses'),
    path('add_course', views.add_course, name='add_course'),
    path('delete_course/<int:course_id>', views.delete_course, name='delete_course'),
    path('update_course/<int:course_id>',
         views.update_course, name='update_course'),    
    path('admin_logout',
         views.admin_logout, name='admin_logout'),
    
    #     ADMIN FACILITIES
    path('admin_dashboard/facilities/', views.admin_facilities,
         name='admin-dashboard-facilities'),
    path('add_facilities', views.add_facilities, name='add_facilities'),
    path('delete_facility/<int:pk>', views.delete_facility, name='delete_facility'),
    path('update_facility/<int:facility_id>',
         views.update_facility, name='update_facility'),    
    path('admin_logout',
         views.admin_logout, name='admin_logout'),

     # ADMIN FORMS
     path('admin_dashboard/forms/', views.forms, name='admin_dashboard_forms'),
     path('create_form/', views.create_form, name='create_form'),
    
     path('admin_dashboard/forms/<str:category>/manage/add_question/<int:form_id>/', views.add_question, name='add_question'),
     path('admin_dashboard/forms/<str:category>/manage/view_form/<int:form_id>/', views.view_form, name='view_form'),
     path('save_form/<int:form_id>/', views.save_form, name='save_form'),
     path('view_summary_data/<int:form_id>/',
     views.view_summary_data, name='view_summary_data'),
]

