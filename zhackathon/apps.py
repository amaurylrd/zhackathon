import os

from django.apps import AppConfig


class ZhackathonConfig(AppConfig):
    name = os.path.realpath(__name__).split(os.sep)[-2]
