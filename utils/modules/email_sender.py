from django.core.mail import EmailMessage, EmailMultiAlternatives, send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags


class EmailSender:
    subject: str
    send_to: list[str]
    body: str
    context: dict
    template: str
    email_from: str
    bcc: list[str]
    cc: list[str]
    context: dict
    attachments: list

    def __init__(
        self,
        subject="",
        body="",
        send_to=None,
        bcc=None,
        cc=None,
        reply_to=None,
        context=None,
        template=None,
        attachments=None,
        email_from=None,
    ):
        self.subject = subject
        self.send_to = send_to
        self.email_from = email_from
        self.body = body
        self.bcc = bcc
        self.cc = cc
        self.reply_to = reply_to
        self.context = context
        self.template = template
        self.attachments = attachments

    def send_email(self):
        email = EmailMessage(
            subject=self.subject,
            body=self.body,
            to=self.send_to,
            from_email=self.email_from,
            bcc=self.bcc,
            cc=self.cc,
            reply_to=self.reply_to,
            attachments=self.attachments,
        )
        email.send()
        return

    def templated_email_send(self):
        # subject: str, send_to: list[str], context: dict, template: str, email_from=None):
        html_message = render_to_string(
            self.template,
            context=self.context,
        )
        plain_message = strip_tags(html_message)

        message = EmailMultiAlternatives(
            subject=self.subject,
            body=plain_message,
            from_email=self.email_from,
            to=self.send_to,
            bcc=self.bcc,
            cc=self.cc,
            reply_to=self.reply_to,
            attachments=self.attachments,
        )

        message.attach_alternative(html_message, "text/html")
        message.send()
        return
