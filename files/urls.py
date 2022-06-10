from django.urls import path

from .views import FileView, FileDetailView, verifyIntegrityView, verifyFileIntegrityView

urlpatterns = [
    path('files/', FileView.as_view()),
    path('files/<str:blob_name>/', FileDetailView.as_view()),
    path('verify/', verifyIntegrityView),
    path('verify/<str:blob_name>/', verifyFileIntegrityView),
]