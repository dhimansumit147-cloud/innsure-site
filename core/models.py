from django.db import models

# Create your models here.
from django.db import models

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    
from django.db import models

class Service(models.Model):
    heading = models.CharField(max_length=150, default="General Service")
    name = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.heading

class Hospital(models.Model):
    name = models.CharField(max_length=200)
    address = models.TextField()

    category = models.CharField(max_length=100, blank=True, null=True)  # Add this field
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    
from django.db import models

class Slider(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)  # <-- added description
    image = models.ImageField(upload_to='slider_images/')
    status = models.CharField(
        max_length=20, 
        choices=[('Active','Active'),('Inactive','Inactive')], 
        default='Active'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    


from django.db import models

class HomeContent(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.title    
    

from django.db import models

class About(models.Model):

    STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='Active'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title