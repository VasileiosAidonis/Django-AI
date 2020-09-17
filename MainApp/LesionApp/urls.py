from django.urls import path
from .views import home, aboutus, license, ChartData

urlpatterns = [
    path('', home, name="home"),
    path('api/chart/data/', ChartData.as_view()),
    path('aboutUs/', aboutus, name="aboutus"),
    path('license/', license, name="license")
]
