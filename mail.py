import smtplib
from email.mime.text import MIMEText


def send_email(message, target):
    sender = "21passbot@gmail.com"
    password = "qkwvlqinsbbjawvw"

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()

    target = str(target)
    try:
        server.login(sender, password)
        msg = MIMEText(str(message))
        msg["Subject"] = "Код подтверждения school21pass_bot"
        server.sendmail(sender, target, msg.as_string())

        return "The message was send successfully"
    except Exception as _ex:
        return f"[Error] {_ex}"
