from django.db import models
from django.contrib.auth.models import User
# Create your models here.



class Profile(models.Model):
    
    class Role(models.TextChoices):
        OWNER = 'owner', 'Owner'
        ORGANIZER = 'organizer', 'Organizer'
        ADMIN = 'admin', 'Admin'
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20, choices=Role.choices)
    rep_id = models.CharField(max_length=20, blank=True)
    entity_name = models.CharField(max_length=200, blank=True)
    about = models.TextField(blank=True)
    image = models.ImageField(upload_to='profiles/', blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.role}"