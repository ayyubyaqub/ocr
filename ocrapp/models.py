from django.db import models

# Create your models here.

class OCRData(models.Model):
    image = models.ImageField(upload_to='images/')
    extracted_text = models.TextField()
    bold_words = models.TextField()
    image_base64 = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
