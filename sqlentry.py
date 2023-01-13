import sqlite3
from sqlite3 import Error
import os
import sys
import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

""" LINES TO UPDATE BEFORE/AFTER UPLOADING TO GITHUB (SENSITIVE DATA):
        * in def send_email(unread_messages):
            line 55
            line 83
"""


"""Check for new messages in SQL database. If new messages exist, forward them via email."""

def main():
    database = "messages.sqlite3"
    
    if check_db_exists(database) != True:
        handle_db_not_exists()

    conn = create_connection(database)

    if conn is not None:
        with conn:
            unread_messages = check_for_new_messages(conn)

    if len(unread_messages) == 0:
        no_new_messages()
    else:
        sent_message_ids = send_email(unread_messages)
        with conn:
            update_sent(sent_message_ids, conn)    



    # TODO: https://tableplus.com/blog/2018/04/sqlite-check-whether-a-table-exists.html
    # Create logs of errors/


def update_sent(sent_messages, conn):
    for i in sent_messages:
        i = int(i)
        cur = conn.cursor()
        cur.execute("UPDATE messages SET is_forwarded = 1 WHERE id = ?", (i,))

    print('finished')


def send_email(unread_messages):
    message = MIMEMultipart()
    message["to"] = "your@real.email.com"
    message["from"] = "Your Photography Website"

    if len(unread_messages) == 1:
        message["subject"] = "1 New Message From" + unread_messages[0][1] + " " + unread_messages[0][2]
    
    else:
        subject = str(len(unread_messages)) + ' New Messages From' + unread_messages[0][1]
        i = 1
        while i < 2 and i < len(unread_messages) - 1:
            subject = subject + ", " + unread_messages[i][1] + " " + unread_messages[i][2]
            i += 1
        if len(unread_messages) == 3:
            subject = subject + " and " + unread_messages[2][1] + " " + unread_messages[2][2]
        elif len(unread_messages) > 3:
            subject = subject + " and others"
        message["subject"] = subject

    email_body = ''
    for i in unread_messages:
        email_body = email_body + i[1] + " " + i[2] + "\n" + i[3] + "\n" + i[5] + "\n" + i[4] + "\n\n\n\n"

    message.attach(MIMEText(email_body))

    try:
        with smtplib.SMTP(host="smtp.gmail.com", port=587) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.login("your_real_email@gmail.com", "Your_real_password")
            smtp.send_message(message)
            print('sent')

    except:
        sys.exit("Email not sent - something went wrong.")
    
    else:
        update_sent = []
        for i in unread_messages:
            update_sent.append(i[0])
        return update_sent


def check_for_new_messages(conn):
    cur = conn.cursor()
    cur.execute("SELECT id, first_name, last_name, email, message, date_created FROM messages WHERE is_forwarded = 0")
    selected = cur.fetchall()
    return selected


def no_new_messages():
    # TODO: send an email every couple of days or so to update user that no new messages have been received.
    sys.exit('no new messages')


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """

    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn


def handle_db_not_exists():
    # TODO: send notification that DB does not exist
    sys.exit('db does not exist')


def check_db_exists(db):
    """ Checks whether the specified database file exists in the folder"""
    return os.path.exists(db)


if __name__ == '__main__':
    main()
