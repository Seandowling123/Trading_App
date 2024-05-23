from django.apps import AppConfig

class MyapiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'myapi'
    
    """def ready(self):
        
        # Start the algo trading task in a separate thread
        trading_algo_thread = threading.Thread(target=mean_reversion.run_trading_algorithm())
        trading_algo_thread.daemon = True
        trading_algo_thread.start()"""
        
 