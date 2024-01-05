from django.urls import path
from .views import DashboardView, LandingPageView, DeleteSongView

urlpatterns = [
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('', LandingPageView.as_view(), name='landing-page'),
    path('delete-song/<int:id>/', DeleteSongView.as_view(), name='delete-song'),

]
