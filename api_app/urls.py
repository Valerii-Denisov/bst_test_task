from django.urls import path
from api_app import views

urlpatterns = [
    path('api/', views.RobotsFactory.as_view(), name='robot_create'),
    path('api/report/', views.FactoryReport.as_view()),
]
