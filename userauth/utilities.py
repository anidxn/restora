import datetime
import os

# ----------- for sending emails ------------
from django.core.mail import send_mail
# import settings.py module
from django.conf import settings 

# prepend current datetime before filename
def get_file_path(request, filename):
    filename_original = filename
    nowTime = datetime.datetime.now().strftime('%Y%m%d%H:%M:%S')
    filename = "%s_%s" % (nowTime, filename_original)
    return os.path.join('images/', filename)

def send_demo_email_to_client():
    subject = 'Test email'
    message = 'This is a test email from django'
    email_from  = settings.EMAIL_HOST_USER
    recipient_list = ['pj.cstech@gmail.com'] # list of recipients
    send_mail(subject, message, email_from, recipient_list)


def send_custom_email(subj, msg, recipient):
    email_from  = settings.EMAIL_HOST_USER
    to_list = [recipient]
    send_mail(subj, msg, email_from, to_list, fail_silently= True)


