# -*- coding: utf-8 -*-

import re
import smtplib
from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
from blog.common import *


class SendEmail(object):
    from_addr = get_config('email', 'from_addr')
    password = get_config('email', 'password')
    smtp_server = get_config('email', 'smtp_server')
    smtp_port = int(get_config('email', 'smtp_port'))

    def __init__(self):
        pass

    @staticmethod
    def _format_addr(s):
        name, addr = parseaddr(s)
        return formataddr((Header(name, 'utf-8').encode(),
                           addr.encode('utf-8') if isinstance(addr, unicode) else addr))

    @staticmethod
    def check_addr(addr):
        if len(addr) >= 5:
            if re.match("[a-zA-Z0-9]+@+[a-zA-Z0-9]+\.+[a-zA-Z]", addr):
                return True
        return False

    @classmethod
    def send_email(cls, to_addr, from_user, title):
        if not cls.check_addr(to_addr):
            return False
        msg = u'您的文章【%s】有了来自用户名为【%s】的一条新评论' % (title, from_user)
        msg = MIMEText(msg, 'plain', 'utf-8')
        msg['From'] = cls._format_addr(u'JusOT <%s>' % cls.from_addr)
        msg['To'] = cls._format_addr(u'作者 <%s>' % to_addr)
        msg['Subject'] = Header(u'您的一篇文章有新的评论', 'utf-8').encode()

        try:
            server = smtplib.SMTP_SSL(cls.smtp_server, cls.smtp_port)
            server.login(cls.from_addr, cls.password)
            server.sendmail(cls.from_addr, [to_addr], msg.as_string())
            server.quit()
            return True
        except IOError:
            raise IOError("error at send_email() in ema")
