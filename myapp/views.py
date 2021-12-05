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

def Data_load_Staging(request):
    
    
    f = open(".\stagingfiles\VM0001_Moto_HBA_Probe1_Deoxy.csv", "r")
    
    for i in range(8):
        info=f.readline()
        if i==4:
            ptname=info.split(',')[1]
            ptname=ptname.rstrip()
            print(ptname)
        if i==6:
            page=info.split(',')[1]
            page=page.strip()
            page=page.rstrip('y')   
            print(page)
        if i==7:
            psex=info.split(',')[1]  
            psex=psex.rstrip() 
            print(psex)     
        #print(f.readline())
    f.close()
    #print(df)
    
    
    #Fetch Patient ID
    cursordl1= connection.cursor()
    queriesdl1=""" Select count(*) from Patient """
    cursordl1.execute(queriesdl1)
    pcount=cursordl1.fetchall()
    pid='P'+str(int(pcount[0][0])+1)
    
    #Insert into PATIENT TABLE
    cursorinsp = connection.cursor()
    p1=ptname
    p2=psex
    p3=page
    p0=pid
    
    queriespt=""" INSERT INTO Patient Values ('"""+ p0 + """','"""+ p1 + """','"""+ p2 +"""','"""+ p3+ """')"""
    cursorinsp.execute(queriespt,{'p0':pid,'p1':ptname,'p2':psex,'p3':page})
    

    #Fetch PexID
    cursordl11= connection.cursor()
    queriesdl11=""" Select count(*) from PatientTreatment """
    cursordl11.execute(queriesdl11)
    pexid=cursordl11.fetchall()
    pexid='PEx'+str(int(pexid[0][0])+1)

    #Fetch ExerciseID based on ExerciseType enetered by DB  admin
    extp= request.POST.get('excercisetype')
    e=extp
   

    cursordfex= connection.cursor()
    queriesdfex=""" Select ExerciseID from Treatment where ExerciseType = '"""+ e +"""' """
    cursordfex.execute(queriesdfex,{'e':extp})
    exeridd=cursordfex.fetchall()
    exeridd=exeridd[0][0]
        
    #Insert into PatientTreatment
    cursor_PT = connection.cursor()
    p01=pexid
    p11=pid
    p21=exeridd
    
    
    querie_PT=""" INSERT INTO PatientTreatment  Values ('"""+ p01 + """','"""+ p11 + """','"""+ p21 +"""')"""
    cursor_PT.execute(querie_PT,{'p01':pexid,'p11':pid,'p21':exeridd})
    
    #Fetch EndPointID
    cursor_epi= connection.cursor()
    queriesd_epi=""" Select count(*)  from Endpoint """
    cursor_epi.execute(queriesd_epi)
    endid=cursor_epi.fetchall()
    endid=endid[0][0]
    
    #Code for Data transformation from excel
    df=pd.read_csv(".\stagingfiles\VM0001_Moto_HBA_Probe1_Deoxy.csv",skiprows=40)
    ddf=pd.read_csv(".\stagingfiles\VM0001_Moto_HBA_Probe1_Oxy.csv",skiprows=40)
    lstcol=[0]
    for i in range(25,49):
        lstcol.append(i)
    df.drop(df.columns[lstcol], axis = 1, inplace = True)
    ddf.drop(ddf.columns[lstcol], axis = 1, inplace = True)

    df2=df.transpose()
    ddf2=ddf.transpose()

    df3=df2.iloc[:,0]
    ddf3=ddf2.iloc[:,0]

    for i in range(1,2801):
        df4=df2.iloc[:,i]
        df5=pd.concat([df3,df4],axis=0)
        df3=df5

        ddf4=ddf2.iloc[:,i]
        ddf5=pd.concat([ddf3,ddf4],axis=0)
        ddf3=ddf5
    concval=df5.values
    concvalo=ddf5.values
    
    cnt=concval.shape[0]
    lstchl=['CH1','CH2','CH3','CH4','CH5','CH6','CH7','CH8','CH9','CH10','CH11','CH12','CH13','CH14','CH15','CH16','CH17','CH18','CH19','CH20','CH21','CH22','CH23','CH24']
    
    #Insert to Endpoint TABLE
    cursor_end = connection.cursor()
    
    
    for i in range(1,int(cnt)):
        j=((i-1)%24)
        k=i-1
        #endid+=i
        #p4=endid
        p5=lstchl[j]
        p6=pexid
        p7=concvalo[k].item()
        p8=concval[k].item()
        querie_end=""" INSERT INTO Endpoint (channelid,pexid,oxyvalue,deoxyvalue) Values  ('"""+ p5 + """' , '"""+ p6 +"""',"""+ str(p7) +""","""+ str(p8) +""")"""
        cursor_end.execute(querie_end,{'p5':lstchl[j],'p6':pexid,'p7':concvalo[k].item(),'p8':concval[k].item()})

    return render(request, 'Patient/trypython.html') 
   
  

def register(request):
    return render(request, 'Patient/TplotForm.html')    

def Data_load_page(request):
    return render(request, 'Patient/DLpage.html')         

'''def dashboard_with_pivot(request):
    return render(request, 'dashboard_with_pivot.html', {})
def pivot_data(request):
    dataset = Patient.objects.all()
    data = serializers.serialize('json', dataset)
    return JsonResponse(data, safe=False)
    
def DL_page(request):
    cursordl1= connection.cursor()
    queriesdl1=""" Select count(*) from Patient """
    cursordl1.execute(queriesdl1)
    pcount=cursordl1.fetchall()
    return render(request, 'Patient/DLpage.html',{'Pcount':pcount})     
    
    
    '''
#cursor = connection.cursor()
#cursor.execute('''SELECT count(*) FROM Patient''')




#def index(request):
#    return HttpResponse("Hello, world")

    