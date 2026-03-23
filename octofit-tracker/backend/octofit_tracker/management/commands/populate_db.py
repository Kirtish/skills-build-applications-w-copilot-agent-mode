from django.core.management.base import BaseCommand
from octofit_tracker.models import User, Team, Activity, Leaderboard, Workout
from django.db import connection

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **kwargs):
        # Clear all collections
        User.objects.all().delete()
        Team.objects.all().delete()
        Activity.objects.all().delete()
        Leaderboard.objects.all().delete()
        Workout.objects.all().delete()

        # Teams
        marvel = Team.objects.create(name='marvel')
        dc = Team.objects.create(name='dc')

        # Users
        ironman = User.objects.create(email='ironman@marvel.com', name='Iron Man', team='marvel')
        captain = User.objects.create(email='captain@marvel.com', name='Captain America', team='marvel')
        batman = User.objects.create(email='batman@dc.com', name='Batman', team='dc')
        superman = User.objects.create(email='superman@dc.com', name='Superman', team='dc')

        # Activities
        Activity.objects.create(user=ironman.email, type='run', duration=30, date='2023-01-01')
        Activity.objects.create(user=captain.email, type='cycle', duration=45, date='2023-01-02')
        Activity.objects.create(user=batman.email, type='swim', duration=60, date='2023-01-03')
        Activity.objects.create(user=superman.email, type='fly', duration=120, date='2023-01-04')

        # Leaderboard
        Leaderboard.objects.create(user=ironman.email, score=100)
        Leaderboard.objects.create(user=captain.email, score=90)
        Leaderboard.objects.create(user=batman.email, score=110)
        Leaderboard.objects.create(user=superman.email, score=120)

        # Workouts
        Workout.objects.create(name='Pushups', description='Do 20 pushups', difficulty='easy')
        Workout.objects.create(name='Situps', description='Do 30 situps', difficulty='easy')
        Workout.objects.create(name='Pullups', description='Do 10 pullups', difficulty='medium')
        Workout.objects.create(name='Squats', description='Do 40 squats', difficulty='medium')

        # Ensure unique index on email for users
        with connection.cursor() as cursor:
            cursor.execute('db.users.createIndex({ "email": 1 }, { "unique": true })')

        self.stdout.write(self.style.SUCCESS('octofit_db database populated with test data.'))
