from django.db import models
from accounts.models import Profile
from initiatives.models import Initiative 

# Create your models here.

class Permit(models.Model):
    class PermitStatus(models.TextChoices):
        PENDING = 'pending', 'Pending'
        ACCEPTED = 'accepted', 'Accepted'
        REJECTED = 'rejected', 'Rejected'
        EXPIRED = 'expired', 'Expired'

    organizer = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='permits')
    initiative = models.OneToOneField(Initiative, on_delete=models.CASCADE, related_name='permit')
    
    permit_number = models.CharField(max_length=50, unique=True)
    qr_code = models.ImageField(upload_to='permits/qrs/', blank=True)
    pdf_file = models.FileField(upload_to='permits/pdfs/', blank=True)
    permit_status = models.CharField(
        max_length=20, 
        choices=PermitStatus.choices, 
        default=PermitStatus.PENDING
    )
    created_at = models.DateTimeField(auto_now_add=True)
    generated_at = models.DateTimeField(null=True, blank=True)
    starts_at = models.DateTimeField()
    expires_at = models.DateTimeField()

    def __str__(self):
        return f"Permit {self.permit_number} - {self.initiative.title}"
