from django.urls import path
from . import views

urlpatterns = [
    path("upload/", views.unified_upload_video, name="upload_video"),
]
