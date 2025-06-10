from django.db import models
from django.contrib.auth.models import User


class TestModel(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class UploadedPDF(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pdf_file = models.FileField(upload_to='pdfs/')
    uploaded_at = models.DateTimeField(auto_now_add=True)