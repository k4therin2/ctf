#!/usr/bin/env python3
import smtplib
import sys

def send_hint(to):
    s = smtplib.SMTP('smtp.case.edu', 25)
    frm = 'noreply@case.edu'
    msg = (
        'Subject: An important message from HacSoc CTF\r\n'
        'From: HacSoc CTF <%s>\r\n'
        'To: %s\r\n'
        'Flag: flag{spoofer_no_spoofing}\r\n'
        '\r\n'
        'lol jk im just playin'
    ) % (frm, to)
    s.sendmail(frm, to, msg)
    s.quit()


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('provide an email')
        sys.exit(1)
    send_hint(sys.argv[1])
