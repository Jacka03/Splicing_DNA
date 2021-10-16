from django.conf import Path
from django.urls import path

from analysis import views

urlpatterns = [
    # path('', views.index, name='home'),
    # path('', views.HomeView.as_view()),
    path('', views.AssemblyView.as_view()),
    path('assembly/', views.AssemblyView.as_view()),
    path('assemblyPools/', views.AssemblyPoolsView.as_view()),
    path('analysis/', views.AnalysisView.as_view()),
    # path('analysis/', views.AnalysisView.as_view()),
    # path('export_excel/', views.DownloadView.as_view()),

]