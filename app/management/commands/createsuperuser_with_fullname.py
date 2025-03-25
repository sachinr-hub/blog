from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import DEFAULT_DB_ALIAS

class Command(BaseCommand):
    help = 'Create a superuser with full_name'

    def add_arguments(self, parser):
        parser.add_argument(
            '--username', dest='username', default=None,
            help='Specifies the username for the superuser.',
        )
        parser.add_argument(
            '--email', dest='email', default=None,
            help='Specifies the email for the superuser.',
        )
        parser.add_argument(
            '--full_name', dest='full_name', default=None,
            help='Specifies the full name for the superuser.',
        )
        parser.add_argument(
            '--password', dest='password', default=None,
            help='Specifies the password for the superuser.',
        )
        parser.add_argument(
            '--database', action='store', dest='database',
            default=DEFAULT_DB_ALIAS,
            help='Specifies the database to use.',
        )

    def handle(self, *args, **options):
        User = get_user_model()
        
        username = options['username']
        email = options['email']
        full_name = options['full_name']
        password = options['password']
        database = options['database']

        if not username:
            username = input("Username: ")
        if not email:
            email = input("Email address: ")
        if not full_name:
            full_name = input("Full name: ")
        if not password:
            password = input("Password: ")

        try:
            user = User.objects.create_superuser(
                username=username,
                email=email,
                full_name=full_name,
                password=password,
            )
            self.stdout.write(self.style.SUCCESS(f'Superuser "{username}" created successfully.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error creating superuser: {e}')) 