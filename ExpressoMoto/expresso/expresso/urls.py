from django.contrib import admin 
from django.urls import path 
from . import views 
  
urlpatterns = [ 
    path('admin/', admin.site.urls), 
    path('', views.home, name='home'),
    path('adicionar/', views.adicionar_documento,name='adicionar_documento'),
    path('entregas/', views.filtrar_documentos, name='listar_documentos'),
    path('remover_documento/', views.remover_documento, name='remover_documento'), 
    path('filtrar/', views.filtrar_documentos, name='filtrar_documentos'),
] 