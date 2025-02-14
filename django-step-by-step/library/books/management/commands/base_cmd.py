from django.core.management.base import BaseCommand

# ./manage.py base_cmd --message "TEST"


class Command(BaseCommand):
    help = "Stampa un messaggio personalizzato con un parametro nominale."

    def add_arguments(self, parser):
        parser.add_argument(
            "--message",  # Nome del parametro
            type=str,
            help="Il messaggio da stampare",
            required=True,  # Rende obbligatorio il parametro
        )

    def handle(self, *args, **kwargs):
        message = kwargs["message"]
        self.stdout.write(self.style.SUCCESS(f"📢 Messaggio: {message}"))
