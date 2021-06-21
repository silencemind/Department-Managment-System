# Importing Essentials Libraries

from typing import OrderedDict
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login
from django.contrib.auth import authenticate
from django.contrib import messages
from department.models import *
from student.models import *
from users.models import Users
from django.contrib.auth import logout as auth_logout
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
import datetime
# from hods.models import hod
from .models import Teacher, teacher_assignnment
# Create your views here.

# Showing The Home Page of Teacher and Showing Their Students As Well
@login_required(login_url='login')
def teacher_index(request):
    teacher1 = get_object_or_404(Teacher, user=request.user.id)
    ass = Assign.objects.filter(teacher=request.user.teacher)
    for x in ass:
        print(dir(x))
        print(x.assigntime_set.all())
 
    return render(request, 'teacher.html', {'teacher1': ass, 't':teacher1})
    # t =Assign.objects.filter(teacher_id=request.user.teacher).all()
    # print(dir(t))

    # for a in t:
        # print(a.teacher)
        # print('Courses:',a.course)
        # s = a.class_id.student_set.all()
        # print(s)

    # s = Student.objects.get(USN=t)
    # c = Class.objects.get(student=s)

    # context = {'teacher': t,'s':'s'}
    # return render(request, 'teacher.html', context)


@login_required(login_url='login')
def teacher_home(request, teacher_id, choice):
    teacher = get_object_or_404(Teacher, id=teacher_id)
    return render(request, 'teacher_students.html', {'teacher': teacher, 'choice': choice})


@login_required(login_url='login')
def view_teacher_students(request, classid):
    print(classid)
    teach = Teacher.objects.get(user=request.user.id)
    print(teach)
    ass = Assign.objects.get(id=classid)
    course = Course.objects.get(assign=ass)

    for x in ass.class_id.student_set.filter():
        print(dir(x))


    return render(request, 'teacher_stud.html', {'s':ass,'teach':teach,'course':course})



# Showing Each Student Attendance and Marks
@login_required(login_url='login')
def each_student_info(request,student):
    t  = Teacher.objects.get(user=request.user.id)
    print(student)
    assi = Assign.objects.filter(teacher= request.user.teacher)
    for ax in assi:
        atnd  = ax.attendance_set.filter(student=student)

    each_attendance = Attendance.objects.filter(assign__in=assi,student=student)
    print(each_attendance)

    # Calculating the Total Attendance By the Individual Student
    count_atnd  = each_attendance.count()
    perc_atnd = count_atnd / 48 * 100
    print(int(perc_atnd))

    student = Student.objects.filter(USN=student)
    for st in student:
        at = st.attendance_set.filter(assign__in=assi, student__in=student)

    return render(request,'each_student_info.html', {"student":st,'at':each_attendance,'assi':assi, 'perc_atnd': int(perc_atnd)})


# def teacher_view_students(request,id):
#     std = Student.objects.get(pk=request.user.id)
#     print('asdas',std)
#     context = {'std':std} 
#     return render(request,'teacher_students.html', context)
@login_required(login_url='login')
def teacher_profile(request):  
    teacher = get_object_or_404(Teacher, user=request.user.id)
    context  = {'teacher':teacher}
    print(dir(teacher))
    print(dir(teacher.user))

    return render(request, 'teacher_profile.html', context)



def update_profile(request,teacher):
    if request.method== "POST":
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        username = request.POST.get('username')
        email = request.POST.get('email')
        update_query = get_object_or_404(Users, teacher=teacher)
        update_query.first_name = fname
        update_query.last_name = lname
        if email in update_query.email:
            return HttpResponse("Email Already Existed")
        update_query.email = email
        update_query.save()
    
        return HttpResponse('UPDATED '+str(teacher))



@login_required(login_url='login')
def view_student_attendence(request,stud,teach):
    today = datetime.date.today()
    print(stud)
    teacher = Teacher.objects.get(user=request.user.id)
    student = Student.objects.get(USN=stud)
    course = Course.objects.filter()
    assign = Assign.objects.filter(course__in=course,teacher=teacher)


    for ax in assign:
        ax = ax
    if Attendance.objects.filter(assign=ax, student=student,attendance_date=today).exists():
        print ("Already Exist")
        return HttpResponse("Already TAKE the attendence")

    else:
        att = Attendance.objects.create(assign=ax, student=student, attendance_date=today)
        att.save()
    # stud_ass = Assign.objects.filter(teacher_id=teach)
    # context  = {"stud":'Attendence Taken','student':student, 's':stud_ass}
    return HttpResponse('Attendance Taken'+str(student))
    
@login_required(login_url='login')
def teacher_view_marks(request,stud,teach):
    today = datetime.date.today()
    teach = Teacher.objects.get(user=request.user.id)
    student = Student.objects.get(USN=stud)
    std_course = StudentCourse.objects.filter()
    print(std_course)
    context = {"student":student, 'teacher':teach}

    return render(request, 'teacher_students_marks.html',context)

@login_required(login_url='login')
def take_marks(request,stud,teach):
    global stds
    if request.method== "POST":
        global stds
        student = Student.objects.get(USN=stud)

        today = datetime.date.today()
        assi = Assign.objects.filter(class_id=student.class_id,teacher_id=teach)
        for ax in assi:
            ax =ax
        std = StudentCourse.objects.filter(student=stud)
        type = request.POST.get('type')
        marks= request.POST.get('marks')
        today = datetime.date.today()
        for stds in std:
            stds =stds 
       

        tm = Markss.objects.create(assign=ax,student=student, marking_date=today, name=type, marks1=marks)
        if tm:
            return HttpResponse("CREATED")
        else:
            return HttpResponse("ERROR")


@login_required(login_url='login')
def promote_students(request,stud,teach):
    pass


@login_required(login_url='login')
def view_assignments_page(request,t):
    ass = Assign.objects.filter(class_id=t)
    
    teacher = get_object_or_404(Teacher, user=request.user.id)
    context= {"t":teacher, 'assi':t}
    return render(request, 'add_assignment.html', context)

@login_required(login_url='login')
def add_assigment(request,assi):
    if request.method == "POST":
        today = datetime.date.today()
        teach = Teacher.objects.get(user=request.user.id)
        assi = Assign.objects.get(class_id=assi,teacher=teach)
        assignment = request.POST.get('assignment')
        t = request.POST.get('teacher')
        print(today, teach, assi, assignment, t)
        insert_query=  teacher_assignnment.objects.create(assign=assi, assignnment=assignment, assignment_date=today)
        if insert_query:
            return HttpResponse("Assignment Created")
        else:
            return HttpResponse("Something Error", insert_query)



@login_required(login_url='login')
def view_assignments(request):
    teach = Teacher.objects.get(user=request.user.id)
    get_assignment_data = Assign.objects.filter(teacher=teach)    
    for gsd in get_assignment_data:
        print(dir(gsd))
        print(gsd.teacher_assignnment_set.all())
    print('===',get_assignment_data)
    context = {'get_assignment':get_assignment_data}
    return render(request, 'view_assignments.html',context)

@login_required(login_url='login')
def delete_assignments(request):
    teach = Teacher.objects.get(user=request.user.id)


@login_required(login_url='login')
def logOut(request):
    auth_logout(request)
    return redirect('login')

