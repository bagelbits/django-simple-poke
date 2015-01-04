import datetime

from django.db import models
from django.utils import timezone

class User(models.Model):
  username = models.CharField(max_length=200)

  def __unicode__(self):
    return self.username

class Poke(models.Model):
  send_user = models.ForeignKey(User, related_name="poker")
  receive_user = models.ForeignKey(User, related_name="pokee")
  poke_date = models.DateTimeField('date poked')

  def __unicode__(self):
    return "Poke from {0} to {1}".format(self.send_user.username, self.receive_user.username)

  # Really just for fun since we can
  def was_poked_recently(self):
    now = timezone.now()
    return now - datetime.timedelta(days=1) <= self.poke_date <= now

  was_poked_recently.admin_order_field = 'poke_date'
  was_poked_recently.boolean = True
  was_poked_recently.short_description = 'Poked recently?'