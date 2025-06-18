from django.db import models
from django.utils import timezone

# Create your models here.

class Client(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(blank=True, null=True)
    contact_number = models.CharField(max_length=20, blank=True, null=True)
    company_url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.id} | {self.name} | {self.email} | {self.contact_number} | {self.company_url} | {self.created_at}"


class RequestType(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.id} | {self.name} | {self.description}"


class ClientRequest(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed'),
    ]

    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    request_type = models.ForeignKey(RequestType, on_delete=models.CASCADE)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField()

    def __str__(self):
        return f"{self.id} | {self.client.name} | {self.request_type.name} | {self.description} | {self.status} | {self.created_at} | {self.updated_at}"