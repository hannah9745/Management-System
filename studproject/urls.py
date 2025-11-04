
from django.contrib import admin
from django.urls import path
from myapp import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('addmin/', views.admin),
    path('add_dpt/', views.add_depart),
    path('view_dep/',views.view_dep),
    path('',views.home),
    path('studentregs/',views.studentReg),
    path('studentview/', views.student_view),
    path('stud_approve/<int:id>', views.student_approve),
    path('stud_del/<int:id>', views.stud_del),
    path('login/', views.loginData),
    path('studedit/', views.stud_edit,name='studedit'),
    path('studupdate/',views.stud_update),
    path('teacherview/', views.teach_view),
    path('teacherreg/', views.teacherreg),
    path('edit_teacher_profile/', views.edit_teacher_profile),
    path('teachpro/', views.teach_profile , name='teachpro'),
    path('dept_students_view/', views.dept_students_view),
    path('logout/',views.logout),

]