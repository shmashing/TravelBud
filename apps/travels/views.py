from django.shortcuts import render, reverse, redirect
from ..users.models import User
from .models import Travel, JoinedUser
from django.contrib import messages
# Create your views here.
#Travel.objects.get(destination='Montana').delete()
def index(request):
    if(not check_user_authentication(request)):
      return redirect('users:home')

    user = User.objects.get(id=request.session['user_id'])

    context = {
      'user': user,
      'myTravels': Travel.objects.filter(user=user),
      'myJoinedTravels': JoinedUser.objects.filter(user=user),
      'otherTravels': Travel.objects.exclude(user=user).order_by('start'),
    }

    return render(request, "travels/index.html", context)

def add_travel(request):
    if(not check_user_authentication(request)):
      return redirect('users:home')

    context = {
      'user': User.objects.get(id=request.session['user_id'])
    }

    return render(request, "travels/add_travel.html", context)

def submit_travel(request, id):
    if(not check_user_authentication(request)):
      return redirect('users:home')

    postData = dict(request.POST.items())

    travel_valid = Travel.objects.makeTravel(postData, User.objects.get(id=request.session['user_id']))

    if(not travel_valid['isValid']):
      for error in travel_valid['errors']:
        messages.add_message(request, messages.INFO, error)

      return redirect('travel:addPlans')

    else:
      return redirect('travel:home')

def show_destination(request, id):
    if(not check_user_authentication(request)):
      return redirect('users:home')

    travel = Travel.objects.get(id=id)
    joiners = JoinedUser.objects.filter(travel=travel)
    context = {
      'travel' : travel,
      'joiners': joiners,
    }

    return render(request, 'travels/show_travel.html', context)

def add_user(request, id):
    if(not check_user_authentication(request)):
      return redirect('users:home')

    travel = Travel.objects.get(id=id)
    user = User.objects.get(id=request.session['user_id'])

    Travel.objects.addUserToTravel(travel.id, user.id)

    return redirect('travel:home')

def check_user_authentication(request):
    try:
      if(request.session['user_logged']):
        user_id = request.session['user_id']
        return True
      else:
        return False
    except:
      return False

