from django.conf import Path
from django.urls import path

from analysis import views

urlpatterns = [
    # path('', views.index, name='home'),
    path('', views.HomeView.as_view()),
    path('analysis/', views.AnalysisView.as_view()),

]