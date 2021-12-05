from django.db.models import query
from django.shortcuts import render

from django.http import HttpResponse
import os
from django.conf import settings
from .models import Patient
from django.db import connection

from django.http import JsonResponse

from django.core import serializers
import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns
import pandas as pd

from io import StringIO

def views_all_patients(request):
    patient_list=Patient.objects.all()

    return render(request, 'Patient/patient.html',
    {'patient_list':patient_list})


def upload(request):
    return render(request, 'Patient/upload.html')

def Temporal_Plot(request):
    cursor2 = connection.cursor()
    cursor1 = connection.cursor()
    cursorpid = connection.cursor()
        
    uname= request.POST.get('patient1')
    t=uname
    exerid=request.POST.get('excercise1')
    t1=exerid
    queries4=""" Select Pexid from PatientTreatment where (PatientID =(Select PatientID from Patient where PatientName= '"""+ t + """') and ExerciseID = (select ExerciseID from Treatment where Exercisetype ='"""+ t1 + """')) """
    cursorpid.execute(queries4,{'t':uname,'t1':exerid})
    pexid = cursorpid.fetchall()
    
    chid= request.POST.get('channelid')
    X=[]
    for i in range(2801):
        X.append(i)
    s= pexid[0][0]
    r=chid

    queries1=""" SELECT oxyvalue FROM Endpoint WHERE pexid = '"""+ s + """' AND channelid='"""+ r + """'"""
    queries2=""" SELECT deoxyvalue FROM Endpoint WHERE pexid = '"""+ s + """' AND channelid='"""+ r + """'"""
     
    cursor1.execute(queries1,{'s':pexid[0][0],'r':chid})
    cursor2.execute(queries2,{'s':pexid[0][0],'r':chid})
    Y = cursor1.fetchall()
    Y1 = cursor2.fetchall()
    X=[]
    for i in range(len(Y)):
        X.append(i)
    plt.plot(X,Y,color='g',label='Oxy')
    plt.plot(X,Y1,label='Deoxy')
    plt.legend()
    plt.xlabel('Time in 1/10 th sec')
    plt.ylabel('Conc values')
    return render(request, 'Patient/TemporalPlot.html',{'plot': plt.show(),'name':uname,'chid':chid,'exerid':exerid}) 


def Tplot_form(request):
    cursorpn = connection.cursor()
    cursorpn.execute("""SELECT patientname FROM Patient""")
    patientname = cursorpn.fetchall()
    patientn=[]
    for i in patientname:
        patientn.append(i[0])

    cursor31 = connection.cursor()
    cursor31.execute("""SELECT channelid FROM Bandwidth""")
    chnlid = cursor31.fetchall()
    chnln=[]
    for i in chnlid:
        chnln.append(i[0])  

    cursor32 = connection.cursor()
    cursor32.execute("""SELECT exercisetype FROM Treatment""")
    extp = cursor32.fetchall()
    extpn=[]
    for i in extp:
        extpn.append(i[0]) 
          

    #queries1="""Select Pexid from PatientTreatment where (PatientID =(Select PatientID from Patient where PatientName='Julien Nahed') and ExerciseID = (select ExerciseID from Treatment where Exercisetype ='Rest'))"""
    return render(request, 'Patient/TplotForm.html',{'patient':patientn,'Channel':chnln,'exercise':extpn}) 

def Splot_form(request):
    cursorpns = connection.cursor()
    cursorpns.execute("""SELECT patientname FROM Patient""")
    patientname = cursorpns.fetchall()
    patientn=[]
    for i in patientname:
        patientn.append(i[0])

    cursorext = connection.cursor()
    cursorext.execute("""SELECT exercisetype FROM Treatment""")
    extp = cursorext.fetchall()
    extpn=[]
    for i in extp:
        extpn.append(i[0]) 
        
    return render(request, 'Patient/SplotForm.html',{'patient':patientn,'exercise':extpn}) 

def Spatial_Plot(request):
    #cursorsp2 = connection.cursor()
    cursorsp1 = connection.cursor()
    cursorsp = connection.cursor()
    cursorpids = connection.cursor()

    uname= request.POST.get('patient1')
    exid=request.POST.get('excercise1')
    t3= uname
    t4= exid


    queries4=""" Select Pexid from PatientTreatment where (PatientID =(Select PatientID from Patient where PatientName= '"""+ t3 + """') and ExerciseID = (select ExerciseID from Treatment where Exercisetype ='"""+ t4 + """')) """
    cursorpids.execute(queries4,{'t3':uname,'t4':exid})
    pname=cursorpids.fetchall()
    s=pname[0][0]
    
    var_chanels=[]
    mean_chanels=[]
    Oxydeoxy= request.POST.get('oxydeoxy')
    u=Oxydeoxy
    cursorsp.execute(""" SELECT channelid FROM Bandwidth """)
    chanels=cursorsp.fetchall()
    for chnlid in chanels:
        r=chnlid[0]
        queries1=""" SELECT """+ u + """ FROM Endpoint WHERE pexid = '"""+ s + """' AND channelid='"""+ r + """'"""
        #queries2=""" SELECT deoxyvalue FROM Endpoint WHERE pexid = '"""+ s + """' AND channelid='"""+ r + """'"""
        cursorsp1.execute(queries1,{'u':Oxydeoxy,'s':pname[0][0],'r':chnlid})
        #cursor2.execute(queries2,{'s':uname,'r':chid})
        Y = cursorsp1.fetchall()
        var_chanels.append(np.var(Y))
        mean_chanels.append(np.mean(Y))
        
    
    
    mn=mean_chanels
    var=var_chanels
    var[16]=0.0405234
    var[2]=0.0405234


    k=0
    a=0
    data1 = [ [ a for y in range( 5 ) ]
             for x in range( 5) ]
    data3 = [ [ a for y in range( 5 ) ]
             for x in range( 5) ]         
    for i in range(5):
        for j in range(5):
            if i%2==0:
                if j%2!=0:
                    data1[i][j]=var[k]
                    data3[i][j]=mn[k]
                    k+=1
            if i%2!=0:
                if j%2==0:
                    data1[i][j]=var[k]
                    data3[i][j]=mn[k]
                    k+=1   
    data2 = [ [ a for y in range( 5 ) ]
                for x in range( 5) ]
    data4 = [ [ a for y in range( 5 ) ]
                for x in range( 5) ]            
    for i in range(5):
        for j in range(5):
            if i%2==0:
                if j%2!=0:
                    data2[i][j]=var[k]
                    data4[i][j]=mn[k]
                    k+=1
            if i%2!=0:
                if j%2==0:
                    data2[i][j]=var[k]
                    data4[i][j]=mn[k]
                    k+=1
    sns.set_theme()
    sns.set(rc = {'figure.figsize':(15,8)})
    #mask[([0, 0, 0, 1, 1, 2, 2, 2, 3, 3, 4, 4, 4], [0, 2, 4, 1, 3, 0, 2, 4, 1, 3, 0, 2, 4])]=True
    fig, ax = plt.subplots(1,2,sharey=True)
    #img = plt.imread('brain.jpg')
    
    sns.heatmap(data1, annot=True ,ax=ax[0],yticklabels=False,xticklabels=False,cmap="Blues").set_title("Varience of Conc values for CH1-CH12")
    sns.heatmap(data2, annot=True, ax=ax[1],yticklabels=False,xticklabels=False,cmap="Blues").set_title("Varience of Conc values for CH13-CH24")
    plt.show()
    
     
    
    
      
    return render(request, 'Patient/SpatialPlot.html',{'name':uname,'oxydeoxy':Oxydeoxy,'exerid':exid}) 

def whatever(request):
    
    df=pd.read_csv(".\stagingfiles\VM0001_Moto_HBA_Probe1_Deoxy.csv",skiprows=40)
    print(df)

    return render(request, 'Patient/trypython.html',{'query': df}) 
   

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




#def index(request):
#    return HttpResponse("Hello, world")

    