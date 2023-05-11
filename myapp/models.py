from django.db import models

# Create your models here.
class student(models.Model):
    name=models.CharField(max_length=50)
    department=models.CharField(max_length=10)
    year=models.CharField(max_length=10)

    def __str__(self):
        return self.name