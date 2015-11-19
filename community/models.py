from django.db import models
from django.contrib.auth.models import AbstractUser
from social.apps.django_app.default.models import DjangoUserMixin
from social.storage.django_orm import BaseDjangoStorage
from social.apps.django_app.default.fields import JSONField
from core.models import Account
from core.models import DetailMatch


class User(AbstractUser, DjangoUserMixin):
    provider = models.CharField(max_length=32)
    uid = models.CharField(max_length=255)
    extra_data = JSONField()
    account_id = models.PositiveIntegerField(null=True)

    @classmethod
    def create_social_auth(cls, user, uid, provider):
        user.account_id = User.normalize_account_id(int(uid))
        user.uid = uid
        user.provider = provider
        user.save()

        return user

    @classmethod
    def username_max_length(cls):
        return 255

    @classmethod
    def user_model(cls):
        return cls

    @staticmethod
    def normalize_account_id(account_id):
        return int(account_id) - 76561197960265728

    @property
    def user(self):
        return self


class Report(models.Model):
    creator = models.ForeignKey(Account, related_name='reports_created')
    reported = models.ForeignKey(Account, related_name='reports_received')
    due_to_match = models.ForeignKey(DetailMatch)
    date_created = models.DateTimeField(auto_now_add=True)

    reason = models.CharField(max_length=500)


class Post(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    sender = models.ForeignKey(Account, related_name='messages_made')
    receiver = models.ForeignKey(Account, related_name='messages_received')

    message = models.CharField(max_length=500)


class CommunityStorage(BaseDjangoStorage):
    user = User