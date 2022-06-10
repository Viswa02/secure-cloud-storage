from datetime import date, datetime
from django.db import models

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

from cloud_handler import generateBlobReadOnlySasUrl

# Create your models here.
class File(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False)
    blob_name = models.CharField(max_length=150, blank=False, null=False)
    size = models.IntegerField()
    sas_url = models.CharField(max_length=300, blank=True, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    verified_at = models.DateTimeField(default=datetime.now)
    integrity_score = models.FloatField(default=100)
    integrity = models.BooleanField(default=True)

    def __str__(self):
        return str(self.blob_name)

    def __repr__(self):
        return str(self)

    def getDict(self):
        return {
            'name': self.name,
            'blob_name': self.blob_name,
            'size': self.size,
            'sas_url': self.sas_url,
            'created_at': self.created_at,
            'verified_at': self.verified_at,
            'integrity_score': self.integrity_score,
            'integrity': self.integrity
        }

    def generateSasUrl(self):
        self.sas_url = generateBlobReadOnlySasUrl(self.blob_name)
        self.save()
        return self.sas_url

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)