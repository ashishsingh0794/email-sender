#!usr/bin/python3
# -*- coding: UTF-8 -*-

from dotenv import dotenv_values

from src.core.logger import initialize_logger
from src.scripts.sendmail import EmailSender
from src.utils.template_loader import TemplateLoader
from src.utils.yaml_reader import get_config

mail_type : str = "confirmation_email"
redirect_url : str = "www.google.com"
customer_name : str = "Ashish Singh"
recipients_lst : list = ["abcd@gmail.com"]
email_data : str = ""

config_cred = dotenv_values(".env")

smtp_server : str = config_cred["smtp_server"]
smtp_port : int = config_cred["smtp_port"]
username : str = config_cred["username"]
password : str = config_cred["password"]
ssl : bool = config_cred["ssl"]

log_config_file :str = config_cred["log_config_file"]
config_mail : dict = get_config(config_cred["mail_config_file"])


if __name__ == "__main__":
    logger = initialize_logger(logger_name=mail_type, log_config_file=log_config_file, logger="app")
    
    if config_mail["type"][mail_type]["mail_content_type"] == "text/html":
        template_loader = TemplateLoader(template_folder=config_mail["base"]["template_folder"], 
                                        template_file=config_mail["type"][mail_type]["template_file"])
        params = config_mail["type"][mail_type]
        params.update({"name": customer_name, "redirect_url": redirect_url})
        email_data = template_loader.get_template_text(**params)

    mailsender = EmailSender(logger=logger, sender_username=username, sender_password=password, server_dtl=(smtp_server, smtp_port), use_SSL=ssl)

    msg = mailsender.set_message(data=email_data, 
                                contenttype=config_mail["type"][mail_type]["mail_content_type"], 
                                subject=config_mail["type"][mail_type]["subject"], 
                                sender=config_mail["base"]["sender"], 
                                image=config_mail["base"]["template_folder"] + config_mail["base"]["logo_img"],
                                attachment=config_mail["type"][mail_type]["attachment"], 
                                attachment_name=config_mail["type"][mail_type]["attachment_name"])

    mailsender.send_all(msg=msg, recipients=recipients_lst)