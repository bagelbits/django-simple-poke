import datetime

from django.utils import timezone
from django.test import TestCase

from pokes.models import Poke, User

class PokeMethodTests(TestCase):
  def test_was_poked_recently_with_future_question(self):
    """
    was_poked_recently() should return False for questions whose
    poke_date is in the future
    """
    time = timezone.now() + datetime.timedelta(days=30)
    future_question = Poke(poke_date=time)
    self.assertEqual(future_question.was_poked_recently(), False)

  def test_was_poked_recently_with_old_question(self):
    """
    was_poked_recently() should return False for questions whose
    poke_date is older than 1 day
    """
    time = timezone.now() - datetime.timedelta(days=30)
    old_question = Poke(poke_date=time)
    self.assertEqual(old_question.was_poked_recently(), False)

  def test_was_poked_recently_with_recent_question(self):
    """
    was_poked_recently() should return True for questions whose
    poke_date is within the last day
    """
    time = timezone.now() - datetime.timedelta(hours=1)
    recent_question = Poke(poke_date=time)
    self.assertEqual(recent_question.was_poked_recently(), True)