from django.db import models
from django.contrib.auth.models import AbstractUser




class CustomUser(AbstractUser):
    bkash_number = models.CharField(max_length=11,blank=True,null=True)
    bkash_username = models.CharField(max_length=255,blank=True,null=True)
    bkash_password = models.CharField(max_length=255,blank=True,null=True)
    bkash_app_key = models.CharField(max_length=255,blank=True,null=True)
    bkash_secret_key = models.CharField(max_length=255,blank=True,null=True)
    mikrotik_host=models.CharField(max_length=32,blank=True,null=True)
    mikrotik_username=models.CharField(max_length=32,blank=True,null=True)
    mikrotik_password=models.CharField(max_length=32,blank=True,null=True)
    mikrotik_port=models.CharField(max_length=32,blank=True,null=True)
    mikrotik_use_ssl = models.BooleanField(default=True,blank=True,null=True)
    mikrotik_verify_ssl = models.BooleanField(default=True,blank=True,null=True)
    mikrotik_ssl_verify_hostname = models.BooleanField(default=True,blank=True,null=True)
    def __str__(self) -> str:
        return f"{self.username} -> {self.email}" 