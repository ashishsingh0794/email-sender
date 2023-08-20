#!usr/bin/python3
# -*- coding: UTF-8 -*-

import mimetypes
import smtplib
import ssl
from email import encoders, utils
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Union

from email_validator import EmailNotValidError, validate_email

from src.core.decorators import exception_handler, exec_retry


class EmailSender:
    def __init__(self, logger, sender_username : str, sender_password : str, server_dtl : tuple, use_SSL : bool = False):
        self.logger = logger
        self.username = sender_username
        self.password = sender_password
        self.server_name = server_dtl[0]
        self.server_port = server_dtl[1]
        self.use_SSL = use_SSL

        if self.use_SSL:
            self.smtpserver = smtplib.SMTP_SSL(self.server_name, self.server_port, context=ssl.create_default_context())
        else:
            self.smtpserver = smtplib.SMTP(self.server_name, self.server_port)
        self.connected = False

    def __str__(self):
        return "\n\tType: Mail Sender \n" \
                "\tConnection to server: ({}, {}) \n" \
                "\tUsername : {} \n" \
                "\tConnected (status): {}\n".format(self.server_name, self.server_port, self.username, self.connected)

    def _build_part(self, data : str, contenttype : str) -> Union[MIMEText, MIMEBase]:
        maintype, subtype = contenttype.split('/')
        if maintype == 'text':
            part = MIMEText(data, _subtype=subtype)
        else:
            part = MIMEBase(maintype, subtype)
            part.set_payload(data)
            encoders.encode_base64(part)
        return part

    def _build_attachment(self, attachment : str, attachment_name : str) -> Union[MIMEText, MIMEBase]:
        mimetype, mimeencoding = mimetypes.guess_type(attachment_name)
        if mimeencoding or (mimetype is None):
            mimetype = 'application/octet-stream'
        mode = 'r' if mimetype.startswith('text/') else 'rb'
        with open(attachment, mode, encoding='utf8') as fd:
            part = self._build_part(fd.read(), mimetype)
        part.add_header('Content-Disposition', 'attachment', filename=attachment_name)
        return part


    def _validate_recipients(self, email : str) -> bool:
        try:
            emailObject = validate_email(email)
            self.logger.info("%s is a valid email address", emailObject.email)
        except EmailNotValidError as errorMsg:
            self.logger.error("EmailSendError: %s - %s", email, str(errorMsg))
            return False
        return True

    def _connect(self) -> None:
        if not self.use_SSL:
            self.smtpserver.starttls()
        try:
            self.smtpserver.login(self.username, self.password)
            self.connected = True
        except Exception as excp:
            self.logger.error(excp)
            self.connected = False        
        self.logger.info(self)

    def _disconnect(self) -> None:
        self.smtpserver.close()
        self.connected = False
        self.logger.info(self)

    def _send_email(self, msg, recipient):
        if self._validate_recipients(recipient):
            msg.replace_header("To", recipient)
            self.logger.info("Sending to %s", recipient)
            self.smtpserver.send_message(msg)
            self.logger.info("Email sent successfully to %s", recipient)
        else:
            self.logger.error("Mail sending to %s failed. Check log for details", recipient)

    @exception_handler
    @exec_retry
    def set_message(self, data : str, contenttype : str, subject : str = "", sender : Union[None, str] = None, attachment : Union[None, str] = None, 
                    attachment_name : Union[None, str] = None, image : Union[None, str] =None) -> MIMEMultipart:
        msg = MIMEMultipart()

        body = MIMEMultipart(_subtype = 'alternative')
        body.attach(self._build_part(data, contenttype))
        msg.attach(body)

        if attachment:
            msg.attach(self._build_attachment(attachment, attachment_name))

        msg['Subject'] = subject
        if sender is None:
            msg['From'] = self.username
        else:
            msg['From'] = sender
        msg["To"], msg["CC"], msg["BCC"] = None, None, None
        msg['Date'] = utils.formatdate(localtime = True)
        msg['Message-ID'] = utils.make_msgid()

        if image:
            with open(image, 'rb') as fp:
                msgImage = MIMEImage(fp.read())
            msgImage.add_header('Content-ID', '<image>')
            msg.attach(msgImage)

        return msg

    @exception_handler
    @exec_retry
    def send_all(self, msg : MIMEMultipart, recipients: Union[tuple, list]) -> None:
        self._connect()

        if not self.connected:
            raise ConnectionError("Not connected to any server. Try self.connect() first")

        if not isinstance(recipients, (list, tuple)):
            raise TypeError("Recipients must be a list or tuple, is {}".format(type(recipients)))

        for recipient in recipients:
            self._send_email(msg, recipient)
            
        self._disconnect()