from django.db import models

class Document(models.Model):
    title = models.CharField(max_length=255)
    pdf_file = models.FileField(upload_to='pdfs/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    faiss_index_path = models.CharField(max_length=500, blank=True)
    processed = models.BooleanField(default=False)

    def __str__(self):
        return self.title