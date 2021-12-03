from django.db.models import query
from django.shortcuts import render

from django.http import HttpResponse

from .models import Patient
from django.db import connection

from django.http import JsonResponse

from django.core import serializers
import numpy as np
from matplotlib import pyplot as plt

def views_all_patients(request):
    patient_list=Patient.objects.all()

    return render(request, 'Patient/patient.html',
    {'patient_list':patient_list})


def upload(request):
    return render(request, 'Patient/upload.html')

def your_template(request):
    cursor1,cursor2 = connection.cursor()
    
    X=[]
    for i in range(2801):
        X.append(i)
    #cursor1.execute("SELECT oxyvalue FROM Endpoint WHERE pexid ='PEx1' AND channelid='CH1'")
    cursor2.execute("SELECT deoxyvalue FROM Endpoint WHERE pexid ='PEx1' AND channelid='CH1'")
    #Y = cursor1.fetchall()
    Y1 = cursor2.fetchall()
    #plt.plot(X,Y,color='g',label='Oxy')
    plt.plot(X,Y1,color='b',label='Deoxy')
    plt.legend()
    plt.xlabel('Time in 1/10 th sec')
    plt.ylabel('Conc values')
    return render(request, 'Patient/template.html',{'query': plt.show()}) 

def whatever(request):
    a=np.array([1,2,3,4])

    return render(request, 'Patient/trypython.html',{'query': a}) 
        

'''def dashboard_with_pivot(request):
    return render(request, 'dashboard_with_pivot.html', {})
def pivot_data(request):
    dataset = Patient.objects.all()
    data = serializers.serialize('json', dataset)
    return JsonResponse(data, safe=False)'''
#cursor = connection.cursor()
#cursor.execute('''SELECT count(*) FROM Patient''')




# Create your views here.

#def index(request):
#    return HttpResponse("Hello, world")

    