"""Pages URL patterns."""

from django.urls import path
from . import views

app_name = 'pages'

urlpatterns = [
    path('about-us/', views.AboutUsView.as_view(), name='about_us'),
    path('faq/', views.FAQView.as_view(), name='faq'),
    path('<slug:slug>/', views.StaticPageView.as_view(), name='static_page'),
]
