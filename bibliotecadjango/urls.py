"""
URL configuration for bibliotecadjango project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from core import views
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('livros/', views.LivroList.as_view(), name='livros-list'),
    path('livros/<int:pk>/', views.LivroDetail.as_view(), name='livro-detail'),
    path('livros/create/', views.LivroCreate.as_view(), name='livro-create'),

    path('autor/', views.AutorList.as_view(), name='autor-list'),
    path('autor/<int:pk>/', views.AutorDetail.as_view(), name='autor-detail'),
    path('autor/create/', views.AutorCreate.as_view(), name='autor-create'),

    path('categoria/', views.CategoriaList.as_view(), name='categoria-list'),
    path('categoria/<int:pk>/', views.CategoriaDetail.as_view(), name='categoria-detail'),
    path('categoria/create/', views.CategoriaCreate.as_view(), name='categoria-create'),

    path('colecoes/', views.ColecaoListCreate.as_view(), name='colecao-list-create'),  
    path('colecoes/<int:pk>/', views.ColecaoDetail.as_view(), name='colecao-detail'),

    # Rota para gerar o schema da API
    path('api/schema/', SpectacularAPIView.as_view(), name='api-schema'),

    # Rota para exibir a documentação no formato Swagger
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='api-schema'), name='api-docs'),
]
