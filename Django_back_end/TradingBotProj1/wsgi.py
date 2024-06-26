"""
WSGI config for TradingBotProj1 project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os
import threading
from myapi.finance_tools import mean_reversion

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TradingBotProj1.settings')

application = get_wsgi_application()

# Start the algo trading task in a separate thread
trading_algo_thread = threading.Thread(target=mean_reversion.run_trading_algorithm)
trading_algo_thread.daemon = True
trading_algo_thread.start()
