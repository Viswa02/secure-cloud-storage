from django.urls import path
from .views import homePage, loginPage, filesPage, fileDetailsPage, verifyPage

urlpatterns = [
    path('', homePage, name='home'),
    path('login/', loginPage, name='login'),
    path('files/', filesPage, name='files'),
    path('files/<blob_name>', fileDetailsPage, name='filedetail'),
    path('verify/', verifyPage, name='verify'),
]