from django.db import models


class TimestampMixin(models.Model):
    """Mixin per aggiungere automaticamente le date di creazione e aggiornamento."""

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True  # Non viene creata una tabella nel database


class OrderedModelMixin(models.Model):
    """Mixin per aggiungere un ordinamento predefinito."""

    class Meta:
        abstract = True
        ordering = ["last_name", "first_name"]


class Author(TimestampMixin, OrderedModelMixin):
    """Modello per rappresentare un autore."""

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    birthdate = models.DateField(null=True, blank=True)  # Può essere opzionale

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Book(TimestampMixin):
    """Modello per rappresentare un libro."""

    title = models.CharField(max_length=200)
    published_date = models.DateField()
    authors = models.ManyToManyField(Author, related_name="books")

    def __str__(self):
        return self.title
