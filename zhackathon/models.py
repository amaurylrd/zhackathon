from django.core.validators import RegexValidator
from django.db import models
from django.db.models import Model
from django.db.models.fields import (
    CharField,
    #    DecimalField,
    DateField,
    URLField,
)

from django.utils.text import gettext_lazy as _


class Festival(Model):
    id = CharField(primary_key=True, max_length=100)
    name = CharField(max_length=100)
    discipline = CharField(max_length=100)
    website = URLField(null=True, blank=True)
    start_date = DateField()
    end_date = DateField()
    # localisation = DecimalField(max_digits=9, decimal_places=6)
    region = CharField(max_length=100)
    department = CharField(max_length=100)
    commune = CharField(max_length=100)
    postcode = CharField(
        max_length=5,
        validators=[RegexValidator("^[0-9]{5}$", _("The postal code must be composed of 5 digits"))],
    )

    class Meta:
        ordering = ["start_date"]
        db_table = "festival"
        app_label = "festival"


class UserBase(Model):
    id = CharField(primary_key=True, max_length=100)
    name = CharField(max_length=100)
    password = CharField(max_length=100)

    class Meta:
        ordering = ["id"]
        db_table = "users"
        app_label = "users"

    def __str__(self):
        return self.name


class Admin(UserBase):

    class Meta:
        ordering = ["id"]
        db_table = "users"
        app_label = "admin"


class User(UserBase):
    favourites = models.ManyToManyField(Festival)

    class Meta:
        ordering = ["id"]
        db_table = "users"
        app_label = "user"


class Comments(Model):
    id = CharField(primary_key=True, max_length=100)
    sender = models.ForeignKey(UserBase, on_delete=models.SET_NULL, null=True)
    festival = models.ForeignKey(Festival, on_delete=models.SET_NULL, null=True)
    date = DateField
    text = CharField(max_length=5000)

    class Meta:
        ordering = ["id"]
        db_table = "comments"
        app_label = "comment"

    def __str__(self):
        return self.text
