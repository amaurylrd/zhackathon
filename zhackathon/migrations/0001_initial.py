# Generated by Django 4.1.3 on 2022-11-23 12:45

import uuid

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Festival",
            fields=[
                ("id", models.CharField(editable=False, max_length=20, primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=100)),
                ("discipline", models.CharField(max_length=200)),
                ("description", models.TextField(blank=True, max_length=500, null=True)),
                ("website", models.URLField(blank=True, null=True)),
                ("period", models.CharField(blank=True, max_length=100, null=True)),
                ("region", models.CharField(blank=True, max_length=100, null=True)),
                ("department", models.CharField(blank=True, max_length=100, null=True)),
                ("commune", models.CharField(blank=True, max_length=100, null=True)),
                (
                    "postcode",
                    models.CharField(
                        blank=True,
                        max_length=5,
                        null=True,
                        validators=[django.core.validators.RegexValidator("^[0-9]{5}$")],
                    ),
                ),
            ],
            options={
                "db_table": "festival",
            },
        ),
        migrations.CreateModel(
            name="Ticketing",
            fields=[
                ("name", models.CharField(max_length=100, primary_key=True, serialize=False)),
                ("total_tickets", models.PositiveIntegerField(editable=False)),
                ("available_tickets", models.PositiveIntegerField()),
                (
                    "status",
                    models.CharField(
                        choices=[("OPEN", "Open"), ("CLOSED", "Closed"), ("LAST PLACES", "Last Places")],
                        default="OPEN",
                        max_length=25,
                    ),
                ),
                ("opened_at", models.DateTimeField(auto_now_add=True)),
                ("festival", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="zhackathon.festival")),
            ],
            options={
                "db_table": "ticketing",
            },
        ),
        migrations.CreateModel(
            name="Comment",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("content", models.TextField(max_length=255)),
                ("author", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ("festival", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="zhackathon.festival")),
                ("liked_by", models.ManyToManyField(related_name="comments_liked", to=settings.AUTH_USER_MODEL)),
            ],
            options={
                "db_table": "comment",
                "ordering": ["-created_at"],
            },
        ),
        migrations.CreateModel(
            name="Rating",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                (
                    "rating",
                    models.IntegerField(
                        validators=[
                            django.core.validators.MinValueValidator(1),
                            django.core.validators.MaxValueValidator(5),
                        ]
                    ),
                ),
                ("festival", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="zhackathon.festival")),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                "db_table": "rating",
                "unique_together": {("user", "festival")},
            },
        ),
    ]
