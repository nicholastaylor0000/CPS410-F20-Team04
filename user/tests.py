from django.test import TestCase
from .models import (UserProfile,
                    delete_overdue_profiles,
                    EXPIRE_AFTER_DAYS)
from django.contrib.auth.models import User
from museum.models import Museum
from django.utils import timezone
from datetime import timedelta

class UserProfileTestCase(TestCase):

    def setUp(self):
        self.museum = Museum(name='museum',location='somewhere',secret_key='super secret')
        self.user = User(username='password',password='username1')
        self.profile = UserProfile()
        self.museum.save()

    def test_saveUser_createUserProfile(self):
        self.user.save()
        # signal creates userprofile
        profile = self.user.userprofile
        self.assertTrue(profile)
        self.assertTrue(profile.qr_token)
        self.assertFalse(profile.is_before_user)

    def test_saveProfile_noUser(self):
        count = UserProfile.objects.all().count()
        self.profile.save()
        self.assertEqual(UserProfile.objects.all().count(), count + 1)
        self.assertEqual(len(self.profile.qr_token), 24)
        self.assertTrue(self.profile.user is None)
        self.assertTrue(self.profile.is_before_user)

    def test_saveProfile_withUser(self):
        self.user.userprofile = self.profile
        self.user.save()
        # signal will save the userprofile
        self.museum.profiles.add(self.profile)
        self.museum.save()
        user = User.objects.get(username='password')
        self.assertTrue(user.userprofile.qr_token, self.profile.qr_token)
        self.assertTrue(self.profile.is_before_user)
        self.assertEqual(self.museum.profiles.count(), 1)


class DeleteOverdueProfilesTestCase(TestCase):

    def setUp(self):
        self.profile = UserProfile()

    def test_delete_none(self):
        delete_overdue_profiles()
        self.assertEqual(UserProfile.objects.all().count(), 0)

    def test_delete_no_overdue(self):
        self.profile.save()
        delete_overdue_profiles()
        self.assertEqual(UserProfile.objects.all().count(), 1)

    def test_delete_overdue(self):
        self.profile.save()
        self.profile.date_created = timezone.now() - timedelta(EXPIRE_AFTER_DAYS)
        self.profile.save()
        delete_overdue_profiles()
        self.assertTrue(self.profile.user is None)
        self.assertEqual(UserProfile.objects.all().count(), 0)
