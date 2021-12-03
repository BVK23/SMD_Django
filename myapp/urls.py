from django.urls import path
from django.urls.resolvers import URLPattern

from . import views

'''urlpatterns= [
    path('',views.index, name='index')
   
]'''

urlpatterns= [
    
    path('patient',views.views_all_patients, name="list-patients"),

]
