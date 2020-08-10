from flask import Flask

from toolbox.mail import mail


app = Flask(__name__)
app.register_blueprint(mail, url_prefix='/mail')


if __name__ == '__main__':
    app.run()
