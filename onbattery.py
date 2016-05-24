#!/usr/bin/env python3
import smtplib
import sqlite3
import json
from datetime import datetime
from email.mime.text import MIMEText
from contextlib import closing

def GetRequired():
    with open('required.json', 'r') as fin:
        return json.loads(fin.read())

def SetOutageInfo(now):
    try:
        con = sqlite3.connect('apcupsd.sqlite')
        with closing(con.cursor()) as cur:
            cur.execute('INSERT INTO apcd_onbattery (onbattery) VALUES (\'{0}\')'.format(now))
            cur.execute('SELECT ID FROM apcd_onbattery WHERE onbattery=\'{0}\''.format(now))
            lastID = cur.fetchone()[0]
            cur.execute('UPDATE apcd_last_onbattery SET last_onbattery=(\'{0}\') WHERE rowid=1'.format(lastID))
        con.commit()
    except sqlite3.Error as e:
        if con:
            con.rollback()
        print('Error {0}:'.format(e.args[0]))
    finally:
        if con:
            con.close()

def SendGmailMsg(required, now):
    gmailAddress = required['sender']
    gmailPassword = required['password'] #App Specific Password

    fromSender = gmailAddress
    toRecipients = required['recipients']

    msg_subject = 'ALERT: Home UPS Power Failure'
    msg_text = 'Home is now on battery power. {0}'.format(now)

    msg = MIMEText(msg_text)
    msg['Subject'] = msg_subject
    msg['From'] = fromSender
    msg['To'] = ", ".join(toRecipients)
    s = smtplib.SMTP_SSL('smtp.gmail.com', '465')
    s.login(gmailAddress, gmailPassword)
    s.sendmail(fromSender, toRecipients, msg.as_string())
    s.quit()

#Main
if __name__ == "__main__":
    now = datetime.now()
    required = GetRequired()
    SetOutageInfo(now)
    SendGmailMsg(required, now)
    