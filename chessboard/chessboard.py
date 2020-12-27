import re
import json
import engine
import telegram


# Simultaneous edits on the same state will cancel each other
# How do you process simultaneous state changes

def parse(event):
    try:
        event = json.loads(event['body'])
        if event['message']['text'].startswith('/'):
            return {
                "command": event['message']['text'].split('@')[0],
                "chat_id": event['message']['chat']['id']
            }
        return {
            "move": event['message']['text'],
            "message_id": event['message']['reply_to_message']['message_id'],
            "file_id": event['message']['reply_to_message']['photo'][-1]['file_id'],
            "chat_id": event['message']['chat']['id']
        }
    except (ValueError, LookupError):
        return {}


def lambda_handler(event, context):
    event = parse(event)

    if not event:
        print('Not a valid event')
        return {
            "statusCode": 200
        }

    if 'command' in event:
        if event['command'] == '/game':

            # Render initial position
            img_byte = engine.render()

            # Send initial position
            telegram.send_file(event['chat_id'], img_byte.getvalue())
        return {
            "statusCode": 200
        }

    # Parse move
    move = event['move'].lstrip()
    regular_move = re.search("^([a-h]|[A-H])[1-8] ((([a-h]|[A-H])[1-8])|(-|k|q|b|n|r|p|K|Q|B|N|R|P))($|\s)", move)
    if not regular_move:
        print(f'Not a regular move: \'{move}\'')
        return {
            "statusCode": 200
        }

    # In-memory binary stream
    img_bytes = telegram.download_file(event['file_id'])

    # Decode state
    notation = engine.image_to_notation(img_bytes)
    state = engine.notation_to_state(notation)

    print(f'Received position: {notation}')

    # Update state
    change = engine.update(state, event['move'])
    if not change:
        print('No change in a position')
        return {
            "statusCode": 200
        }

    # Render position
    img_bytes = engine.render(state)

    notation = engine.state_to_notation(state)
    print(f'Updated position: {notation}')

    # Send position
    telegram.edit_file(event['chat_id'], event['message_id'], img_bytes.getvalue())

    return {
        "statusCode": 200
    }

