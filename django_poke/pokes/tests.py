import datetime

from django.utils import timezone
from django.test import TestCase

from django.core.urlresolvers import reverse

from pokes.models import Poke, User

#########################################################
#                         Models                        #
#########################################################

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


#########################################################
#                          Views                        #
#########################################################
def create_user(username):
  """
  Creates a user with the given `username`.
  """
  return User.objects.create(username=username)

def create_poke(sender, receiver, days):
  """
  Creates a poke between two given users, `sender` and `receiver` with a
  given timestamp offset by a number of `days` to now (negative for
  questions published in the past, positive for questions that have yet
  to be published).
  """
  time = timezone.now() + datetime.timedelta(days=days)
  return Poke.objects.create(send_user=sender,
                             receive_user=receiver,
                             poke_date=time)


class PokeIndexViewTests(TestCase):
  def test_index_view_with_no_pokes(self):
    """
    If no pokes exist, an appropriate message should be displayed.
    """
    response = self.client.get(reverse('pokes:index'))
    self.assertEqual(response.status_code, 200)
    self.assertContains(response, "No pokes are available.")
    self.assertQuerysetEqual(response.context['poke_list'], [])

  def test_index_view_with_a_past_poke(self):
    """
    Pokes with a poke_date in the past should be displayed on the index page
    """
    user_1 = create_user(username="Bob")
    user_2 = create_user(username="George")
    create_poke(user_1, user_2, days=-30)
    response = self.client.get(reverse('pokes:index'))
    self.assertQuerysetEqual(
      response.context['poke_list'],
      ['<Poke: Poke from Bob to George>']
    )

  def test_index_view_with_a_future_poke(self):
    """
    Pokes with a poke_date in the future should not be displayed on the index
    page.
    """
    user_1 = create_user(username="Bob")
    user_2 = create_user(username="George")
    create_poke(user_1, user_2, days=30)
    response = self.client.get(reverse('pokes:index'))
    self.assertContains(response, "No pokes are available.",
                        status_code=200)
    self.assertQuerysetEqual(response.context['poke_list'], [])

  def test_index_view_with_a_future_poke_and_past_poke(self):
    """
    Even if both past and future pokes exist, only past pokes should be
    displayed.
    """
    user_1 = create_user(username="Bob")
    user_2 = create_user(username="George")
    create_poke(user_1, user_2, days=30)
    create_poke(user_1, user_2, days=-30)
    response = self.client.get(reverse('pokes:index'))
    self.assertQuerysetEqual(
      response.context['poke_list'],
      ['<Poke: Poke from Bob to George>']
    )

  def test_index_view_with_two_past_pokes(self):
    """
    The poke index page may display multiple questions.
    """
    user_1 = create_user(username="Bob")
    user_2 = create_user(username="George")
    create_poke(user_1, user_2, days=-30)
    create_poke(user_2, user_1, days=-30)
    response = self.client.get(reverse('pokes:index'))
    self.assertQuerysetEqual(
      response.context['poke_list'],
      ['<Poke: Poke from George to Bob>', '<Poke: Poke from Bob to George>']
    )


# Views to test:
# add user
# user pokes
# new poke