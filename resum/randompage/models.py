from django.db import models
# Create your models here.
import uuid

class AddToDatabase(models.Model):
    email_name = models.EmailField(max_length=254)
    pdf = models.FileField(upload_to='books/pdfs/')
    random_url = models.UUIDField(default=uuid.uuid4)