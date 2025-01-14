from django.apps import AppConfig
import os


class AppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app'
    verbose_name = '网站管理'
    path = os.path.dirname(os.path.abspath(__file__)) 