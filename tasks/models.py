from audioop import reverse
from django.db import models
from django.db.models import Q, F
from django.contrib.auth.models import User



class Task(models.Model):
 
    STATUS_CHOICES = [
        ("todo", "To Do"),
        ("in_progress", "In Progress"),
        ("done", "Done"),
    ]

    PRIORITY_CHOICES = [
        ("low", "Low"),
        ("medium", "Medium"),
        ("high", "High"),
    ]

    title = models.CharField(max_length=256)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="todo")
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default="medium")
    due_date = models.DateField(null=True, blank=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tasks", null=True, blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('tasks:task-detail', kwargs={'pk': self.pk})
    
    class Meta:
        ordering = ['-priority', 'due_date']
        
