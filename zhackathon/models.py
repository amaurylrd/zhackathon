from django.core.validators import RegexValidator
from django.db.models import Model
from django.db.models.fields import (
    CharField,
    DateField,
    DecimalField,
    DurationField,
    URLField,
)
from django.utils.text import gettext_lazy as _


class Festival(Model):
    identifiant = CharField(primary_key=True, max_length=255)
    nom_du_festival = CharField(max_length=255)
    discipline_dominante = CharField(max_length=255)
    annee_de_creation = DateField()
    site = URLField(null=True, blank=True)
    periode = DurationField()
    geolocalisation = DecimalField(max_digits=9, decimal_places=6)
    region_principale = CharField(max_length=255)
    department_principal = CharField(max_length=255)
    commune_principale = CharField(max_length=255)
    code_postal_commune = CharField(
        max_length=5,
        validators=[RegexValidator("^[0-9]{5}$", _("Invalid postal code"))],
    )

    class Meta:
        ordering = ["annee_de_creation"]
        db_table = "festival"
