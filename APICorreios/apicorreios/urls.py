"""apicorreios URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from app_apicorreios import views

urlpatterns = [
    path('upload/', views.upload_file, name='upload_file'),
    path('gerar_pdf/', views.gerar_pdf, name='gerar_pdf'),
    path('baixar_excel/', views.baixar_excel, name='baixar_excel'),
]
