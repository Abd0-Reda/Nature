from django.apps import AppConfig
from django.apps import AppConfig


class Config(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'shop'


class CartConfig(AppConfig):  
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'cart' 

    def ready(self):
        import cart.signals  
