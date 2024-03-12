from django.test import TestCase
from django.utils import timezone
from django.contrib.auth.models import User
from Cronos_core.models import Crons, Logs, Profiles, PasswordTemporaryToken, ActivationTemporaryToken
from Cronos_API import COMMANDS
from datetime import timedelta


class CronsTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.cron = Crons.objects.create(
            minutes='30',
            hours='12',
            day_of_month='*',
            months='*',
            day_of_week='*',
            command='open',
            user=self.user
        )

    def test_get_minutes_choices(self):
        choices = Crons.get_minutes_choices()
        self.assertEqual(len(choices), 61)  # 60 minutes + each/any option

    def test_get_hours_choices(self):
        choices = Crons.get_hours_choices()
        self.assertEqual(len(choices), 25)  # 24 hours + each/any option

    def test_get_day_of_month_choices(self):
        choices = Crons.get_day_of_month_choices()
        self.assertEqual(len(choices), 33)  # 31 days + separator + each/any option

    def test_get_months_choices(self):
        choices = Crons.get_months_choices()
        self.assertEqual(len(choices), 14)  # 12 months + separator + each/any option

    def test_get_day_of_week_choices(self):
        choices = Crons.get_day_of_week_choices()
        self.assertEqual(len(choices), 9)  # 7 days + separator + each/any option

    def test_get_command_choices(self):
        choices = Crons.get_command_choices()
        self.assertEqual(len(choices), len(COMMANDS))  # Assuming COMMANDS is defined somewhere

    def test_cron_creation(self):
        self.assertEqual(self.cron.minutes, '30')
        self.assertEqual(self.cron.hours, '12')
        self.assertEqual(self.cron.day_of_month, '*')
        self.assertEqual(self.cron.months, '*')
        self.assertEqual(self.cron.day_of_week, '*')
        self.assertEqual(self.cron.command, 'open')
        self.assertEqual(self.cron.user, self.user)
        self.assertEqual(self.cron.validated, False)
        self.assertEqual(self.cron.is_paused, False)
        self.assertTrue(self.cron.create_date <= timezone.now())
        self.assertTrue(self.cron.updated_date <= timezone.now())

    def test_cron_str_representation(self):
        self.assertEqual(str(self.cron), "30 12 * * * open")

    def test_cron_update(self):
        self.cron.minutes = '0'
        self.cron.save()
        updated_cron = Crons.objects.get(pk=self.cron.pk)
        self.assertEqual(updated_cron.minutes, '0')

    def test_cron_deletion(self):
        self.cron.delete()
        self.assertFalse(Crons.objects.filter(pk=self.cron.pk).exists())


class LogsTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.cron = Crons.objects.create(
            minutes='30',
            hours='12',
            day_of_month='*',
            months='*',
            day_of_week='*',
            command='open',
            user=self.user
        )
    def test_logs_creation(self):
        log = Logs.objects.create(log='test log', user=self.user, cron=self.cron)
        self.assertEqual(log.log, 'test log')
        self.assertEqual(log.create_date.date(), timezone.now().date())
        self.assertEqual(log.user, self.user)
        self.assertEqual(log.cron, self.cron)


class ProfilesModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser')
        self.profile = Profiles.objects.create(
            first_name='John',
            last_name='Doe',
            user=self.user
        )

    def test_profiles_fields(self):
        self.assertEqual(self.profile.first_name, 'John')
        self.assertEqual(self.profile.last_name, 'Doe')
        self.assertEqual(self.profile.user, self.user)

    def test_profiles_str(self):
        self.assertEqual(str(self.profile), 'John Doe')

    def test_profiles_user_null(self):
        profile = Profiles.objects.create(
            first_name='Jane',
            last_name='Smith',
            user=None
        )
        self.assertIsNone(profile.user)

    def test_profiles_user_delete(self):
        self.user.delete()
        profile = Profiles.objects.get(id=self.profile.id)
        self.assertIsNone(profile.user)


class PasswordTemporaryTokenTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.token = PasswordTemporaryToken.objects.create(user=self.user)

    def test_save_generates_token_and_expiration_date(self):
        self.assertIsNotNone(self.token.change_pwd_token)
        self.assertIsNotNone(self.token.expires_at)

    def test_token_validity(self):
        self.assertTrue(self.token.is_valid())

    def test_token_expired(self):
        self.token.expires_at = timezone.now() - timedelta(hours=1)
        self.token.save()
        self.assertFalse(self.token.is_valid())


class ActivationTemporaryTokenTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser')
        self.token = ActivationTemporaryToken.objects.create(user=self.user)

    def test_save_generates_token_and_expiration_date(self):
        self.assertIsNotNone(self.token.activation_token)
        self.assertIsNotNone(self.token.expires_at)

    def test_expiration_date(self):
        expected_expiration_date = timezone.now() + timedelta(days=7)
        self.assertEqual(self.token.expires_at.date(), expected_expiration_date.date())

    def test_token_validity(self):
        self.assertTrue(self.token.is_valid())

    def test_token_expired(self):
        self.token.expires_at = timezone.now() - timedelta(days=1)
        self.assertFalse(self.token.is_valid())
