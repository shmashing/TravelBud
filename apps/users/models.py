from __future__ import unicode_literals
import bcrypt
import re
from django.db import models


EMAIL_REGEX = re.compile(r'[a-zA-Z0-9.+_-]+@[a-zA-Z0-9.+_-]+\.[a-zA-Z]+$')
NAME_REGEX = re.compile(r'[a-zA-Z0-9.,-]*$')
# Create your models here.
class UserManager(models.Manager):
  def login(self, postData):
    username = postData['username']
    password = postData['password']
  
    try:
      user = User.objects.get(username=username.lower())
      new_hash = bcrypt.hashpw(password.encode(), user.password.encode())

      if(new_hash == user.password):
        return [True, user]

      else:
        return [False, "Password doens't match username"]
     
    except:
      return [False, "Incorrect Username/Password"]

  def register(self, postData):
    user_valid = {'valid':True, 'errors':[], 'user':None}

    try:
      User.objects.get(username=postData['username'].lower())
      user_valid['valid']=False
      user_valid['errors'].append('Username Taken')

    except:
      pass
    
    try:
      User.objects.get(email=postData['email'].lower())
      user_valid['valid']=False
      user_valid['errors'].append('Email Taken')
    
    except:
      pass


    email = str(postData['email'].lower())
    if(not EMAIL_REGEX.match(email)):
      user_valid['valid']=False
      user_valid['errors'].append('Please enter a valid email')


    first_name = postData['first_name']
    if(len(first_name) < 3) or (not NAME_REGEX.match(first_name)):
      user_valid['valid']=False
      user_valid['errors'].append('Please enter a valid first name')


    last_name = postData['last_name']
    if(len(last_name) < 2) or (not NAME_REGEX.match(last_name)):
      user_valid['valid']=False
      user_valid['errors'].append('Please enter a valid last name')

    username = postData['username'].lower()
    if(str(username) == '') or (not NAME_REGEX.match(first_name)):
      user_valid['valid']=False
      user_valid['errors'].append('Please enter a username')

    clearPassNoHash = postData['password']
    if(len(clearPassNoHash)<8):
      user_valid['valid']=False
      user_valid['errors'].append('Password must be 8 characters or more')
   
    if(user_valid['valid']):
      clearPassNoHash = clearPassNoHash.encode()
      hashPass = bcrypt.hashpw(clearPassNoHash, bcrypt.gensalt())
      user = User.objects.create(first_name=str(first_name), 
                                 last_name=str(last_name), 
                                 username=username, 
                                 email=str(email).lower(), 
                                 password=hashPass
      )

      user.save()
      user_valid['user'] = user

    for error in user_valid['errors']:
      print(error)

    return user_valid

class User(models.Model):
  first_name = models.CharField(max_length=45)
  last_name = models.CharField(max_length=45)
  username = models.CharField(max_length=45)
  email = models.CharField(max_length=100)
  password = models.CharField(max_length=100)
  objects = UserManager()
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)



