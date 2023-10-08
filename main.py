import smtplib
import imaplib
import email
import re
from email.mime.text import MIMEText
import time

# Email account configuration
EMAIL_ADDRESS = 'examplemail@gmail.com'  # Your email address
APP_PASSWORD = ''      # Your app password

# Predefined response
KEYWORD = 'python'
RESPONSE_SUBJECT = 'Re: Your Subject'
RESPONSE_BODY = "Here's how to learn Python: https://www.python.org/doc/"

# Function to send an email
def send_email(recipient, subject, body):
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(EMAIL_ADDRESS, APP_PASSWORD)

        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = recipient

        server.sendmail(EMAIL_ADDRESS, recipient, msg.as_string())
        server.quit()
        print(f"Autoresponse sent to {recipient}")
    except Exception as e:
        print(f"Error sending autoresponse: {e}")

# Function to check and respond to emails
def check_and_respond():
    try:
        mail = imaplib.IMAP4_SSL('imap.gmail.com')
        mail.login(EMAIL_ADDRESS, APP_PASSWORD)
        mail.select("inbox")

        result, data = mail.uid("search", None, "UNSEEN")
        email_uids = data[0].split()

        for uid in email_uids:
            result, message_data = mail.uid("fetch", uid, "(RFC822)")
            raw_email = message_data[0][1]
            email_message = email.message_from_bytes(raw_email)

            subject = email_message["Subject"]
            sender = email_message["From"]

            # Get the email's payload and join it into a single string
            body = ""
            for part in email_message.walk():
                if part.get_content_type() == "text/plain":
                    body += part.get_payload(decode=True).decode("utf-8", "ignore")

            if subject == RESPONSE_SUBJECT:
                continue  # Don't respond to your own autoresponse

            # Use a regular expression to find the keyword in the email body
            if re.search(r'\b{}\b'.format(re.escape(KEYWORD)), body, re.IGNORECASE):
                send_email(sender, RESPONSE_SUBJECT, RESPONSE_BODY)
    except Exception as e:
        print(f"Error checking and responding to emails: {e}")

if __name__ == "__main__":
    print("Autoresponder bot is running...")
    while True:
        check_and_respond()
        print("Waiting for the next check...")
        time.sleep(60)  # 1m timer
