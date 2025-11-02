"""
URL configuration for studproject project.

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
from myapp import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('addmin/', views.admin),
    path('add_dpt/', views.add_depart),
    path('view_dep/',views.view_dep),
    path('',views.home),
    path('studentregs/',views.studentRegg),
    path('studentview/', views.student_view),
    path('stud_approve/<int:id>', views.student_approve),
    path('stud_del/<int:id>', views.stud_del),
    path('login/', views.loginData),
    path('studedit/<int:id>', views.stud_edit,),
    path('studupdate/<int:ids>',views.stud_update),
    path('logout/',views.logout)
]