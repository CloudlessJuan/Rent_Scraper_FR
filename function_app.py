import logging
from scraper import fetch_and_upload_city_data
import azure.functions as func

app = func.FunctionApp()

@app.schedule(schedule="0 0 11 * * 1", arg_name="myTimer", run_on_startup=False,
              use_monitor=False) 
def timer_trigger(myTimer: func.TimerRequest) -> None:
    if myTimer.past_due:
        logging.info('The timer is past due!')

    fetch_and_upload_city_data()
    logging.info('Python timer trigger function executed.')