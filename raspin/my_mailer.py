# -*- coding: utf-8 -*-

import os.path
import datetime
import smtplib
from email import Encoders
from email.Utils import formatdate
from email.MIMEBase import MIMEBase
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
SMTP = "smtp.gmail.com"
PORT = 587
ADDRESS = "yousuke0303.sender@gmail.com"
PASSWORD = "3Fjeo5Fr-X"

def create_message(from_addr, to_addr, subject, body, mime=None, attach_file=None):
    """
    メッセージを作成する
    @:param from_addr 差出人
    @:param to_addr 宛先
    @:param subject 件名
    @:param body 本文
    @:param mime MIME
    @:param attach_file 添付ファイル
    @:return メッセージ
    """
    msg = MIMEMultipart()
    msg["From"] = from_addr
    msg["To"] = to_addr
    msg["Date"] = formatdate()
    msg["Subject"] = subject
    body = MIMEText(body)
    msg.attach(body)
    # 添付ファイル
    if mime != None and attach_file != None:
        attachment = MIMEBase(mime['type'], mime['subtype'])
        file = open(attach_file['path'])
        attachment.set_payload(file.read())
        file.close()
        Encoders.encode_base64(attachment)
        msg.attach(attachment)
        attachment.add_header("Content-Disposition", "attachment", filename=attach_file['name'])
    return msg

def send(from_addr, to_addrs, msg):
    """
    メールを送信する
    @:param from_addr 差出人
    @:param to_addr 宛先(list)
    @:param msg メッセージ
    """
    smtpobj = smtplib.SMTP(SMTP, PORT)
    smtpobj.ehlo()
    smtpobj.starttls()
    smtpobj.ehlo()
    smtpobj.login(ADDRESS, PASSWORD)
    smtpobj.sendmail(from_addr, to_addrs, msg.as_string())
    smtpobj.close()

def send_mail_with_picture (to_ad, title, body, attach_path):
    mime = {'type': 'image/jpeg', 'subtype': 'jpeg'}
    attach_file = {'name': 'image.jpeg', 'path': attach_path}
    msg = create_message(ADDRESS, to_ad, title, body, mime, attach_file)

    # 送信
    send(ADDRESS, [to_ad], msg)
