import lambda_function
import telegram
import time


while 1:
    event = {
        'body': telegram.get_updates()
    }

    lambda_function.lambda_handler(event, None)
    time.sleep(5)
