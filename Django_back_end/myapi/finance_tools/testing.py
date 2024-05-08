from apscheduler.schedulers.background import BackgroundScheduler
import time
from get_financial_data import get_close_prices
import threading

def my_function():
    print(get_close_prices('SPY'))
    print("Executing my function at 1 second past the minute")

def schedule():
    # Create a scheduler
    scheduler = BackgroundScheduler()

    # Add the job to execute my_function at 1 second past each minute
    scheduler.add_job(my_function, 'cron', second='1')

    # Start the scheduler
    scheduler.start()

    # Keep the program running
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopping the scheduler")
        scheduler.shutdown()

schedule()

"""# Check order status
order_status = order.status
if order_status == 'filled':
    print("Order has been executed successfully.")
    print(f"Average filled price: {order.filled_avg_price}")
else:
    print("Order is still pending or partially filled.")"""
