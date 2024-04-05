from django.core.management.base import BaseCommand
from myapp.models import GSL, Tunnel, Weiche, Bruecke

class Command(BaseCommand):
    help = 'Describe what this command does.'

    def handle(self, *args, **options):
        # Delete all instances of Tunnel, Weiche, and Bruecke models
        Tunnel.objects.all().delete()
        Weiche.objects.all().delete()
        Bruecke.objects.all().delete()

        # Once the child model instances are deleted, delete all instances of the GSL model
        GSL.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Successfully deleted data'))






