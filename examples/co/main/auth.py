from main.models import UserProfile
from django.contrib.auth.backends import ModelBackend

class ProfileUserModelBackend(ModelBackend):

    def get_user(self, user_id):
        try:
            return UserProfile.objects.get(pk=user_id)
        except self.user_class.DoesNotExist:
            return None

    @property
    def user_class(self):
        return UserProfile

