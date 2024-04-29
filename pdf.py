from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle as PS
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.graphics.shapes import Line, Drawing
from reportlab.lib import colors
from io import BytesIO

styles = getSampleStyleSheet()
styles.add(PS(name='Times', fontName='Times', fontSize=9.5))
styles.add(PS(name='Times-Bold', fontName='Times-Bold', fontSize=9.5))

pdfmetrics.registerFont(TTFont('BCSans-Regular', 'BCSans-Regular.ttf'))
pdfmetrics.registerFont(TTFont('BCSans-Bold', 'BCSans-Bold.ttf'))
    
styles.add(PS(name='BCSans-Regular', fontName='BCSans-Regular', fontSize=9))
styles.add(PS(name='BCSans-Light', fontName='BCSans-Regular', fontSize=8, textColor=colors.grey))
styles.add(PS(name='BCSans-Bold', fontName='BCSans-Bold', fontSize=9))

normal_style = styles["BCSans-Regular"]
bold_style = styles["BCSans-Bold"]
light_style = styles["BCSans-Light"]

def footer(canvas, doc):
    width = 40*cm
    height = 1*cm
    canvas.saveState()
    d = Drawing(width,height)
    l = Line(460,0,0,0,
     strokeColor=colors.grey, strokeWidth=0.1)
    d.add(l)
    P = Paragraph("BC Public Service Agency&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Mailing Address: " + "<br></br>" + "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;PO Box 9110 Stn Prov Govt" + "<br></br>" + "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Victoria BC V8W 9B1", light_style)
    w, h = P.wrap(doc.width, doc.bottomMargin)
    d.drawOn(canvas, doc.leftMargin, h+45)
    P.drawOn(canvas, doc.leftMargin, h)
    canvas.restoreState()

def form(supervisor):

    buff = BytesIO()
    doc = SimpleDocTemplate(
        buff,
        pagesize=letter,
        leftMargin=2.54*cm, rightMargin=2.54*cm,
        topMargin=1*cm, bottomMargin=1*cm,
        fontSize=9.5,
    )

    flowables = []
    paraSpacer = Spacer(1, 0.5*cm)

    logo = Image("BC_public_service.jpg")
    logo.drawHeight = 2.39*cm
    logo.drawWidth = 7.99*cm
    logo.hAlign = 0

    flowables.append(logo)
    flowables.append(paraSpacer)

    flowables.append(Paragraph(supervisor['superName'], normal_style))
    if(supervisor['ministry'] != "Left Blank"):
        flowables.append(Paragraph(supervisor['ministry'], normal_style))

    fullAddress = supervisor['address']
    if(supervisor['street_address']):
        fullAddress = (
            f"{supervisor['street_address']} <br/> PO Box {supervisor['prefix']} Stn Prov Govt <br/>{supervisor['city_town']}, {supervisor['province']} {supervisor['postal']}")

    flowables.append(Paragraph(fullAddress, normal_style))
    flowables.append(paraSpacer)

    greeting = "Dear " + supervisor['superName'] + ", "

    flowables.append(Paragraph(greeting, normal_style))
    flowables.append(paraSpacer)

    publicServiceWeek = "June 9 to 15, 2024"

    corporatePlan = '<u><a color="blue" href="' + 'https://www2.gov.bc.ca/assets/gov/careers/about-the-bc-public-service/corporate-digital/corporateplan_2023.pdf' + \
        '">' + 'Corporate Plan' + '</a></u>'

    paragraphs = ["It’s time to celebrate your employees’ career milestones! Enclosed, you’ll find your employees’ service pin(s) and a list of which pin goes to which employees.", f"Public Service Week is {publicServiceWeek}.", f"This is a wonderful opportunity to thank your employees for their contributions and celebrate their commitment to the BC Public Service. Recognition initiatives such as the Service Pin program support the retention goal set out in the {corporatePlan} by providing a positive and rewarding employee experience. If you are unable to present the pins during Public Service Week, you are encouraged to save the presentation for a suitable date.", "Please consider the employee’s individual preferences and comfort level when presenting their service pin. If your employee doesn’t work in the same office as you, or works remotely, please mail the pin as soon as possible. Consider hosting a virtual presentation during a team meeting or connect with your employee directly to congratulate them.", "Personalized messages from supervisors and executives are encouraged and may be added to the card attached to the pins.", "The pin(s) in this package should be presented to: "]

    for index, item in enumerate(paragraphs):
        if index == 1:
            flowables.append(Paragraph(item, bold_style))
        else:
            flowables.append(Paragraph(item, normal_style))
        flowables.append(paraSpacer)

    pinsHeading = "<b>" + "Employee" + "</b>" + "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;" + "Milestone"
    flowables.append(Paragraph(pinsHeading, normal_style))
    flowables.append(Spacer(1, 0.2*cm))

    for eachStaff in supervisor['staff']:
        text = "<b>" + f'{eachStaff[0]}' + "</b>" + "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;" + f'{eachStaff[1]}' 
        line = Paragraph(text, bold_style)
        flowables.append(line)

    flowables.append(paraSpacer)

    webAddress = '<u><a color="blue" href="' + 'https://www.dcv.gov.bc.ca/Product/Listing/4251_Flags-and-Pins' + \
        '">' + 'Distribution Centre Victoria' + '</a></u>'

    important = "Important"
    conclusion = f"Only employees who registered themselves or were registered by you or a ministry representative are included in this package. If you have an employee who is eligible and did not register, you can order additional service pins (at your organization’s cost) any time from the {webAddress}."

    flowables.append(Paragraph(important, bold_style))
    flowables.append(paraSpacer)
    flowables.append(Paragraph(conclusion, normal_style))
    flowables.append(paraSpacer)

    emailAddress = '<u><a color="blue" href="' + 'mailto:Corporate.Engagement@gov.bc.ca' + \
        '">' + 'Corporate.Engagement@gov.bc.ca' + '</a></u>'

    recognitionContact = '<u><a color="blue" href="' + 'https://compass.gww.gov.bc.ca/ministry-recognition-contacts/' + \
        '">' + 'organization’s recognition contact' + '</a></u>'

    questions = [f"If you have questions about service pins, please connect with your {recognitionContact}.",
                 "Thank you for taking the time to celebrate your employees!",
                 "Corporate Engagement, BC Public Service Agency" + "<br/>" + emailAddress
                ]

    for each in questions:
        flowables.append(Paragraph(each, normal_style))
        flowables.append(paraSpacer)

    doc.build(flowables, onFirstPage=footer)

    pdf = buff.getvalue()
    buff.close()
    return pdf