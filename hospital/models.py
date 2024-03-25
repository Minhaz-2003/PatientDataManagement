from django.db import models


# Create your models here.
class Patient(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    gender = models.CharField(max_length=10)
    telephone = models.CharField(max_length=11)
    address = models.CharField(max_length=100)
    date = models.DateField()
    bloodgroup = models.CharField(max_length=5)

    def __str__(self):
        return self.name


class Doctor(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    gender = models.CharField(max_length=10)
    telephone = models.CharField(max_length=11)
    address = models.CharField(max_length=100)
    date = models.DateField()
    bloodgroup = models.CharField(max_length=5)
    specialisation = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Appointment(models.Model):
    doctorname = models.CharField(max_length=50)
    patientname = models.CharField(max_length=50)
    doctoremail = models.EmailField(max_length=50)
    patientemail = models.EmailField(max_length=50)
    appointmentDate = models.DateField()
    appointmentTime = models.TimeField()
    symptoms = models.CharField(max_length=100)
    prescription = models.CharField(max_length=200)
    status=models.BooleanField()

    def __str__(self):
        return self.patientname+ "you have appointment with"+self.doctorname+ "on"+str(self.appointmentDate)+"at"+ str(self.appointmentTime)
