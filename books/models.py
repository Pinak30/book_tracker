from django.db import models

# Create your models here.

class Book(models.Model):
    STATUS_CHOICES = [
        ('R', 'Read'),
        ('CR', 'Currently Reading'),
        ('WR', 'Want to Read'),
    ]

    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    genre = models.CharField(max_length=100)
    status = models.CharField(max_length=2, choices=STATUS_CHOICES, default='WR')
    date_added = models.DateTimeField(auto_now_add=True)
    date_started = models.DateField(null=True, blank=True)
    date_finished = models.DateField(null=True, blank=True)
    progress = models.CharField(max_length=100, blank=True, null=True, help_text="E.g., '50% completed' or 'Chapter 5 of 20'")