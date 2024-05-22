from django.apps import AppConfig

class MyapiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'myapi'
    
    """def ready(self):
        # Import your function here and call it
        from .finance_tools import mean_reversion
        mean_reversion.run_trading_algorithm()"""
 