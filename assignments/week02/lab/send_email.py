#!/bin/python
import smtplib

USER = 'crisewing_demobox'
PW = 's00p3rs3cr3t'
from_addr = "Roy Batty <test@pythonclass.com>"
to_addrs = "demo@crisewing.com"
SUBJECT = "I've seen things..."
MESSAGE = " I've seen things you people wouldn't believe. Attack ships on fire off the shoulder of Orion. I watched C-beams glitter in the dark near the Tannhauser gate. All those moments will be lost in time... like tears in rain... "


def send_mail():
    template = "From: %s\r\nTo: %s\r\nSubject: %s\r\n\r\n"
    headers = template % (from_addr, to_addrs, SUBJECT)
    server = smtplib.SMTP('smtp.webfaction.com', 587)
    server.set_debuglevel(True)
    server.ehlo()
    server.starttls()
    server.ehlo()  # re-identify after TLS begins
    server.login(USER, PW)
    email_body = headers + MESSAGE
    server.sendmail(from_addr, [to_addrs, ], email_body)
    server.close()
