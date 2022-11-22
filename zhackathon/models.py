from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import Model
from django.db.models.fields import (
    CharField,
    DateField,
    DecimalField,
    IntegerField,
    DurationField,
    URLField,
)


class Festival(Model):
    identifiant = CharField(primary_key=True, max_length=100)
    nom_du_festival = CharField(max_length=100)
    discipline_dominante = CharField(max_length=100)
    annee_de_creation = DateField()
    site = URLField(null=True, blank=True)
    periode = DurationField()
    geolocalisation = DecimalField(max_digits=9, decimal_places=6)
    region_principale = CharField(max_length=100)
    department_principal = CharField(max_length=100)
    commune_principale = CharField(max_length=100)
    code_postal_commune = IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)])

    class Meta:
        ordering = ["annee_de_creation"]
        db_table = "festival"
