from scrapy.mail import MailSender


class email:
    def __init__(self):
        print("db", "check create_mail_server")
        self.owner_email = ["owner email address"]
        self.create_mail_server()
        pass

    def create_mail_server(self):
        self.mailer = MailSender(mailfrom="sender email ",
                                 smtphost="host server", smtpport=1)

    def send_email(self, to, cc, subject, html_body):
        self.mailer.send(to=to, subject=subject,
                         body=html_body, mimetype="text/html")

    def send_error_email(self, html_body):
        self.mailer.send(to=self.owner_email, subject="Subject",
                         body=html_body, mimetype="text/html")
