from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from account.models import Profile
from dj.settings import BASE_DIR
from os import path
import json


class Command(BaseCommand):
    def handle(self, *args, **options):
        print("Start creating users")
        User.objects.all().delete()
        Profile.objects.all().delete()
        f = open(path.join(BASE_DIR, "data", "users.json"))
        raw = f.read()
        f.close()
        js = json.loads(raw)
        for i in js:
            p = Profile()
            u = User()
            u.username = i['username']
            u.email = i['username']
            u.set_password(i['password'])
            u.is_active = True
            if i['is_admin']:
                u.is_superuser = True
                u.is_staff = True
            u.save()
            p.user = u
            p.wins = i['wins']
            p.lose = i['lose']
            p.leave = i['leave']
            p.all = i['all']
            p.coins = i['coins']
            p.phone = i['phone']
            p.rating = i['rating']
            p.birthday = i['birthday']
            p.gender = i['gender']
            p.country = i['country']
            p.save()
            print i['username']