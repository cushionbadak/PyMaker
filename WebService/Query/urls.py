from django.urls import path

from . import views

app_name='Query'
urlpatterns = [
    path('', views.query, name='query'),
    path('Answer/', views.answer, name='answer'),
]