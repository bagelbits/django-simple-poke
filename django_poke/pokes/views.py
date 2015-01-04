from django.shortcuts import get_object_or_404, render, get_list_or_404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic
from django.utils import timezone
from django.db.models import Q

from pokes.models import Poke, User


class IndexView(generic.ListView):
  template_name = 'pokes/index.html'
  context_object_name = 'poke_list'

  def get_queryset(self):
    """
    Return all pokes not including pokes set in the future. Shows all
    """
    return Poke.objects.filter(
        poke_date__lte=timezone.now()
      ).order_by('-poke_date')

class NewUserView(generic.ListView):
  template_name = 'pokes/new_user.html'
  context_object_name = 'user_list'

  def get_queryset(self):
    """
    Return all users.
    """
    return User.objects.order_by('-username')

def add_user(request):
  username = request.POST['username'].strip()
  try:
    if not username:
      raise KeyError
    user = User.objects.filter(username__iexact=username)
    if not user:
      raise User.DoesNotExist
  except User.DoesNotExist:
    User.objects.create(username=username)
    return HttpResponseRedirect(reverse('pokes:index'))
  except KeyError:
    # Redisplay new user form.
    return render(request, 'pokes/new_user.html', {
      'error_message' : "Username must be provided.",
      'user_list' : User.objects.order_by('-username'),
    })
  else:
    # Redisplay new user form.
    return render(request, 'pokes/new_user.html', {
      'error_message' : "User already exists.",
      'user_list' : User.objects.order_by('-username'),
    })

# Convert to detail or list view?
def detail(request, user_id):
  user = get_object_or_404(User, pk=user_id)
  poke_list = Poke.objects.filter(
    Q(send_user__exact=user) | Q(receive_user__exact=user)).order_by('-poke_date')
  user_list = User.objects.exclude(username__exact=user.username).order_by('-username')
  return render(request, 'pokes/detail.html', {
    'user' : user,
    'poke_list' : poke_list,
    'user_list' : user_list})

def create_poke(request, user_id):
  sender_id = user_id
  receiver_id = request.POST['receiver']

  try:
    send_user = User.objects.get(id=sender_id)
    receive_user = User.objects.get(id=receiver_id)
  except ValueError:
    user = get_object_or_404(User, pk=sender_id)
    poke_list = Poke.objects.filter(
      Q(send_user__exact=user) | Q(receive_user__exact=user))
    user_list = User.objects.exclude(username__exact=user.username).order_by('-username')
    return render(request, 'pokes/detail.html', {
      'error_message' : "User not selected.",
      'user' : user,
      'poke_list' : poke_list,
      'user_list' : user_list})
  except User.DoesNotExist:
    user = get_object_or_404(User, pk=sender_id)
    poke_list = Poke.objects.filter(
      Q(send_user__exact=user) | Q(receive_user__exact=user))
    user_list = User.objects.exclude(username__exact=user.username).order_by('-username')
    return render(request, 'pokes/detail.html', {
      'error_message' : "Selected user does not exist.",
      'user' : user,
      'poke_list' : poke_list,
      'user_list' : user_list})
  else:
    time = timezone.now()
    Poke.objects.create(send_user=send_user,
                        receive_user=receive_user,
                        poke_date=time)
    return HttpResponseRedirect(reverse('pokes:index'))