from email.mime.text import MIMEText
from StringIO import StringIO
import smtplib

import weechat

weechat.register("emailme", "asadoughi", "0.0.1", "GPL", "Send e-mail "
                 "based on private messages and highlights.", "", "")
weechat.hook_print("", "irc_privmsg", "", 1, "notify_show", "")

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER = "email@gmail.com"
PASSWORD = "password"
RECIPIENTS = ["recipient@gmail.com"]


class EmailNotifier(object):
    def __init__(self, server, port, sender, password):
        self.smtp_server = server
        self.smtp_port = port
        self.sender = sender
        self.password = password

    def notify(self, recipients, subject, body=""):
        session = smtplib.SMTP(self.smtp_server, self.smtp_port)
        session.ehlo()
        session.starttls()
        session.login(self.sender, self.password)
        for recipient in recipients:
            msg = MIMEText(StringIO().read())
            msg["Subject"] = "%s" % subject
            msg["From"] = self.sender
            msg["To"] = recipient
            email = msg.as_string() + body
            session.sendmail(self.sender, recipient, email)
        session.quit()


def notify_show(data, bufferp, uber_empty, tagsn, isdisplayed,
                ishilight, prefix, message):
    if (bufferp == weechat.current_buffer()):
        pass
    elif weechat.buffer_get_string(bufferp, "localvar_type") == "private":
        show_notification(prefix, message)
    elif int(ishilight):
        buffer = (weechat.buffer_get_string(bufferp, "short_name") or
                  weechat.buffer_get_string(bufferp, "name"))
        show_notification(buffer, prefix + ": " + message)

    return weechat.WEECHAT_RC_OK


def show_notification(chan, message):
    en = EmailNotifier(SMTP_SERVER, SMTP_PORT, SENDER, PASSWORD)
    en.notify(RECIPIENTS, "weechat: " + chan, chan + ": " + message)
