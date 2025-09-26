"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from myapp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/student/', views.StudentRegisterView.as_view(), name='student_register'),
    path('register/Teacher/', views.TeacherRegisterView.as_view(), name='teacher_register'),
    path('login/',views.alllogin.as_view(),name='login'),
    path('api/admin/teachers/',views.TeacherListview.as_view(),name='TeacherListview'),
    path('api/admin/students/',views.StudentListview.as_view(),name='StudentListview'),
    path('api/admin/approve-teacher/<int:pk>/',views.approveTeacherview.as_view(),name='approve-teacher'),
    path('api/admin/approve-student/<int:pk>/',views.approveStudentview.as_view(),name='approve-student'),
    path('api/admin/delete-Teacher/<int:pk>/',views.deleteTeachertview.as_view(),name='delete-Teacher'),
    path('api/admin/delete-student/<int:pk>/',views.deleteStudentview.as_view(),name='delete-student'),
    path('api/teacher/profile/',views.TeacherProfileview.as_view(),name='teacherprofile'),
    path('api/teacher/students/',views.StudentTeachListview.as_view(),name='StudentListview'),
    path('api/teacher/update/', views.TeacherProfileUpdateView.as_view(), name='teacher_update'),

    path('api/student/profile/', views.StudentProfileView.as_view(), name='studentprofile'),
    path('api/student/update/', views.StudentProfileUpdateView.as_view(), name='student_update'),
    path('api/teachers/list/', views.ALLTeachersListView.as_view(), name='teacher_update'),








    # path('student_home/',views.student_home.as_view(),name='student_home'),
    # path('admin_home/',views.admin_home.as_view(),name='admin_home'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
