from django.db import models
from django.core.validators import RegexValidator
# Create your models here.


alphanumeric = RegexValidator(r'^[0-9a-zA-Z]*$', 'Only alphanumeric characters are allowed.')

class Vocher(models.Model):
    unique_id = models.CharField(max_length=32, null=False, blank=False, validators=[alphanumeric])