from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from invokes import invoke_http
import os


NEW_ACCOUNT_EMAIL_SUBJECT = "Change your SKOR password"
PASSWORD_RESET_EMAIL_SUBJECT = "Reset your SKOR password"
REPORT_ISSUE_EMAIL_SUBJECT = "Bug Reported"
smtp_servers= {
    "google": {"server": 'smtp.gmail.com', "port":'587'},
    "outlook": {"server": 'smtp-mail.outlook.com', "port":'587'},
    "yahoo": {"server": 'smtp.mail.outlook.com', "port":'587'},
}

def getSelectedEmail():
    getSelectedSkorEmailUrl = os.environ.get('getSelectedSkorEmailUrl') or "http://localhost:8087/getSelectedSkorEmail"
    skorEmail = invoke_http(getSelectedSkorEmailUrl, method='GET')

    if skorEmail:
        host_email = skorEmail['data']['email']
        host_email_password = skorEmail['data']['password']
        smtp_server = smtp_servers[skorEmail['data']['domain']]
    
    return host_email, host_email_password, smtp_server

def sendPasswordEmail(recipient, subject, password, testMode):
    host_email, host_password, smtp_server = getSelectedEmail()

    text = f"Welcome to SKOR, class participation system for Interacting Design and Prototyping, IS211! You are receiving this email because a new account has just been created for you. Your new account has been created with the following:\n\n\tUsername: {recipient}\n\tPassword: {password}\n\nClick this link: https://skor.smu.edu.sg to visit SKOR. Please login to your account and change your password.\n\nBest Regards,\nSKOR (skorsmu@gmail.com)"

    if testMode == 1:
        recipient = host_email

    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg.attach(MIMEText(text))

    smtp = smtplib.SMTP(smtp_server['server'], port=smtp_server['port'])
    smtp.starttls()

    smtp.login(host_email, host_password)
    smtp.sendmail(host_email, recipient, msg.as_string())

    smtp.quit()

def sendResetPasswordEmail(recipient, subject, password, testMode):
    host_email, host_password, smtp_server = getSelectedEmail()

    text = f"You have requested for a password reset. Your new password is {password}. Please login with this password and change your password!"

    if testMode == 1:
        recipient = host_email

    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg.attach(MIMEText(text))

    smtp = smtplib.SMTP(smtp_server['server'], port=smtp_server['port'])
    smtp.starttls()

    smtp.login(host_email, host_password)
    smtp.sendmail(host_email, recipient, msg.as_string())

    smtp.quit()

def sendIssueReportEmail(subject, userName, userEmail, message):
    host_email, host_password, smtp_server = getSelectedEmail()

    msg = MIMEMultipart()
    msg['Subject'] = subject
    text = f"User {userName} ({userEmail}) has reported an issue.\n Issue: {message}"
    msg.attach(MIMEText(text))

    smtp = smtplib.SMTP(smtp_server['server'], port=smtp_server['port'])
    smtp.starttls()

    smtp.login(host_email, host_password)
    smtp.sendmail(host_email, host_email, msg.as_string())

    smtp.quit()
    return host_email

def sendContactUsEmail(subject, userName, userEmail, message):
    host_email, host_password, smtp_server = getSelectedEmail()
    recipient_email = "skor@smu.edu.sg"

    msg = MIMEMultipart()
    msg['Subject'] = subject
    text = f"User: {userName} ({userEmail}) is trying to contact us.\n\n {message}"
    msg.attach(MIMEText(text))

    smtp = smtplib.SMTP(smtp_server['server'], port=smtp_server['port'])
    smtp.starttls()

    smtp.login(host_email, host_password)
    smtp.sendmail(host_email, recipient_email, msg.as_string())

    smtp.quit()
    return host_email

