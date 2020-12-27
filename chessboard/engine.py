from io import BytesIO
from PIL import Image
from pathlib import Path


_PIECE_TO_IMAGE = {
    'k': 'black_king.png',
    'q': 'black_queen.png',
    'b': 'black_bishop.png',
    'n': 'black_knight.png',
    'r': 'black_rook.png',
    'p': 'black_pawn.png',
    'K': 'white_king.png',
    'Q': 'white_queen.png',
    'B': 'white_bishop.png',
    'N': 'white_knight.png',
    'R': 'white_rook.png',
    'P': 'white_pawn.png'
}

_INIT_STATE = [["r", "n", "b", "q", "k", "b", "n", "r"],
               ["p", "p", "p", "p", "p", "p", "p", "p"],
               ["-", "-", "-", "-", "-", "-", "-", "-"],
               ["-", "-", "-", "-", "-", "-", "-", "-"],
               ["-", "-", "-", "-", "-", "-", "-", "-"],
               ["-", "-", "-", "-", "-", "-", "-", "-"],
               ["P", "P", "P", "P", "P", "P", "P", "P"],
               ["R", "N", "B", "Q", "K", "B", "N", "R"]]

_OFFSET = -50


def render(state=_INIT_STATE):
    """
    :param state: <class 'list'>
    :return: <class '_io.BytesIO'>
    """
    chessboard = Image.open(Path(__file__).parent.joinpath('images').joinpath('chessboard_annotated.png'))

    for row in range(8):
        for col in range(8):
            # Render a piece if the square is occupied
            if state[row][col] != "-":
                square = (col * round(chessboard.width / 8), row * round(chessboard.height / 8))
                piece = Image.open(Path(__file__).parent.joinpath('images').joinpath(_PIECE_TO_IMAGE[state[row][col]]))
                piece = piece.resize((150, 150))
                chessboard.paste(piece, square, piece)

    img_byte = BytesIO()
    chessboard.save(img_byte, format='PNG')

    # encode position
    notation = state_to_notation(state)
    img_byte = notation_to_image(notation, img_byte)

    return img_byte


def update(state, move):
    """
    Updates the state
    :param state: <class 'list'> List (8x8)
    :param move: <class 'str'>  Move/add/remove a piece
     Move a piece from one square to another: "d2 d4"
     Add a piece to the square: "d8 Q"
     Remove a piece from the square: "d8 -"
    :return: <class 'bool'> Returns True if the state has been changed otherwise returns False
    """
    old_square = move.split(' ')[0]

    # Transform into coordinates: "d2" -> [3][2]
    old_square_cord = [0, 0]
    old_square_cord[0] = ord(old_square[0].lower()) - 97
    old_square_cord[1] = 7 - (int(old_square[1]) - 1)

    command = move.split(' ')[1]

    if len(command) == 1:
        # Remove a piece from the square
        if command == '-':
            state[old_square_cord[1]][old_square_cord[0]] = "-"
            return True
        # Add a piece to the square
        elif command in ('k', 'q', 'b', 'n', 'r', 'p', 'K', 'Q', 'B', 'N', 'R', 'P'):
            state[old_square_cord[1]][old_square_cord[0]] = command
            return True
        return False
    elif len(command) == 2:
        new_square = command

        # Transform into coordinates: "d4" -> [3][3]
        new_square_cord = [0, 0]
        new_square_cord[0] = ord(new_square[0].lower()) - 97
        new_square_cord[1] = 7 - (int(new_square[1]) - 1)

        # Return if there is nothing to move
        if state[old_square_cord[1]][old_square_cord[0]] == "-":
            return False

        # Return if squares are the same
        if old_square_cord[1] == new_square_cord[1] and old_square_cord[0] == new_square_cord[0]:
            return False

        # Move the piece to a new square
        state[new_square_cord[1]][new_square_cord[0]] = state[old_square_cord[1]][old_square_cord[0]]
        state[old_square_cord[1]][old_square_cord[0]] = "-"
        return True

    return False


def state_to_notation(state):
    """
    Encodes state to notation
    :param state: <class 'list'> List (8x8): [['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'], ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'], ...]
    :return: <class 'str'>  String: "rnbqkbnr/pppppppp/--------/--------/--------/--------/PPPPPPPP/RNBQKBNR"
    """
    notation = '/'.join([''.join(row) for row in state])
    return notation


def notation_to_image(notation, img_byte):
    """
    Encodes notation to image
    :param notation: <class 'str'> String: "rnbqkbnr/pppppppp/--------/--------/--------/--------/PPPPPPPP/RNBQKBNR"
    :param img_byte: <class '_io.BytesIO'>
    :return: <class '_io.BytesIO'>
    """
    image = Image.open(img_byte)

    # chars to bits
    bits = [format(ord(char), '08b') for char in notation]
    bits = list(''.join(bits))

    # bits to pixels
    encoding = [(int(bits[i]) * _OFFSET, int(bits[i]) * _OFFSET, int(bits[i]) * _OFFSET) for i in range(0, len(bits))]

    pixels = image.load()
    for i in range(0, len(encoding)):
        # change pixel color value
        pixels[i, 0] = (pixels[i, 0][0] + encoding[i][0], pixels[i, 0][1] + encoding[i][1], pixels[i, 0][2] + encoding[i][2])

    img_byte = BytesIO()
    image.save(img_byte, format='PNG')

    return img_byte


def image_to_notation(img_byte):
    """
    Decodes notation from image
    :param img_byte: <class '_io.BytesIO'>
    :return: <class 'str'> String: "rnbqkbnr/pppppppp/--------/--------/--------/--------/PPPPPPPP/RNBQKBNR"
    """
    image = Image.open(img_byte)
    ref_im = Image.open(Path(__file__).parent.joinpath('images').joinpath('chessboard.png'))

    # ref_pixels to ref_values
    ref_pixels = [ref_im.getpixel((i, 0)) for i in range(0, 568)]

    # pixels to bits
    pixels = [image.getpixel((i, 0)) for i in range(0, 568)]
    bits = [round((sum(pixels[i]) - (sum(ref_pixels[i]) + _OFFSET * 3)) / (-_OFFSET * 3)) for i in range(0, len(pixels))]
    bits = [str(-(bit - 1)) for bit in bits]

    # bits to chars
    chars = [''.join(bits[i:i + 8]) for i in range(0, 568, 8)]
    chars = [chr(int(i, 2)) for i in chars]
    notation = ''.join(chars)

    return notation


def notation_to_state(notation):
    """
    Decodes state from notation
    :param notation: <class 'str'> String: "rnbqkbnr/pppppppp/--------/--------/--------/--------/PPPPPPPP/RNBQKBNR"
    :return: <class 'list'> List (8x8): [['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'], ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'], ...]
    """
    state = [list(row) for row in notation.split('/')]
    return state
