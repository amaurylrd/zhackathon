import os

from django.apps import AppConfig


class ZhackathonConfig(AppConfig):
    name = os.path.realpath(__file__).split(os.sep)[-2]
