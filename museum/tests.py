from django.test import TestCase, Client
from .models import Museum
from .forms import CreateGroupForm
import secrets
from django.contrib.auth.models import User
from user.models import UserProfile

class CreateDeleteGroupTestCase(TestCase):

    def setUp(self):
        _basic_setup(self)

    def test_create_one_userprofile_issaved(self):
        form = CreateGroupForm({
            'museum': self.museum.id,
            'name': 'group',
            'number': 1
        })
        form.is_valid()
        count = UserProfile.objects.all().count()
        pdf = form.create_users_pdf(self.user)
        self.assertEqual(UserProfile.objects.all().count(), count + 1)

    def test_create_two_userprofiles_issaved(self):
        form = CreateGroupForm({
            'museum': self.museum.id,
            'name': 'group',
            'number': 2
        })
        form.is_valid()
        count = UserProfile.objects.all().count()
        pdf = form.create_users_pdf(self.user)
        self.assertEqual(UserProfile.objects.all().count(), count + 2) 

class ToggleHideTestCase(TestCase):
    
    def setUp(self):
        _basic_setup(self)
        self.client.force_login(self.admin)
        self.url = f'/museum/{self.museum.id}/hide-user'

    def test_hideUser(self):
        response = self.client.post(self.url, data = {'profile': str(self.user.id)})
        self.assertTrue(self.user.userprofile in self.museum.hidden_profiles.all())

    def test_unhideUser(self):
        for _ in range(2):
            response = self.client.post(self.url, data = {'profile': str(self.user.id)})
        self.assertTrue(self.user.userprofile not in self.museum.hidden_profiles.all())

    def test_cannotHideUser(self):
        self.client.force_login(self.user)
        response = self.client.post(self.url, data = {'profile': str(self.user.id)})
        self.assertEqual(response.status_code, 403)

    def test_hideUser_noUser(self):
        response = self.client.post(self.url, data = {'profile': str(self.user.id + 10)})
        self.assertEqual(response.status_code, 404)     


def _basic_setup(tc):
    tc.museum = Museum.objects.create(
        name='museum',
        location='somewhere',
        secret_key='super secret',
    )
    tc.user = User.objects.create(
        username='username',
    )
    tc.admin = User.objects.create(
        username='admin',
        password='password',
    )
    tc.museum.profiles.add(tc.user.userprofile)
    tc.museum.admins.add(tc.admin)
    tc.museum.save()
    tc.client = Client()