from __future__ import unicode_literals

from django.db import models

import re
import bcrypt, datetime

USERNAME_REGEX = re.compile(r'^[a-zA-Z]+$')
# Create your models here.
class UserManager(models.Manager):
    def validation(self, data):
        errors = []
        try:
            User.usrMgr.get(username = data['username'])
            errors.append("Username had already been used")
            return (False, errors)
        except:
            pass
        if len(data['name'])< 3 or not data['name'].isalpha:
            errors.append("Name has to longer than 3 letters and must only be letters")
        if len(data['username']) < 3:
            errors.append("Username has to be longer than 3 letters")
        elif not USERNAME_REGEX.match(data['username']):
            errors.append("Username is Invalid. It has to be letter ONLY!")
        if len(data['password']) == 0:
            errors.append("Password is required")
        elif len(data['password'])<8:
            errors.append("Password must be at least 8 characters")
        elif not data['password'] == data['confirm']:
            errors.append("Password must match the Password Confirmation")

        if not len(errors) == 0:
            return (False, errors)
        hashed = bcrypt.hashpw(data['password'].encode(), bcrypt.gensalt())
        x = User.usrMgr.create(name = data['name'], username = data['username'], password = hashed, doh = data['doh'])
        return (True, x)

    def login(self, data):
        errors = []
        if len(data['username'])==0:
            errors.append("Username is required")
            return (False, errors)
        elif not User.usrMgr.filter(username = data['username']).exists():
            errors.append("Username is Not Registered")
            return (False, errors)
        x = User.usrMgr.get(username = data['username'])
        if len(data['password']) == 0:
            errors.append("Password is required")
        elif not bcrypt.hashpw(data['password'].encode(), x.password.encode()) ==  x.password.encode():
            errors.append("Password is Invalid. Try again!")
        if not len(errors) == 0:
            return (False, errors)
        x.save()
        return (True, x)

class User(models.Model):
    name = models.CharField(max_length = 90)
    username = models.CharField(max_length = 60)
    password = models.CharField(max_length = 256)
    doh = models.DateField(blank = True, null = True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    usrMgr = UserManager()
