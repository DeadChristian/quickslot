import smtplib
from email.message import EmailMessage

# UPDATE these with your real email/login
EMAIL_ADDRESS = "your_email@gmail.com"
EMAIL_PASSWORD = "your_app_password"

def send_confirmation(to_email, name, service, datetime_str, payment, deposit_required=False, deposit_amount=0):
    msg = EmailMessage()
    msg["Subject"] = f"Your {service} booking with QuickSlot"
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = to_email

    body = f"""Hi {name},

Thanks for booking your {service} with QuickSlot!

📅 Appointment: {datetime_str}
💳 Payment method: {payment}
"""

    if deposit_required:
        body += f"""
A deposit of ${deposit_amount} is required to confirm this booking.

Please send your deposit via {payment} as soon as possible. Your slot is not locked in until it's received.
"""

    body += """

If you have any questions, reply to this email.
Looking forward to your session!

— QuickSlot
"""

    msg.set_content(body)

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)
        return True
    except Exception as e:
        print("Email error:", e)
        return False
