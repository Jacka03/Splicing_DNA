from django.conf import Path
from django.urls import path

from analysis import views

urlpatterns = [
    # path('', views.index, name='home'),
    path('analysis/', views.AnalysisView.as_view()),
    path('home/', views.HomeView.as_view()),
]