import io
import pandas as pd
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A5, landscape
from reportlab.pdfbase.pdfmetrics import stringWidth
from pypdf import PdfWriter, PdfReader
from reportlab.rl_config import defaultPageSize
from tqdm import tqdm


# root = "/Users/samisaade/dev/Invites/InvitationTemplate"
save_path = "reserved"


guestlist = pd.read_csv("example.csv")
names = guestlist['Name']

with tqdm(total=len(names)) as pb:
    for name in names:
        # create a new PDF with Reportlab
        size = 35
        packet = io.BytesIO()
        width, height = landscape(A5)
        can = canvas.Canvas(packet, pagesize=landscape(A5))
        can.setFont("Times-Roman", size)
        text_width = stringWidth(name,fontName="Times-Roman",fontSize=size)
        can.drawString(width/2-text_width/2, height/2, name)
        can.save()

        #move to the beginning of the StringIO buffer
        packet.seek(0)

        pdf_content = packet.getvalue()

        # finally, write "output" to a real file
        with open(f"{save_path}/{name}_reserved.pdf", "wb") as f:
            f.write(pdf_content)
        pb.update(1)
        

