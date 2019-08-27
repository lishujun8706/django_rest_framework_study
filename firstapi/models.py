from __future__ import unicode_literals
from django.db import models

# Create your models here.
class UserInfo(models.Model):
    user_type_choices = (
        (1,'general'),
        (2,'VIP'),
        (3,'SVIP'),
    )
    user_type = models.IntegerField(choices=user_type_choices)
    username = models.CharField(max_length=32,unique=True)
    password = models.CharField(max_length=64)
    group = models.ForeignKey("UserGroup",on_delete=models.CASCADE,null=True)
    role = models.ManyToManyField("Role")

class UserToken(models.Model):
    user = models.OneToOneField(to='UserInfo',on_delete=models.CASCADE)
    token = models.CharField(max_length=64)

class Role(models.Model):
    title = models.CharField(max_length=64)

class UserGroup(models.Model):
    title = models.CharField(max_length=64)