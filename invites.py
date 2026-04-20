import io
import pandas as pd
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase.pdfmetrics import stringWidth
from pypdf import PdfWriter, PdfReader
from reportlab.rl_config import defaultPageSize
from tqdm import tqdm


root = "InvitationTemplate"
save_path = "guest_invites"


guestlist = pd.read_csv("example.csv")
names = guestlist['Guest']

with tqdm(total=len(names)) as pb:
    for name in names:
        # read your existing PDF
        existing_pdf = PdfReader(open(f"{root}/Template.pdf", "rb"))
        output = PdfWriter()
        page = existing_pdf.pages[0]
        width = page.mediabox.width
        height = page.mediabox.height

        print(f"width: {width} - hieght {height}")
        width = 842
        height = 596

        # create a new PDF with Reportlab
        packet = io.BytesIO()
        can = canvas.Canvas(packet, pagesize=[width,height])
        can.setFont("Times-Roman", 18)
        text_width = stringWidth(name,fontName="Times-Roman",fontSize=18)
        can.drawString(width/2-text_width/2, height/2, name)
        can.save()

        new_pdf = PdfReader(packet)

        #move to the beginning of the StringIO buffer
        packet.seek(0)

        # add the "watermark" (which is the new pdf) on the existing page
        page.merge_page(new_pdf.pages[0])
        output.add_page(page)

        # finally, write "output" to a real file
        output_stream = open(f"{save_path}/{name}_Official Invite.pdf", "wb")
        output.write(output_stream)
        output_stream.close()
        pb.update(1)
        

