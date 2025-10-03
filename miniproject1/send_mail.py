import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(sender_email, sender_password, receiver_email, subject, body):
    
    try:
        # Set up the MIME structure
        message = MIMEMultipart()
        message['From'] = sender_email
        message['To'] = receiver_email
        message['Subject'] = subject
        message.attach(MIMEText(body, 'plain'))

        # Connect to the server and send email
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()  # Secure the connection
            server.login(sender_email, sender_password)
            server.send_message(message)

        print("Email sent successfully.")
    except Exception as e:
        print(f"Failed to send email: {e}")

# Usage
send_email(
    sender_email="varunreddyvvr@gmail.com",
    receiver_email="varunreddyphysics@gmail.com",
    subject="congralutions",
    body="hi friwnds this is varun",
    sender_password="yyag vghx plxn ylym"
)
