from django.urls import path
from .views import UploadPDFView, ChatView

urlpatterns = [
    path('upload/', UploadPDFView.as_view(), name='upload-pdf'),
    path('chat/', ChatView.as_view(), name='chat'),
]