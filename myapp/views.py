from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import authenticate,login as auth_login,logout as auth_logout
from myapp.models import Department
from myapp.models import User
from myapp.models import Student1



def loginData(request):
    if request.method=='GET':

        return render(request,'login.html')
    else:
        uname=request.POST['uname']
        pswd=request.POST['pswd']
        print(uname,pswd)
        user=authenticate(request,username=uname,password=pswd)
        if user is not None and user.usertype=='student' and user.is_active==True:
            auth_login(request,user)
            request.session['lid']=user.id
            return render(request,'studpro.html')
        else:
            return render(request,'login.html')





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
def studentRegg(request):
    if request.method=='GET':
        # User.objects.filter(username=u).exists()
        dep=Department.objects.all()
        return render(request,'studentregs.html',{'dep':dep})
    else:
        f=request.POST['fname']
        l=request.POST['lname']
        a=request.POST['age']
        e=request.POST['email']
        ph=request.POST['phone']
        d=request.POST['depart']
        u=request.POST['uname']
        p=request.POST['pswd']
        user_data=User.objects.create(first_name=f,last_name=l,email=e,username=u,password=p,usertype='student',is_active=False)
        user_data.save()
        stud_data= Student1.objects.create(age=a,phone=ph,department_id_id=d,stud_id_id=user_data.id)
        stud_data.save()
        return HttpResponse('Sucessfully created!')

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
    if request.method == 'GET':
        userdata = User.objects.get(id=request.session['lid'])
        print(userdata,"jhjdakjd")
        data = Student1.objects.get(stud_id=userdata)

        return render(request, 'studpro.html', {'stud': data, 'user': userdata})
    

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



def logout(request):
    if 'lid' in request.session:
        del request.session['lid']
    auth_logout(request)
    return redirect('/login')
 





 
