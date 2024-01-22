from django.db import models

# Create your models here.
class GeminiImage(models.Model):
    text_field = models.CharField(max_length=100)
    image_field = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.text_field
