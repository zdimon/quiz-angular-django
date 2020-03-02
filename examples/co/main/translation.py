from modeltranslation.translator import translator, TranslationOptions
from main.models import UserProfile

class UserProfileTranslationOptions(TranslationOptions):
    fields = ('desc',)
translator.register(UserProfile, UserProfileTranslationOptions)
