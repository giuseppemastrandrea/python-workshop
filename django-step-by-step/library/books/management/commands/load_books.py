import json
import os
from django.core.management.base import BaseCommand
from books.models import Author, Book
from datetime import datetime


class Command(BaseCommand):
    help = "Carica autori e libri da file JSON"

    def add_arguments(self, parser):
        parser.add_argument(
            "json_files", nargs="+", type=str, help="Percorsi dei file JSON da caricare"
        )

    def handle(self, *args, **options):
        for json_file in options["json_files"]:
            if not os.path.exists(json_file):
                self.stderr.write(f"❌ Il file {json_file} non esiste.")
                continue

            self.stdout.write(f"📂 Caricando dati da {json_file}...")
            with open(json_file, "r", encoding="utf-8") as file:
                try:
                    data = json.load(file)
                except json.JSONDecodeError:
                    self.stderr.write(
                        f"❌ Errore nel file JSON {json_file}, verifica il formato."
                    )
                    continue

            for item in data.get("books", []):
                # Creiamo o recuperiamo gli autori
                author_instances = []
                for author_data in item.get("authors", []):
                    first_name = author_data["first_name"]
                    last_name = author_data["last_name"]
                    birthdate = author_data.get("birthdate")

                    # Convertiamo la data di nascita in formato Django
                    birthdate_obj = None
                    if birthdate:
                        try:
                            birthdate_obj = datetime.strptime(
                                birthdate, "%Y-%m-%d"
                            ).date()
                        except ValueError:
                            self.stderr.write(
                                f"⚠️ Data di nascita non valida per {first_name} {last_name}: {birthdate}"
                            )

                    author, _ = Author.objects.get_or_create(
                        first_name=first_name,
                        last_name=last_name,
                        defaults={"birthdate": birthdate_obj},
                    )

                    # Aggiorniamo la data di nascita se è cambiata
                    if birthdate_obj and author.birthdate != birthdate_obj:
                        author.birthdate = birthdate_obj
                        author.save()

                    author_instances.append(author)

                # Creiamo o aggiorniamo il libro
                book, created = Book.objects.get_or_create(
                    title=item["title"], published_date=item["published_date"]
                )
                if created:
                    book.authors.set(author_instances)
                    book.save()
                    self.stdout.write(f"📖 Aggiunto libro: {book.title}")
                else:
                    self.stdout.write(f"✅ Libro già esistente: {book.title}")

            self.stdout.write(
                self.style.SUCCESS(
                    f"✅ Caricamento da {json_file} completato con successo!"
                )
            )
