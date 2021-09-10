from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from allauth.account.signals import user_signed_up

from .models import VendorProfile

@receiver(user_signed_up)
def new_user_signup(sender, **kwargs):
    p = VendorProfile(user = kwargs['user'])
    p.save()