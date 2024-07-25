from django.db import models
class TextResult(models.Model):
    input_text = models.TextField()
    processed_text = models.TextField()
# Create your models here.
