from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import authenticate,login as auth_login,logout as auth_logout
from myapp.models import Department
from myapp.models import User
from myapp.models import Student1
from myapp.models import Teacher1
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test,login_required
from django.contrib.auth import logout as django_logout


def loginData(request):
    if request.method == 'POST':
        uname = request.POST.get('uname')
        pswd = request.POST.get('pswd')

        user = authenticate(request, username=uname, password=pswd)
        print("AUTH USER:", user)

        if user is not None:
            print("USERTYPE:", getattr(user, 'usertype', None))
            usertype = getattr(user, 'usertype', None)

            if usertype == 'student' and user.is_active:
                auth_login(request, user)
                request.session['lid'] = user.id
                return redirect('studedit')

            elif usertype == 'teacher':
                auth_login(request, user)
                request.session['lid'] = user.id
                return redirect('teachpro')
            
            elif usertype == 'admin':
                auth_login(request, user)
                request.session['lid'] = user.id
                return redirect('admin')

            else:
                messages.error(request, 'User not active or invalid type')
        else:
            messages.error(request, 'Invalid credentials')

    return render(request, 'login.html')



def admin(request):
    return render(request,'admin.html')
def add_depart(request):
    if request.method=='GET':
        return render(request,'add_depart.html')
    else:
        dep=request.POST['dept']
        data=Department.objects.create(department_name=dep)
        data.save()
        return HttpResponse('Sucess!')
def view_dep(request):
    data=Department.objects.all()
    return render(request,'dept.html',{'data':data})
def home(request):
    return render(request,'home.html')

def is_admin(user):
    return user.is_authenticated and user.usertype == 'admin'

@user_passes_test(is_admin, login_url='loginDataa')
def admin_dashboard(request):
    return render(request, 'admin.html')
@user_passes_test(is_admin, login_url='loginDataa')
def add_department(request):
    if request.method == 'POST':
        dept_name = request.POST.get('dept')
        if dept_name:
            Department.objects.create(department_name=dept_name)
            return redirect('view_dep')
    return render(request, 'add_depart.html')

@user_passes_test(is_admin, login_url='loginDataa')
def view_dep(request):
    depts = Department.objects.all()
    return render(request, 'dept.html', {'data': depts})

@user_passes_test(is_admin, login_url='loginDataa')
def delete_department(request, id):
    dept = get_object_or_404(Department, id=id)
    dept.delete()
    return redirect('view_dep')

@user_passes_test(is_admin, login_url='loginDataa')
def student_list(request):
    students = Student1.objects.select_related('stud_id', 'department_id').all()
    return render(request, 'studentview.html', {'students': students})

@user_passes_test(is_admin, login_url='loginDataa')
def teacher_list(request):
    teachers = Teacher1.objects.select_related('teach_id', 'department_id').all()
    return render(request, 'teacherview.html', {'teachers':teachers})

def studentReg(request):
    if request.method == 'GET':
        dep = Department.objects.all()
        return render(request, 'studentregs.html', {'dep': dep})
    else:
        f = request.POST['fname']
        l = request.POST['lname']
        a = request.POST['age']
        e = request.POST['email']
        ph = request.POST['phone']
        d = request.POST['depart']
        u = request.POST['uname']
        p = request.POST['pswd']

        user_data = User(
            first_name=f,
            last_name=l,
            email=e,
            username=u,
            usertype='student',
            is_active=False
        )
        user_data.set_password(p)
        user_data.save()

        stud_data = Student1.objects.create(
            age=a,
            phone=ph,
            department_id_id=d,
            stud_id_id=user_data.id
        )
        stud_data.save()

        messages.success(request, 'student registered succesfuly! please log in')
        return redirect('loginDataa')

# from django.contrib.auth.models import myapp.User
# User.objects.filter(is_superuser=True)
# user = User.objects.get(username='admin') 
# user.delete()


#  If you already have a user and just want to make them admin:
# u = User.objects.get(username='')
# u.usertype = 'admin'
# u.set_password('newpassword')  # optional: to reset password
# u.save()

# from myapp.models import User  
# admin = User.objects.create_user(
#     username='adminn',          
#     password='123',    
#     usertype='admin',
#     first_name='Admin',
#     last_name='User',
#     email='adminn@example.com'

# )

# username: adminn
# password: admin123

def student_view(request):
    data=Student1.objects.all()
    return render(request,'studentv.html',{'data':data})

def student_approve(request,id):
    stud=Student1.objects.get(id=id)
    stud.stud_id.is_active=True
    stud.stud_id.save()
    return HttpResponse('Success!')

def stud_del(request,id):
    stud=Student1.objects.filter(id=id)
    user=Student1.objects.get(id=id)
    print(user)
    data=user.stud_id
    stud.delete()
    data.delete()
    return redirect('studentview')
    
def stud_edit(request):
    if 'lid' not in request.session:
            return redirect('/login')
    if request.method == 'GET':
        student = Student1.objects.get(stud_id_id = request.session['lid'])
        print("jfnkjv",student)
        return render(request, 'studpro.html', {'stud': student})
    

def stud_update(request):
    user = User.objects.get(id=request.session['lid'])
    print(user,'afkjajf')
    stud = Student1.objects.get(stud_id_id=user)
    
    if request.method == "POST":
        user.first_name = request.POST.get('fname', user.first_name)
        user.last_name = request.POST.get('lname', user.last_name)
        user.email = request.POST.get('email', user.email)
        stud.age = request.POST.get('age', stud.age)
        stud.phone = request.POST.get('phone', stud.phone)
        user.save()
        stud.save()
        return redirect('studedit') 

    return render(request, 'login.html', {'stud': stud, 'user': user})

def teacherreg(request):
    if request.method == 'GET':
        dep = Department.objects.all()
        return render(request, 'teacherreg.html', {'dep': dep})
    else:
        f = request.POST['fname']
        l = request.POST['lname']
        a = request.POST['age']
        e = request.POST['email']
        ph = request.POST['phone']
        d = request.POST['depart']
        u = request.POST['uname']
        p = request.POST['pswd']

        user_data = User(
            first_name=f,
            last_name=l,
            email=e,
            username=u,
            usertype='teacher',
            is_active=True
        )
        user_data.set_password(p)
        user_data.save()

        teacher_data = Teacher1.objects.create(
            age=a,
            phone=ph,
            department_id_id=d,
            teach_id_id=user_data.id
        )
        teacher_data.save()

        return HttpResponse(' Teacher successfully registered!')
    


def teach_view(request):
    data=Teacher1.objects.all()
    return render(request,'teacherv.html',{'data':data})

def teach_profile(request):
    teacher_id = request.session.get('lid')  
    if not teacher_id:
        return redirect('/login')
    else:
        teacher = Teacher1.objects.get(teach_id_id=teacher_id)
        return render(request, 'teacherpro.html', {'teacher': teacher})

  

def dept_students_view(request):
    teacher_id = request.session.get('lid')
    if not teacher_id:
        return redirect('/login')
    teacher = Teacher1.objects.get(teach_id_id=teacher_id)
    students = Student1.objects.filter(department_id=teacher.department_id, stud_id__usertype='student')
    return render(request, 'tcr_view_dep_std.html', {'students': students , 'teacher':teacher})




def edit_teacher_profile(request):
    teacher_id = request.session.get('lid')
    if not teacher_id:
        return redirect('/login')

    user = User.objects.get(id=teacher_id)
    teacher = Teacher1.objects.get(teach_id=user)

    if request.method == 'POST':
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.email = request.POST.get('email', user.email)
        teacher.age = request.POST.get('age', teacher.age)
        teacher.phone = request.POST.get('phone', teacher.phone)
        user.save()
        teacher.save()
        return redirect('teachpro')



# def logout(request):
#     if 'lid' in request.session:
#         del request.session['lid']
#     auth_logout(request)
#     return redirect('/login')
def logout(request):
    django_logout(request)        
    return redirect('loginDataa')
 





 
# from myapp.models import Student1
# Student1.objects.values_list('id', flat=True)
