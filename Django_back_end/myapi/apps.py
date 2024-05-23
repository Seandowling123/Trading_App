from django.apps import AppConfig
import threading
from .finance_tools import mean_reversion

class MyapiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'myapi'
    
    def ready(self):
        
        # Start the algo trading task in a separate thread
        trading_algo_thread = threading.Thread(target=mean_reversion.run_trading_algorithm())
        trading_algo_thread.daemon = True
        trading_algo_thread.start()
        
 