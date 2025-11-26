
from django.contrib import admin
from django.urls import path
from myapp import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('addmin/', views.admin_dashboard, name="admin"),
    path('add_dept/',views.add_department, name="add_dept"),
    path('delete_department/<int:id>/', views.delete_department, name='delete_department'),

    path('view_dep/',views.view_dep,name='view_dep'),
    path('view_dep/', views.view_dep, name='view_dep'),
    path('logout/', views.logout, name='logout'),
    path('addmin/', views.admin),
    path('addmin/', views.admin_dashboard, name="addmin"),

    path('add_dept/', views.add_depart),
    path('view_dep/',views.view_dep),
    path('',views.home),
    path('studentregs/',views.studentReg),
    path('studentview/', views.student_view,name="studentview"),
    path('stud_approve/<int:id>', views.student_approve),
    path('stud_del/<int:id>', views.stud_del,name="stud_del"),
    path('login/', views.loginData),
    path('studedit/', views.stud_edit,name='studedit'),
    path('studupdate/',views.stud_update),
    path('teacherview/', views.teach_view),
    path('teacherreg/', views.teacherreg),
    path('edit_teacher_profile/', views.edit_teacher_profile),
    path('teachpro/', views.teach_profile , name='teachpro'),
    path('dept_students_view/', views.dept_students_view),
    path('admindash/', views.admin_dashboard),
    path('delete_department/<int:id>', views.delete_department, name='deletedepart'),
    path('logout/',views.logout),


]