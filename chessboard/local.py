import chessboard
import telegram
import json

"""

Run the engine locally to process a single event

"""

event = {
    'body': json.dumps(telegram.get_updates())
}

chessboard.lambda_handler(event, None)
