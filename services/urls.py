"""Services URL patterns."""

from django.urls import path
from . import views

app_name = 'services'

urlpatterns = [
    path('', views.ServiceListView.as_view(), name='service_list'),
    path('request-consultation/', views.request_consultation, name='request_consultation'),
    path('<slug:slug>/', views.ServiceDetailView.as_view(), name='service_detail'),
]
