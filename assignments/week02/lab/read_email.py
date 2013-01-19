import imaplib

USER = ''
PW = ''
from_addr = 'Roy Batty <test@pythonclass.com>'


def mail_login():
    conn = imaplib.IMAP4_SSL('mail.webfaction.com')
    conn.login(USER, PW)
    conn.debug = 4
    return conn


def list_mail():
    conn = mail_login()
    conn.list()


def inbox_status():
    conn = mail_login()
    vals = '(MESSAGES RECENT UIDNEXT UIDVALIDITY UNSEEN)'
    conn.status('INBOX', vals)


def search_inbox(query):
    conn = mail_login()
    print 'searching for: ' + str(query)
    conn.select('INBOX')
    conn.search(None, '(FROM "' + query + '")')

