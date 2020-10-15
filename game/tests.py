from django.test import TestCase
from .models import RawGameResult, GameResult
from museum.models import Museum, Simulator
from user.models import UserProfile
from django.contrib.auth.models import User
from django.utils import timezone
import secrets
import datetime

class GameResultTestCase(TestCase):

    def setUp(self):
        start_time = timezone.now()
        end_time = start_time + datetime.timedelta(seconds=1)

        self.museum = Museum(secret_key=secrets.token_hex(24),name='museum')
        self.simulator = Simulator(name='simulator')
        self.pilot = User(username='pilot',password='testing123')
        self.copilot = User(username='copilot', password='testing123')
        self.museum.save()
        self.simulator.museum = self.museum
        self.simulator.save()
        self.pilot.save()
        self.copilot.save()

        self.rgr = RawGameResult(
            u1_qr_token = self.pilot.userprofile.qr_token,
            u2_qr_token = self.copilot.userprofile.qr_token,
            museum_secret_key = self.museum.secret_key,
            museum_id = self.museum.pk,
            sim_id = self.simulator.pk,
            start_time = start_time,
            end_time = end_time,
            score=10,
            num_of_rolls=10,
        )

        self.rgr2 = RawGameResult(
            u1_qr_token = self.pilot.userprofile.qr_token,
            u2_qr_token = self.copilot.userprofile.qr_token,
            museum_secret_key = self.museum.secret_key,
            museum_id = self.museum.pk,
            sim_id = self.simulator.pk,
            start_time = start_time,
            end_time = end_time,
            score=10,
            num_of_rolls=10,
        )


    def test_create_RawGameResult_valid(self):
        self.assertTrue(self.rgr.is_valid())

    def test_create_RawGameResult_onePlayer_valid(self):
        self.rgr.u2_qr_token = ''
        self.assertTrue(self.rgr.is_valid())

    def test_RawGameResult_bad_museum_key_invalid(self):
        self.rgr.museum_secret_key = 'blah'
        self.assertFalse(self.rgr.is_valid())

    def test_RawGameResult_bad_museum_id_invalid(self):
        self.rgr.museum_id = -1
        self.assertFalse(self.rgr.is_valid())

    def test_RawGameResult_bad_sim_id_invalid(self):
        self.rgr.sim_id = -1
        self.assertFalse(self.rgr.is_valid())

    def test_RawGameResult_bad_qrcode_id_invalid(self):
        self.rgr.u1_qr_token = 'blah'
        self.assertFalse(self.rgr.is_valid())

    def test_RawGameResult_bad_zeroSeconds(self):
        self.rgr.end_time = self.rgr.start_time
        self.assertFalse(self.rgr.is_valid())

    def test_create_GameResult(self):
        self.rgr.save() # signal creates game result object
        game_result = GameResult.objects.get(raw_result=self.rgr)
        self.assertTrue(game_result)
        self.assertEqual(game_result.simulator.pk, self.simulator.pk)
        self.assertEqual(game_result.pilot.pk, self.pilot.userprofile.pk)
        self.assertEqual(game_result.copilot.pk, self.copilot.userprofile.pk)

    def test_is_gameresult_not_saved(self):
        self.assertFalse(self.rgr.is_gameresult())
        self.assertFalse(self.rgr2.is_gameresult())

    def test_is_gameresult_saved(self):
        self.rgr.save()
        self.assertTrue(self.rgr.is_gameresult())
        self.assertTrue(self.rgr2.is_gameresult())

    def test_wont_create_duplicate(self):
        self.rgr.save()
        self.rgr2.save()
        self.assertEqual(GameResult.objects.filter(raw_result=self.rgr).count(),1)
        self.assertEqual(GameResult.objects.filter(raw_result=self.rgr2).count(),0)
