# -*- coding: utf-8 -*- 
__author__ = 'yank'
__date__ = '2018/6/1/20:21'

from django.contrib.auth import get_user_model
from django.dispatch import receiver
from django.db.models.signals import post_save

User = get_user_model()


# django 自带信号量
@receiver(post_save, sender=User)
def create_user(sender, instance=None, created=False, **kwargs):
    if created:
        password = instance.password
        instance.set_password(password)
        instance.save()