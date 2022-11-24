import uuid

from django.contrib.auth.models import User
from django.core import validators
from django.db import models
from django.db.models.query import QuerySet


class Festival(models.Model):
    id = models.CharField(max_length=20, primary_key=True, editable=False)
    name = models.CharField(max_length=100)
    discipline = models.CharField(max_length=200)
    description = models.TextField(max_length=500, blank=True, null=True)
    website = models.URLField(null=True, blank=True)
    period = models.CharField(max_length=100, null=True, blank=True)
    region = models.CharField(max_length=100, null=True, blank=True)
    department = models.CharField(max_length=100, null=True, blank=True)
    commune = models.CharField(max_length=100, null=True, blank=True)
    postcode = models.CharField(
        max_length=5, null=True, blank=True, validators=[validators.RegexValidator("^[0-9]{5}$")]
    )

    ratings: QuerySet["Rating"]
    comments: QuerySet["Comment"]
    ticketings: QuerySet["Ticketing"]

    class Meta:
        db_table = "festival"

    def get_average_rating(self):
        return self.ratings.aggregate(models.Avg("rating"))["rating__avg"] or None

    def get_comments(self):
        comments = self.comments.all()
        comments.order_by("-created_at")
        return comments


class Ticketing(models.Model):
    class Status(models.TextChoices):
        OPEN = "OPEN"
        CLOSED = "CLOSED"
        LAST_PLACES = "LAST PLACES"

    name = models.CharField(primary_key=True, max_length=100)
    festival = models.ForeignKey(Festival, on_delete=models.CASCADE, related_name="ticketings")
    total_tickets = models.PositiveIntegerField(editable=False)
    available_tickets = models.PositiveIntegerField()
    status = models.CharField(max_length=25, choices=Status.choices, default=Status.OPEN)
    opened_at = models.DateTimeField(auto_now_add=True, editable=False)

    class Meta:
        db_table = "ticketing"

    def open(self):
        self.status = self.Status.OPEN
        self.save()

    def close(self):
        self.status = self.Status.CLOSED
        self.save()

    def is_open(self):
        return self.status != self.Status.CLOSED

    # def book_if_open(self): # TODO déplacer dans la logique
    #     if self.is_open():
    #         self.available_tickets -= 1
    #         if self.available_tickets == 0:
    #             self.status = self.Status.CLOSED
    #         self.save()

    def save(self, *args, **kwargs):
        if not self.available_tickets:
            self.available_tickets = self.total_tickets
        super().save(*args, **kwargs)


class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    festival = models.ForeignKey(Festival, on_delete=models.CASCADE, related_name="comments")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    content = models.TextField(max_length=255)
    liked_by = models.ManyToManyField(User, related_name="comments_liked", blank=True)

    class Meta:
        ordering = ["-created_at"]
        db_table = "comment"

    def get_total_likes(self):
        return self.liked_by.count()

    def like(self, user):
        self.liked_by.add(user)
        self.save()

    def unlike(self, user):
        self.liked_by.remove(user)
        self.save()


class Rating(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    festival = models.ForeignKey(Festival, on_delete=models.CASCADE, related_name="ratings")
    rating = models.IntegerField(validators=[validators.MinValueValidator(0), validators.MaxValueValidator(5)])

    class Meta:
        db_table = "rating"
        unique_together = ("user", "festival")
