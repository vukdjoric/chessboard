import re
import telegram
import engine


def lambda_handler(event, context):
    update = telegram.parse(event['body'])

    if not update:
        print('Not a valid update')
        return

    if 'command' in update:
        if update['command'] == '/game':
            # Render initial position
            img_byte = engine.render()
            # Send initial position
            telegram.send_board(update['chat_id'], img_byte.getvalue())
        return

    # Parse move
    move = update['move'].lstrip()
    regular_move = re.search("^(\s*)([a-h]|[A-H])[1-8] ((([a-h]|[A-H])[1-8])|(-|k|q|b|n|r|p|K|Q|B|N|R|P))($|\s)", move)
    if regular_move is None:
        return

    # In-memory binary stream
    img_bytes = telegram.get_image(update['file_id'])

    # Decode state
    notation = engine.image_to_notation(img_bytes)
    state = engine.notation_to_state(notation)

    print(f'Received position: {notation}')

    # Update state
    change = engine.update(state, update['move'])
    if not change:
        return

    # Render position
    img_bytes = engine.render(state)

    notation = engine.state_to_notation(state)
    print(f'Updated position: {notation}')

    # Send position
    telegram.update_board(update['chat_id'], update['message_id'], img_bytes.getvalue())
