from django.urls import path
from .views import DashboardView, LandingPageView

urlpatterns = [
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('', LandingPageView.as_view(), name='landing-page'),
]
