import base64
import qrcode
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from simulator.settings import HOST

'''
returns a string of a base 64 embedded image of a qr code representing
the passed token. This is so the qr code can be displayed in html. 
'''
def qr_b64(token):
    qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=5,
            border=4,
        )
    qr.add_data(token)
    qr.make(fit=True)
    im = qr.make_image(fill_color="black", back_color="white")

    with io.BytesIO() as output:
        im.save(output, format="PNG")
        contents = output.getvalue()

    encoded_string = str(base64.b64encode(contents))
    return encoded_string[2:-3]

def group_pdf(name, profiles):
    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer)
    for x, profile in enumerate(profiles):
        h = x % 2
        v = int((x % 10) / 2)

        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=3,
            border=4,
        )
        qr.add_data(f'{HOST}/register/{profile.qr_token}')
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        h_inch = inch + 3.5 * inch * h
        v_inch = 1.2*inch + (2 * inch * v)
        pdf.drawInlineImage(img, h_inch,v_inch)

        text = pdf.beginText()
        text.setTextOrigin(h_inch + 25, v_inch)
        text.textLine(text=profile.display_name)
        pdf.drawText(text)

        if (x + 1) % 10 == 0:
            pdf.showPage()

    pdf.save()
    buffer.seek(0)
    return buffer
