import pandas as pd
from PIL import Image, ImageDraw, ImageFont
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
import os
import textwrap

SENDER_EMAIL = "varunclg5@gmail.com"         
SENDER_PASSWORD = "chdmsizigwwktyvv"         # <-- Replace with Gmail App Password
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
TEMPLATE_FILE = "certificate_template.png"    
FONT_PATH =  "arial.ttf"

FONT_SIZE = 60                                


os.makedirs("output", exist_ok=True)

df = pd.read_excel("students.xlsx")


def generate_certificate(name, roll, dept):
    
    template = Image.open(TEMPLATE_FILE)
    draw = ImageDraw.Draw(template)
    font = ImageFont.truetype(FONT_PATH, FONT_SIZE)

    text = f"This certificate is proudly presented to {name} bearing the roll no  {roll} of {dept} department in recognition of outstanding performance, dedication, and commitment in the hackathon event.."

    wrapped_text = textwrap.fill(text, width=50)   


    W, H = template.size  

    bbox = draw.multiline_textbbox((0, 0), wrapped_text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]


    x = (W - text_width) / 2
    y = (H - text_height) / 2  

    
    draw.multiline_text((x, y), wrapped_text, fill="black", font=font, align="center")

    file_path = f"output/{roll}.png"
    template.save(file_path)
    return file_path


def send_email(to_email, subject, body, attachment_path):
    msg = MIMEMultipart()
    msg["From"] = SENDER_EMAIL
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    
    with open(attachment_path, "rb") as attach_file:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attach_file.read())
    encoders.encode_base64(part)
    part.add_header("Content-Disposition", f"attachment; filename={os.path.basename(attachment_path)}")
    msg.attach(part)

    
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.send_message(msg)

# Main loop
for _, row in df.iterrows():
    cert_file = generate_certificate(row["Name"], row["Roll Number"], row["Department"])
    send_email(
        row["Email"],
        "Certificate of Participation",
        f"Dear {row['Name']},\n\nPlease find your certificate attached.\n\nBest regards,\nEvent Team",
        cert_file
    )
    print(f"Sent to {row['Name']} - {row['Email']}")
