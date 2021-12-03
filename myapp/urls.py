from django.urls import path
from django.urls.resolvers import URLPattern

from . import views

'''urlpatterns= [
    path('',views.index, name='index')
   
]'''

urlpatterns= [
    
    path('patient',views.views_all_patients, name="list-patients"),
    path('upload',views.upload, name="upload"),
    path('Tplot',views.your_template, name="Tplot"),
    path('try', views.whatever, name='trypython'),
    path('Tplotform', views.Tplot_form, name='TplotForm')
    
    

]

