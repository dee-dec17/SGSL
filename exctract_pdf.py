import requests # type: ignore
import os
import smtplib
from email.message import EmailMessage

# ✅ Step 1: List of PDF URLs
pdf_urls = [
    "https://www.srigayatrishipping.com/assets/img/ProfileSGSL.pdf",
    "https://www.srigayatrishipping.com/assets/img/Flyer.jpg"
]

# ✅ Step 2: Create a folder for PDFs
download_folder = "pdfs"
os.makedirs(download_folder, exist_ok=True)

pdf_files = []
for url in pdf_urls:
    pdf_name = os.path.join(download_folder, url.split("/")[-1])
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        with open(pdf_name, "wb") as f:
            f.write(response.content)
        pdf_files.append(pdf_name)
        print(f"✅ Downloaded: {pdf_name}")
    except Exception as e:
        print(f"❌ Failed to download {url}: {e}")

# ✅ Step 3: Send Email using SendGrid
import sendgrid # type: ignore
from sendgrid.helpers.mail import Mail, Attachment, FileContent, FileName, FileType # type: ignore

SENDGRID_API_KEY = "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"  # Replace with your API key - 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
SENDER_EMAIL = "developer.sgsl.auto@gmail.com"  # Replace with verified SendGrid email
RECEIVER_EMAIL = ["deekshitha.kolusu@gmail.com", "anudeep833@gmail.com"]

sg = sendgrid.SendGridAPIClient(SENDGRID_API_KEY)
message = Mail(
    from_email=SENDER_EMAIL,
    to_emails=RECEIVER_EMAIL,
    subject="📎 PDF Attachments",
    html_content="<p>Hi,<br><br>Please find the attached PDFs.<br><br>Best,<br>Your Script</p>"
)

# ✅ Attach PDFs
import base64

for pdf in pdf_files:
    with open(pdf, "rb") as f:
        file_data = f.read()
        encoded_file = base64.b64encode(file_data).decode()  # 🔹 Fixed encoding
        attachment = Attachment(
            FileContent(encoded_file),
            FileName(os.path.basename(pdf)),
            FileType("application/pdf")
        )
        message.attachment = attachment

try:
    response = sg.send(message)
    print("✅ Email sent successfully!")
except Exception as e:
    print(f"❌ Error sending email: {e}")
