from email.message import EmailMessage
import smtplib

from bottle import (
    Bottle,
    HTTPError,
    abort,
    request,
)


app = Bottle()


def send_email(to, subject=None, text=None, html=None):
    message = EmailMessage()
    message['From'] = app.config['smtp_username']
    message['To'] = to

    if subject is None:
        subject = ''
    message['Subject'] = subject

    if text is not None:
        message.set_content(text)
    elif html is not None:
        message.set_content(html, subtype='html')

    with smtplib.SMTP(app.config['smtp_host'], app.config['smtp_port']) as s:
        s.starttls()
        s.login(app.config['smtp_username'], app.config['smtp_password'])
        s.send_message(message)


@app.route('/mail/send', method='POST')
def send():
    if not request.json:
        abort(400, 'request is null')

    if not request.json['to']:
        abort(400, 'missing `to`')

    try:
        send_email(
            request.json['to'],
            request.json.get('subject'),
            request.json.get('text'),
            request.json.get('html'),
        )
    except smtplib.SMTPException as e:
        abort(400, e)

    return dict(status='ok')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
