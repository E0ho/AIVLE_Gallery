from django.dispatch import receiver
from allauth.account.signals import user_signed_up
from django.contrib.auth import get_user_model

# @receiver(user_signed_up)
# def user_signed_up_(request, user, **kwargs):
#     User = get_user_model()
#     split = str(user.email).split(" ")
#     user.username = split[0]
#     user.save()