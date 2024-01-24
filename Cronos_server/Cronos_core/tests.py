from django.test import TestCase
from django.utils import timezone
from django.contrib.auth.models import User
from .models import Crons

class CronsTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.cron = Crons.objects.create(
            minutes='*',
            hours='*',
            day_of_month='*',
            months='*',
            day_of_week='*',
            command='ls',
            user=self.user
        )

    def test_get_day_of_week_choices(self):
        choices = Crons.get_day_of_week_choices()
        self.assertEqual(choices, [
            ('mon', 'Monday'), ('tue', 'Tuesday'), ('wed', 'Wednesday'), ('thu', 'Thursday'),
            ('fri', 'Friday'), ('sat', 'Saturday'), ('sun', 'Sunday'), ('*', 'each/any')
        ])

    def test_create_cron(self):
        self.assertEqual(self.cron.minutes, '*')
        self.assertEqual(self.cron.hours, '*')
        self.assertEqual(self.cron.day_of_month, '*')
        self.assertEqual(self.cron.months, '*')
        self.assertEqual(self.cron.day_of_week, '*')
        self.assertEqual(self.cron.command, 'ls')
        self.assertEqual(self.cron.user, self.user)

    def test_create_date(self):
        self.assertIsNotNone(self.cron.create_date)
        self.assertIsInstance(self.cron.create_date, timezone.datetime)

    def test_updated_date(self):
        self.assertIsNotNone(self.cron.updated_date)
        self.assertIsInstance(self.cron.updated_date, timezone.datetime)

    def test_validated(self):
        self.assertFalse(self.cron.validated)

    def test_is_paused(self):
        self.assertFalse(self.cron.is_paused)
