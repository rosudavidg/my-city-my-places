import smtplib
import os
from get_docker_secret import get_docker_secret


def send_activation_link(to_email, token):
    gmail_user = get_docker_secret(os.environ['EMAIL_ADDRESS'])
    sent_from = 'My City - My Places'
    gmail_password = get_docker_secret(os.environ['EMAIL_PASSWORD'])
    base_url = os.environ['BASE_URL']

    to = [to_email]
    subject = 'My City - My Places Activation link'
    body = """\
    Hello and thanks for registration!\n
    Here is your activation link:\n
    %s\n\n
    """ % (f'http://localhost:3000/activate/' + token)

    email_text = '\r\n'.join(['To: %s' % ','.join(to),
                              'From: %s' % sent_from,
                              'Subject: %s' % subject,
                              '', body])

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(gmail_user, gmail_password)
        server.sendmail(sent_from, to, email_text)
        server.close()
    except:
        raise Exception("Sending activation link via email failed.")


def send_family_invitation_link(to_email, token):
    gmail_user = get_docker_secret(os.environ['EMAIL_ADDRESS'])
    sent_from = 'My City - My Places'
    gmail_password = get_docker_secret(os.environ['EMAIL_PASSWORD'])

    to = [to_email]
    subject = 'My City - My Places Family Invitation'
    body = """\
    Click to join:\n
    %s\n\n
    """ % (f'http://localhost:3000/families/join/' + token)

    email_text = '\r\n'.join(['To: %s' % ','.join(to),
                              'From: %s' % sent_from,
                              'Subject: %s' % subject,
                              '', body])

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(gmail_user, gmail_password)
        server.sendmail(sent_from, to, email_text)
        server.close()
    except:
        raise Exception("Sending activation link via email failed.")


def send_export_link(to_email, export_id):
    gmail_user = get_docker_secret(os.environ['EMAIL_ADDRESS'])
    sent_from = 'My City - My Places'
    gmail_password = get_docker_secret(os.environ['EMAIL_PASSWORD'])

    to = [to_email]
    subject = 'My City - My Places Export '
    body = """\
    Click to import:\n
    %s\n\n
    """ % (f'http://localhost:3000/exports/{export_id}')

    email_text = '\r\n'.join(['To: %s' % ','.join(to),
                              'From: %s' % sent_from,
                              'Subject: %s' % subject,
                              '', body])

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(gmail_user, gmail_password)
        server.sendmail(sent_from, to, email_text)
        server.close()
    except:
        raise Exception("Sending activation link via email failed.")
