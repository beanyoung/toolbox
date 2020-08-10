from email.message import EmailMessage
import smtplib

from flask import (
    Blueprint,
    request,
)

from toolbox import (
    utils,
    exceptions,
)

import config


mail = Blueprint('mail', __name__)


def send_email(to, subject=None, text=None, html=None):
    message = EmailMessage()
    message['From'] = config.smtp_username
    message['To'] = to

    if subject is None:
        subject = ''
    message['Subject'] = subject

    if text is not None:
        message.set_content(text)
    elif html is not None:
        message.set_content(html, subtype='html')

    with smtplib.SMTP(config.smtp_host, config.smtp_port) as s:
        s.starttls()
        s.login(config.smtp_username, config.smtp_password)
        s.send_message(message)


@mail.route('/send', methods=['POST'])
@utils.rest
def send():
    request_json = request.get_json(silent=True)
    if not request_json:
        raise exceptions.BadRequest('request json is invalid')

    try:
        send_email(
            request_json['to'],
            request_json.get('subject'),
            request_json.get('text'),
            request_json.get('html'),
        )
    except smtplib.SMTPException as e:
        raise exceptions.UnknownError(e)

    return dict(status='ok')
