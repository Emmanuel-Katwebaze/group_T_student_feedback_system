from django.urls import path
from . import views

urlpatterns = [

    # STUDENT URLS
    path('signin', views.signin, name='signin'),
    path('signup', views.signup, name='signup'),
    path('student_dashboard', views.student_dashboard, name='student_dashboard'),
    path('student_logout',
         views.student_logout, name='student_logout'),

    path('student_view_all_forms/', views.student_view_all_forms,
         name='student_view_all_forms'),
    path('student_view_form/<int:form_id>/',
         views.student_view_form, name='student_view_form'),
]
