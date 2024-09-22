from django.db import models
from django.contrib.auth.models import AbstractUser




class CustomUser(AbstractUser):
    mikrotik_host=models.CharField(max_length=32,blank=True,null=True)
    mikrotik_username=models.CharField(max_length=32,blank=True,null=True)
    mikrotik_password=models.CharField(max_length=32,blank=True,null=True)
    mikrotik_port=models.CharField(max_length=32,blank=True,null=True)
    mikrotik_use_ssl = models.BooleanField(default=True,blank=True,null=True)
    mikrotik_verify_ssl = models.BooleanField(default=True,blank=True,null=True)
    mikrotik_host_verify_ssl = models.BooleanField(default=True,blank=True,null=True)
    def __str__(self) -> str:
        return f"{self.username} -> {self.email}" 