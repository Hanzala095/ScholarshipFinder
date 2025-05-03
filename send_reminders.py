import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from database.db import get_connection
from datetime import datetime, timedelta

# Email account details (use a project-specific Gmail)
EMAIL_ADDRESS = 'yourprojectemail@gmail.com'
EMAIL_PASSWORD = 'yourpassword'

def send_email(to_email, subject, body):
    message = MIMEMultipart()
    message['From'] = EMAIL_ADDRESS
    message['To'] = to_email
    message['Subject'] = subject

    message.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(message)
            print(f"✅ Email sent to {to_email}")
    except Exception as e:
        print(f"❌ Failed to send email to {to_email}: {e}")

def check_and_send_reminders():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    today = datetime.now().date()
    upcoming_deadline = today + timedelta(days=5)  # 5 days before deadline

    query = """
        SELECT se.email, s.name, s.deadline
        FROM student_emails se
        JOIN scholarships s ON se.scholarship_id = s.id
        WHERE s.deadline = %s
    """
    cursor.execute(query, (upcoming_deadline,))
    results = cursor.fetchall()

    cursor.close()
    conn.close()

    for row in results:
        email = row['email']
        scholarship_name = row['name']
        deadline = row['deadline']

        subject = f"Reminder: {scholarship_name} deadline approaching!"
        body = f"Hello,\n\nThis is a reminder that the deadline for the scholarship '{scholarship_name}' is on {deadline}.\n\nMake sure to apply before it's too late!\n\nBest of luck,\nScholarship Finder Team"

        send_email(email, subject, body)

if __name__ == '__main__':
    check_and_send_reminders()
