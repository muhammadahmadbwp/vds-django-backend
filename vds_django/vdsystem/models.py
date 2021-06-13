from django.db import models
from django.db.models.fields import AutoField
from users.models import UserProfile
from django.utils.translation import gettext_lazy as _

# Create your models here.

# class VDSPrediction(models.Model):
#     id = AutoField(primary_key=True)
#     user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True, related_name='user_id')
#     description = models.CharField(max_length=1000, blank=True, null=True)
#     output = models.FileField(_("output"), upload_to='output', blank=True, null=True)

#     class Meta:
#         verbose_name = 'vdsprediction'
#         verbose_name_plural = 'vdspredictions'
