from modeltranslation.translator import translator, TranslationOptions
from .models import Page

class PageTranslationOptions(TranslationOptions):
    fields = ('title', 'content', 'meta_title', 'meta_keywords', 'meta_description')

translator.register(Page, PageTranslationOptions)