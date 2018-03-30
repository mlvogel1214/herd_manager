from __future__ import unicode_literals

from django.db import models
from ..users.models import User

class herdManager(models.Manager):
    def add(self, postData):
        Herd.objects.create(species = postData['species'].upper(), sex = postData['sex'].lower(), tag = postData['tag'], date_of_birth = postData['date_of_birth'])

    def delete(self, postData, id):
        b= Herd.objects.get(id=id)
        b.delete()

    def add_validator(self, postData):
        errors = {}
        if not postData['species'] or not postData['sex'] or not postData['tag'] or not postData['date_of_birth']:
            errors['fields']= 'All fields required'
            return errors

class OffManager(models.Manager):
    def offValidator(self, postData):
        errors = {}
        if not postData['sex'] or not postData['tag'] or not postData['sire'] or not postData['date_of_birth']:
            errors['fields'] = 'All fields required'
            return errors
            
    def addOff(self, postData):
        dad = Herd.objects.get(tag = postData['sire'])
        Offspring.objects.create(species = postData['species'], sex = postData['sex'], tag = postData['tag'], date_of_birth = postData['date_of_birth'], animal=Herd.objects.get(id = postData['id']), sire = dad)
        Herd.objects.create(species = postData['species'], sex = postData['sex'], tag = postData['tag'], date_of_birth = postData['date_of_birth'])

class Herd(models.Model):
    species = models.CharField(max_length = 255)
    sex = models.CharField(max_length = 10)
    tag = models.IntegerField()
    date_of_birth = models.DateField(null = True)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = herdManager()

class Offspring(models.Model):
    species = models.CharField(max_length = 255)
    sex = models.CharField(max_length = 255)
    tag = models.IntegerField()
    date_of_birth = models.DateField(null = True)
    animal = models.ForeignKey(Herd, related_name='offspring')
    sire = models.ForeignKey(Herd, related_name='sire', default= 0)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = OffManager()

