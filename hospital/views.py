import re

from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.models import User, Group
from django.contrib.auth import login, authenticate, logout
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt


def homepage(request):
    return render(request, "index.html")


def aboutpage(request):
    return render(request, "about.html")


@csrf_exempt
def loginpage(request):
    error = ""
    if request.method == 'POST':
        u = request.POST['email']
        p = request.POST['password']

        user = authenticate(request, username=u, password=p)
        try:
            if user is not None:
                error = "No"
                login(request, user)
                g = request.user.groups.all()[0].name
                if g == 'Patient':
                    d = {error: error}
                    return render(request, "patienthome.html", d)
        except Exception as e:
            print(e)

    return render(request, "login.html")


def Home(request):
    if not request.user.is_active:
        return redirect('loginpage')
    g = request.user.groups.all()[0].name
    if g == 'Patient':
        return render(request, 'patienthome.html')


def profile(request):
    if not request.user.is_active:
        return redirect('loginpage')
    g = request.user.groups.all()[0].name
    if g == 'Patient':
        patient_details = Patient.objects.all().filter(email=request.user)
        d = {'patient_details': patient_details}
        return render(request, 'pateintprofile.html', d)


def createaccount(request):
    error = ""  # Initialize error variable
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        repeatpassword = request.POST['repeatpassword']
        gender = request.POST['gender']
        telephone = request.POST['telephone']
        address = request.POST['address']
        date = request.POST['date']
        bloodgroup = request.POST['bloodgroup']

        try:
            if password == repeatpassword:
                Patient.objects.create(name=name, email=email, gender=gender, telephone=telephone, address=address,
                                       date=date, bloodgroup=bloodgroup)
                user = User.objects.create_user(first_name=name, email=email, password=password, username=email)
                patient_group = Group.objects.get(name='Patient')
                patient_group.user_set.add(user)
                user.save()
                error = "No"

        except Exception as e:
            # raise e
            error = "Yes"
    d = {'error': error}
    return render(request, "createaccount.html", d)


def Logout(request):
    logout(request)
    return redirect('loginpage')


error = ""


def MakeAppointments(request):
    if not request.user.is_active:
        return redirect('loginpage')
    alldoctors = Doctor.objects.all()
    d = {'alldoctors': alldoctors}

    if request.method == 'POST':
        temp = request.POST['doctoremail']
        doctoremail = temp.split()[0]
        doctorname = temp.split()[1]
        patientname = request.POST['patientname']
        patientemail = request.POST['patientemail']
        appointmentDate = request.POST['appointmentDate']
        appointmentTime = request.POST['appointmentTime']
        symptoms = request.POST['symptoms']

        try:
            Appointment.objects.create(doctorname=doctorname, doctoremail=doctoremail, patientname=patientname,
                                       patientemail=patientemail, appointmentTime=appointmentTime,
                                       appointmentDate=appointmentDate, symptoms=symptoms, status=True, prescription="")
            error = "No"
        except Exception as e:
            # raise e
            error = "Yes"
        e = {'error': error}
        return render(request,'pateintmakeappointments.html',e)
    return render(request, 'pateintmakeappointments.html', d)
