#!/usr/bin/env python3
import smtplib
import sqlite3
import json
from datetime import datetime, timedelta
from email.mime.text import MIMEText
from contextlib import closing

def GetRequired():
    with open('required.json', 'r') as fin:
        return json.loads(fin.read())

def GetOutageInfo(required, now):
    try:
        con = sqlite3.connect('apcupsd.sqlite')
        with closing(con.cursor()) as cur:
            cur.execute('INSERT INTO apcd_offbattery (offbattery) VALUES (\'{0}\')'.format(now))
            cur.execute('SELECT last_onbattery FROM apcd_last_onbattery WHERE rowid=1')
            lastID = cur.fetchone()[0]
            cur.execute('SELECT onbattery FROM apcd_onbattery WHERE rowid={0}'.format(lastID))
            lastonbatt = cur.fetchone()[0]
        con.commit()
    except sqlite3.Error as e:
        if con:
            con.rollback()
        print('Error {0}:'.format(e.args[0]))
    finally:
        if con:
            con.close()

    then = datetime.strptime(lastonbatt, '%Y-%m-%d %H:%M:%S.%f')
    delta = (now - then)
    
    return str(timedelta(seconds=delta.seconds))

def SendGmailMsg(required, now, downtime):
    gmailAddress = required['sender']
    gmailPassword = required['password'] #App Specific Password

    fromSender = gmailAddress
    toRecipients = required['recipients']

    msg_subject = 'ALERT: Home UPS Power Restore'
    msg_text = 'Home is now operating normally {0}. Power was off for {1}'.format(now,downtime)

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
    downtime = GetOutageInfo(required, now)
    SendGmailMsg(required, now, downtime)
