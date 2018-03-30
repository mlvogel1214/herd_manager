from __future__ import unicode_literals
from django.db import models
import bcrypt
import re


EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):

    def register_validate(self, postData):
        errors = {}
        if len(postData['first_name']) < 2 or len(postData['last_name']) < 2:
            errors['name'] = "Both names must be 2+ characters."
        if not postData['first_name'].isalpha() or not postData['last_name'].isalpha():
            errors['alpha'] = "Both names must only contain letters."
        if not postData['email']:
            errors['email'] = "Email field is required."
        if not postData['last_name'] == 'Vogel':
            errors['valid'] = 'You must be a Vogel'
        user = User.objects.filter(email = postData['email'])
        if user:
            errors['user'] = "An account with that email already exists."
        if not EMAIL_REGEX.match(postData['email']):
            errors['match'] = "Email format is invalid."
        if len(postData['password']) < 8:
            errors['password'] = "Password must be 8+ characters."
        if postData['conf'] != postData['password']:
            errors['conf'] = "Password confirmation must match password."
        return errors

    def login_validate(self, postData):
        errors = {}
        if not postData['email'] or not postData['password']:
            errors['blank'] = "All fields must be complete."
            return errors
        if not len(User.objects.filter(email = postData['email'])):
            errors['email'] = "Email does not match any records."
        if len(User.objects.filter(email = postData['email'])):
            b=User.objects.get(email= postData['email']).password
            password = b
            check = bcrypt.checkpw(postData['password'].encode(), password.encode())    
            if check != True:
                errors['password'] = 'Password does not exist'  
        return errors

    def register(self, postData):
        return self.create(first_name = postData['first_name'], last_name = postData['last_name'], company = postData['company'], email = postData['email'], password = bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt()))

    def login(self, postData):
        return self.get(email = postData['email'])

    def reset_passwordds(self, postData, id):
        b = User.objects.get(id = id)
        b.password.delete()
        b.password = bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt())
        b.save()

class User(models.Model):
    first_name = models.CharField(max_length = 255)
    last_name = models.CharField(max_length = 255)
    company = models.CharField(max_length = 255)
    email = models.CharField(max_length = 255)
    password = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()
