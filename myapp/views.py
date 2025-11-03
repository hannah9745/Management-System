from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate,login as auth_login,logout as auth_logout
from myapp.models import Department
from myapp.models import User
from myapp.models import Student1
from myapp.models import Teacher1
from django.contrib import messages



def loginData(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        uname = request.POST['uname']
        pswd = request.POST['pswd']
        user = authenticate(request, username=uname, password=pswd)

        if user is not None:
            if getattr(user, 'usertype', None) == 'student' and user.is_active:
                auth_login(request, user)
                request.session['lid'] = user.id
                return redirect('studedit')
            elif getattr(user, 'usertype', None) == 'teacher':
                auth_login(request, user)
                request.session['teacher'] = user.id
                return redirect('teach_profile')
           
           

            else:
                messages.error(request, 'not active')
        else:
            messages.error(request, 'invalid cred')

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

        return HttpResponse('Successfully created!')


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
            is_active=False
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
    teacher_id = request.session.get('teachid')  
    if not teacher_id:
        return render(request, 'error.html', {'error': 'No teacher ID found in session. Please log in again.'})

    try:
        duser = User.objects.get(id=teacher_id)
        teacher = Teacher1.objects.get(teach_id=User)
        return render(request, 'teachpro.html', {'teacher': teacher, 'user': User})
    except User.DoesNotExist:
        return render(request, 'error.html', {'error': f'User with id {teacher_id} does not exist.'})
    except Teacher1.DoesNotExist:
        return render(request, 'error.html', {'error': f'Teacher profile not found for user id {teacher_id}.'})
    
def dept_students_view(request):
    teacher_id = request.session.get('teachid')
    if not teacher_id:
        return render(request, 'error.html', {'error': 'No teacher ID in session.'})
    teacher = Teacher1.objects.get(teach_id=teacher_id)
    dept = teacher.department_id
    students = Student1.objects.filter(department_id=dept, stud_id__usertype='student')
    return render(request, 'dept_students.html', {'students': students, 'dept': dept})


def edit_teacher_profile(request):
    teacher_id = request.session.get('teachid')
    if not teacher_id:
        return redirect('teach_profile')

    user = User.objects.get(id=teacher_id)
    teacher = Teacher1.objects.get(teach_id=user)

    if request.method == 'POST':
        # Get form data
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.email = request.POST.get('email', user.email)
        teacher.age = request.POST.get('age', teacher.age)
        teacher.phone = request.POST.get('phone', teacher.phone)
        user.save()
        teacher.save()
        return redirect('teach_profile')

    return render(request, 'edit_teacher_profile.html', {'teacher': teacher, 'user': user})

def logout(request):
    if 'lid' in request.session:
        del request.session['lid']
    auth_logout(request)
    return redirect('/login')
 





 
