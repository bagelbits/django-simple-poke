from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic
from django.utils import timezone

from pokes.models import Poke, User


class IndexView(generic.ListView):
  template_name = 'pokes/index.html'
  context_object_name = 'poke_list'

  def get_queryset(self):
    """
    Return all pokes not including pokes set in the future. Shows all
    """
    poke_list = Poke.objects.filter(
        poke_date__lte=timezone.now()
      ).order_by('-poke_date')

    formated_poke_list = []
    for poke in poke_list:
      formated_poke = {
        'send_id' : poke.send_user
      }
      formated_poke_list.append(formated_poke)
    print poke_list
    print formated_poke_list

    return poke_list

def new_user(request, user_id):
  pass

class DetailView(generic.ListView):
  model = User
  template_name = 'pokes/detail.html'

  def get_queryset(self):
    pass

def create_poke(request, user_id):
  pass