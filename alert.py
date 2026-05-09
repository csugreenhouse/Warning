import smtplib
from email.message import EmailMessage
import time
import ssl

# to install email package, run pip install secure-smtplib

smtp_server = "smtp.gmail.com"
port = 465  
sender_email = "csugreenhouse@gmail.com"  
app_password = "ssrl ohkt qvjt huhe" 

# to send image in email, use this code:
# msg = EmailMessage()
# msg['Subject'] = 'Subject of the email'
# msg['From'] = sender_email
# msg['To'] = recipients
# msg.set_content('This is the body of the email')
# with open('image.jpg', 'rb') as img:
#     img_data = img.read()
#     msg.add_attachment(img_data, maintype='image', subtype='jpeg', filename='image.jpg')

def send_email(subject, body, recipients, images=None):
    # how to create a body that looks good in an email? 

    context = ssl.create_default_context()

    # Create the email message
    msg = EmailMessage()
    msg.set_content(body)
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = recipients

    try:
        # Connect to the server and send the email
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(sender_email, app_password)
            for image in images or []:
                with open(image, 'rb') as img:
                    img_data = img.read()
                    msg.add_attachment(img_data, maintype='image', subtype='jpeg', filename=image)
            msg.add_attachment
            server.send_message(msg)
        print("Email sent successfully!")

    except Exception as e:
        print(f"An error occurred: {e}")

