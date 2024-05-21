from apscheduler.schedulers.background import BackgroundScheduler
import time
from get_financial_data import get_close_prices
from execute_orders import buy, sell, get_order_status, get_prev_orders

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

id = '123test'
 
order_id = buy('SPY', 1)
print(order_id)

sts = get_order_status(order_id)
print(sts)
