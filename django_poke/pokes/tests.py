import datetime

from django.utils import timezone
from django.test import TestCase

from django.core.urlresolvers import reverse

from pokes.models import Poke, User

def create_user(username):
  """
  Creates a user with the given `username`.
  """
  return User.objects.create(username=username)

def create_poke(sender, receiver, days=0):
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

#########################################################
#                         Models                        #
#########################################################

class PokeMethodTests(TestCase):
  def test_was_poked_recently_with_future_poke(self):
    """
    was_poked_recently() should return False for pokes whose
    poke_date is in the future
    """
    time = timezone.now() + datetime.timedelta(days=30)
    future_poke = Poke(poke_date=time)
    self.assertEqual(future_poke.was_poked_recently(), False)

  def test_was_poked_recently_with_old_poke(self):
    """
    was_poked_recently() should return False for pokes whose
    poke_date is older than 1 day
    """
    time = timezone.now() - datetime.timedelta(days=30)
    old_poke = Poke(poke_date=time)
    self.assertEqual(old_poke.was_poked_recently(), False)

  def test_was_poked_recently_with_recent_poke(self):
    """
    was_poked_recently() should return True for pokes whose
    poke_date is within the last day
    """
    time = timezone.now() - datetime.timedelta(hours=1)
    recent_poke = Poke(poke_date=time)
    self.assertEqual(recent_poke.was_poked_recently(), True)

  def test_User_prints_correctly(self):
    """

    """
    new_user = User(username='Test')
    self.assertEqual(str(new_user), 'Test')


#########################################################
#                          Views                        #
#########################################################

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

class PokeNewUserViewTests(TestCase):
  def test_new_user_view_with_no_users(self):
    """
    If no users exist, an appropriate message should be displayed.
    """
    response = self.client.get(reverse('pokes:new_user'))
    self.assertEqual(response.status_code, 200)
    self.assertContains(response, "No users currently exist.")
    self.assertQuerysetEqual(response.context['user_list'], [])

  def test_new_user_view_with_one_user(self):
    """
    Existing user should be displayed on new user page
    """
    user_1 = create_user(username="Bob")
    response = self.client.get(reverse('pokes:new_user'))
    self.assertQuerysetEqual(
      response.context['user_list'],
      ['<User: Bob>']
    )

  def test_new_user_view_with_two_users(self):
    """
    Multiple existing user should be displayed on new user page
    """
    user_1 = create_user(username="Bob")
    user_2 = create_user(username="George")
    response = self.client.get(reverse('pokes:new_user'))
    self.assertQuerysetEqual(
      response.context['user_list'],
      ['<User: George>', '<User: Bob>']
    )

class PokeAddUserViewTests(TestCase):
  def test_add_user_view_to_add_user(self):
    """
    Should be able to add users
    """
    response = self.client.post(reverse('pokes:add_user'), {'username': 'Bob'})
    self.assertEqual(response.status_code, 302)
    response = self.client.get(reverse('pokes:new_user'))
    self.assertEqual(response.status_code, 200)
    self.assertQuerysetEqual(
      response.context['user_list'],
      ['<User: Bob>']
    )

  def test_add_user_view_to_existing_user(self):
    """
    Cannot add existing user.
    """
    response = self.client.post(reverse('pokes:add_user'), {'username': 'Bob'})
    self.assertEqual(response.status_code, 302)
    response = self.client.post(reverse('pokes:add_user'), {'username': 'Bob'})
    self.assertEqual(response.status_code, 200)
    self.assertContains(response, "User already exists.")

  def test_add_user_view_to_add_case_insentive_user(self):
    """
    User names should currently be case insensitive.
    """
    response = self.client.post(reverse('pokes:add_user'), {'username': 'Bob'})
    self.assertEqual(response.status_code, 302)
    response = self.client.post(reverse('pokes:add_user'), {'username': 'bob'})
    self.assertEqual(response.status_code, 200)
    self.assertContains(response, "User already exists.")

  def test_add_user_view_no_user(self):
    """
    If not username is supplied, nothing should be added.
    """
    response = self.client.post(reverse('pokes:add_user'), {'username': ''})
    self.assertEqual(response.status_code, 200)
    self.assertContains(response, "Username must be provided.")

class PokeUserDetailViewTests(TestCase):
  def test_user_detail_view_no_pokes(self):
    """
    If no pokes exist for the user, an appropriate message should be displayed.
    """
    user_1 = create_user(username="Bob")
    response = self.client.post(reverse('pokes:detail',
                                        args=(user_1.id,)))
    self.assertEqual(response.status_code, 200)
    self.assertContains(response, "No pokes for user.")
    self.assertQuerysetEqual(response.context['poke_list'], [])

  def test_user_detail_view_with_poke(self):
    """
    If poke exists, list should show.
    """
    user_1 = create_user(username="Bob")
    user_2 = create_user(username="George")
    create_poke(user_1, user_2)
    response = self.client.post(reverse('pokes:detail',
                                        args=(user_1.id,)))
    self.assertQuerysetEqual(response.context['poke_list'],
      ['<Poke: Poke from Bob to George>']
    )

  def test_user_detail_view_with_multiple_pokes(self):
    """
    If multiple pokes exists, list should show.
    """
    user_1 = create_user(username="Bob")
    user_2 = create_user(username="George")
    create_poke(user_1, user_2)
    create_poke(user_1, user_2, days=-1)
    response = self.client.post(reverse('pokes:detail',
                                        args=(user_1.id,)))
    self.assertQuerysetEqual(response.context['poke_list'],
      ['<Poke: Poke from Bob to George>', '<Poke: Poke from Bob to George>']
    )

class PokeNewPokeViewTests(TestCase):
  def test_new_poke_view_create_poke(self):
    """
    Should be able to create a poke
    """
    user_1 = create_user(username="Bob")
    user_2 = create_user(username="George")

    response = self.client.post(reverse('pokes:create_poke', args=(user_1.id,))
                              , {'receiver': user_2.id})
    self.assertEqual(response.status_code, 302)
    response = self.client.get(reverse('pokes:index'))
    self.assertEqual(response.status_code, 200)
    self.assertQuerysetEqual(response.context['poke_list'], ['<Poke: Poke from Bob to George>'])

  def test_new_poke_view_create_poke_no_user(self):
    """
    Should not create a poke if no reciever is given
    """
    user_1 = create_user(username="Bob")
    user_2 = create_user(username="George")

    response = self.client.post(reverse('pokes:create_poke', args=(user_1.id,))
                              , {'receiver': ''})
    self.assertEqual(response.status_code, 200)
    self.assertContains(response, "User not selected.")

  def test_new_poke_view_create_poke_nonexistent_user(self):
    """
    Should not create a poke if user doesn't exist
    """
    user_1 = create_user(username="Bob")

    response = self.client.post(reverse('pokes:create_poke', args=(user_1.id,))
                              , {'receiver': 20})
    self.assertEqual(response.status_code, 200)
    self.assertContains(response, "Selected user does not exist.")

# Views to test:
# new poke