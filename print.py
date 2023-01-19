from os import getenv

from brother_ql.backends.helpers import send
from brother_ql.conversion import convert
from brother_ql.raster import BrotherQLRaster
from PIL import Image, ImageDraw, ImageFont

backend = getenv('PRINTER_BACKEND')
model = getenv('PRINTER_MODEL')
printer = getenv('PRINTER_ADDRESS')

label_width = 696
label_height = 271
temp_file = "label-temp.png"


def break_fix(text, width, font, draw):
    if not text:
        return
    lo = 0
    hi = len(text)
    while lo < hi:
        mid = (lo + hi + 1) // 2
        t = text[:mid]
        # w, h = draw.textsize(t, font=font)
        # w, h = draw.textbbox(t, font=font)
        left, top, right, bottom = font.getbbox(t)
        w, h = right - left, bottom - top
        if w <= width:
            lo = mid
        else:
            hi = mid - 1
    t = text[:lo]
    # w, h = draw.textsize(t, font=font)
    left, top, right, bottom = font.getbbox(t)
    w, h = right - left, bottom - top
    yield t, w, h
    yield from break_fix(text[lo:], width, font, draw)


def fit_text(img, text, color, font, spacing, align, left, top):
    width = img.size[0] - 2
    draw = ImageDraw.Draw(img)
    pieces = list(break_fix(text, width, font, draw))
    height = sum(p[2] for p in pieces)
    if height > img.size[1]:
        raise ValueError("text doesn't fit")
    y = top  # (img.size[1] - height + top) // 2
    for t, w, h in pieces:
        x = left  # (img.size[0] - w) // 2
        draw.text((x, y), t, font=font, fill=color,
                  spacing=spacing, align=align)
        y += h


def print_label(label_line_1, label_line_2, order_id, label_id):
    image = Image.new('RGB', (label_width, label_height), color=(255, 255, 255))
    draw = ImageDraw.Draw(image)
    # specified font size
    font1 = ImageFont.truetype('fonts/RobotoCondensed-Regular.ttf', 65)
    font2 = ImageFont.truetype('fonts/RobotoCondensed-Regular.ttf', 40)
    font3 = ImageFont.truetype('fonts/RobotoCondensed-Regular.ttf', 30)

    fit_text(image, label_line_1, (0, 0, 0), font1, 40, 'left', 0, 0)
    fit_text(image, label_line_2, (0, 0, 0), font2, 40, 'left', 0, 220)
    fit_text(image, order_id, (0, 0, 0), font3, 30, 'right', 500, 220)
    image.save('labels/order-' + order_id + '-' + label_id + '' + temp_file)

    # exit()

    qlr = BrotherQLRaster(model)
    qlr.exception_on_warning = True

    instructions = convert(
        qlr=qlr,
        images=[image],  # Takes a list of file names or PIL objects.
        label='62x29',
        rotate='0',  # 'Auto', '0', '90', '270'
        threshold=90.0,  # Black and white threshold in percent.
        dither=False,
        compress=False,
        red=False,  # Only True if using Red/Black 62 mm label tape.
        dpi_600=False,
        hq=True,  # False for low quality.
        cut=False
    )

    try:
        result = send(instructions=instructions, printer_identifier=printer, backend_identifier=backend, blocking=True)
        return result['outcome']
    except Exception as error:
        return f"Error printer:[{error}]"




