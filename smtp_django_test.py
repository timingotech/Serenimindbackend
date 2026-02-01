import os
import sys
import django
import smtplib
import ssl

# Ensure project root is on sys.path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)

# Configure Django settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")

django.setup()

from django.conf import settings  # noqa: E402


def main() -> None:
    print("Using SMTP host:", settings.EMAIL_HOST)
    print("Using SMTP port:", settings.EMAIL_PORT)
    print("Using TLS:", settings.EMAIL_USE_TLS)
    print("From email:", settings.EMAIL_HOST_USER)

    smtp_host = settings.EMAIL_HOST
    smtp_port = settings.EMAIL_PORT
    username = settings.EMAIL_HOST_USER
    password = settings.EMAIL_HOST_PASSWORD
    from_email = username
    to_email = username  # send to yourself

    print(f"\nConnecting to {smtp_host}:{smtp_port} ...")

    try:
        server = smtplib.SMTP(smtp_host, smtp_port, timeout=30)

        if settings.EMAIL_USE_TLS:
            print("Starting TLS...")
            context = ssl.create_default_context()
            server.starttls(context=context)
            print("TLS started.")

        print("Logging in...")
        server.login(username, password)
        print("Login successful.")

        msg = f"""From: {from_email}\nTo: {to_email}\nSubject: Test Email from Django SMTP\n\nThis is a test email to verify the SMTP configuration from the Django backend environment.\n"""

        print("Sending email...")
        server.sendmail(from_email, [to_email], msg)
        print("Email sent successfully.")

        server.quit()
        print("SMTP connection closed. Test completed successfully.")
    except Exception as e:  # pragma: no cover - diagnostic script
        print("\nSMTP test failed with error:", repr(e))


if __name__ == "__main__":
    main()
