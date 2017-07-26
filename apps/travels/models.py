from __future__ import unicode_literals
from django.db import models
from ..users.models import User
import datetime

# Create your models here.
class TravelManager(models.Manager):
  def makeTravel(self, postData, user):
    travel_validation = {
      'isValid': True,
      'errors': [],
      'travel': None
    }

    
    dest = str(postData['destination'])
    desc = str(postData['description'])
    start = postData['start']
    end = postData['end']
 
    if(len(dest)==0):
      travel_validation['isValid'] = False
      travel_validation['errors'].append("Please enter a destination")
      
    if(len(desc)==0):
      travel_validation['isValid'] = False
      travel_validation['errors'].append("Please enter a description")

    time = datetime.datetime.now()
    time = [time.year, time.month, time.day]
    if(not self.validateTime(start, time)):
      travel_validation['isValid'] = False
      travel_validation['errors'].append("Please enter a valid start date")

    time = [start[0:4], start[5:7], start[8:10]]
    if(not self.validateTime(end, time)):
      travel_validation['isValid'] = False
      travel_validation['errors'].append("Please enter a valid end date")

    if(travel_validation['isValid']):
      start = start[0:10]
      print(start)
      travel = Travel.objects.create(destination=dest, plans=desc, user=user, start=start[0:10], end=end[0:10])
      travel_validation['travel']=travel


    return travel_validation

  def validateTime(self, time1, time2):
    try:
      start_y = int(time1[0:4])
      start_m = int(time1[5:7])
      start_d = int(time1[8:10])

      year = int(time2[0])
      month = int(time2[1])
      day = int(time2[2])
  
      if(start_y < year):
        return False

      elif(start_y == year):
        if(start_m < month):
          return False     

        elif(start_m == month):
          if(start_d <= day):
            return False 

      return True       
  
    except:
      return False

  def addUserToTravel(self, travel_id, user_id):
    travel = Travel.objects.get(id=travel_id)
    user = User.objects.get(id=user_id)
    user_joined = False
   
    joined_users = JoinedUser.objects.filter(travel=travel)
    for join in joined_users:
      if user.id == join.user.id:
        user_joined = True

    if(not user_joined):
      JoinedUser.objects.create(travel=travel, user=user)


class Travel(models.Model):
  destination = models.CharField(max_length=100)
  plans = models.TextField(max_length=1000)
  user = models.ForeignKey(User)
  start = models.DateField()
  end = models.DateField()
  objects = TravelManager()
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  def joinedUsers(self):
    user_ids = []

    joins = JoinedUser.objects.filter(travel=self)
    for join in joins:
      user_ids.append(join.user.id)

    return user_ids

class JoinedUser(models.Model):
  travel = models.ForeignKey(Travel)
  user = models.ForeignKey(User)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

