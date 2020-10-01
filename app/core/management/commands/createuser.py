import getpass

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

UserModel = get_user_model()


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument(
            '--staff',
            action='store_true',
            help='Create a new staff user.',
        )

    def handle(self, *args, **options):

        first_name = input('First Name: ')
        if not first_name:
            raise ValueError('No First name')

        username = input('Username: ')
        if not username:
            raise ValueError('No Username')

        email = input('Email: ')
        if not email:
            raise ValueError('No Email Address')

        password = None
        password_correct = False

        while not password_correct:
            password = getpass.getpass()
            password2 = getpass.getpass('Password (confirm): ')
            if password == password2:
                password_correct = True
            else:
                self.stdout.write(
                    self.style.ERROR('The passwords do not match, '
                                     'please re-enter them!'),
                )
        try:
            if options['staff']:
                UserModel.objects.create_staff_user(
                    first_name=first_name,
                    username=username,
                    email=email,
                    password=password,
                )
                self.stdout.write(
                    self.style.SUCCESS(f'New Staff User '
                                       f'Successful: {username} ({email})'),
                )
            else:
                UserModel.objects.create_user(
                    first_name=first_name,
                    username=username,
                    email=email,
                    password=password,
                )
                self.stdout.write(
                    self.style.SUCCESS(f'New User Successful '
                                       f'Created: {username} ({email})'),
                )

        except ValueError:
            self.stdout.write(
                self.style.ERROR('Failed to create user!'),
            )
