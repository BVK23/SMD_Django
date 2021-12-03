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
    cursor2 = connection.cursor()
    cursor1 = connection.cursor()
    
    uname= request.POST.get('user_name')
    print(type(uname))
    X=[]
    for i in range(2801):
        X.append(i)
    s= uname 
    queries1=""" SELECT oxyvalue FROM Endpoint WHERE pexid = '"""+ s + """' AND channelid='CH1'"""
    queries2=""" SELECT deoxyvalue FROM Endpoint WHERE pexid = '"""+ s + """' AND channelid='CH1'"""
     
    cursor1.execute(queries1,{'s':uname} )
    cursor2.execute(queries2,{'s':uname})
    Y = cursor1.fetchall()
    print(Y)
    Y1 = cursor2.fetchall()
    plt.plot(X,Y,color='g',label='Oxy')
    plt.plot(X,Y1,label='Deoxy')
    plt.legend()
    plt.xlabel('Time in 1/10 th sec')
    plt.ylabel('Conc values')
    return render(request, 'Patient/TemporalPlot.html',{'plot': plt.show(),'name':uname}) 

def whatever(request):
    a=np.array([1,2,3,4])

    return render(request, 'Patient/trypython.html',{'query': a}) 

def Tplot_form(request):
    return render(request, 'Patient/TplotForm.html')    

def register(request):
    return render(request, 'Patient/TplotForm.html')    
        

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

    