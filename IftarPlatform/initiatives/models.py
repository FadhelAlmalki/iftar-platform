from django.db import models
from accounts.models import Profile


class City(models.Model):
    name = models.CharField(max_length=100, unique=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Initiative(models.Model):
    
    class InitiativeStatus(models.TextChoices):
        PENDING = 'pending', 'Pending'
        ACCEPTED = 'accepted', 'Accepted'
        REJECTED = 'rejected', 'Rejected'
    
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='initiatives')
    title = models.CharField(max_length=200)
    description = models.TextField()
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=True)
    place = models.CharField(max_length=200)
    image = models.ImageField(upload_to='images/')
    created_at = models.DateTimeField(auto_now_add=True)
    starts_at = models.DateTimeField()
    ends_at = models.DateTimeField()
    init_status = models.CharField(max_length=20, choices=InitiativeStatus.choices, default=InitiativeStatus.PENDING)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.title


