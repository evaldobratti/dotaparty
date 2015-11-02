from django.db import models
from django.contrib.auth.models import AbstractUser
from social.apps.django_app.default.models import UserSocialAuth

class User(AbstractUser):

    @property
    def account_id(self):
        account_id = User.normalize_account_id(UserSocialAuth.objects.get(user=self).uid)
        return account_id

    @staticmethod
    def normalize_account_id(account_id):
        return int(account_id) - 76561197960265728