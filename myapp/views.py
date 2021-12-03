from django.db.models import query
from django.shortcuts import render

from django.http import HttpResponse

from .models import Patient
from django.db import connection



def views_all_patients(request):
    patient_list=Patient.objects.all()

    return render(request, 'Patient/patient.html',
    {'patient_list':patient_list})

#cursor = connection.cursor()
#cursor.execute('''SELECT count(*) FROM Patient''')




# Create your views here.

#def index(request):
#    return HttpResponse("Hello, world")

    