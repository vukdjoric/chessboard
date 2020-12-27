from pathlib import Path
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw


def annotate_chessboard():
    in_file = Path(__file__).parent.joinpath('images').joinpath('chessboard.png')
    out_file = Path(__file__).parent.joinpath('images').joinpath('chessboard_annotated.png')

    chessboard = Image.open(in_file)
    draw = ImageDraw.Draw(chessboard)
    font = ImageFont.truetype("Helvetica.ttc", 35)

    # annotate rows '1-8'
    for row in range(8):
        square = (10, row * round(chessboard.height / 8) + 10)
        color = chessboard.getpixel(1 * (round(chessboard.height / 8), row * round(chessboard.height / 8)))
        draw.text(square, str(8 - row), fill=color, font=font)

    # annotate columns 'a-h'
    for col in range(8):
        square = (col * round(chessboard.width / 8) + 125, 7 * round(chessboard.height / 8) + 115)
        color = chessboard.getpixel((col * round(chessboard.width / 8), 6 * round(chessboard.height / 8)))
        draw.text(square, chr(97 + col), fill=color, font=font)

    chessboard.show()
    chessboard.save(out_file, format='PNG')
