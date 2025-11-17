import os
import django
import ssl
import smtplib

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

# Test SMTP connection directly
print("Testing SMTP connection to smtp.go54mail.com...")

try:
    # Create connection
    smtp = smtplib.SMTP('smtp.go54mail.com', 587, timeout=30)
    smtp.set_debuglevel(1)  # Enable debug output
    
    print("\n[OK] Connected to SMTP server")
    
    # Create SSL context that doesn't verify certificates
    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE
    
    # Start TLS
    smtp.starttls(context=context)
    print("\n[OK] STARTTLS successful")
    
    # Login
    smtp.login('team@serenimind.com.ng', 'Timilehin1.2')
    print("\n[OK] Login successful")
    
    # Send email
    from_addr = 'team@serenimind.com.ng'
    to_addr = 'team@serenimind.com.ng'
    
    msg = f"""From: {from_addr}
To: {to_addr}
Subject: Test Email from SereniMind

This is a test email to verify the email configuration.
"""
    
    smtp.sendmail(from_addr, [to_addr], msg)
    print("\n[OK] Email sent successfully!")
    
    smtp.quit()
    
except smtplib.SMTPAuthenticationError as e:
    print(f"\n[ERROR] Authentication failed: {e}")
except smtplib.SMTPDataError as e:
    print(f"\n[ERROR] Data error (policy rejection): {e}")
    print("\nThis might mean:")
    print("1. The sender email is not properly configured")
    print("2. SPF/DKIM records need to be set up")
    print("3. The email account needs verification")
except Exception as e:
    print(f"\n[ERROR] Error: {e}")
    import traceback
    traceback.print_exc()



