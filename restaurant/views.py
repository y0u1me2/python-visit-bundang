from django.shortcuts import render
from .models import Restaurant
import logging
logger = logging.getLogger('restaurant')


def list(request):
    restaurant_list = Restaurant.objects.all()
    context = {'restaurant_list' : restaurant_list}

    return render(request, 'restaurant/list.html', context)